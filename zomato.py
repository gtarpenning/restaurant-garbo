import requests as req
import json
import pandas as pd


API_KEY = 'd355c02b0770fb0b64bd3e6721686b91'
CITY = 'San Francisco'
TERM = 'Sushi'

baseLink = "https://developers.zomato.com/api/v2.1/"
h = {"User-agent": "curl/7.43.0", "Accept": "application/json", "user_key": API_KEY}


def get_data(city, term):
    r = req.get(baseLink + 'cities?q=' + city.replace(' ', '%20'), headers=h)
    cityID = str(json.loads(r.text)['location_suggestions'][0]['id'])

    r = req.get(baseLink + 'search?city_id=' + cityID + '&q=' + term, headers=h)
    response = json.loads(r.text)

    rDict = {}
    for restaurant in response['restaurants']:
        r = restaurant['restaurant']
        rDict[r] = {}
        rDict[r]['z-cost'] = r['average_cost_for_two']
        rDict[r]['z-rating'] = r['user_rating']['aggregate_rating']
        rDict[r]['z-votes'] = r['user_rating']['votes']
        rDict[r]['z-o_support'] = r['opentable_support']
    return rDict


def main():
    print(get_data(CITY, TERM))


if __name__ == '__main__':
    main()
