import requests
from bs4 import BeautifulSoup
import pandas as pd
from itertools import zip_longest

# Create empty lists, columns of data we want to scrap
ArticleTitle_list = []
Category_list = []
Link_list = []


class News:
    def GetSoup(self):
        # Save page content
        GetLink = requests.get("https://www.euronews.com/culture/culture-news")
        src = GetLink.content
        # Create soup project to parse content
        soup = BeautifulSoup(src, 'lxml')
        return soup

    def GetElements(self):
        soup = self.GetSoup()  # we called method
        # find the elements containing info we need
        ArticleTitle = soup.find_all("h2", {"class":"m-object__title qa-article-title"})
        Category = soup.find_all("span", {"class":"program-name"})
        return ArticleTitle, Category

    def FillLists(self):
        # Loop over returned lists to extract needed info into other lists
        ArticleTitle, Category = self.GetElements()
        for i in range(len(ArticleTitle)):
            ArticleTitle_list.append(ArticleTitle[i].text)
            Link_list.append(ArticleTitle[i].find("a").attrs['href'])
            Category_list.append(Category[i].text)
        return ArticleTitle_list, Category_list, Link_list

    def SaveResults(self):
        # Create csv file and fill it with values
        ArticleTitle, Category, Link_list = self.FillLists()
        df = pd.DataFrame({
             'Title': ArticleTitle,
             'Category': Category,
             'Link': Link_list,
        })
        df.to_csv('EuroNews.csv')





