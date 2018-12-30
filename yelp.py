""" Review Scraping """
import util
from bs4 import BeautifulSoup as bs
import requests as req
import pandas as pd
import numpy as np
from tqdm import tqdm


LOC = 'San Francisco'
TERM = ''
URL = 'https://www.yelp.com/biz'


def f_text(s):
    return s.get_text().strip().split(' ')


def scrape_yelp_reviews(link, numReviews):
    returnBin = []
    pages = int(numReviews / 20)
    for i in range(pages):
        """ Every 20 reviews, get next page """
        r = req.get(link + '?start=' + str(i*20))
        s = bs(r.text, 'html.parser')
        reviews = s.find_all('div', {'class': 'review'})
        for rev in reviews[1:]:  # Skip first emtpy one
            userMedia = rev.find('div', {'class': 'media-story'})
            userReviews = userMedia.find('li', {'class': 'review-count'})
            userReviews = int(userReviews.get_text().strip().split(' ')[0])
            reviewBin = rev.find('div', {'class': 'review-wrapper'})
            rating = reviewBin.find('div', {'class': 'i-stars'})['title']
            rating = float(rating.strip().split(' ')[0])
            text = reviewBin.find('p').get_text().strip()
            returnBin.append([rating, userReviews, text])
    return returnBin


def scrape_yelp_other_data(link):
    r = req.get(link)
    s = bs(r.text, 'html.parser')
    photoCount = int(f_text(s.find('a', {'class': 'see-more'}))[2])
    revCount = int(f_text(s.find('span', {'class': 'review-count'}))[0])
    popDishBin = s.find_all('div', {'class': 'popular-dish-content'})
    dishBin = []
    if popDishBin is None:
        return [photoCount, revCount, dishBin]
    for d in popDishBin:
        name = d.find('div', {'class': 'h4'}).get_text().strip()
        numPhotos = d.find('small', {'class': 'photo-count'})
        numPhotos = int(f_text(numPhotos)[0])
        numReviews = d.find('small', {'class': 'review-count'})
        numReviews = int(f_text(numReviews)[0])
        dishBin.append([name, numPhotos, numReviews])
    return photoCount, revCount, dishBin


def print_review_stats(other, df):
    print('Mean rating:', np.mean(df['rating']))
    print('Mean user review count:', np.mean(df['total_reviews']))
    print('Sample size:', len(df['review']))
    print('Photo count:', other[0])
    print('Review count:', other[1])
    print('Review photo ratio:', other[0]/other[1])
    print('Popular dishes', other[2])


def make_yelp_review_dict(restaurants, num):
    rDict = {}
    for r in restaurants[:num]:
        url = URL + r['url'].split('/biz')[1].split('?')[0]
        n = r['name']
        rDict[n] = {}
        rDict[n]['y-reviews'] = scrape_yelp_reviews(url, num)
        photoCount, revCount, dishBin = scrape_yelp_other_data(url)
        rDict[n]['y-photoCount'] = photoCount
        rDict[n]['y-revCount'] = revCount
        rDict[n]['y-dishBin'] = dishBin
    return rDict


def get_data_by_city(num, city, term):
    rests = util.get_top_yelp(city, term, num)
    return make_yelp_review_dict(rests, num)
