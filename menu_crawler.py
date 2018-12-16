""" Menu Scraping """
import util
from bs4 import BeautifulSoup as bs
import requests as req


LOC = 'San Francisco'
SEARCH = 'thai food'


def format_menu(menuLink):
    r = req.get(menuLink)
    s = bs(r.text, 'html.parser')
    menu_bin = s.find('div', {'class': 'menu-sections'})
    for dish in s.find_all('h4'):
        print(dish)
    return menu_bin


def make_menu_bin():
    # searchBin = util.google_search('la viga')
    yelpBin = util.get_top_yelp(location=LOC, term=SEARCH, num=20)
    for restaurant in yelpBin['businesses']:
        print('\n' + restaurant['name'])
        # print("Checking out " + restaurant['name'] + "'s menu")
        menuLink = util.get_restaurant_menu(name=restaurant['name'])
        menuDict = format_menu(menuLink)
        # print(menuDict)


make_menu_bin()
