""" Logistic Regression File """
import infatuation
import yelp
import zomato
import michelin
import basicInfo
import pandas as pd
import util


CITY = 'San Francisco'
TERM = 'sushi'


def _merge(x, y):
    """Given two dicts, merges by key, creating new if no key found in x ."""
    for key in x:
        if key in y:
            x[key] = _merge(x[key], y[key])
            y[key] = None
    for key in y:
        if y[key] is not None:
            x[key] = y[key]
    return x


def test_pull(num, city, term):
    i_names = list(infatuation.get_data_by_city(num, city).keys())
    y_names = list(yelp.get_data_by_city(num, city, term).keys())
    z_names = list(zomato.get_data_by_city(num, city, term).keys())
    m_names = list(michelin.get_data_by_city(num, city).keys())
    b_names = list(basicInfo.get_data_by_city(num, city, term).keys())
    u = set(i_names + y_names + z_names + m_names + b_names)
    u_t = set(y_names + z_names + b_names)
    print("Total unique r names:", len(u))
    print("unique between termed:", len(u_t))


# returns a dictionary of all data for a given city, with rest names as keys
def pull_data_by_city_term(num, city, term):
    """ All functions should return a DICTIONARY of the data, with the NAME of
    the restaurant as the KEYS.
    This will allow for proper DF creation, and servers as a simple continuity
    check. We may need to write a function that checks for similar rest names
    and concatonates key/dict pairs in the full DF/dictionary.
    """
    mDict = {}
    # No term for infatuation
    mDict = _merge(mDict, infatuation.get_data_by_city(num, city))
    mDict = _merge(mDict, yelp.get_data_by_city(num, city, term))
    mDict = _merge(mDict, zomato.get_data_by_city(num, city, term))
    # No term for michelin
    mDict = _merge(mDict, michelin.get_data_by_city(num, city))
    mDict = _merge(mDict, basicInfo.get_data_by_city(num, city, term))

    # util.store_data(mDict, 'penis')


# test_pull(20, CITY, TERM)
pull_data_by_city_term(10, CITY, TERM)
# bobby = util.open_data('penis')
# print(bobby)
