from bs4 import BeautifulSoup
import requests
import csv
from urllib import parse

def main():
    # Initial Values 
    searchTerm = ""
    accentureWeb = 'https://www.accenture.com/'
    # First Part: Get Country Codes and filter by languages
    source = requests.get( accentureWeb + 'de-de/careers/jobsearch?' ).text
    soup = BeautifulSoup(source, 'lxml')
    countrylist = soup.find('ul', class_="countrylist")
    cs = {}
    lang = []
    for country in countrylist.find_all(class_='list-group-item'):
        countryCode = country['data-country-site']
        # Filter by languages german (de) and english (en)
        if 'en' in countryCode or 'de' in countryCode:      
            cs[countryCode] = [ countryCode[3:5] , country['value'], country.text.split()[2] ]
    # Second Part: Get Jobs for each country
    url = "https://www.accenture.com/api/sitecore/JobSearch/FindJobs"
    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-language": "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7",
        "content-type": "application/json; charset=UTF-8",
        "sec-ch-ua": "\"Google Chrome\";v=\"93\", \" Not;A Brand\";v=\"99\", \"Chromium\";v=\"93\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "x-requested-with": "XMLHttpRequest"
        }
    # Save results in csv file
    csv_file = open('accenture_scrape.csv', 'w')
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Country', 'Job-Description', 'Link'])
    for countryCode in cs:
        # Payload holds the search values (Entry Level Jobs)
        payload = "{\"f\":1,\"s\":9,\"k\":\"" + searchTerm + "\",\"lang\":\"" + cs[countryCode][0] + "\",\"cs\":\"" + countryCode + "\",\"df\":\"[{\\\"metadatafieldname\\\":\\\"skill\\\",\\\"items\\\":[]},{\\\"metadatafieldname\\\":\\\"location\\\",\\\"items\\\":[]},{\\\"metadatafieldname\\\":\\\"postedDate\\\",\\\"items\\\":[]},{\\\"metadatafieldname\\\":\\\"travelPercentage\\\",\\\"items\\\":[]},{\\\"metadatafieldname\\\":\\\"jobTypeDescription\\\",\\\"items\\\":[{\\\"term\\\":\\\"entry-level job\\\",\\\"selected\\\":true}]},{\\\"metadatafieldname\\\":\\\"businessArea\\\",\\\"items\\\":[]},{\\\"metadatafieldname\\\":\\\"specialization\\\",\\\"items\\\":[]},{\\\"metadatafieldname\\\":\\\"workforceEntity\\\",\\\"items\\\":[]}]\",\"c\":\"" + cs[countryCode][1] + "\",\"sf\":0,\"syn\":false,\"isPk\":false,\"wordDistance\":0,\"userId\":\"\"}"
        #                 ?       ?             searchTerm (consultant)         Language (en)                         countryCode (us-en)                                   Name of the field: Selections                               Name of the field: Selections                                 Name of the field:   Selections                                     Name of the field:     Selections                                      Name of the field: Selections                     Entry-Level Job is selected                                                      Name of the field: Selections                                     Name of the field:   Selections                                    Name of the field:     Selections                     countryName (Deutschland)       ?           ?               ?                   ?             ?
        # Get the Jobs Table
        response = requests.request("POST", url, data=payload, headers=headers)
        dict = response.json()
        jobs = dict['documents']
        for job in jobs:
            # Add Country Code to jobUrl before adding it to the csv
            jobUrl = job['jobDetailUrl'].split('/')
            jobUrl[3] = countryCode
            csv_writer.writerow([str(cs[countryCode][1]) + " (" + str(cs[countryCode][2]) + ")" , job['title'], '/'.join(jobUrl) ])
            # accentureWeb + countryCode + "/jobdetails?id=" + job['id'] + "&title=" + parse.quote_plus(job['title'], safe='()')
    csv_file.close()

if __name__=="__main__":
    main()


# Payload in Detail:
#  "{\"f\":1,
#    \"s\":9,
#    \"k\":\"\",
#    \"lang\":\"en\",
#    \"cs\":\"za-en\",
#    \"df\":\"[{\\\"metadatafieldname\\\":\\\"skill\\\",
#               \\\"items\\\":[]},
#              {\\\"metadatafieldname\\\":\\\"location\\\",
#               \\\"items\\\":[]},
#              {\\\"metadatafieldname\\\":\\\"postedDate\\\",
#               \\\"items\\\":[]},
#              {\\\"metadatafieldname\\\":\\\"travelPercentage\\\",
#               \\\"items\\\":[]},
#              {\\\"metadatafieldname\\\":\\\"jobTypeDescription\\\",
#               \\\"items\\\":[]},
#              {\\\"metadatafieldname\\\":\\\"businessArea\\\",
#               \\\"items\\\":[]},
#              {\\\"metadatafieldname\\\":\\\"specialization\\\",
#               \\\"items\\\":[]},
#              {\\\"metadatafieldname\\\":\\\"workforceEntity\\\",
#               \\\"items\\\":[]}]\",
#   \"c\":\"South Africa\",
#   \"sf\":1,
#   \"syn\":false,
#   \"isPk\":false,
#   \"wordDistance\":0,
#   \"userId\":\"\"}",

