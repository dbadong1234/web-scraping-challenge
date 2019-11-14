#!/usr/bin/env python
# coding: utf-8

# Load Dependencies 
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
from splinter import Browser
import os
from urllib.parse import urlsplit

# ChromeDriver path
executable_path = {"executable_path":"/Users/deanna/Downloads/chromedriver"}
browser = Browser("chrome", **executable_path, headless = False)

# NASA News Site
url = "https://mars.nasa.gov/news/"
browser.visit(url)

# Beautiful Soup parses HTML results 
html = browser.html
soup = bs(html,"html.parser")

# # NASA Mars News
# Print Title and Paragraphs 
title = soup.find("div",class_="content_title").text
paragraph = soup.find("div", class_="article_teaser_body").text
print(f"Title: {title}")
print(f"Para: {paragraph}")


# # JPL Mars Space Images - Featured Image
# URL to navigate to Featured Mars image 
featured_image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(featured_image_url)

base_url = "{0.scheme}://{0.netloc}/".format(urlsplit(featured_image_url))
print(base_url)

xpath = "//*[@id=\"page\"]/section[3]/div/ul/li[1]/a/div/div[2]/img"

mars_feat_image = browser.find_by_xpath(xpath)
img = mars_feat_image[0]
img.click()
html_image = browser.html
soup = bs(html_image, "html.parser")
img_url = soup.find("img", class_="fancybox-image")["src"]
feat_img_url = base_url + img_url
print(feat_img_url)


# # Mars Weather
url_weather = "https://twitter.com/marswxreport?lang=en"
browser.visit(url_weather)
html_weather = browser.html
soup = bs(html_weather, "html.parser")

# To find weather with BS use soup.find('div', attrs=('class': 'tweet', 'data-name': 'Mars Weather'))
mars_weather = soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
print(mars_weather)


# # Mars Facts
facts_url = 'https://space-facts.com/mars/'

facts_table = pd.read_html(facts_url)
facts_table[0]
facts_df = facts_table[0]
# change column names
facts_df.columns = ['Measurement', 'Value']
facts_df.set_index('Measurement')

# Convert Pandas df to HTML String 
facts_html_string = facts_df.to_html()
facts_html_string


# # Mars Hemispheres
hemi_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
browser.visit(hemi_url)

base_hemi_url = "{0.scheme}://{0.netloc}/".format(urlsplit(hemi_url))
print(base_hemi_url)


#Create empty list for image urls 
hemi_image_urls = []

# Get a List of All the Hemispheres
links = browser.find_by_css("a.product-item h3")

for item in range(len(links)):
    hemisphere = {}
    
    # Find Element on Each Loop to Avoid a Stale Element Exception
    browser.find_by_css("a.product-item h3")[item].click()
    
    # Title
    hemisphere["title"] = browser.find_by_css("h2.title").text
    
    # Find Sample Image Anchor Tag & Extract <href>
    sample_element = browser.find_link_by_text("Sample").first
    hemisphere["img_url"] = sample_element["href"]
    

    # Append Hemisphere Object to List
    hemi_image_urls.append(hemisphere)
    
    # Navigate Backwards
    browser.back()

hemi_image_urls


