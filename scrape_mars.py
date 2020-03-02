def scrape():
    from bs4 import BeautifulSoup
    from selenium import webdriver
    import pandas as pd
    import urllib
    import time

    URL_mars_news = "https://mars.nasa.gov/news/"
    URL_mars_image = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    URL_mars_weather = "https://twitter.com/marswxreport?lang=en"
    URL_mars_facts = "http://space-facts.com/mars/"
    URL_mars_hemispheres = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

    # navigate through the URLs and save the htmls
    driver = webdriver.Firefox()
    driver.get(URL_mars_news)
    time.sleep(1)
    html_mars_news = driver.page_source

    driver.get(URL_mars_image)
    time.sleep(1)
    html_mars_image = driver.page_source

    # driver = webdriver.Firefox()
    driver.get(URL_mars_weather)
    time.sleep(1)
    html_mars_weather = driver.page_source

    driver.get(URL_mars_hemispheres)
    time.sleep(1)
    html_mars_hemispheres = driver.page_source


    # Grab Mars News
    soup = BeautifulSoup(html_mars_news, "html.parser")
    mars_latest_news = soup.find("div", class_="list_text")
    mars_latest_news_dict = {
        "date": mars_latest_news.contents[0].text,
        "headline": mars_latest_news.contents[1].text,
        "teaser": mars_latest_news.contents[2].text
    }

    # Grab latest JPL Mars Image
    soup = BeautifulSoup(html_mars_image, "html.parser")
    mars_image = soup.find_all("a", class_="fancybox")
    mars_image_URL = urllib.parse.urljoin("https://www.jpl.nasa.gov", mars_image[1]["data-fancybox-href"])

    # Get Mars Weather
    soup = BeautifulSoup(html_mars_weather, "html.parser")
    mars_weather = soup.find("div", class_="css-901oao r-jwli3a r-1qd0xha r-a023e6 r-16dba41 r-ad9z0x r-bcqeeo r-bnwqim r-qvutc0").text

    # Scrape Mars Facts Table
    dfs = pd.read_html(URL_mars_facts)
    mars_facts = dfs[0]

    # Grab Mars Hemispheres Images
    soup = BeautifulSoup(html_mars_hemispheres, "html.parser")
    mars_hemispheres = soup.find_all("div", class_="item")
    mars_hemisphere_URLs = []
    for item in mars_hemispheres:
        # cycle through each hemisphere link and grab the download link for the enhance tif file
        mars_hemisphere_link = urllib.parse.urljoin("https://astrogeology.usgs.gov", item.a["href"])
        driver.get(mars_hemisphere_link)
        html_mars_hemisphere = driver.page_source
        soup = BeautifulSoup(html_mars_hemisphere, "html.parser")
        mars_hemisphere_download_link = soup.find("div", class_="downloads")

        # append URL to list
        mars_hemisphere_URLs.append(
            {
                "title": item.div.a.text,
                "img_url": mars_hemisphere_download_link.ul.li.a["href"]
            }
        )

    driver.close()

    return {
        "news": mars_latest_news_dict,
        "image": mars_image_URL,
        "weather": mars_weather,
        "facts": mars_facts,
        "hemispheres": mars_hemisphere_URLs
    }

# test code
if __name__ == "__main__":
    result = scrape()
    print(result)