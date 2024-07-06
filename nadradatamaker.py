import pandas as pd
import random
from faker import Faker
import uuid
from datetime import datetime, timedelta

# Load the Telco.csv file into a pandas DataFrame
df = pd.read_csv('Telco.csv')

# Initialize the Faker library for generating random data
fake = Faker()

# Create a dictionary to store unique CNICs with corresponding random information
unique_cnic_info = {}

# Function to generate a random date of birth
def random_date_of_birth():
    start_date = datetime(1950, 1, 1)
    end_date = datetime(2005, 12, 31)
    random_days = random.randint(0, (end_date - start_date).days)
    return (start_date + timedelta(days=random_days)).strftime('%Y-%m-%d')

# Iterate through unique CNICs and generate random information
for cnic in df['CNIC'].unique():
    unique_cnic_info[cnic] = {
        'First Name': fake.first_name(),
        'Last Name': fake.last_name(),
        'Date of Birth': random_date_of_birth(),
        'Location Coordinates X': random.uniform(24.0, 35.0),  # Adjust the range as needed
        'Location Coordinates Y': random.uniform(60.0, 77.0),  # Adjust the range as needed
        'City': fake.city(),
        'Age': random.randint(18, 70),  # Adjust the age range as needed
        'Gender': random.choice(['Male', 'Female']),
        'Profession': fake.job(),
        'Father Name': fake.first_name_male() + ' ' + fake.last_name(),
    }

# Create a new DataFrame from the generated information
new_df = pd.DataFrame.from_dict(unique_cnic_info, orient='index')

# Save the generated information to a new CSV file
new_df.to_csv('Generated_Info.csv', index_label='CNIC')

print("Random information generated for unique CNICs and saved as Generated_Info.csv.")
