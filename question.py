import json
import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
from sol import Sol


class Question:

    def __init__(self):
        self.__question = None
        self.__url = None
        self.__script = None
        self.__entries = None
        self.__connection = None
        self.__json_file_loc = None
        self.__req_entries = []

    def search(self, url):
        self.__url = url
        print("Scanning {}".format(self.__url))
        req = requests.get(self.__url)
        soup = BeautifulSoup(req.content, 'html.parser')
        try:
            self.__script = soup.find_all('script', attrs={'type': 'application/ld+json'})[0]
            entries = str(self.__script)
            entries = entries.replace('</script>', '')
            entries = entries.replace('<script type="application/ld+json">', '')
            self.__entries = json.loads(entries.strip())
        except:
            print("Error!!! \nWebsite not found...")

    '''
    def dump_json(self):
        if self.__entries is not None:
            folder_name = 'Questions'
            file_name = self.__question + '.json'
            os.makedirs(folder_name, exist_ok=True)
            self.__json_file_loc = os.path.join(folder_name, file_name)
            self.__connection = open(self.__json_file_loc, 'w')
            json.dump(self.__entries, self.__connection, indent=4, ensure_ascii=True)
    '''

    def extract_info(self):
        if self.__entries is not None:
            self.__question = self.__entries['mainEntity']['name']
            special_chars = ['?', ':', ';', '-']
            for special_char in special_chars:
                self.__question = self.__question.replace(special_char, '')
            entries = self.__entries['mainEntity']['suggestedAnswer']
            for entry in entries:
                s = Sol()
                s.set_question(self.__question)
                s.set_text(entry.get('text', None))
                author_info = entry.get('author', None)
                if author_info is not None:
                    s.set_url(author_info.get('url', None))
                    s.set_description(author_info.get('description', None))
                    s.set_author_name(author_info.get('name', None))
                self.__req_entries.append(s)
        else:
            print("Error!!!")

    def load_excel(self):
        question = []
        author_name = []
        description = []
        text = []
        url = []
        for entry in self.__req_entries:
            question.append(entry.get_question())
            author_name.append(entry.get_author_name())
            description.append(entry.get_description())
            text.append(entry.get_text())
            url.append(entry.get_url())

        new_info = pd.DataFrame({"Question": question,
                                 "Author-Name": author_name,
                                 "Description": description,
                                 "Text": text,
                                 "Url": url})

        if not os.path.isfile('Quora_Info.xlsx'):
            old_info = pd.DataFrame()
            old_info.to_excel('Quora_Info.xlsx')
        with pd.ExcelWriter("Quora_Info.xlsx", if_sheet_exists='replace', mode="a") as writer:
            new_info.to_excel(writer, sheet_name=self.__question, na_rep='?')





