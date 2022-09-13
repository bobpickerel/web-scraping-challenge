from bs4 import BeautifulSoup
import requests
import os
import time
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

def scrape_info():
    # Find the news on the mars news site
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    mars_news_url = 'https://redplanetscience.com/'

    browser.visit(mars_news_url)
    # add sleep to let the page render
    time.sleep(1)
    
    mars_news_html = browser.html
    mars_news_soup = BeautifulSoup(mars_news_html, 'lxml')
    mars_news = mars_news_soup.find('div', class_='content_title')
    mars_news_title = mars_news.text

    mars_news_d = mars_news_soup.find('div', class_='article_teaser_body')
    mars_news_desc = mars_news_d.text
    browser.quit()
    

    # Find the image on the jpl site
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    mars_image_url = 'https://spaceimages-mars.com/'

    browser.visit(mars_image_url)
    browser.links.find_by_partial_text('FULL IMAGE').click()
    featured_image_url = browser.url

    featured_image_html = browser.html
    time.sleep(1)
    featured_image_soup = BeautifulSoup(featured_image_html, 'html.parser')
    mars_image = featured_image_soup.find('div', class_='floating_text_area')
    featured_image_location = mars_image.a['href']
    featured_image_location = featured_image_url + featured_image_location
    browser.quit()

    # get Mars table info
    mars_facts_url = 'https://galaxyfacts-mars.com/'
    mars_tables = pd.read_html(mars_facts_url)

    mars_df = mars_tables[0]
    mars_df.columns = ['Mars - Earth Comparison', 'Mars', 'Earth']
    mars_df = mars_df.drop(index=0)
    # export table to html file
    mars_df.to_html('Missions_to_Mars/marstableData.html', index=False)

    # define mars image list
    mars_img_list = []
    mars_data = {}
    hemispheres = []
    mars_dict = {}

    # Find the image on the mars hemispheres site
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    mars_hemi_url = 'https://marshemispheres.com/'

    browser.visit(mars_hemi_url)

    mars_enhanced_soup = BeautifulSoup(browser.html, 'html.parser')

    mars_enhanced_list = []
    mars_enhanced = mars_enhanced_soup.find_all('h3')
    for i in mars_enhanced:
        if i.text != 'Back':
            mars_enhanced_list.append(i.text.strip())
    
    for hemisphere in mars_enhanced_list:
        browser.links.find_by_partial_text(hemisphere).click()
        mars_hemi_soup = BeautifulSoup(browser.html, 'html.parser')
        mars_hemi_image = mars_hemi_soup.find('img', class_='wide-image')
        
        # get location of the image and concat it to form full url
        mars_hemi_image_location = mars_hemi_image['src']
        mars_hemi_image_location = mars_hemi_url + mars_hemi_image_location
        
        # get information for title
        mars_hemi_title = mars_hemi_soup.find('h2', class_='title')
        mars_title = mars_hemi_title.text
        mars_title = mars_title.strip('Enhanced').strip()
    
        # add items to a dictionary


        mars_dict = {
            "title": mars_title,
            "img_url": mars_hemi_image_location
            }
        
        # add dictionary to a list
        mars_img_list.append(mars_dict)

        browser.back()
    
    browser.quit()

    
    # Store data in a dictionary
    mars_data = {
        "mars_news_title": mars_news_title,
        "mars_news_desc": mars_news_desc,
        "featured_image_location": featured_image_location,
        "hemispheres": mars_img_list
    }  
    
    return mars_data