import requests
from bs4 import BeautifulSoup
import json
import re

word = "barrier"

URL = f'https://www.thesaurus.com/browse/{word}'

page = requests.get(URL)
if page.status_code == 200:
    soup = BeautifulSoup(page.content, 'html.parser')

the_script = soup.find('script', text=re.compile("window.INITIAL_STATE"))
the_script = the_script.text
the_script = the_script.replace("window.INITIAL_STATE = ", "")
the_script = the_script.replace(':undefined', ':"undefined"')
the_script = the_script.replace(';', '')
data = json.loads(the_script, encoding='utf-8')

# with open('test1.json', 'w', encoding='utf-8') as f:
#     json.dump(data, f, ensure_ascii=False, indent=4)

synonyms = {}
synonyms[word] = {}
for each_tab in data["searchData"]["tunaApiData"]["posTabs"]:
    for syn in each_tab["synonyms"]:
        sim = float(syn["similarity"])
        if sim not in synonyms[word].keys():
            synonyms[word][sim] = []
        synonyms[word][sim].append(syn["term"])

print(synonyms)
