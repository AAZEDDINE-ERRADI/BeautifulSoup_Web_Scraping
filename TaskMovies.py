import requests
from bs4 import BeautifulSoup
import pandas as pd
from itertools import zip_longest

# Create empty lists, column of data ew want to srap
MovieTitle = []
IMDBRating = []
Year = []
Links = []

class Top_Movies:
    def GetSoup(self):
        # Save page content
        GetLink = requests.get("https://www.imdb.com/chart/top/?ref_=nv_mv_250")
        src = GetLink.content
        # Create soup object to parse content
        soup = BeautifulSoup(src, 'lxml')
        return soup

    def GetElements(self):
        soup = self.GetSoup() # we called the method
        # Find the elements containing info we need
        MovieTitle = soup.find_all("td", {"class":"titleColumn"})
        IMDBRating = soup.find_all("td", {"class":"ratingColumn imdbRating"})
        Year = soup.find_all("span", {"class":"secondaryInfo"})
        return MovieTitle, IMDBRating, Year, Links

    def FillLists(self):
        # Loop over returned lists to extract needed info into other list
        MovieTitle, IMDBRating, Year, Links = self.GetElements()
        for i in range(len(MovieTitle)):
            MovieTitle.append(MovieTitle[i].text)
            Links.append(MovieTitle[i].find("a").attrs['href'])
            IMDBRating.append(IMDBRating[i].text)
            Year.append(Year[i].text)
        return MovieTitle, IMDBRating, Year, Links

    def SaveResults(self):
        # Create csv file and fill it with values
        MovieTitle, IMDBRating, Year, Links = self.FillLists()
        result = list(zip_longest(MovieTitle, IMDBRating, Year, Links))
        df = pd.DataFrame(result)
        df.columns = ['Movie Title', 'IMDB Rating', 'Year', 'Link']
        df.to_csv('movies.csv')

