# import dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import pymongo
import pandas as pd

# open a new window with the later link
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

# ----------------------scrape the Nasa Mars News---------------------------
def mars_news(browser):
    # set connection to the news site
    nasa_url = 'https://mars.nasa.gov/news/'
    browser.visit(nasa_url)

    # set up the Beautiful Soup connection
    html = browser.html
    soup = bs(html,'html.parser')

    # get the first news title and quick summary info
    slide = soup.select_one("ul.item_list li.slide")
    title = slide.find('div',class_='content_title').text
    para = slide.find('div',class_='article_teaser_body').text

    # return the news title and paragraph text
    return title, para

# ----------------------scrape the Mars featured image---------------------------
def mars_featureImg(browser):
    # set connection to the news site
    marsImg_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(marsImg_url)

    # find the button to click
    fullImg_button = browser.find_by_id('full_image')
    # clicks the button and brings us to the full image
    fullImg_button.click()

    # splinter: image located in more info > 'more info' button
    moreInfo_button = browser.links.find_by_partial_text('more info')
    moreInfo_button.click()

    # activate the ability to parse the webpage
    html = browser.html
    img_soup = bs(html,'html.parser')

    # image located in img element with class 'main_image'
    img_url = img_soup.find('figure',class_='lede').find('a').get('href')
    img_url = 'https://www.jpl.nasa.gov'+img_url

    # return the featured image url
    return img_url

# ----------------------scrape the Mars Facts---------------------------
def mars_facts(browser):
    # set connection to the news site
    marsFacts_url = 'https://space-facts.com/mars/'
    browser.visit(marsFacts_url)
    
    # gather the facts from the table
    facts_table = pd.read_html(marsFacts_url)

    # use index 0 since it returns a string of values
    mars_df = facts_table[0]
    # rename the columns
    mars_df.columns = ['Fact','Value']

    # return the table of mars facts
    return mars_df

# ----------------------scrape the Mars Hemisphere Images---------------------------
def hemisphere_images(browser):
    # set connection to the news site
    marsHem_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(marsHem_url)

    # activate the ability to parse the webpage
    html = browser.html
    hem_soup = bs(html,'html.parser')

    # collect the item containers
    hem_url = hem_soup.find_all('div',class_='item')

    # create the title and image dictionary for the hemisphere images
    hem_dict = []
    for hem in range(len(hem_url)):
        hem_item = {}    
        # click on each of the links
        browser.find_by_css('a.product-item h3')[hem].click()
        # get the enhanced image title
        hem_item["img_title"] = browser.find_by_css('h2.title').text
        # get the enhanced image link
        hem_item["img_url"] = browser.links.find_by_text('Sample')['href']
        # add it to the hemisphere dictionary
        hem_dict.append(hem_item)
        # have to go back to the main browser page
        browser.back()

    # return the hemisphere image info
    return hem_dict

# ----------------------gather all the info scraped from the other functions---------------------------
def scrape():
    # call the functions
    title, paragraph = mars_news(browser)
    featureImg_url = mars_featureImg(browser)
    table = mars_facts(browser)
    hem_img = hemisphere_images(browser)

    # create the data dictionary to store the info
    data = {
        "news_title":title,
        "news_paragraph":paragraph,
        "featured_image_url":featureImg_url,
        "facts":table,
        "hemisphere_images":hem_img
    }
    
    # close the testing browser
    browser.quit()
    return data

print(scrape())