""" Michelin Guide scraper """

import requests as req
from bs4 import BeautifulSoup as bs
import pandas as pd

CITY = 'San Francisco'
City = CITY.replace(" ", "-").lower()
baseLink = 'https://guide.michelin.com/us/'
# Ratings are : Plate, Bib Gourmand, 1 star, 2 stars, 3 stars
ratingDict = {'‹': 1, '=': 2, 'm': 3, 'n': 4, 'o': 5}


def get_all_michelin(city):
    return get_michelin(city, 5000)


def get_michelin(city, number):
    dataBin = {}
    dataList = []
    if number <= 100:
        link = baseLink + City + '/restaurants/page/1?max='
        + number + '&sort=relevance&order=desc'
        data = scrape_michelin_page(link)
        dataList.append(data)
    else:
        pages = int(number/100 + 2)
        for page in range(1, pages):
            page = str(page)
            link = baseLink + City + '/restaurants/page/' + page + '?max=100&sort=relevance&order=desc'
            data = scrape_michelin_page(link)
            if data is False:
                break
            dataList.append(data)
    dataList = dataList[:number]
    for data in dataList:
        dataBin.update(data)
    return dataBin


def scrape_michelin_page(link):
    r = req.get(link)
    if r.status_code != 200:
        print('Something is broken with the michelin request')
        return False

    s = bs(r.text, 'html.parser')
    links = s.find_all('div', {'class': 'grid-restaurants__item__body'})
    data = {}
    for f in links:
        nameValues = f.find('div', {'class': 'resto-inner-title'}).get_text().strip().split('\n')
        name = nameValues[0]
        ratingRaw = nameValues[1].strip()
        rating = ratingDict[ratingRaw]
        restInfoHelper = f.find('div', {'class': 'resto-inner-category'}).get_text().strip().split("·")
        cuisine = restInfoHelper[0].strip()
        neighborhood = restInfoHelper[1].strip()
        price = restInfoHelper[2].strip()
        data.update({name: [rating, price, cuisine, neighborhood]})
    return data


def make_df_michelin(dataDict):
    axes = ['rating', 'price', 'cuisine', 'neighborhood']
    df = pd.DataFrame.from_dict(dataDict, orient='index', columns=axes)
    return df


def main():
    df1 = make_df_michelin(get_all_michelin(CITY))
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(df1)


main()
