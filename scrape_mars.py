# dependencies
from bs4 import BeautifulSoup as bs

import requests
from splinter import Browser
from selenium import webdriver
import pandas as pd

def scrape():
    # set up for scraping NASA website
    executable_path = {"executable_path": "chromedriver"}
    browser = Browser("chrome", **executable_path, headless=False)

    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)

    html = browser.html
    soup = bs(html, "html.parser")

    # Title
    news_title = soup.body.find('div', class_='content_title').get_text()
    # article teaser text
    news_p = soup.find('div', class_='article_teaser_body').get_text()

    # set up for scraping JPL site for images
    executable_path = {"executable_path": "chromedriver"}
    browser = Browser("chrome", **executable_path, headless=False)

    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)

    html = browser.html
    soup = bs(html, "html.parser")

    featured_img = soup.find('a', class_='button fancybox')['data-fancybox-href']

    featured_image_url = "https://www.jpl.nasa.gov" + featured_img
    
    # mars weather tweets scrape set up
    executable_path = {"executable_path": "chromedriver"}
    browser = Browser("chrome", **executable_path, headless=False)

    url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url)

    html = browser.html
    soup = bs(html, "html.parser")

    tweets = soup.find_all("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")

    for tweet in tweets:
        tweet_parent = tweet.find_parent("div", class_="content")
        tweet_id = tweet_parent.find("a", class_="account-group js-account-group js-action-profile js-user-profile-link js-nav")["href"]
        if tweet_id == '/MarsWxReport':
            mars_weather = tweet_parent.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").get_text()
            if mars_weather[:3] == "Sol":
                break

    # Mars Facts
    url = 'https://space-facts.com/mars/'

    table_facts = pd.read_html(url)

    df = table_facts[0]
    df.columns = ["Description", "Value"]
    df.set_index(df["Description"], inplace=True)

    df = df[['Value']]

    table_facts = df.to_html()
    table_facts = table_facts.replace('\n', '')

    executable_path = {"executable_path": "chromedriver"}
    browser = Browser("chrome", **executable_path, headless=False)

    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)

    html = browser.html
    soup = bs(html, "html.parser")

    h3s = soup.find_all("h3")

    titles = []
    for h3 in h3s:
        h3 = str(h3)
        h3 = h3[4:-14]
        titles.append(h3)
    titles

    img_urls = []
    for title in titles:
        browser.click_link_by_partial_text(title)

        html = browser.html
        soup = bs(html, "html.parser")

        img_urls.append(soup.find("div", class_="downloads").find("a")["href"])
    img_urls

    hemisphere_image_urls = []
    for title, img_url in zip(titles, img_urls):
        hemisphere_image_urls.append({"title": title, "img_url":img_url})

    hemisphere_image_urls

    mars_data = {"news_title": news_title, "news_p": news_p, "featured_image_url": featured_image_url,\
    "mars_weather": mars_weather, "html_table": table_facts, "hemisphere_image_urls": hemisphere_image_urls}

    return mars_data



