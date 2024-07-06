import pandas as pd
import random

# Load the Crime_Cases_10000.csv file into a pandas DataFrame
crime_cases_df = pd.read_csv('Crime_Cases_2.01.csv')

# Load the telco_2.0.csv file into a pandas DataFrame
telco_df = pd.read_csv('TELCO_2.0.csv')

# Initialize an empty list to store the data for the crime report
crime_report_data = []

# Iterate through each unique case number in Crime_Cases_10000.csv
for case_number in crime_cases_df['case number'].unique():
    # Get the corresponding row in Crime_Cases_10000.csv
    case_row = crime_cases_df[crime_cases_df['case number'] == case_number].iloc[0]

    # Determine the number of suspects based on the "no of suspects" column
    num_suspects = case_row['no of suspects']

    # Get random CNICs from the telco dataset for the number of suspects
    random_cnic_list = random.sample(list(telco_df['CNIC']), num_suspects)

    # Create a new row for each suspect with the same case number and status
    for cnic in random_cnic_list:
        crime_report_row = {
            'case number': case_number,
            'status': case_row['progress'],
            'suspect': cnic
        }

        # Append the row to the crime report data list
        crime_report_data.append(crime_report_row)

# Create a DataFrame from the crime report data
crime_report_df = pd.DataFrame(crime_report_data)

# Save the DataFrame to a CSV file
crime_report_df.to_csv('crime_report_2.0.csv', index=False)

print("Crime report generated with separate entries for each suspect and saved as crime_report.csv.")
