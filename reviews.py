""" Review Scraping """
import util
from bs4 import BeautifulSoup as bs
import requests as req
import pandas as pd
import numpy as np
from tqdm import tqdm


LOC = 'San Francisco'
TERM = 'Sushi'


def get_yelp_reviews(link, numReviews):
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
            rating = reviewBin.find('div', {'class': 'i-stars'})['title'].strip()
            rating = float(rating.split(' ')[0])
            text = reviewBin.find('p').get_text().strip()
            returnBin.append([rating, userReviews, text])
    return returnBin


def main():
    rests = util.get_top_yelp(LOC, TERM, 1)['businesses']
    rDict = {}
    for r in rests[:2]:
        print('\nGathering reviews for:', r['name'])
        url = 'https://www.yelp.com/biz' + r['url'].split('/biz')[1].split('?')[0]
        rDict[r['name']] = get_yelp_reviews(url, 100)
        axes = ['rating', 'total_reviews', 'review']
        df = pd.DataFrame(rDict[r['name']], columns=axes)
        print('Mean rating:', np.mean(df['rating']))
        print('Mean user review count:', np.mean(df['total_reviews']))
        print('Sample size:', len(df['review']))


main()
