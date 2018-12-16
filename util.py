""" Quick Restaurant Data Scraping (AGGREGATION) """
import requests as req
from bs4 import BeautifulSoup as bs

# Yelp API key
API_KEY = 'RERrcqtrW3V1ARX5kr_3VC9H8DnboL7bkyVf5HdQ-XiRi-hPm2jX_TRBUuc8lDFtYKKF2B_PT1fDai2hsVwCdirNc5Hrk7k9krlw7Vt---u9tZTXjbDZGRyYAxnOW3Yx'


def get_all_infatuation():
    r = req.get('https://www.theinfatuation.com/api/v1/reviews?' +
                'sort=&city=san-francisco&offset=16&limit=1000')
    if r.status_code != 200:
        print('Something is broken with the infatuation request')
        return False

    s = bs(r.text, 'html.parser')
    links = s.find_all('a', 'feature--table__content')
    data = []

    for f in links:
        name = f.find('div', {'class': 'review-table__title'})
        rating = f.find('div', {'class': 'rating'})
        neighborhood = f.find('div', {'class': 'review-table__neighborhood'})
        price = f.find('div', {'class': 'price-rating large'})['data-price']

        data.append({
            'name': name.string,
            'rating': rating.string,
            'neighborhood': neighborhood.string,
            'price': int(price)
        })
    return data


def _ratingSort(item):
    return item['rating']


def print_sorted_data(data, s):  # _ratingSort
    data.sort(reverse=True, key=s)
    for rest in data:
        print(rest['name'], rest['rating'])


def get_restaurant_menu(name):
    """ Google search --> Yelp lookup """
    r = req.get('https://www.google.com/search?q=' + name + ' yelp')
    s = bs(r.text, 'html.parser')
    # This is finding the first link on google responses
    resp = s.find('div', {'class': 'g'})
    aTag = resp.find('a', href=True)
    # Format the found link to be a normal link
    link = aTag['href'].split('=')[1].split('&')[0]

    """ SOME ERROR HANDLING FOR NON YELP NEEDED"""
    menuLink = get_yelp_menu_link(link)
    if menuLink:
        return menuLink
    else:
        print("Failed with yelp, will keep trying lol")
        return False


def get_yelp_menu_link(link):
    r = req.get(link)
    s = bs(r.text, 'html.parser')
    menu = s.find('a', {'class': 'menu-explore'})
    if menu:
        return 'https://www.yelp.com' + menu['href']
    else:
        print("Tried to find menu, FAILED")
        return False


def get_top_yelp(location, term, num):
    payload = {
        'term': term,
        'location': location,
    }

    headers = {'Authorization': 'Bearer %s' % API_KEY}
    r = req.get('https://api.yelp.com/v3/businesses/search',
                headers=headers, params=payload)
    response = r.json()

    return response


if __name__ == '__main__':
    data = get_all_infatuation()
    print_sorted_data(data, _ratingSort)
