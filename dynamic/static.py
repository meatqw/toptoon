import requests
from bs4 import BeautifulSoup

headers = {"accept": "*/*",
           "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36"}


# save img
def save(url, url_img, img_id, path):
    headers['referer'] = url
    req = requests.get(url_img, stream=True, headers=headers)
    with open(f"{path}/{img_id}.jpg", 'wb') as fd:
        for chunk in req.iter_content(4028):
            fd.write(chunk)
        fd.close()


def clearing_text(text):
    result = text.replace('&quot;', '', ).replace('\r', '').replace('\n', '').replace('\t', '').replace('&nbsp;', '')\
        .replace("\'", "").replace('\xa0', '').replace('\u200b', '').strip()
    return result


def get_content(url):

    # proxies = {
    #     "http": f"http://{proxy}",
    #     "https": f"https://{proxy}",
    # }

    try:
        request = requests.get(url, headers=headers)
        # redirect check
        if request.status_code == 200:
            content = BeautifulSoup(request.content, 'html.parser')
            return content
        else:
            print(request.status_code)
            return None

    except Exception as e:
        print(e)
        return None
