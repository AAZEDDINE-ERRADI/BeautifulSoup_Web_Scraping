import requests
from bs4 import BeautifulSoup
import pandas as pd
from itertools import zip_longest

# Create empty lists, columns of data we want to scrap
jobTitle_list = []
CompanyName_list = []
LocationName_list = []
JobSkills_list = []
Links_list = []

class Jobs:
    def getSoup(self):
        # Save page content
        getlink = requests.get("https://wuzzuf.net/search/jobs/?q=python&a=hpb")
        src = getlink.content
        # Create soup object to parse content
        soup = BeautifulSoup(src, "lxml")
        return soup

    def getElements(self):
        soup = self.getSoup()  # we called the method
        # Find the elements containing info we need
        jobTitle = soup.find_all("h2", {"class": "css-m604qf"})
        companyName = soup.find_all("a", {"class": "css-17s97q8"})
        locationName = soup.find_all("span", {"class": "css-5wys0k"})
        jobSkills = soup.find_all("div", {"class": "css-y4udm8"})
        return jobTitle, companyName, locationName, jobSkills

    def FillLists(self):
        # Loop over returned lists to extract needed info into other lists
        jobTitle, companyName, locationName, jobSkills = self.getElements()
        for i in range(len(jobTitle)):
            jobTitle_list.append(jobTitle[i].text)
            Links_list.append(jobTitle[i].find("a").attrs['href'])
            CompanyName_list.append(companyName[i].text)
            LocationName_list.append(locationName[i].text)
            JobSkills_list.append(jobSkills[i].text)
        return jobTitle_list, CompanyName_list, LocationName_list, JobSkills_list, Links_list

    def saveResults(self):
        # Create csv file and fill it with values
        jobTitle, CompanyName, LocationName, JobSkills, Links_list = self.FillLists()
        result = list(zip_longest(jobTitle, CompanyName, LocationName, JobSkills, Links_list))
        df = pd.DataFrame(result)
        df.columns = ['job title', 'company name', 'location name', 'job skills', 'links']
        df.to_csv('data.csv')


    # def saveResultsWithZip(self):
        # jobTitle, CompanyName, LocationName, JobSkills, Links_list = self.FillLists()
        # fileList = [jobTitle, CompanyName, LocationName, JobSkills, Links_list]
        # exported = zip_longest(*fileList)
        # with open("newData.csv", "w") as myfile:
            # wr = csv.writer(myfile)
            # wr.writerow(["jobTitle", "CompanyName", "LocationName", "JobSkills", "Links_list"])
            # wr.writerows(exported)





