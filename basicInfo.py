''' Yelp API basic info on the restaurant '''
import util
import requests as req
import pandas as pd


LOC = 'San Francisco'
TERM = 'Mexican'
API_KEY = 'RERrcqtrW3V1ARX5kr_3VC9H8DnboL7bkyVf5HdQ-XiRi-hPm2jX_TRBUuc8lDFtYKKF2B_PT1fDai2hsVwCdirNc5Hrk7k9krlw7Vt---u9tZTXjbDZGRyYAxnOW3Yx'


def get_rest_info(id):
    infoBin = []
    headers = {'Authorization': 'Bearer %s' % API_KEY}
    r = req.get('https://api.yelp.com/v3/businesses/' + id,
                headers=headers)
    response = r.json()
    price = response['price']
    days = response['hours']
    restHours = {}
    for day in days[0]['open']:
        dayHours = (day['start'], day['end'])
        restHours[day['day']] = dayHours
    coords = (response['coordinates']['latitude'],
              response['coordinates']['longitude'])
    categories = []
    for category in response['categories']:
        categories.append(category["title"])
    phone = response['phone']
    isClaimed = response['is_claimed']
    transactions = response['transactions']
    infoBin += [price, restHours, coords, categories, phone,
                isClaimed, transactions]
    return infoBin


def make_df_for_rests(loc, term, numRestaurants):
    restaurants = util.get_top_yelp(loc, term, numRestaurants)['businesses']
    restNames = []
    restInfo = []
    for rest in restaurants:
        restNames.append(rest['name'])
        restInfo.append(get_rest_info(rest['id']))
    axes = ['price', 'hours', 'coordinates', 'categories', 'phone',
            'isClaimed', 'transactions']
    df = pd.DataFrame.from_dict(dict(zip(restNames, restInfo)),
                                orient='index', columns=axes)
    return df


def main():
    numRestaurants = 5
    df1 = make_df_for_rests(LOC, TERM, numRestaurants)
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(df1)


main()
