import pandas as pd
import random
from datetime import datetime, timedelta

# Load the CSV file into a pandas DataFrame
df = pd.read_csv('CNIC_CDR.csv')

# Function to generate a random date between 2019-01-01 and today
def random_date():
    start_date = datetime(2019, 1, 1)
    end_date = datetime.now()
    random_days = random.randint(0, (end_date - start_date).days)
    return start_date + timedelta(days=random_days)

# Add a new column "activate at" with random dates
df['activate at'] = [random_date().strftime('%Y-%m-%d %H:%M:%S') for _ in range(len(df))]

# Save the modified DataFrame back to a CSV file
df.to_csv('Telco.csv', index=False)

print("Random dates added to CNIC_CDR.csv and saved as CNIC_CDR_with_dates.csv.")
