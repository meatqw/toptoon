import requests
from bs4 import BeautifulSoup
from auth import authorization
import os
from sqlalchemy import insert
from db import engine, get_item, items
import translators as ts
import remanga
import time
from random import randint
from bot import send_msg

url_auth = 'https://toptoon.com/login/login_proc'
url_latest = 'https://toptoon.com/latest'
url_hashtag = 'https://toptoon.com/hashtag'
url_weekly = "https://toptoon.com/weekly"

path_ = '/toptoon/'

tg_ids = ['678552606', '1655138958']

def cookie_valid_check_from_content(content):
    """CHECK VALIDATION COOKIE"""
    check_element = content.find('a', {'data-adult': '3'})
    if check_element != None:
        return True
    else:
        return False



def hashtag_handler(url, headers, resource):
    req_get_data = requests.get(url, headers=headers)
    
    all = []
    titles = ''
    links = ''
    if req_get_data.status_code == 200:
        for i in req_get_data.json():
            if i['ribbon']['adult'] == True and i['ribbon']['new'] == True:
                title = i['meta']['title']
                link = 'https://toptoon.com' + i['meta']['comicsListUrl']
                
                titles += title + '\n'
                links += link + '\n'
    
    en = ts.google(titles[:-1], from_language='ko', to_language='en')
    ru = ts.google(titles[:-1], from_language='ko', to_language='ru')
    
    n = 0
    while n < len(links.split('\n')[:-1]):
        data = {'link': links.split('\n')[:-1][n], 'orig_title': titles.split('\n')[:-1][n], 'en_title': en.split('\n')[n], 'ru_title': ru.split('\n')[n], 'resource': resource}
        
        all.append(data)
        n +=1 
                
    return all
    
def add_data_in_db(data):
    # add title in Remanga
    
    
    remanga.main(data)
    
    # add title in db    
    ins = insert(items).values(
        link = data['link'],
        orig_title = data['orig_title'],
        en_title = data['en_title'],
        ru_title = data['ru_title'],
        resource = data['resource']
    )
    conn = engine.connect()
    conn.execute(ins)
    
    time.sleep(randint(20, 40))

def get_items(url):
    """GET LINKS AND TITLE"""
    
    # check cookies file
    if os.path.exists(os.path.abspath(path_ + 'cookies')):
        cookie = open(os.path.abspath(path_ + 'cookies'), 'r+').read()
    else:
        print('Cookie file is not exists')
        print('Authorization')
        authorization()
    
    if os.path.exists(os.path.abspath(path_ + 'cookies')):
        cookie = open(os.path.abspath(path_ + 'cookies'), 'r+').read()
        
        # get data from site
        headers = {"accept": "*/*",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36",
                'cookie': f'rm_session={cookie};'}
            
        req_get_data = requests.get(url, headers=headers)
        
        print(req_get_data.status_code)
        content = BeautifulSoup(req_get_data.content, 'html.parser')
        
        count = 0
        if cookie_valid_check_from_content(content):
            
            print("Cookie is valid")
            # get hashtag data 
            if url == url_hashtag:
                js_content = ' '.join([str(i) for i in content.find_all('script')])
                hashtag_url = js_content.split('HashTag.init({')[1].split("fileUrl: '")[1].split("',")[0]
                hashtag_data = hashtag_handler(hashtag_url, headers, url)
                
                for i in hashtag_data:
                    
                    # check data in database
                    old = get_item(i['link'])
                    print(old)
                    
                    if old == None:
                        
                        print(i)
                        add_data_in_db(i)
                        
                        count += 1
                    
            else:
                all = content.find('div', {'id': 'commonComicList'}).find_all('li')
                
                titles = ''
                links = ''
                for li in all:
                    
                    if li.find('span', {'class': 'icon_19_red'}) != None:
                        
                        link = 'https://toptoon.com' + li.find('a').get('href')
                        title = li.find('span', {'class': 'thumb_tit_text'}).text
                        
                        titles += title + '\n'
                        links += link + '\n'

                print('translate')
                # translat   
                en = ts.google(titles[:-1], from_language='ko', to_language='en')
                ru = ts.google(titles[:-1], from_language='ko', to_language='ru')
                
                print(en)
                        
                print(len(links.split('\n')[:-1]))
                n = 0
                while n < len(links.split('\n')[:-1]):
                    # check data in database
                    old = get_item(links.split('\n')[:-1][n])
                    print(old)
                    if old == None:
                        
                        data = {'link': links.split('\n')[:-1][n], 'orig_title': titles.split('\n')[n], 'en_title': en.split('\n')[n], 'ru_title': ru.split('\n')[n], 'resource': url}
                        print(data)
                        add_data_in_db(data)
                        
                        count += 1
                    n += 1
                
            
            print(f'NEW DATA: {count}')
            for tg_id in tg_ids: 
                send_msg(tg_id, f'{url}: {count}')
            
        else:
            print('Cookie not valid')
            auth = authorization()
            if auth != False:
                print(f'Restart app with URL: {url}')
                pass
            else:
                print('Bad auth')
            
    else:
        print('No working accounts')

def main():
    print('LATEST')
    try:
        get_items(url_latest)
        
    except Exception as e:
        print(e)
        
    print('HASHTAG')
    try:
        get_items(url_hashtag)
    except Exception as e:
        print(e)
        
    print('WEEKLY')
    try:
        get_items(url_weekly)
    except Exception as e:
        print(e)
        
    
main()
