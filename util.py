""" Quick Restaurant Data Scraping """
import requests as req
from bs4 import BeautifulSoup as bs
import pickle


# Yelp API key
API_KEY = 'RERrcqtrW3V1ARX5kr_3VC9H8DnboL7bkyVf5HdQ-XiRi-hPm2jX_TRBUuc8lDFtYKKF2B_PT1fDai2hsVwCdirNc5Hrk7k9krlw7Vt---u9tZTXjbDZGRyYAxnOW3Yx'
HEADERS = {'Authorization': 'Bearer %s' % API_KEY}


def get_yelp_menu_link(link):
    r = req.get(link)
    s = bs(r.text, 'html.parser')
    menu = s.find('a', {'class': 'menu-explore'})
    if menu:
        return 'https://www.yelp.com' + menu['href']
    else:
        print("Tried to find menu, FAILED")
        return False


def find_google_menu_link(name, term):
    """ Google search --> Yelp lookup """
    r = req.get('https://www.google.com/search?q=' + name + " " + term)
    s = bs(r.text, 'html.parser')
    # This is finding the first link on google responses
    resp = s.find('div', {'class': 'g'})
    aTag = resp.find('a', href=True)
    # Format the found link to be a normal link
    return aTag['href'].split('=')[1].split('&')[0]


def get_top_yelp(location, term, num):
    """ NOW RETURNS LIST OF BUSINESSES """
    totalList = []
    numRequests = int(num/50) + 1

    for i in range(numRequests):
        payload = {
            'term': term,
            'location': location,
            'limit': 50,
            'offset': i*50
        }

        r = req.get('https://api.yelp.com/v3/businesses/search',
                    headers=HEADERS, params=payload)
        totalList += r.json()['businesses']

    return totalList[:num]


def store_data(data, fileName):
    with open(fileName, "wb") as f:
        pickle.dump(data, f)


def open_data(fileName):
    d = None
    try:
        with open(fileName, 'rb') as f:
            d = pickle.load(f)
    except Exception:
        d = None
    return d


def main():
    print(len(get_top_yelp('San Francisco', 'sushi', 70)))


if __name__ == '__main__':
    main()
