import pandas as pd

from NonPar_Inputs import valuation_date_str, IssueDate,Duration,Entryage,frequency,premiumterm, exp_inflation,polterm,Maturity_date,SA,AnnualPremium
from NonPar_Assumptions import initial_fixed_expense_best_estimate, initial_percent_premium_best_estimate, initial_percent_sa_best_estimate, maintenance_fixed_expense_reserving,maintenance_percent_premium_reserving,claims_expense_reserving,Mortality_Rates_Realisitic,Lapses_BestEstimate

### Time and dates

import pandas as pd
from datetime import datetime
from math import floor, ceil

# Convert the input string to a datetime object
valuation_date = datetime.strptime(valuation_date_str, "%Y-%m-%d")

# Create a list of numbers from 0 to 400 for 'Number of Months'
No_of_months = list(range(401))

# Create a list of dates starting from the valuation date as datetime objects
dates = [(valuation_date + pd.DateOffset(months=i)).strftime("%Y-%m-%d") for i in No_of_months]
dates_datetime = [valuation_date + pd.DateOffset(months=i) for i in No_of_months]


Inception_Date = pd.to_datetime(IssueDate)

# Calculate the complete months since inception
complete_months = [Duration + min(i, polterm * 12 - Duration) for i in No_of_months]

# Calculate the Duration IF since inception
Duration_inception = [round(complete_months[i] / 12, 6) if dates_datetime[i] >= Inception_Date else 0.0 for i in No_of_months]


# Calculate the Age
Age = [Entryage + duration for duration in Duration_inception]

