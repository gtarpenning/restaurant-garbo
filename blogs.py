import requests as req
from bs4 import BeautifulSoup as bs


# City to locate Infatuation reviews
CITY = 'San Francisco'


def get_all_infatuation(city):
    r = req.get('https://www.theinfatuation.com/api/v1/reviews?' +
                'sort=&city=' + city + '&offset=16&limit=1000')
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


if __name__ == '__main__':
    c = CITY.replace(' ', '-')
    data = get_all_infatuation(c)
    print_sorted_data(data, _ratingSort)
