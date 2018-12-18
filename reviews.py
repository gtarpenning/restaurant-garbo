""" Review Scraping """
import util
from bs4 import BeautifulSoup as bs
import requests as req
import pandas as pd
import numpy as np
from selenium import webdriver
from tqdm import tqdm
import regex as re


LOC = 'San Francisco'
TERM = 'Sushi'


class Driver(object):
    def __init__(self):
        chromeOptions = webdriver.ChromeOptions()
        prefs = {"profile.managed_default_content_settings.images": 2}
        chromeOptions.add_experimental_option("prefs", prefs)
        self.driver = webdriver.Chrome(chrome_options=chromeOptions)

    def getDriver(self):
        return self.driver


def get_goog_reviews(link, numReviews, s):
    returnBin = []
    s = s.getDriver()
    s.get(link)
    s.find_element_by_link_text('View all Google reviews')
    s.click()
    print(s)
    soup = bs(s.page_source, 'lxml')
    print(soup)
    # a = soup.find('a', {'data-async-trigger': 'reviewDialog'})
    # print(a)


def make_goog_review_bin(restaurants, num):
    rDict = {}
    sel = Driver()
    for r in restaurants[:num]:
        print('\nGathering reviews for:', r['name'])
        url = 'https://www.google.com/search?q=' + r['name']
        rDict[r['name']] = get_goog_reviews(url, 100, sel)
        axes = ['rating', 'total_reviews', 'review']
        print_review_stats(pd.DataFrame(rDict[r['name']], columns=axes))


def f_text(s):
    return s.get_text().strip().split(' ')


def scrape_yelp_reviews(link, numReviews):
    returnBin = []
    pages = int(numReviews / 20)
    for i in range(pages):
        """ Every 20 reviews, get next page """
        r = req.get(link + '?start=' + str(i*20))
        s = bs(r.text, 'html.parser')
        photoCount = int(f_text(s.find('a', {'class': 'see-more'}))[2])
        revCount = int(f_text(s.find('span', {'class': 'review-count'}))[0])
        reviews = s.find_all('div', {'class': 'review'})
        for rev in reviews[1:]:  # Skip first emtpy one
            userMedia = rev.find('div', {'class': 'media-story'})
            userReviews = userMedia.find('li', {'class': 'review-count'})
            userReviews = int(userReviews.get_text().strip().split(' ')[0])
            reviewBin = rev.find('div', {'class': 'review-wrapper'})
            rating = reviewBin.find('div', {'class': 'i-stars'})['title']
            rating = float(rating.strip().split(' ')[0])
            text = reviewBin.find('p').get_text().strip()
            returnBin.append([rating, userReviews, photoCount, revCount, text])
    return returnBin


def print_review_stats(df):
    print('Mean rating:', np.mean(df['rating']))
    print('Mean user review count:', np.mean(df['total_reviews']))
    print('Sample size:', len(df['review']))
    print('Photo count:', df['photoCount'][0])
    print('Review count:', df['review count'][0])
    print('Review photo ratio:', df['photoCount'][0]/df['rev count'][0])


def make_yelp_review_bin(restaurants, num):
    rDict = {}
    for r in restaurants[:num]:
        print('\nGathering reviews for:', r['name'])
        url = 'https://www.yelp.com/biz'
        url += r['url'].split('/biz')[1].split('?')[0]
        rDict[r['name']] = scrape_yelp_reviews(url, 100)
        axes = ['rating', 'total_reviews', 'photoCount', 'rev count', 'review']
        print_review_stats(pd.DataFrame(rDict[r['name']], columns=axes))


def main():
    num_restaurants = 10
    rests = util.get_top_yelp(LOC, TERM, num_restaurants)['businesses']
    yelpDict = make_yelp_review_bin(rests, num_restaurants)
    # googDict = make_goog_review_bin(rests, num_restaurants)


main()
