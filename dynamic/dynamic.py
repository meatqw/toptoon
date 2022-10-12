from selenium import webdriver
# import undetected_chromedriver.v2 as uc
import os
import settings

# from selenium.webdriver.common.by import By

# def threading_start(th_num, target, arr):
#    """Create threads"""
#    th_arr = numpy.array_split(arr, th_num)
#    threads = []

#    for i in th_arr:
#       threads.append(Thread(target=target, args=(i,)))

#    for a in threads:
#        a.start()
#        time.sleep(random.randrange(3, 5))
#        print(f'[INFO]: {proxy_list}')

#    for a in threads:
#       a.join()


def create_driver(proxy=False, headless=False, ext=False, undetected=False):
    """ Create driver
    proxy state: address or False
    headless state: True or False
    ext state: True or False
    """

    # using proxy
    if proxy is not False:
        options_proxy = {
            'proxy': {
                'http': f'http://{proxy}',
                'https': f'https://{proxy}',
                'no_proxy': 'localhost,127.0.0.1,dev_server:8080'
            }
        }

    # using undetected chromedriver
    if undetected:
        print('[DRIVER]: UNDETECTED MODE - ON')
        # options = uc.ChromeOptions()
    else:
        print('[DRIVER]: UNDETECTED MODE - OFF')
        chrome = os.path.abspath(settings.DRIVER)

        caps = webdriver.DesiredCapabilities().CHROME
        caps["pageLoadStrategy"] = "eager"

        options = webdriver.ChromeOptions()


    # using headless mode
    if headless:
        print('[DRIVER]: HEADLESS MODE - ON')
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--window-size=1920x1080')
    else:
        print('[DRIVER]: HEADLESS MODE - OFF')

    # using extensions
    if ext:
        print('[DRIVER]: EXT - ON')
        options.add_extension(settings.EXT_PATH)
        # options.add_argument(f'--load-extension={settings.EXT_PATH}')
    else:
        print('[DRIVER]: EXT - OFF')

    if proxy is not False:
        print('[DRIVER]: PROXY - ON')
        # undetected
        if undetected:
            # undetected add proxy
            options.add_argument(f"--proxy-server={proxy}")

            # driver = uc.Chrome(options=options)
        else:
            driver = webdriver.Chrome(executable_path=chrome, desired_capabilities=caps, options=options,
                                  seleniumwire_options=options_proxy)
    else:
        print('[DRIVER]: PROXY - OFF')
        # undetected
        if undetected:
            # driver = uc.Chrome(options=options)
            pass
        else:
            driver = webdriver.Chrome(executable_path=chrome, desired_capabilities=caps, options=options)


    return driver


