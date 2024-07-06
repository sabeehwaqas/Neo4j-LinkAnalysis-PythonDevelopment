import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Load the existing CDR data from 'CDR.csv'
cdr_df = pd.read_csv('CDR.csv')

# Extract unique caller numbers from the CDR data
unique_caller_numbers = cdr_df['Caller Number'].unique()

# Create a DataFrame for unique caller numbers and CNIC
cnic_df = pd.DataFrame(columns=['CNIC','Caller Number',  'Activate At'])

# Generate unique 11-digit CNIC numbers for each unique caller number
unique_cnic_numbers = np.random.randint(10000000000, 99999999999, size=len(unique_caller_numbers), dtype=np.int64)

# Populate the DataFrame with unique caller numbers, CNIC, and activation dates
cnic_df['Caller Number'] = unique_caller_numbers
cnic_df['CNIC'] = unique_cnic_numbers

# Modify the generate_activation_dates() function
def generate_activation_dates():
    start_date = datetime(2019, 1, 1)
    end_date = datetime(2019, 12, 31)
    return [start_date + timedelta(days=np.random.randint(0, (end_date - start_date).days + 1)) for _ in range(len(unique_cnic_numbers))]

# Generate activation dates for CNICs
activation_dates = generate_activation_dates()
cnic_df['Activate At'] = activation_dates

# Save the DataFrame to a CSV file
cnic_df.to_csv('CNIC.csv', index=False)

# Create a list to store CNIC and associated CDR numbers
cnic_cdr_data = []

# Assign two numbers from CDR to each CNIC
for cnic in unique_cnic_numbers:
    cdr_numbers = np.random.choice(unique_caller_numbers, size=2, replace=False)
    for cdr_number in cdr_numbers:
        cnic_cdr_data.append({'CNIC': cnic, 'CDR Number': cdr_number})

# Create a DataFrame from the list
cnic_cdr_df = pd.DataFrame(cnic_cdr_data, columns=['CNIC', 'CDR Number'])

# Filter out activation dates that are after the respective CDR numbers
for index, row in cnic_cdr_df.iterrows():
    cnic = row['CNIC']
    cdr_number = row['CDR Number']
    activate_date = cnic_df.loc[cnic_df['CNIC'] == cnic, 'Activate At'].values[0]
    cdr_date_str = cdr_df.loc[cdr_df['Caller Number'] == cdr_number, 'Call Date'].values[0]
    cdr_date = pd.to_datetime(cdr_date_str)

    i=1
    while activate_date > cdr_date:
        print(i)
        activate_date = generate_activation_dates()[0]
        cnic_df.loc[cnic_df['CNIC'] == cnic, 'Activate At'] = activate_date
        i+=1
    print("success")

# Save the updated DataFrame to a CSV file
cnic_df.to_csv('CNIC.csv', index=False)

# Save the DataFrame with CNIC-CDR pairs to a CSV file
cnic_cdr_df.to_csv('CNIC_CDR.csv', index=False)


