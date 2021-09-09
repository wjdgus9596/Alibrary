import pandas as pd
from selenium import webdriver as wb
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs
import requests

def main(df,point):
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    chromedriver_path = point + "/chromedriver.exe"
    driver = wb.Chrome(chromedriver_path, options=chrome_options)

    list = []
    linklist = []
    for line in df:
        url = 'https://youtube.com/results?search_query=' + line
        driver.get(url)
        soup = bs(driver.page_source, 'html.parser')
        search_titles = soup.select("a[id=video-title]")
        first_title = []
        first_link = []
        for title in search_titles:
            title = title.get('title')
            first_title.append(title)
        search_links = soup.select("a[id=thumbnail]")
        for link in search_links:
            link = link.get('href')
            first_link.append(link)
        list1 = first_title[0]
        list2 = 'https://www.youtube.com' + first_link[0]
        list.append(list1)
        linklist.append(list2)

    '''csv 저장'''
    info = pd.DataFrame({"추천영상":list, "url": linklist})
    return info

if __name__ == '__main__':
    main()