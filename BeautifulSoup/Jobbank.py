import attr
import requests
from bs4 import BeautifulSoup
import pandas as pd
from itertools import zip_longest
import re

# Create empty lists
JobCanadaTitle_list = []
JobCanadaCompany_list = []
JobCanadaLocation_list = []
Salary_list = []
DateListedJob_list = []

class JobsCanada:
   def GetSoup(self):
       # Save page content
       GetLink = requests.get("https://www.jobbank.gc.ca/jobsearch/jobsearch?searchstring=Data+analyst&locationstring=")
       src = GetLink.content
       # Create soup object to parse content
       soup = BeautifulSoup(src,"lxml")
       return soup

   def GetElements(self):
       soup = self.GetSoup() # we called method
       # find the elements containing info we need
       JobCanadaTitle = soup.find_all("span",{"class":"noctitle"})
       JobCanadaCompany = soup.find_all("li",{"class":"business"})
       JobCanadaLocation = soup.find_all("li",{"class":"location"})
       Salary = soup.find_all("li",{"class":"salary"})
       DateListedJob = soup.find_all("li",{"class":"date"})
       return JobCanadaTitle, JobCanadaCompany, JobCanadaLocation, Salary, DateListedJob
   def FillLists(self):
       # Loop over returned lists to extract need info other lists
       JobCanadaTitle, JobCanadaCompany, JobCanadaLocation, Salary, DateListedJob = self.GetElements()
       for i in range(len(JobCanadaTitle)):
           JobCanadaTitle_list.append(JobCanadaTitle[i].text)
           JobCanadaCompany_list.append(JobCanadaCompany[i].text)
           JobCanadaLocation_list.append(JobCanadaLocation[i].text)
           Salary_list.append(Salary[i].text)
           DateListedJob_list.append(DateListedJob[i].text)
       return JobCanadaTitle_list, JobCanadaCompany_list, JobCanadaLocation_list, Salary_list, DateListedJob_list
   def SaveResults(self):
       # Create cvs file and fill it with value
       JobCanadaTitle, JobCanadaCompany, JobCanadaLocation, Salary, DateListedJob = self.FillLists()
       df = pd.DataFrame({
           'Job Title': JobCanadaTitle,
           'Company Name': JobCanadaCompany,
           'Company Location': JobCanadaLocation,
           'Salary': Salary,
           'Date Listed Job': DateListedJob,
       })
       df.to_csv('Jobbank.csv')