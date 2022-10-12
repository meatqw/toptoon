import requests
 
def send_msg(text):
    token = "5745625677:AAH8zJW4RW9R4wtUMsm45HjXZKkaZ2wyZ3c"
    chat_id = "1655138958"
    url_req = "https://api.telegram.org/bot" + token + "/sendMessage" + "?chat_id=" + chat_id + "&text=" + text
    results = requests.get(url_req)
    return results