import requests
import json
import pandas as pd

class PoetryInterface:
    def __init__(self):
        self.api_url = "https://poetrydb.org"

    def get_poetry_by_author(self, author):
        response = requests.get(f"{self.api_url}/author/{author}")
        if response.status_code == 200:
            data = response.json()
            if type(data) is dict and 'status' in data and "status" == 404:
                return None
            return data
        else:
            return None
        
    def get_poetry_by_line(self, line):
        response = requests.get(f"{self.api_url}/lines/{line}")
        if response.status_code == 200:
            data = response.json()
            if type(data) is dict and 'status' in data and "status" == "404":
                return None
            return data
        else:
            return None

class WikitionaryInterface:
    def __init__(self):
        self.api_url = "https://en.wiktionary.org/w/api.php"

    def get_word_data(self, word):
        response = requests.get(f"{self.api_url}/w/api.php?action=query&format=json&titles={word}&prop=extracts&explaintext=&exsectionformat=plain")
        if response.status_code == 200:
            data = response.json()
            page = next(iter(data['query']['pages'].values()))
            return page.get('extract', None)
        else:
            return None
        
