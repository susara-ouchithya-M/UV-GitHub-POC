import pandas as pd

from NonPar_MPF import Policy_info
from NonPar_Assumptions import inflation_best_estimate

policyid = 2
valuation_date_str = "2022-12-31"

# Filter the DataFrame to find the row for the given policy ID
policy_data = Policy_info[Policy_info['Policy ID'] == policyid]

# Extract the required information
if not policy_data.empty:
    Duration = policy_data['Duration Elapsed'].values[0]    
    polterm = policy_data['Policy Term'].values[0]
    Entryage = policy_data['Issue Age'].values[0]
    frequency = 12  #Manually Change this  
    premiumterm = policy_data['Premium Term'].values[0]
    IssueDate = pd.to_datetime(policy_data['Issue Date'].values[0])
    Maturity_date = IssueDate + pd.DateOffset(years=polterm) - pd.Timedelta(days=1)
    SA = policy_data['Sum Assured'].values[0]
    AnnualPremium = policy_data['Annual Premium'].values[0]
    exp_inflation = inflation_best_estimate
    
    # Print the extracted information
    print(f"Valuation Date: {valuation_date_str}")
    print(f"Policy Id: {policyid}")
    print(f"Issue Date: {IssueDate}")
    print(f"Duration: {Duration}")
    print(f"Policy Term: {polterm}")
    print(f"Entry Age: {Entryage}")
    print(f"Frequency: {frequency}")
    print(f"Premium Term: {premiumterm}")
    print(f"Maturity Date: {Maturity_date.strftime('%Y-%m-%d')}")
    print(f"Sum Assured: {SA}")
    print(f"Annual Premium: {AnnualPremium}")
else:
    print(f"No data found for Policy ID: {policyid}")
