from urllib import request
import requests
from dynamic.dynamic import create_driver
from selenium.webdriver.common.by import By
import requests
from bs4 import BeautifulSoup
import time
import base64
import os

login = 'Танторик'
password = 'Vargon165318'


def auth():
    """Auth in remanga, parsing and save token"""
    driver = create_driver(headless=True)

    driver.get('https://remanga.org/')
    time.sleep(10)

    ok_btn = driver.find_element(
        By.XPATH, "//*[contains(text(), ' Принять ')]")
    ok_btn.click()

    time.sleep(4)

    log_btn = driver.find_element(By.XPATH, "//*[contains(text(), 'Войти')]")
    log_btn.click()

    time.sleep(3)

    log_btn_how = driver.find_element(
        By.XPATH, "//*[contains(text(), 'Через Почту')]")
    log_btn_how.click()

    time.sleep(3)

    # authentication
    login_input = driver.find_element(By.XPATH, "//input[@name='user']")
    password_input = driver.find_element(By.XPATH, "//input[@name='password']")

    login_input.send_keys(login)
    time.sleep(2)
    password_input.send_keys(password)
    time.sleep(2)

    btn_login = driver.find_element(By.XPATH, "//button[@type='submit']")
    btn_login.click()

    time.sleep(8)

    for i in driver.get_cookies():
        if i['name'] == 'token':
            with open(os.path.abspath('cookiesUser'), 'w+') as cookie_file:
                cookie_file.write(i['value'])

    driver.close()


def test_token():
    if os.path.exists(os.path.abspath('cookiesUser')):
        cookie = open(os.path.abspath('cookiesUser'), 'r+').read()
        
        # get data from site
        headers = {"accept": "*/*",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36",
                'authorization': f'bearer {cookie}',
                'content-type': 'application/json',
                'origin': 'https://remanga.org',
                'referer': 'https://remanga.org/'}
    
    request = requests.get('https://api.remanga.org/api/users/current/', headers=headers)
    return request.status_code


def add_title(data):
    """Send title on remanga""" 
    
    
    if os.path.exists(os.path.abspath('cookiesUser')):
        cookie = open(os.path.abspath('cookiesUser'), 'r+').read()
        
        # get data from site
        headers = {"accept": "*/*",
            "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36",
                'authorization': f'bearer {cookie}',
                'content-type': 'application/json',
                'origin': 'https://remanga.org',
                'referer': 'https://remanga.org/'}
        
        print(headers)
        
    with open(os.path.abspath("title.jpg"), "rb") as image_file:
        img = base64.b64encode(image_file.read())
    
    link = data['link']
    orig_title = data['orig_title']
    en_title = data['en_title']
    ru_title = data['ru_title']
    resource = data['resource']
    
    
    
    title_data = {"rus_name": ru_title,
            "en_name": en_title,
            "another_name": orig_title,
            "issue_year": "2022",
            "original_link": link,
            "anlate_link": link,
            "adaptation_link": "",
            "user_message": "Описание, теги и обложку изменим позднее на подходящие",
            "description": "Позже",
            "type": 1,
            "status": 1,
            "age_limit": 2,
            "categories": [5, 6, 12],
            "genres": [5, 25, 21],
            "publishers": [10355],
            "cover": 'data:image/jpeg;base64,' + str(img)[2:-1]}
    
    request = requests.post('https://api.remanga.org/api/titles/', headers=headers, json=title_data)
    print(request.json())


def main(data):
    if test_token() == 200:
        try:
            add_title(data)
        except Exception as e: 
            print(e)
    else:
        print('Bad token')
        try:
            auth()
            add_title(data)
        except Exception as e:
            print(e)