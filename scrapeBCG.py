# ScrapeBCG.py
from bs4 import BeautifulSoup
import requests
import csv
from urllib import parse

def main():
    # Initial Values 
    keywords = ["trainee", "Trainee", "student", "Student", "graduate", "Graduate", "final year"]
    searchTerm = ""
    bcgWeb = 'https://talent.bcg.com/en_US/apply/SearchJobs/?folderOffset='


    # Save results in csv file
    csv_file = open('bcg_scrape.csv', 'w')
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Job Title', 'Link', 'Job-Description'])


    # Scrape Webpage
    i = 0
    while (i < 1000):
        try:
            source = requests.get( bcgWeb + str(i) ).text
            soup = BeautifulSoup(source, 'lxml')

            jobList = soup.find_all(True, class_='listSingleColumnItem')
            if jobList == None or not jobList:
                break

            for job in jobList:
                title = job.find('a').text
                link = job.find('a')['href']

                source = requests.get(link).text
                soup = BeautifulSoup(source, 'lxml')

                description = soup.find(True, {"class":["jobDetailDescription", "noBorderTop"]}).text

                save = False
                for keyword in keywords:
                    if keyword in str(description):
                        save = True
                        break
                if save:
                    csv_writer.writerow([str(title), str(link)])
        except Exception:
            break

        i += 20

    csv_file.close()

if __name__ == "__main__":
    main()


