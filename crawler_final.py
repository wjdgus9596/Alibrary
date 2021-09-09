from selenium import webdriver as wb
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bs
import pandas as pd

def main(point):

    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    chromedriver_path = point + "/chromedriver.exe"
    driver = wb.Chrome(chromedriver_path, options=chrome_options)


    '''
    크롤 - 구독업데이트
    '''
    url = "https://www.youtube.com/feed/subscriptions"
    driver.get(url)

    soup = bs(driver.page_source, 'lxml')
    title = soup.select('a#video-title')
    soup = bs(driver.page_source, 'lxml')
    time = soup.find_all('span','style-scope ytd-grid-video-renderer')
    view_num = [soup.find_all('span','style-scope ytd-grid-video-renderer')[n].string for n in range(0,len(time))]

    title_list = []
    time_list = []

    x = 1
    y = 0
    for i in range(len(title)):
        if "일" in view_num[y] or "중" in view_num[y]:
            view_num.insert(0,"dsf")
        if "최초" not in view_num[y]:
            if "중" not in view_num[x]:
                if "일" not in view_num[x]:
                    title_list.append(title[i].text.strip())
                    time_list.append(view_num[x])
        x += 2
        y += 2


    info = pd.DataFrame({'업데이트영상':title_list})
    timeinfo = pd.DataFrame({'시간':time_list})
    # print(timeinfo)


    '''
    크롤 - 시청기록
    '''
    history_url = "https://myactivity.google.com/activitycontrols/youtube?hl=ko&utm_medium=web&utm_source=youtube&pli=1"
    driver.get(history_url)

    # 스크롤 다운
    body = driver.find_element_by_tag_name('body')
    body.send_keys(Keys.PAGE_DOWN)
    for i in range(1,500):
        body.send_keys(Keys.PAGE_DOWN)
        #time.sleep(0.6)
    soup = bs(driver.page_source, 'lxml')

    history_title = soup.select('div.QTGV3c')

    his_title_list = []
    his_search_list = []

    for i in range(len(history_title)):
        a = history_title[i].text.strip()
        if "검색했습니다" in a:
            a=a.replace("을(를) 검색했습니다.","")
            his_search_list.append(a)
        else:
            a=a.replace("을(를) 시청했습니다.", "")
            his_title_list.append(a)

    '''
    시청기록+검색기록 csv merge
    '''
    his_titleinfo = pd.DataFrame({'시청기록':his_title_list})
    his_searchinfo = pd.DataFrame({'검색기록':his_search_list})
    crawl_merge = pd.concat([info,timeinfo,his_titleinfo,his_searchinfo],axis=1)
    crawl_merge = crawl_merge.fillna('')
    return crawl_merge
if __name__ == '__main__':
    main()