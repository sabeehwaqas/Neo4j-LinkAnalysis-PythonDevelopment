import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta

# Initialize the Faker library for generating random data
fake = Faker()

# Load the passport_2.0.csv file into a pandas DataFrame
passport_df = pd.read_csv('passport_2.0.csv')

# Function to generate a random date
def random_date(start_date, end_date):
    random_time = random.uniform(0, (end_date - start_date).total_seconds())
    return (start_date + timedelta(seconds=random_time)).strftime('%Y-%m-%d')

# Function to generate a random flight number
def random_flight_number():
    return fake.random_int(min=1000, max=9999)

# Function to generate a random departure country
def random_departure_country():
    countries = ["USA", "Canada", "UK", "Australia", "Germany", "France", "Japan", "China", "South Korea", "Brazil"]
    return random.choice(countries)

# Create a list of dictionaries with exit and entry details
exit_entry_data = []

# Iterate through each passport number
for passport_number in passport_df['Passport Number']:
    exit_date = random_date(datetime(2022, 1, 1), datetime(2023, 12, 31))
    entry_date = random_date(datetime(2023, 1, 1), datetime(2023, 12, 31))
    flight_number = random_flight_number()
    departure_country = random_departure_country()

    exit_entry_info = {
        'Passport Number': passport_number,
        'Exit Date': exit_date,
        'Entry Date': entry_date,
        'Flight Number': flight_number,
        'Departure Country': departure_country
    }

    exit_entry_data.append(exit_entry_info)

# Create a DataFrame from the list of exit and entry details
exit_entry_df = pd.DataFrame(exit_entry_data)

# Save the DataFrame to a new CSV file
exit_entry_df.to_csv('exit_entry_detail.csv', index=False)

print("Exit and entry details generated and saved as exit_entry_detail.csv.")
