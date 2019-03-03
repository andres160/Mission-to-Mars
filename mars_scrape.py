import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
from splinter import Browser
import time


# Dealing with the headline

def get_images():
    # your functin should bulild this list of dictionaries
    # return it as a dict, having a key of images
    
 #Mars Featured Image

    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)


    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)

#stir soup for scraping
    html = browser.html
    soup = bs(html, "html.parser")

#have webdriver click links to get to the full image I want
    browser.click_link_by_partial_text('FULL IMAGE')

#had to add this, wasn't working and docs recommended waiting between clicks
    time.sleep(5)
    browser.click_link_by_partial_text('more info')

#stir new soup for scraping the image url
    new_html = browser.html
    new_soup = bs(new_html, 'html.parser')
    temp_img_url = new_soup.find('img', class_='main_image')
    back_half_img_url = temp_img_url.get('src')

    recent_mars_image_url = "https://www.jpl.nasa.gov" + back_half_img_url

    return {"url":recent_mars_image_url}


def get_weather():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)
    url_weather = "https://twitter.com/marswxreport?lang=en"
    browser.visit(url_weather)
    html_weather = browser.html
    soup = bs(html_weather, "html.parser")
    mars_weather = soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    return {'mars_weather':mars_weather}


def get_mars_headline():
    url = "https://mars.nasa.gov/api/v1/news_items/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    resp = requests.get(url).json()
    first_item = resp.get('items')[0]
    return {"item_title": first_item.get('title'), 
            "item_desc": first_item.get('description')
           }

def get_mars_facts_table():
    tables = pd.read_html("https://space-facts.com/mars/") # list of tables, even if there's 1
    table_we_want = tables[0]
    table_we_want.columns = ['Parameter', "Value"]
    formatted =  table_we_want.to_html(classes=["table-bordered", "table-striped", "table-hover"])
    return {"html_table_facts": formatted}


def scrape_master():
    print('scraping stuff')
    facts_table_dict = get_mars_facts_table()
    headlines_dict = get_mars_headline()
    image_dict = get_images()
    weather_dict = get_weather()
    merged_dict = {**facts_table_dict, **headlines_dict, **weather_dict, **image_dict}
    print('done merging')
    # merged dict will be the new data in mongodb
    return merged_dict