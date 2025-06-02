###
import pandas as pd

from NonPar_MPF import file_path

sheet_name_mortality = 'Mortality'
Mortality = pd.read_excel(file_path, sheet_name=sheet_name_mortality)

Mortality_Rates_Realisitic = Mortality.iloc[3:106, 3:5]
Mortality_Rates_Reserving = Mortality.iloc[3:106, 5:7]

print(Mortality_Rates_Realisitic)
print(Mortality_Rates_Reserving)

###
sheet_name_lapses = 'Lapses'
Lapses = pd.read_excel(file_path, sheet_name=sheet_name_lapses)

Lapses_BestEstimate = Lapses.iloc[1:12, 0:2]
Lapses_Reserving = Lapses.iloc[1:12, 3:5]

print(Lapses_BestEstimate)
print(Lapses_Reserving)

###sheet_name_lapses = 'Yield Curve'
YieldCurve = pd.read_excel(file_path, sheet_name=sheet_name_lapses)

YieldCurveTable = YieldCurve.iloc[2:83, 0:3]

print(YieldCurveTable)

### Other assumptions

sheet_name = 'Assumptions'

Assumption = pd.read_excel(file_path, sheet_name=sheet_name, header=None)

### Best Estimate

#Mortality Rates
mortality_best_estimate_male = Assumption.iloc[3, 1]
mortality_best_estimate_female = Assumption.iloc[3, 3]

#Expenses
initial_fixed_expense_best_estimate = Assumption.iloc[11, 1]
initial_percent_premium_best_estimate = Assumption.iloc[12, 1]
initial_percent_sa_best_estimate = Assumption.iloc[13, 1]
maintenance_fixed_expense_best_estimate = Assumption.iloc[15, 1]
maintenance_percent_premium_best_estimate = Assumption.iloc[16, 1]
maintenance_percent_reserve_best_estimate = Assumption.iloc[17, 1]
claims_expense_best_estimate = Assumption.iloc[18, 1]

#Inflation
inflation_best_estimate = Assumption.iloc[20, 1]

#Tax Rates
shareholder_tax_rate = Assumption.iloc[23, 1]
policyholder_tax_rate = Assumption.iloc[24, 1]

#Solvency Margin
solvency_margin_reserves = Assumption.iloc[27, 2]
solvency_margin_sar = Assumption.iloc[28, 2]
minimum_solvency_ratio = Assumption.iloc[29, 2]



print("Mortality Assumption")
print(f"Mortality Best Estimate Male: {mortality_best_estimate_male * 100:.2f}%")
print(f"Mortality Best Estimate Female: {mortality_best_estimate_female * 100:.2f}%")

print(" ")
print("Expense Assumption")
print(f"Initial Fixed Expense Best Estimate: {initial_fixed_expense_best_estimate}")
print(f"Initial Percent Premium Best Estimate: {initial_percent_premium_best_estimate * 100:.2f}%")
print(f"Initial Percent SA Best Estimate: {initial_percent_sa_best_estimate * 100:.2f}%")
print(f"Maintenance Fixed Expense Best Estimate: {maintenance_fixed_expense_best_estimate}")
print(f"Maintenance Percent Premium Best Estimate: {maintenance_percent_premium_best_estimate * 100:.2f}%")
print(f"Maintenance Percent Reserve Best Estimate: {maintenance_percent_reserve_best_estimate * 100:.2f}%")
print(f"Claims Expense Best Estimate: {claims_expense_best_estimate}")

print(" ")
print("Inflation")
print(f"Inflation Best Estimate: {inflation_best_estimate * 100:.2f}%")

print(" ")
print("Tax Rates")
print(f"Shareholder Tax Rate: {shareholder_tax_rate * 100:.2f}%")
print(f"Policyholder Tax Rate: {policyholder_tax_rate * 100:.2f}%")

print(" ")
print("Solvency Margin")
print(f"Solvency Margin Reserves: {solvency_margin_reserves * 100:.2f}%")
print(f"Solvency Margin SAR: {solvency_margin_sar * 100:.2f}%")
print(f"Minimum Solvency Ratio: {minimum_solvency_ratio * 100:.2f}%")


# Reserving

#Mortality Rates
mortality_reserving_male = Assumption.iloc[3, 13]
mortality_reserving_female = Assumption.iloc[3, 15]

#Expenses
initial_fixed_expense_reserving = Assumption.iloc[11, 13]
initial_percent_premium_reserving = Assumption.iloc[12, 13]
initial_percent_sa_reserving = Assumption.iloc[13, 13]
maintenance_fixed_expense_reserving = Assumption.iloc[15, 13]
maintenance_percent_premium_reserving = Assumption.iloc[16, 13]
maintenance_percent_reserve_reserving = Assumption.iloc[17, 13]
claims_expense_reserving = Assumption.iloc[18, 13]

#Inflation
inflation_reserving = Assumption.iloc[20, 13]

#Interest Rates
reserve_ir = Assumption.iloc[7, 13]



print("Mortality Assumption")
print(f"Mortality Reserving Male: {mortality_reserving_male * 100:.2f}%")
print(f"Mortality Reserving Female: {mortality_reserving_female * 100:.2f}%")

print(" ")
print("Expense Assumption")
print(f"Initial Fixed Expense Reserving: {initial_fixed_expense_reserving}")
print(f"Initial Percent Premium Reserving: {initial_percent_premium_reserving * 100:.2f}%")
print(f"Initial Percent SA Reserving: {initial_percent_sa_reserving * 100:.2f}%")
print(f"Maintenance Fixed Expense Reserving: {maintenance_fixed_expense_reserving}")
print(f"Maintenance Percent Premium Reserving: {maintenance_percent_premium_reserving * 100:.2f}%")
print(f"Maintenance Percent Reserve Reserving: {maintenance_percent_reserve_reserving * 100:.2f}%")
print(f"Claims Expense Reserving: {claims_expense_reserving}")

print(" ")
print("Inflation")
print(f"Inflation Reserving: {inflation_reserving * 100:.2f}%")

print(" ")
print("Interest Rate")
print(f"Reserve IR: {reserve_ir * 100:.2f}%")