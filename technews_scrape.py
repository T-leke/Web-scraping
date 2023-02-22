import bs4
from urllib.request import urlopen as uReq 
from bs4 import BeautifulSoup as soup
import pandas as pd
import pymysql.cursors
import time


def get_news():

    def read_url(url):
        uClient = uReq(url)
        page_html = uClient.read()
        uClient.close()
        page_soup = soup(page_html, "html.parser")
        return page_soup

    url1 = 'https://techcrunch.com/'
    url2 = 'https://venturebeat.com/'

    soup1 = read_url(url1)
    soup2 = read_url(url2)


    def techcrunch():
        news1 = soup1.findAll('h2',{'class':'post-block__title'})
        headnews = {}
        for headline in news1:
            headnews[headline.a.text.strip('\n\t')] = headline.a.get('href')
        news_frame = pd.DataFrame(list(headnews.items()), columns = ['News_headline','News_link'])
        return news_frame.head(5)


    def vbeat():
        news2 = soup2.find('div',{'class':'MainBlock'}).findAll('article')
        headnews = {}
        for headline in news2:
            headnews[headline.h2.text.strip('\n')] = headline.find('a').get('href')
        news_frame = pd.DataFrame(list(headnews.items()), columns = ['News_headline','News_link'])   
        return news_frame.head(5)

    total_news = pd.concat([techcrunch(),vbeat()], ignore_index = True)

    news_list = list(total_news['News_headline'])
    link_list = list(total_news['News_link'])

    connection = pymysql.connect(host='Sql137.main-hosting.eu',
                                user='u729604969_central',
                                password='suseJevoli1',
                                db='u729604969_hexeba',
                                charset='utf8mb4',
                                cursorclass=pymysql.cursors.DictCursor
                                )





    for i in range(len(news_list)):
        with connection.cursor() as cursor:
            sql = 'INSERT INTO TECH_NEWS (news_headline, news_link) VALUES("{}","{}")'.format(news_list[i],link_list[i])
            #print(news_list[i],link_list[i])
            cursor.execute(sql)
            connection.commit()

while True:
    get_news()
    print('code is currently running........')
    time.sleep(3600)


# with connection.cursor() as cursor:

#     sql = 'DELETE FROM TECH_NEWS'

#     cursor.execute(sql)
#     connection.commit()           
        
# with connection.cursor() as cursor:
    
#     sql = 'SELECT * FROM TECH_NEWS'
    
#     cursor.execute(sql)
#     table = cursor.fetchall()
#     connection.commit()

# print(table)