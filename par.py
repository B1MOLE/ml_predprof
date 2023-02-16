import requests
from bs4 import BeautifulSoup

def parse(url):
    rs = requests.get(url)
    root = BeautifulSoup(rs.content, 'html.parser')
    article = root.select("p, span, br, h1, h2, h3, h4, h5, h6")
    text = ""

    for i in article:
        if len(text) > 100000:
            return ""
        text += " " + i.text
    return text