import requests

def get_raw_html(url):
    req = requests.get(url)
    if req.status_code == requests.codes.ok:
        return req.text 
    return None