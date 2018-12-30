''' Yelp API basic info on the restaurant '''
import util
import requests as req
import pandas as pd


LOC = 'San Francisco'
TERM = 'Mexican'
API_KEY = 'RERrcqtrW3V1ARX5kr_3VC9H8DnboL7bkyVf5HdQ-XiRi-hPm2jX_TRBUuc8lDFtYKKF2B_PT1fDai2hsVwCdirNc5Hrk7k9krlw7Vt---u9tZTXjbDZGRyYAxnOW3Yx'
HEADERS = {'Authorization': 'Bearer %s' % API_KEY}


def get_rest_info_dict(id):
    r = req.get('https://api.yelp.com/v3/businesses/' + id,
                headers=HEADERS)
    response = r.json()

    returnDict = {}
    returnDict['y-price'] = response['price']
    days = response['hours']
    returnDict['restHours'] = {}
    for day in days[0]['open']:
        dayHours = (day['start'], day['end'])
        returnDict['restHours'][day['day']] = dayHours
    returnDict['coords'] = (response['coordinates']['latitude'],
                            response['coordinates']['longitude'])
    returnDict['categories'] = []
    for category in response['categories']:
        returnDict['categories'].append(category["title"])
    returnDict['phone'] = response['phone']
    returnDict['isClaimed'] = response['is_claimed']
    returnDict['transactions'] = response['transactions']

    return returnDict


def get_data_by_city(num, city, term):
    restaurants = util.get_top_yelp(city, term, num)
    rDict = {}
    for rest in restaurants:
        rDict[rest['name']] = get_rest_info_dict(rest['id'])

    return rDict


def main():
    numRestaurants = 5
    df1 = make_df_basic_info(LOC, TERM, numRestaurants)
    with pd.option_context('display.max_rows', None, 'display.max_columns', None):
        print(df1)


if __name__ == '__main__':
    main()
