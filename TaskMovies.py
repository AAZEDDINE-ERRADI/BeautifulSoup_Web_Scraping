import requests
from bs4 import BeautifulSoup
import pandas as pd
from itertools import zip_longest

# Create empty lists, column of data ew want to srap
movietitle = []
ratings = []
year = []


class TopMovies:
    def getsoup(self):
        # Save page content
        getlink = requests.get("https://www.imdb.com/chart/top/?ref_=nv_mv_250")
        src = getlink.content
        # Create soup object to parse content
        soup = BeautifulSoup(src, 'lxml')
        return soup

    def getelements(self):
        # we called the method
        soup = self.getsoup()
        # Find the elements containing info we need
        section = soup.find("tbody", class_="lister-list")
        movietitle = section.find_all("td", class_="titleColumn")
        ratings = section.find_all("td", class_="ratingColumn imdbRating")
        year = section.find_all("span", class_="secondaryInfo")
        return movietitle, ratings, year

    def fillelists(self):
        # Loop over returned lists to extract needed info into other list
        movietitle, ratings, year = self.getelements()
        for i in range(len(movietitle)):
            movietitle.append(movietitle[i].text)
            ratings.append(ratings[i].text)
            year.append(year[i].text)
        return movietitle, ratings, year

    def saveresults(self):
        # Create csv file and fill it with values
        movietitle, ratings, year = self.fillelists()
        result = list(zip_longest(movietitle, ratings, year))
        df = pd.DataFrame(result)
        df.columns = ['Movie Title', 'IMDB Rating', 'Year']
        df.to_csv('movies.csv')

