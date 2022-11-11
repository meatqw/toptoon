from dynamic.dynamic import create_driver
from selenium.webdriver.common.by import By
import requests
from bs4 import BeautifulSoup
import time
import json
import os

url = 'https://toptoon.com/latest'
path_ = '/toptoon/'
# path_ = '/home/oleg/python/toptoon/'

def get_account():
    """GET VALID ACCOUNT"""
    with open(os.path.abspath(path_ + 'acc.json'), 'r+') as acc_file:
        acc = [i for i in json.load(acc_file)]
        
    if len(acc) > 0:
        return acc[0]
    else:
        return None
        
        
def cookie_valid_check():
    
    cookie = open(os.path.abspath(path_ + 'cookies'), 'r+').read()
    
    headers = {"accept": "*/*",
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36",
            'cookie': f'rm_session={cookie};'}
    
    # req 
    req_get_data = requests.get(url, headers=headers)
    content = BeautifulSoup(req_get_data.content, 'html.parser')

    check_element = content.find('a', {'data-adult': '3'})
    print(check_element)
    if check_element != None:
        return True
    else:
        return False
    


def authorization():
    
    account = get_account()
    if account != None:
    
        driver = create_driver(headless=False)

        driver.get('https://toptoon.com/latest?layer=/alert/auth/login')
        time.sleep(9)

        print('Site load')
        # authentication
        login_input = driver.find_element(By.XPATH, "//input[@name='userId']")
        password_input = driver.find_element(By.XPATH, "//input[@name='userPw']")

        print('enter data')
        login_input.send_keys(account['login'])
        time.sleep(5)
        password_input.send_keys(account['password'])
        time.sleep(5)

        print('click ok')
        btn_login = driver.find_element(By.XPATH, "//button[@class='confirm-button']")
        btn_login.click()

        time.sleep(10)
        
        cookies_data = driver.get_cookies()
        
        print('driver close')
        driver.close()

        print('save cookies')
        for i in cookies_data:
            if i['name'] == 'rm_session':
                print(i['value'])
                with open(os.path.abspath(path_ + 'cookies'), 'w+') as cookie_file:
                    cookie_file.write(i['value'])

        if cookie_valid_check():
            return True
        else:
            print('Not valid')
            return False
            
    else:
        print('No working accounts')
        return False