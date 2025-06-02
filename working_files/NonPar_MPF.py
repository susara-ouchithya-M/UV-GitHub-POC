import pandas as pd

file_path = r'working_files\250523_Python_Exercise_Model_Non_Par.xlsx'
sheet_name_policyinfo = 'Policy Data'
Policy_info = pd.read_excel(file_path, sheet_name=sheet_name_policyinfo)

print(Policy_info)


num_rows, num_columns = Policy_info.shape

print(f"Number of rows: {num_rows}")
print(f"Number of columns: {num_columns}")


issue_age_column = "Issue Age"

min_issue_age = Policy_info[issue_age_column].min()
max_issue_age = Policy_info[issue_age_column].max()

print(min_issue_age)
print(max_issue_age)

new_policies_count = Policy_info[Policy_info['Duration Elapsed'] == 0].shape[0]
existing_policies_count = Policy_info[Policy_info['Duration Elapsed'] > 0].shape[0]


print(f'Number of new policies: {new_policies_count}')
print(f'Number of existing policies: {existing_policies_count}')