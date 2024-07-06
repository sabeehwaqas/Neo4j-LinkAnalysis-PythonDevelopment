import pandas as pd
import random
import string
from faker import Faker
from datetime import datetime, timedelta

# Initialize the Faker library for generating random data
fake = Faker()

# Load the telco.csv file into a pandas DataFrame
telco_df = pd.read_csv('TELCO_2.0.csv')

# Function to generate a random 12-digit alphanumeric passport number
def random_passport_number():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(12))

# Function to generate a random passport expiry date (between 2024 and 2030)
def random_expiry_date():
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2030, 12, 31)
    random_time = random.uniform(0, (end_date - start_date).total_seconds())
    return (start_date + timedelta(seconds=random_time)).strftime('%Y-%m-%d')

# Function to generate a random place of birth
def random_place_of_birth():
    return fake.city()

# Create a list of dictionaries with passport information
passport_data = []

# Iterate through unique CNICs from telco.csv
for cnic in telco_df['CNIC'].unique():
    passport_info = {
        'CNIC': cnic,
        'Passport Number': random_passport_number(),
        'Passport Expiry Date': random_expiry_date(),
        'Place of Birth': random_place_of_birth()
    }
    passport_data.append(passport_info)

# Create a DataFrame from the list of passport information
passport_df = pd.DataFrame(passport_data)

# Save the DataFrame to a CSV file
passport_df.to_csv('passport_2.0.csv', index=False)

print("Passport information generated and saved as passport.csv.")
