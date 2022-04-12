import requests
from bs4 import BeautifulSoup
import pandas as pd
from itertools import zip_longest

# Create empty lists, columns of data we want to scrap
JobTitle_list = []
CompanyName_list = []
CompanyLocation_list = []
JobType_list = []
NumberEmployees_list = []
JobPoster_list = []
# AboutJob_list = []
CompanyPageLinkedin_list = []
Link_list = []


class Jobs:
    def GetSoup(self):
        # Save page content
        GetLink = requests.get("https://www.linkedin.com/jobs/search/")
        src = GetLink.content
        # Create soup object to parse content
        soup = BeautifulSoup(src, "lxml")
        return soup

    def getElements(self):
        soup = self.GetSoup() # we called method
        # find the elements containing info we need
        JobTitle = soup.find_all("h1", {"class": "t-24 t-bold"})
        CompanyName = soup.find_all("span", {"class":"jobs-unified-top-card__company-name"})
        CompanyLocation = soup.find_all("span", {"class":"jobs-unified-top-card__bullet"})
        JobType = soup.find_all("li", {"class":"jobs-unified-top-card__job-insight"})
        NumberEmployees = soup.find_all("li", {"class":"jobs-unified-top-card__job-insight"})
        JobPoster = soup.find_all("p", {"class":"jobs-poster__name name t-16 t-black t-bold mb0"})
        # AboutJob = soup.find_all()
        CompanyPageLinkedin = soup.find_all("a", {"href":"/company/creamfinance/life/"})
        return JobTitle, CompanyName, CompanyLocation, JobType, NumberEmployees, JobPoster, CompanyPageLinkedin

    def FillLists(self):
        #
        # Loop over returned lists to extract needed info into other lists
        JobTitle, CompanyName, CompanyLocation, JobType, NumberEmployees, JobPoster, CompanyPageLinkedin = self.getElements()
        for i in range (len(JobTitle)):
            JobTitle_list.append(JobTitle[i].text)
            Link_list.append(JobTitle[i].find("a").attrs['href'])
            CompanyName_list.append(CompanyName[i].text)
            CompanyLocation_list.append(CompanyLocation[i].text)
            JobType_list.append(JobType[i].text)
            NumberEmployees_list.append(NumberEmployees[i].text)
            JobPoster_list.append(JobPoster[i].text)
            CompanyPageLinkedin_list(CompanyPageLinkedin[i].text)
        return JobTitle_list, CompanyName_list, CompanyLocation_list, JobType_list, NumberEmployees_list, JobPoster_list, CompanyPageLinkedin_list, Link_list

    def SaveResults(self):
        # Create csv file and fill it with values
        JobTitle, CompanyName, CompanyLocation, JobType, NumberEmployees, JobPoster, CompanyPageLinkedin, Link_list = self.FillLists()
        df = pd.DataFrame({
            'title': JobTitle,
            'Company Name': CompanyName,
            'Company Location': CompanyLocation,
            'JobType': JobType,
            'Number of Employees': NumberEmployees,
            'JobPoster': JobPoster,
            'Company Page': CompanyPageLinkedin,
            'Link': Link_list
        })
        df.to_csv('linkedin.csv')
