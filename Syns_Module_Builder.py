import os
import requests
from bs4 import BeautifulSoup
import json
import re


class Syns_Module_Builder:
    URL_BASE = 'https://www.thesaurus.com/browse/'

    def __init__(self, base_dir, syn_mod_name, word_list=[]):
        self.base_dir = base_dir
        self.syn_mod_name = syn_mod_name
        self.__build_file_name__()
        self.word_list = word_list
        self.syns_dict = {}

        self.__obtain_syns__()

    def __build_file_name__(self):
        if self.base_dir[-1] != '/':
            self.base_dir += '/'
        self.syn_mod_file_name = f'{self.base_dir}{self.syn_mod_name}.syn'

    def __obtain_syns__(self):
        module_exists = os.path.exists(self.syn_mod_file_name)

        if module_exists:
            with open(self.syn_mod_file_name, 'r', encoding='utf-8') as f:
                self.syns_dict = json.load(f)
            print('USING EXISTING MODULE')
            return self.syns_dict
        else:
            print('CREATING NEW MODULE')
            self.__capture_syns__()
            with open(self.syn_mod_file_name, 'w', encoding='utf-8') as f:
                json.dump(self.syns_dict, f, ensure_ascii=False, indent=4)
            print('NEW MODULE CREATION COMPLETE')
            return self.syns_dict

    def __capture_syns__(self):
        for word in self.word_list:
            URL = f'{Syns_Module_Builder.URL_BASE}{word}'
            page = requests.get(URL)
            if page.status_code != 200:
                continue
            else:
                soup = BeautifulSoup(page.content, 'html.parser')
                the_script = soup.find(
                    'script',
                    text=re.compile("window.INITIAL_STATE"))
                the_script = the_script.text
                the_script = the_script.replace("window.INITIAL_STATE = ", "")
                the_script = the_script.replace(':undefined', ':"undefined"')
                the_script = the_script.replace(';', '')
                data = json.loads(the_script, encoding='utf-8')

                self.syns_dict[word] = {}
                for a_tab in data["searchData"]["tunaApiData"]["posTabs"]:
                    for syns in a_tab["synonyms"]:
                        sim = float(syns["similarity"])
                        syn = syns["term"]
                        self.syns_dict[word][syn] = sim
