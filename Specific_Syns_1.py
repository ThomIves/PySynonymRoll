import requests
from bs4 import BeautifulSoup
import sys

URL_Front = "https://www.thesaurus.com/browse/"
word = "barrier"

URL = f'{URL_Front}{word}'

page = requests.get(URL)
if page.status_code == 200:
    soup = BeautifulSoup(page.content, 'html.parser')

# print(soup.prettify())
html_file_text = soup.prettify()

with open('barrier_thesaurus_dot_com.html', 'w', encoding='utf-8') as f:
    f.write(html_file_text)
