import requests
from bs4 import BeautifulSoup
import pandas as pd
from itertools import zip_longest

# Create empty lists, column of data ew want to srap
movietitle_list = []
ratings_list = []
year_list = []


class TopMovies:
    def getsoup(self):
        # Save page content
        getlink = requests.get("https://www.imdb.com/chart/top/").text
        # src = getlink.content
        # Create soup object to parse content
        soup = BeautifulSoup(getlink, 'lxml')
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
            movietitle_list.append(movietitle[i].text.strip())
            ratings_list.append(ratings[i].text.strip())
            year_list.append(year[i].text.strip())
        return movietitle_list, ratings_list, year_list

    def saveresults(self):
        # Create csv file and fill it with values
        movietitle, ratings, year = self.fillelists()
        result = list(zip_longest(movietitle, ratings, year))
        df = pd.DataFrame(result)
        df.columns = ['Movie Title', 'IMDB Rating', 'Year']
        df.to_csv('IMDBMovies.csv')

