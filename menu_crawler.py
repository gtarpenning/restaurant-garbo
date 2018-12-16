""" Menu Scraping """
import util
from bs4 import BeautifulSoup as bs
import requests as req

""" TODO
- Finish creating dictionary of every ingredient in every dish on menu
- Get menu data from non-yelp menus
- Pipeline into FlavorDB
- Harmony score for each dish
"""


LOC = 'San Francisco'
SEARCH = 'thai food'


def _yelp_dish_parse(dish):
    if dish.find('h4') is None:
        return None, None, None
    else:
        name = dish.find('h4').get_text().strip()
        description = None
        if dish.find('p') is not None:
            """ Found a description for the item """
            description = dish.find('p').get_text().strip()
        price = dish.find('div', {'class': 'menu-item-prices'})
        if price:
            price = price.get_text().strip()
        else:
            """ No price on yelp menu """
            price = None
    return name, description, price


def format_yelp_menu(menuLink):
    r = req.get(menuLink)
    s = bs(r.text, 'html.parser')
    menu = s.find('div', {'class': 'container biz-menu'})

    dishDict = {}
    for dish in menu.find_all('div', {'class': 'arrange_unit'}):
        name, description, price = _yelp_dish_parse(dish)
        if name is not None:
            dishDict[name] = {
                'ingredients': description,
                'price': price
            }

    return dishDict


def make_menu_bin():
    # searchBin = util.google_search('la viga')
    yelpBin = util.get_top_yelp(location=LOC, term=SEARCH, num=20)
    for restaurant in yelpBin['businesses']:
        print('\n' + restaurant['name'])
        # print("Checking out " + restaurant['name'] + "'s menu")
        menuLink = util.get_restaurant_menu_link(name=restaurant['name'])
        menuDict = format_yelp_menu(menuLink)
        print(menuDict)


make_menu_bin()
