import requests
import pandas as pd
from bs4 import BeautifulSoup

# Set the API endpoint and your API key
endpoint = "https://api.glassdoor.com/api/api.htm"
api_key = "your_api_key_here"

# Set the parameters for the API request
# In this case, we are searching for data scientist jobs in Europe
params = {
    "t.p": "your_partner_id_here",
    "t.k": api_key,
    "userip": "your_user_ip_here",
    "useragent": "your_user_agent_here",
    "format": "json",
    "v": "1",
    "action": "jobs-prog",
    "countryId": "8",  # 8 corresponds to Europe
    "jobTitle": "data scientist",
    "pg": "1",  # Page number
}

# Make the API request and get the response
response = requests.get(endpoint, params=params)

# Parse the response into a Beautiful Soup object
soup = BeautifulSoup(response.text, "html.parser")

# Find all job listings in the response
job_listings = soup.find_all("job")

# Create an empty list to store the data
data = []

# Loop through the job listings
for job in job_listings:
    # Get the data for each job listing
    job_title = job.find("jobtitle").text
    company = job.find("company").text
    location = job.find("formattedlocation").text
    summary = job.find("snippet").text

    # Append the data for each job listing to the data list
    data.append({"job_title": job_title, "company": company, "location": location, "summary": summary})

# Create a Pandas dataframe from the data list
df = pd.DataFrame(data)

# Print the dataframe
print(df)
