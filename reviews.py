""" Review Scraping """
import util
from bs4 import BeautifulSoup as bs
import requests as req
import pandas as pd


LOC = 'San Francisco'
TERM = 'Sushi'


def get_yelp_reviews(link):
    r = req.get(link)
    s = bs(r.text, 'html.parser')
    reviews = s.find_all('div', {'class': 'review'})
    returnBin = []
    for rev in reviews[1:]:  # Skip first emtpy one
        userMedia = rev.find('div', {'class': 'media-story'})
        userReviews = userMedia.find('li', {'class': 'review-count'}).get_text().strip()
        reviewBin = rev.find('div', {'class': 'review-wrapper'})
        rating = reviewBin.find('div', {'class': 'i-stars'})['title'].strip()
        text = reviewBin.find('p').get_text().strip()
        returnBin.append([rating, userReviews, text])
    return returnBin


def main():
    rests = util.get_top_yelp(LOC, TERM, 10)['businesses']
    rDict = {}
    for r in rests:
        url = 'https://www.yelp.com/biz' + r['url'].split('/biz')[1].split('?')[0]
        rDict[r['name']] = get_yelp_reviews(url)
    print(rDict)


main()
