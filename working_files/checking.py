import pandas as pd

# Checking file
file_path = '250523_Python_Exercise_Model_Non_Par.xlsx'
sheet_name_policyinfo = 'Policy Data'
Policy_info = pd.read_excel(file_path, sheet_name=sheet_name_policyinfo)

print(Policy_info)
