

# Import Splinter, BeautifulSoup, and Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
import requests as request


# Set the executable path and initialize Splinter
executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)


# ### Visit the NASA Mars News Site

url = 'https://redplanetscience.com/'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)




# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('div.list_text')

# slide_elem.find('div', class_='content_title')


# Use the parent element to find the first a tag and save it as `news_title`
# .get_text GET TEXT AND NOT THE HTML TAGS
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# Use the parent element to find the paragraph text
# 'div', class_='article_teaser_body' is inside div class ="col-md-8"
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### JPL Space Images Featured Image


# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')



# find the relative image url
img_url_rel = img_soup.find('img', class_='headerimage fade-in').get('src')
img_url_rel



# Use the base url to create an absolute url
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url


# ### Mars Facts


df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.head()


df.columns=['Description', 'Mars', 'Earth']
df.set_index('Description', inplace=True)
df



df.to_html()


# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ### Hemispheres

# ####4 pages 
# base_url =  https://marshemispheres.com/
# link_1 =https://marshemispheres.com/cerberus.html
# link_2 =https://marshemispheres.com/schiaparelli.html
# link_3 =https://marshemispheres.com/syrtis.html
# link_4 =https://marshemispheres.com/valles.html



# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'
browser.visit(url)

response = request.get(url)


html = browser.html
soup_obj = soup(html, 'html.parser')



# extract in format hemisphere_image_urls = [ hemispheres = {title:"",image:"url"}]


# Create a list to hold the images and titles.
hemisphere_image_urls = []

# Get a list of all of the hemispheres will go to each .html file length of this is 4 so loop go thru 4 times
links = browser.find_by_css('a.product-item img')

# Next, loop through those links, click the link, find the sample anchor, return the href
for i in range(len(links)):
    hemisphere = {}
    
    # find link and click
    browser.find_by_css('a.product-item img')[i].click()
    
    # Next, we find the Sample image anchor tag and extract the href
    element = browser.find_link_by_text('Sample').first
    img_url = element['href']
    title = browser.find_by_css("h2.title").text
    
    # Append hemisphere object to list
    hemisphere["img_url"] = img_url
    hemisphere["title"] = title
    hemisphere_image_urls.append(hemisphere)
    # Finally, we navigate bac,
    browser.back()



hemisphere_image_urls



# 5. Quit the browser
browser.quit()




