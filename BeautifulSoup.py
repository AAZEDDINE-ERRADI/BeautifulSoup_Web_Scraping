import requests
from bs4 import BeautifulSoup
import csv
from itertools import zip_longest

# Create empty lists
jobTitle = []
CompanyName = []
LocationName = []
JobSkills = []
Links = []

# Save page content
getlink = requests.get("https://wuzzuf.net/search/jobs/?q=python&a=hpb")
src = getlink.content
print(src)

# Create soup object to parse content
soup = BeautifulSoup(src, "lxml")
print(soup)

# Find the elements containing info we need
jobTitle = soup.find_all("h2", {"class":"css-m604qf"})
CompanyName = soup.find_all("a", {"class":"css-17s97q8"})
LocationName = soup.find_all("span", {"class":"css-5wys0k"})
JobSkills = soup.find_all("div", {"class":"css-y4udm8"})
print(jobTitle, CompanyName, LocationName, JobSkills)

# Loop over returned lists to extract needed info into other lists
for i in range (len(jobTitle)):
    jobTitle.append(jobTitle[i].text)
    Links.append(jobTitle[i].find("a").attrs['target'])
    CompanyName.append(CompanyName[i].text)
    LocationName.append(LocationName[i].text)
    JobSkills.append(JobSkills[i].text)
print(CompanyName, LocationName, JobSkills, Links)

# Create csv file and fill it with values
fileList = [jobTitle, CompanyName, LocationName, JobSkills, Links]
exported = zip_longest(*fileList)
with open("\Users\Azdinerradi\Downloads\jobs.csv", "w") as myfile:
       wr = csv.writer(myfile)
       wr.writerow("job Title", "Company Name", "Loction Name", "Job Skills", "Links")
       wr.writerows(exported)



