import json
import requests


def get_url(url):
    url_str = f"{url}"
    print(url_str)
    response = requests.get(url_str)

    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(f"{url}")
    js = json.loads(content)
    return js
