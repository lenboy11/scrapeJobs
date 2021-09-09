from bs4 import BeautifulSoup
import requests
import csv

def main():
    # Initial Values 
    searchTerm = ""
    accentureWeb = 'https://www.accenture.com/de-de/careers/jobsearch?'
    # First Part: Get Country Codes and filter by languages
    source = requests.get( accentureWeb ).text
    soup = BeautifulSoup(source, 'lxml')
    countrylist = soup.find('ul', class_="countrylist")
    cs = {}
    try:
        for country in countrylist.find_all(class_='list-group-item'):
            countryLanguageCode = country['data-country-site'] # Country Code, e.g. za-en (South Africa - English)
            languageCode = country['data-page-language']
            countryCode = country['value']
            # Determine Language (English, German, Spanish, ...)
            textlist = country.text.split() # contains "countryName   ( languageName )"  where the spacing is uncommon and country name can have spaces, e.g. South Africa
            indexl = 1
            indexr = 4
            for i in range(2,len(textlist)):
                if textlist[i] == "(":
                    indexl = i
                elif textlist[i] == ")":
                    indexr = i
                    break
            countryName = ' '.join(textlist[:indexl])   # country['value'] might be in non latin-letters
            languageName = ' '.join(textlist[indexl+1:indexr])
            cs[countryLanguageCode] = [ countryCode, languageCode, countryName, languageName ] # Example -> Key: cn-zh | Values: 中国大陆 (for API), zh-cn (for API), China/Mainland (for UI), Chinese (for UI)
    except Exception as e:
        print("Exception while fetching countryCodes and languageCodes: " + str(e))
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
    csv_file = open('accenture_scrape.csv', 'w', encoding='UTF-8', newline='')
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Country', 'Language', 'Job-Description', 'Link'])
    for code in cs:
        # Payload holds the search values (Entry Level Jobs)
        payload = ("{\"f\":1,\"s\":9,\"k\":\"" + searchTerm + "\",\"lang\":\"" + cs[code][1] + "\",\"cs\":\"" + code + "\",\"df\":\"[{\\\"metadatafieldname\\\":\\\"skill\\\",\\\"items\\\":[]},{\\\"metadatafieldname\\\":\\\"location\\\",\\\"items\\\":[]},{\\\"metadatafieldname\\\":\\\"postedDate\\\",\\\"items\\\":[]},{\\\"metadatafieldname\\\":\\\"travelPercentage\\\",\\\"items\\\":[]},{\\\"metadatafieldname\\\":\\\"jobTypeDescription\\\",\\\"items\\\":[]},{\\\"metadatafieldname\\\":\\\"businessArea\\\",\\\"items\\\":[]},{\\\"metadatafieldname\\\":\\\"specialization\\\",\\\"items\\\":[]},{\\\"metadatafieldname\\\":\\\"workforceEntity\\\",\\\"items\\\":[]}]\",\"c\":\"" +cs[code][0].encode("utf8").decode("utf8") + "\",\"sf\":0,\"syn\":false,\"isPk\":false,\"wordDistance\":0,\"userId\":\"\"}")
        #                 ?       ?             searchTerm (consultant)         languageCode (zh-cn)           countryLanguageCode (cn-zh)                                   Name of the field: Selections                               Name of the field: Selections                                 Name of the field:   Selections                                     Name of the field:     Selections                                      Name of the field: Selections       || For Entry-Level Jobs: {\\\"term\\\":\\\"entry-level job\\\",\\\"selected\\\":true}                 Name of the field: Selections                                     Name of the field:   Selections        countryCode (中国大陆)   ?         ?              ?                      ?            ?
        #                 ?       ?             searchTerm (trainee)            languageCode (es)              countryLanguageCode (cl-es)                                   Name of the field: Selections                               Name of the field: Selections                                 Name of the field:   Selections                                     Name of the field:     Selections                                      Name of the field: Selections                             Name of the field: Selections                                                   Name of the field: Selections                                     Name of the field:   Selections        countryCode (Chile)     ?         ?              ?                      ?            ?
        # Get the Jobs Table
        try: 
            response = requests.request("POST", url, data=payload, headers=headers) # Issues with non latin letters like Chinese
            dict = response.json()
        except Exception as e:
            dict = { 'documents' : [] }
            print( "Exception while sending API Call: " + str(e) )
        
        jobs = dict['documents']
        for job in jobs:
            # Add Country Code to jobUrl before adding it to the csv
            jobUrl = job['jobDetailUrl'].split('/')
            jobUrl[3] = code
            try:
                csv_writer.writerow([cs[code][2], cs[code][3], job['title'], '/'.join(jobUrl) ])
            except Exception as e:
                print("Exception while writing in csv: " + str(e)) # Solved by opening with encoding='UTF-8'

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

#{\"f\":1,\"s\":9,
# \"k\":\"train\",
# \"lang\":\"zh-cn\",
# \"cs\":\"cn-zh\",
# \"df\":\"[{\\\"metadatafieldname\\\":\\\"skill\\\",
#            \\\"items\\\":[]},
#           {\\\"metadatafieldname\\\":\\\"location\\\",
#            \\\"items\\\":[]},
#           {\\\"metadatafieldname\\\":\\\"postedDate\\\",
#            \\\"items\\\":[]},
#           {\\\"metadatafieldname\\\":\\\"travelPercentage\\\",
#            \\\"items\\\":[]},
#           {\\\"metadatafieldname\\\":\\\"jobTypeDescription\\\",
#            \\\"items\\\":[]},
#           {\\\"metadatafieldname\\\":\\\"businessArea\\\",
#            \\\"items\\\":[]},
#           {\\\"metadatafieldname\\\":\\\"specialization\\\",
#            \\\"items\\\":[]},
#           {\\\"metadatafieldname\\\":\\\"workforceEntity\\\",
#            \\\"items\\\":[]}]\",
# \"c\":\"中国大陆\",
# \"sf\":0,
# \"syn\":false,
# \"isPk\":false,
# \"wordDistance\":0,
# \"userId\":\"\"}",