# Calculate the Premium payment date
premium_payment_date = [
    None if i == 0 else (IssueDate if frequency == 0 else (Inception_Date + pd.DateOffset(months=floor(round(Duration_inception[i-1] * frequency, 4) * 12 // frequency))).strftime("%Y-%m-%d"))
    for i in No_of_months
]

# Calculate the Anniversary date
anniversary_date = [
    None if i == 0 else (IssueDate if frequency == 0 else (Inception_Date + pd.DateOffset(months=floor(Duration_inception[i-1]) * 12)).strftime("%Y-%m-%d"))
    for i in No_of_months
]

# Calculate the Policy term
policy_term = [
    None if i == 0 else (1 if Duration_inception[i] <= polterm and (dates_datetime[i-1] >= Inception_Date and dates_datetime[i] < Maturity_date) else 0)
    for i in No_of_months
]

# Calculate the Premium term
premium_term = [
    None if i == 0 else (1 if Duration_inception[i] <= premiumterm and (complete_months[i] == 1 or ((complete_months[i]-1) % (12/frequency)) == 0) else 0)
    for i in No_of_months
]

# Calculate premium paid
premium_paid = [
    None if i == 0 else (0 if Duration_inception[i-1] > premiumterm else min((premiumterm * 12), ceil(complete_months[i-1] + 1 / (12/frequency))))
    for i in No_of_months
]

# Calculate anniversary month
anniversary_month = [
    None if i == 0 else (1 if pd.to_datetime(anniversary_date[i]) > dates_datetime[i-1] and pd.to_datetime(anniversary_date[i]) <= dates_datetime[i] else 0)
    for i in No_of_months
]

# Calculate inflation
inflation = [1.000]
for i in range(1, len(No_of_months)):
    inflation.append(float((1 + exp_inflation) ** (1/12) * inflation[i-1]))

# Calculate financial year
financial_year = [
    str(dates_datetime[i].year + 1) if dates_datetime[i].month > 3 else str(dates_datetime[i].year)
    for i in No_of_months
]


# Combine the data into a DataFrame
data1 = {
    "No. of Months since valuation date": No_of_months,
    "Date": dates,
    "No. of complete months since inception": complete_months,
    "Duration IF since inception": Duration_inception,
    "Age": Age,
    "Premium payment date": premium_payment_date,
    "Anniversary date": anniversary_date,
    "Policy Term": policy_term,
    "Premium Term": premium_term,
    "No of premiums paid": premium_paid,
    "Anniversary month": anniversary_month,
    "Inflation": inflation,
    "Financial Year": financial_year
}

cashflows_Table = pd.DataFrame(data1)

# Show the DataFrame
print(cashflows_Table)


### Benefits

# Convert strings to Timestamp objects
Duration_inception_dt = [pd.to_datetime(date) for date in Duration_inception]
dates = [pd.to_datetime(date) for date in dates]
polterm = pd.to_datetime(polterm)
Maturity_date = pd.to_datetime(Maturity_date)

Lump_Sum_DB = [
    SA if Duration_inception_dt[i] <= polterm and dates[i] <= Maturity_date else 0
    for i in No_of_months
]



# Add the new column to the existing DataFrame
cashflows_Table["Lump Sum DB"] = Lump_Sum_DB

# Show the updated DataFrame
print(cashflows_Table)

# Cash flows before probabilities

premiumterm = pd.to_datetime(premiumterm)

premium = [
    None if i == 0 else (AnnualPremium if frequency == 0 else AnnualPremium // frequency) if premium_term[i] == 1 and Duration_inception_dt[i] <= premiumterm else 0
    for i in No_of_months
]


# Calculate death payouts
Death_payout = [SA if Duration_inception_dt[i] <= polterm and dates[i] <= Maturity_date else 0
    for i in No_of_months
]

# Calculate Initial Expenses
Initial_Expense = [
    None if i == 0 else (initial_fixed_expense_best_estimate+ initial_percent_premium_best_estimate*AnnualPremium + initial_percent_sa_best_estimate* Lump_Sum_DB[i]) if Duration_inception[i-1] == 0 else 0
    for i in No_of_months
]

# Calculate Maintenance Expense
Maintenance_Expense = [
    None if i == 0 else (
        ((maintenance_fixed_expense_reserving  * inflation[i-1] * (1/12))+ (maintenance_percent_premium_reserving * premium[i]))
        if Duration_inception[i-1] != 0 and Duration_inception_dt[i] <= polterm and dates[i] <= Maturity_date else 0
    )
    for i in No_of_months
]

# Calculate Death Claim Expenses
Death_Claim_Expense = [
    None if i == 0 else (claims_expense_reserving * inflation[i]) if Duration_inception_dt[i] <= polterm and dates[i] <= Maturity_date else 0
    for i in No_of_months
]



# Add the new columns to the DataFrame
cashflows_Table["Premiums"] = premium
cashflows_Table["Death Payout"] = Death_payout
cashflows_Table["Initial Expense"] = Initial_Expense
cashflows_Table["Maintenance Expense"] = Maintenance_Expense
cashflows_Table["Death Claim Expense"] = Death_Claim_Expense

# Show the updated DataFrame
print(cashflows_Table)

import numpy as np

# Mortality Rates
Mortality_Rates_Independent = [
    None if i == 0 else format(
        round(
            1 - (1 - Mortality_Rates_Realisitic.loc[Mortality_Rates_Realisitic.iloc[:, 0] == np.floor(Age[i]), Mortality_Rates_Realisitic.columns[1]].values[0]) ** (1/12),
            6
        ), '.6f'
    ) if Duration_inception[i-1] != Duration_inception[i] and Duration_inception_dt[i] != 0 else format(0, '.6f')
    for i in No_of_months
]

# Lapse Rates
Lapses_Rates_Independent = []
for i in No_of_months:
    if i == 0:
        Lapses_Rates_Independent.append(None)
    else:
        try:
            # Filter the matching row
            matching_rows = Lapses_BestEstimate.loc[Lapses_BestEstimate.iloc[:, 0] == np.ceil(Duration_inception[i])]
            
            if not matching_rows.empty:
                lapse_rate = matching_rows[Lapses_BestEstimate.columns[1]].values[0]
                lapse_rate_adjusted = round(1 - (1 - lapse_rate) ** (1/12), 6)
                Lapses_Rates_Independent.append(format(lapse_rate_adjusted, '.6f'))
            else:
                # Handle case where no matching row is found
                Lapses_Rates_Independent.append(format(0, '.6f'))
        
        except IndexError:
            # Handle index error if accessing values[0] fails
            Lapses_Rates_Independent.append(format(0, '.6f'))

# Probability In Force (Dependant)
# Initialize the list with the first element set to 1 (as a float for consistency)
Probability_In_Force = [1.0]

# Iterate over the months starting from the second month (index 1)
for i in range(1, len(No_of_months)):
    # Ensure values are numeric; convert if necessary
    mortality_rate = float(Mortality_Rates_Independent[i])
    lapse_rate = float(Lapses_Rates_Independent[i])
    
    if Duration_inception[i-1] != Duration_inception[i]:
        prob = (Probability_In_Force[i-1] 
                - Probability_In_Force[i-1] * mortality_rate 
                - Probability_In_Force[i-1] * lapse_rate)
    else:
        prob = Probability_In_Force[i-1]
    
    # Round the probability to 6 decimal places
    prob_rounded = round(prob, 6)
    
    # Append the rounded probability to the list
    Probability_In_Force.append(prob_rounded)

# Format and print the results
Probability_In_Force_formatted = [f"{p:.6f}" for p in Probability_In_Force]

# Deaths
Deaths = [
    Probability_In_Force[i-1] * float(Mortality_Rates_Independent[i]) if i != 0 else None
    for i in No_of_months
]

# Lapses
Lapse = [
    Probability_In_Force[i-1] * float(Lapses_Rates_Independent[i]) if i != 0 else None
    for i in No_of_months
]


# Add the new columns to the DataFrame
cashflows_Table["Mortality Rates Independent"] = Mortality_Rates_Independent
cashflows_Table["Lapses Rates Independent"] = Lapses_Rates_Independent
cashflows_Table["Probability In Force Dependent"] = Probability_In_Force_formatted
cashflows_Table["Deaths"] = Deaths
cashflows_Table["Lapse"] = Lapse

# Show the updated DataFrame
print(cashflows_Table)


### Cash flows after probabilities

# Premium after probabilities
Premium_after_probabilities = [
    premium[i] * Probability_In_Force[i-1] if i != 0 else None
    for i in No_of_months
]

# Death Benefit after probabilities
DB_after_probabilities = [
    Death_payout[i] * Deaths[i] if i != 0 else None
    for i in No_of_months
]

# Death Benefit after probabilities
Initial_Expense_after_probabilities = [
    Initial_Expense[i] * Probability_In_Force[i-1] if i != 0 else None
    for i in No_of_months
]

# Death Benefit after probabilities
Maintenance_Expense_after_probabilities = [
    Maintenance_Expense[i] * Probability_In_Force[i-1] if i != 0 else None
    for i in No_of_months
]

# Claim Expense after probabilities
Claim_Expense_after_probabilities = [
    Death_Claim_Expense[i] * Deaths[i] if i != 0 else None
    for i in No_of_months
]

# Add the new columns to the DataFrame
cashflows_Table["Premium after probabilities"] = Premium_after_probabilities
cashflows_Table["Death Benefit after probabilities"] = DB_after_probabilities
cashflows_Table["Initial Expense after probabilities"] = Initial_Expense_after_probabilities
cashflows_Table["Maintenance Expense after probabilities"] = Maintenance_Expense_after_probabilities
cashflows_Table["Claim Expense after probabilities"] = Claim_Expense_after_probabilities

# Show the updated DataFrame
print(cashflows_Table)


