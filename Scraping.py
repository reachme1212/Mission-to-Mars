# Import dependencies

from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    
    browser = Browser('chrome', **executable_path, headless=False) #if you dont want to see action turn headless=True
        
    news_title, news_paragraph = mars_news(browser)
    
    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemispheres" : hemispheres(browser),
        "last_modified": dt.datetime.now()
        
    }

    browser.quit()
    return data
# Visit the mars nasa news site
# .is_element_present_by_css -accomplishing two things searching for elements with 
# a specific combination of tag (div) and attribute (list_text)

def mars_news(browser):
    
    url = 'https://redplanetscience.com'
    browser.visit(url)

    # Optional delay wait_time=1
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # CSS works from right to left,<=====
    html = browser.html
    news_soup = soup(html, 'html.parser')

    
    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    
    except AttributeError:

        return None, None

           
    return news_title,news_p

###Image Scraping###
def featured_image(browser):

    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:

    # find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
    
    except AttributeError:
        return None   

    # Use the base url to create an absolute url
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    
    return img_url

# ## Mars Facts
def mars_facts():
    try:
        
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    
    except BaseException:
      return None

    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)
    
    return df.to_html(classes="table table-striped")

def hemispheres(browser):
    # 1. Use browser to visit the URL 
    url = 'https://marshemispheres.com/'
    browser.visit(url)

    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []
    links = browser.find_by_css('a.product-item img')
    
    
    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    for i in range(len(links)):
        # find link and click
        hemisphere = {}
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
    return hemisphere_image_urls

if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())