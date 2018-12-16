""" Menu Scraping """
import util
from bs4 import BeautifulSoup as bs
import requests as req
import pandas as pd
from textblob import TextBlob


""" TODO
- Finish creating dictionary of every ingredient in every dish on menu
- Get menu data from non-yelp menus
- Pipeline into FlavorDB
- Harmony score for each dish
"""


LOC = 'San Francisco'
SEARCH = 'Italian food'


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


def get_ingredients(itemDescription):
	decriptionBlob = TextBlob(itemDescription)
	ingredientBin = []
	for np in decriptionBlob.noun_phrases:
		blob = TextBlob(np)
		tag = blob.tags
		filteredTags = list(filter(lambda x: x[1] in ["NN", "NNS", "JJ"], tag))
		if len(filteredTags) > 0:
			ingredient = ""
			for phrase in filteredTags:
				ingredient += phrase[0] + " "
			ingredientBin.append(ingredient.strip())
	return ingredientBin


def format_yelp_menu(menuLink):
    r = req.get(menuLink)
    s = bs(r.text, 'html.parser')
    menu = s.find('div', {'class': 'container biz-menu'})

    dishDict = {}
    for dish in menu.find_all('div', {'class': 'arrange_unit'}):
        name, description, price = _yelp_dish_parse(dish)

        """ TODO TextBlob description Analysis """
        if description is not None:
            description = get_ingredients(description + name)
        if name is not None:
            dishDict[name] = {
                'ingredients': description,
                'price': price
            }

    return dishDict


def make_menu_bin():
    yelpBin = util.get_top_yelp(location=LOC, term=SEARCH, num=20)
    for restaurant in yelpBin['businesses']:
        print('\n' + restaurant['name'])
        menuLink = util.get_restaurant_menu_link(name=restaurant['name'])
        menuDict = {}
        if menuLink is not None:
            menuDict = format_yelp_menu(menuLink)
        else:
            print("Trying non yelp solution")

        menuDF = pd.DataFrame(menuDict).transpose()
        print(menuDF)


make_menu_bin()
