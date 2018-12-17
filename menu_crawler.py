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
            try:
                t = price.table
                price = t.find('td').get_text().strip()
            except Exception:
                price = None
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
    if menu is None:  # NO YELP MENU
        return None

    dishDict = {}
    for dish in menu.find_all('div', {'class': 'arrange_unit'}):
        name, description, price = _yelp_dish_parse(dish)
        """if description is not None:
            description = get_ingredients(description + ' ' + name)"""
        if name is not None:
            dishDict[name] = {
                'ingredients': description,
                'price': price
            }

    return dishDict


def get_menu_from_html(link):
    r = req.get(link)
    s = bs(r.text, 'html.parser')
    body = s.body
    h1 = body.find_all('h1')
    h2 = body.find_all('h2')
    h3 = body.find_all('h3')
    h4 = body.find_all('p')
    print(h1, h2, h3, h4)


def get_menu_from_menupages(link):
    # https://menupages.com/mangrove-kitchen/312-divisadero-st-san-francisco
    print('TODO')


def get_non_yelp_menu(name):
    link = util.find_google_menu_link(name, 'menupages')
    print(link)
    if 'menupages' in link:
        return get_menu_from_menupages(link)

    link = util.find_google_menu_link(name, 'menu')
    if 'html' in link:
        print("trying to rawdog it")
        return get_menu_from_html(link)

    return None


def get_flavor_DB_lookup(ingredient):
    pairList = []
    return pairList


def get_harmony_score(menu):
    aggregateScore = 0
    for item in menu:
        pairs = get_flavor_DB_lookup(menu)
        aggregateScore += sum(pairs) / (len(pairs) + 1)
    return 0


def make_menu_bin():
    yelpBin = util.get_top_yelp(location=LOC, term=SEARCH, num=5)
    aggregateMenuBin = []
    for restaurant in yelpBin['businesses']:
        maybeYelpUrl = restaurant['url'].split('/biz')[1].split('?')[0]
        menuDict = format_yelp_menu('https://www.yelp.com/menu' + maybeYelpUrl)
        if menuDict is None:
            print("No Yelp menu, or something broke, trying non")
            menuDict = get_non_yelp_menu(restaurant['name'])
        menuDF = pd.DataFrame(menuDict).transpose()
        if menuDF is not None:
            aggregateMenuBin.append([restaurant['name'], menuDF])
    return aggregateMenuBin


def main():
    menuBin = make_menu_bin()
    harmonyDict = {}
    for menu in menuBin:
        harmonyDict[menu[0]] = get_harmony_score(menu[1])


if __name__ == '__main__':
    main()
