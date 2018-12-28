import requests as req
from bs4 import BeautifulSoup as bs
import pandas as pd
import util


# City to locate Infatuation reviews
CITY = 'San Francisco'
baseLink = 'https://www.theinfatuation.com'


def get_all_infatuation(city):
    r = req.get(baseLink + '/api/v1/reviews?sort=&city=' +
                city + '&offset=16&limit=1000')
    if r.status_code != 200:
        print('Something is broken with the infatuation request')
        return False

    s = bs(r.text, 'html.parser')
    links = s.find_all('a', 'class=feature--table__content')
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
            'price': int(price),
            'link': baseLink + f['href']
        })
    return data


def _ratingSort(item):
    return item['rating']


def print_sorted_data(data, s):  # _ratingSort
    data.sort(reverse=True, key=s)
    for rest in data:
        print(rest['name'], rest['rating'])


def add_review_text(rBin):
    for i, rest in enumerate(rBin):
        r = req.get(rest['link'])
        s = bs(r.text, 'html.parser')
        reviewHtml = s.find_all('div', {'class': 'post__content__text-block'})
        reviewText = ''
        for p in reviewHtml:
            reviewText += p.get_text().strip() + '\n'
        dishesHtml = s.find_all('div', {'class': 'post__content__dish-block'})
        dishTextDict = {}
        for p in dishesHtml:
            name = p.find('span', {'class': 'dish-block__name'})
            text = p.find('p')
            dishTextDict[name.get_text().strip()] = text.get_text().strip()

        rBin[i]['review'] = reviewText
        rBin[i]['dishes'] = dishTextDict
    return rBin


if __name__ == '__main__':
    c = CITY.replace(' ', '-')
    fName = 'blogs.data'
    data = None
    if util.open_data(fName) is None:
        print("Getting new data")
        data = get_all_infatuation(c)[:5]
        data = add_review_text(data)
        # util.store_data(data, fName)
    else:
        print("Using stored data")
        # data = util.open_data(fName)
    df = pd.DataFrame(data)
    print(df)
