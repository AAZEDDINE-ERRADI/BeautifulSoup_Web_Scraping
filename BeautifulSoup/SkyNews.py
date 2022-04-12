import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
from itertools import zip_longest

# Create empty lists, columns of data we want to scrap
TitleNews_list = []
Description_list = []
DateTime_list = []
Fotball_list = []
ArticleLink_list = []

class Sky:
    def GetSoup(self):
        # Save page content
        GetLink = requests.get("https://www.skysports.com/football/news")
        src = GetLink.content
        # Create soup object to parse content
        soup = BeautifulSoup(src, "lxml")
        return soup

    def GetElements(self):
        soup = self.GetSoup() # we called method
        # find the elements containing info we need
        TitleNews = soup.find_all("h4", {"class":"news-list__headline"})
        Description = soup.find_all("p", {"class":"news-list__snippet"})
        DateTime = soup.find_all("span", {"class":"label__timestamp"})
        Fotball = soup.find_all("a", {"class":"label__tag"})
        return TitleNews, Description, DateTime, Fotball

    def FillLists(self):
        # Loop over returned lists to extract need info into other lists
        TitleNews, Description, DateTime, Fotball = self.GetElements()
        for i in range(len(TitleNews)):
            TitleNews_list.append(TitleNews[i].text)
            ArticleLink_list.append(TitleNews[i].find("a").attrs['href'])
            Description_list.append(Description[i].text)
            DateTime_list.append(DateTime[i].text)
            Fotball_list.append(Fotball[i].text)
        return TitleNews_list, Description_list, DateTime_list, Fotball_list, ArticleLink_list

    def SaveResults(self):
        # Create csv file and fill it with value
        TitleNews, Description, DateTime, Fotball, ArticleLink_list = self.FillLists()
        df = pd.DataFrame({
            'Title News': TitleNews,
            'Description': Description,
            'Date/Time': DateTime,
            'Fotball': Fotball,
            'Article Link': ArticleLink_list,
        })
        df.to_csv('SkyNews.csv')