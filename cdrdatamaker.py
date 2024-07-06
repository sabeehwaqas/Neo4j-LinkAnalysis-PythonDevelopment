import pandas as pd
import numpy as np

# Define the number of rows you want to generate
num_rows = 20000

# Define the columns you want to include in your CSV file
columns = ['Call Date', 'Call Time', 'Duration (Seconds)', 'Caller Number', 'Receiver Number']

# Create an empty DataFrame with the specified columns
df = pd.DataFrame(columns=columns)

# Generate random data for each column
df['Call Date'] = np.random.choice(pd.date_range(start='2021-01-01', end='2021-12-31'), size=num_rows)
df['Call Time'] = np.random.choice(pd.date_range(start='2021-01-01 00:00:00', end='2021-01-01 23:59:59', freq='s').strftime('%H:%M:%S'), size=num_rows)
df['Duration (Seconds)'] = np.random.randint(low=1, high=3600, size=num_rows)

# Generate 5000 unique caller numbers
unique_caller_numbers = np.random.choice(np.arange(923000000, 923999999), size=5000, replace=False)

# Generate 15000 duplicate caller numbers
duplicate_caller_numbers = np.random.choice(unique_caller_numbers, size=15000)

# Combine unique and duplicate caller numbers
caller_numbers = np.concatenate((unique_caller_numbers, duplicate_caller_numbers))

# Set caller numbers
df['Caller Number'] = caller_numbers

# Set receiver numbers as any of the caller numbers
df['Receiver Number'] = np.random.choice(caller_numbers, size=num_rows, replace=True)

# Save the DataFrame to a CSV file
df.to_csv('CDR.csv', index=False)