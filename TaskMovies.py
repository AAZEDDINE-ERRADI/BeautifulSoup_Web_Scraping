import requests
from bs4 import BeautifulSoup
# import csv
# from itertools import zip_longest

# Create empty list
MovieTitle = []
IMDBRating = []
Year = []
Links = []

# Save page content
GetLink = requests.get("https://www.imdb.com/chart/top/?ref_=nv_mv_250")
src = GetLink.content
print(src)

# Create soup object to parse content
soup = BeautifulSoup(src, 'lxml')
print(soup)

# Find the elements containing info we need
MovieTitle = soup.find_all("td", {"class":"titleColumn"})
IMDBRating = soup.find_all("td", {"class":"ratingColumn imdbRating"})
Year = soup.find_all("span", {"class":"secondaryInfo"})
print (MovieTitle, IMDBRating, Year, Links)

# Loop over returned lists to extract needed info into other list
for i in range (len(MovieTitle)):
    MovieTitle.append(MovieTitle[i].text)
    Links.append(MovieTitle[i].find("a").attrs['href'])
    IMDBRating.append(IMDBRating[i].text)
    Year.append(Year[i].text)
print(MovieTitle, IMDBRating, Year, Links)

# Create csv file and fill it with values
# fileList = [MovieTitle, IMDBRating, Year, Links]
# exported = zip_longest(*fileList)
# with open("\Users\Azdin erradi\Desktop\Movies.csv", "w") as myfile:
   # wr = csv.writer(myfile)
   # wr.writerow("MovieTitle", IMDBRating, Year, Links)
   # wr.writerows(exported)

