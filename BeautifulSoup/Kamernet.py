import attr
import requests
from bs4 import BeautifulSoup
import pandas as pd
from itertools import zip_longest
import re

# Create empty lists
City_list = []
RoomType_list = []
RentPrice_list = []
SurfaceSize_list = []
AvailableInDate_list = []
Url_list = []

class RealState:
    def GetSoup(self):
        # Save page content
        GetLink = requests.get("https://kamernet.nl/huren/kamers-nederland")
        src = GetLink.content
        # Create soup object to parse content
        soup = BeautifulSoup(src,"lxml")
        return soup

    def GetElements(self):
        soup = self.GetSoup() # we called method
        # find the elements containing info we need
        City = soup.find_all("div",{"class":"tile-city"})
        RoomType = soup.find_all("div", {"class":"tile-room-type"})
        RentPrice = soup.find_all("div", {"class":"tile-rent"})
        SurfaceSize = soup.find_all("div", {"class":"tile-surface"})
        AvailableInDate = soup.find_all("div",{"class":"left"})
        div = soup.find('div', class_='row search-results')
        Url = div.find_all("a", attrs={'href': re.compile("^https://")})
        return City, RoomType, RentPrice, SurfaceSize, AvailableInDate, Url
    def FillLists(self):
        # Loop over returned lists to extract need info other lists
        City, RoomType, RentPrice, SurfaceSize, AvailableInDate, Url = self.GetElements()
        for i in range (len(City)):
            City_list.append(City[i].text)
            # Url_list.append(City[i].find("a").attrs['href'])
            RoomType_list.append(RoomType[i].text)
            RentPrice_list.append(RentPrice[i].text)
            SurfaceSize_list.append(SurfaceSize[i].text)
            AvailableInDate_list.append(AvailableInDate[i].text)
            Url_list.append(Url[i].get('href'))
        return City_list, RoomType_list, RentPrice_list, SurfaceSize_list, AvailableInDate_list, Url_list

    def SaveResults(self):
        # Create csv file and fill it with value
        City, RoomType, RentPrice, SurfaceSize, AvailableInDate, url_list = self.FillLists()
        df = pd.DataFrame ({
          'City': City,
          'Room Type': RoomType,
          'Rent Price': RentPrice,
          'Surface Size': SurfaceSize,
          'Available in date': AvailableInDate,
          'URL': url_list,
        })
        df.to_csv('Kamerent.csv')

