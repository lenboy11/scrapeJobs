# ScrapeGoogle.py
import requests
import csv
from urllib import parse

JobType = 'INTERN'
JobType = 'FULL_TIME'
url = "https://careers.google.com/api/v3/search/?degree=ASSOCIATE&degree=BACHELORS&degree=MASTERS&employment_type=" + JobType + "&jlo=en_US&q="

headers = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7",
    "sec-ch-ua": "\"Google Chrome\";v=\"93\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"93\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "x-client-data": "CIm2yQEIorbJAQjEtskBCKmdygEIjtHKAQiq8soBCIyeywEI7/LLAQiz+MsBCJ75ywEI9vnLAQiw+ssBCL3+ywEIn//LAQjj/8sBCPP/ywEI+f/LAQ==",
    "x-csrftoken": "JnnaChP8UfeUxYYQnoFi5K22a7DHCHrK"
    }

# Save results in csv file
csv_file = open('google_scrape.csv', 'w')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Country', 'Job-Title', 'Link', 'Experience'])

    # Get the Jobs Table
response = requests.request("POST", url, headers=headers)
dict = response.json()
for key in dict:
    print(key + "ey")
    for key2 in dict[key]:
        print(key2 + "ey")


csv_file.close()



# https://careers.google.com/api/v3/search/?
# degree=ASSOCIATE
# &degree=BACHELORS
# &degree=MASTERS
# &distance=50
# &employment_type=FULL_TIME
# &jlo=en_US
# &location=Miami%2C%20FL%2C%20USA&q=

# fetch("https://careers.google.com/api/v3/search/?degree=ASSOCIATE&degree=BACHELORS&degree=MASTERS&distance=50&employment_type=FULL_TIME&employment_type=INTERN&jlo=en_US&location=Miami%2C%20FL%2C%20USA&q=", {
