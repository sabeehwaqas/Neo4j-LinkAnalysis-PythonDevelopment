import pandas as pd
import random
import string
from faker import Faker
from datetime import datetime, timedelta

# Initialize the Faker library for generating random data
fake = Faker()

# Function to generate a random 5-digit alphanumeric case number
def random_case_number():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(5))

# Function to generate random crime details
def random_case_detail():
    crimes = [
        "Robbery at a convenience store",
        "Burglary in a residential area",
        "Assault in a public place",
        "Car theft",
        "Shoplifting at a mall",
        "Vandalism in a park",
        "Drug trafficking",
        "Forgery and fraud",
        "Homicide",
        "Kidnapping",
        "Arson",
        "Cybercrime",
        "Human trafficking",
        "Public disturbance",
        "Domestic violence",
        "Identity theft",
        "Assault on an officer",
        "Trespassing",
        "Stalking",
        "Child abuse",
        "Environmental crime",
    ]
    return random.choice(crimes)

# Function to generate a random date and time for FIR
def random_time_of_fir():
    start_date = datetime(2019, 1, 1)
    end_date = datetime(2023, 1, 1)
    random_time = random.uniform(0, (end_date - start_date).total_seconds())
    return (start_date + timedelta(seconds=random_time)).strftime('%Y-%m-%d %H:%M:%S')

# Function to generate a random number of suspects (between 1 and 10)
def random_no_of_suspects():
    return random.randint(1, 10)

# Function to generate random progress (closed or pending)
def random_progress():
    return random.choice(['closed', 'pending'])

# Function to generate a random 8-digit police station number
def random_police_station_number():
    return ''.join(random.choice(string.digits) for _ in range(8))

# Create a list of dictionaries with random data
data = []
for _ in range(10000):  # Generating 10,000 entries
    case_data = {
        'case number': random_case_number(),
        'case detail': random_case_detail(),
        'time of fir': random_time_of_fir(),
        'no of suspects': random_no_of_suspects(),
        'progress': random_progress(),
        'police station numbers': random_police_station_number(),
    }
    data.append(case_data)

# Create a DataFrame from the list of dictionaries
df = pd.DataFrame(data)
print(df.head())

# Save the DataFrame to a CSV file
df.to_csv('Crime_Cases_2.01.csv', index=False)

print("Random crime cases data generated and saved as Crime_Cases_10000.csv.")
