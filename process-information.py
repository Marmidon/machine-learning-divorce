import pickle
from bs4 import BeautifulSoup
import numpy as np
import pprint
import re
import gc
import sys

spouse_possible_names = ['Spouse(s)', 'Spouse', 'Spouses']
divorce_possible_names = ['div.','div','divorced','divorced.']
global dashes
dashes = 0
global empty_pages
empty_pages = 0

class Singer:
    def __init__(self):
        self.page_title = ""
        self.genres = []
        self.birth_year = 0
        self.marriages = []


class Marriage:
    def __init__(self):
        self.married_year = None
        self.divorced = False
        self.divorced_year = None
        self.married_famous_person = False



def process_file(category_name):
    global empty_pages
    raw_data = pickle.load( open( category_name + ".pkl", "rb" ))
    singers = []
    for page in raw_data:
        singer_information = Singer()
        soup = BeautifulSoup(page, 'lxml')
        if soup.title is None:
            empty_pages += 1
            continue
        singer_information.page_title = str(soup.title)
        print(soup.title.string)
        for biography in soup.find_all(name='table',class_='infobox'):
            for row in biography.find_all(name='tr'):
                process_biography_row(row, singer_information)
        #print(singer_information.genres)
        #print(singer_information.page_title)
        singers.append(singer_information)
        #print(gc.collect())
    return singers

def process_biography_row(row, singer_information):
    for row_name in row.find_all(name='th'):
        if (row_name.text == 'Genres'):
            singer_information.genres = []
            content = row.findChildren('td')[0]
            genres = content.find_all('a')
            for genre in genres:
                singer_information.genres.append(genre.text.lower())
                #print(genre.text.lower())
            return
        if (row_name.text in spouse_possible_names):
            singer_information.marriages = []
            content = row.findChildren('td')[0]

            # each marriage info is inside div
            for div in content.findChildren('div'):
                # sometimes marriages are inside another div
                sub_divs = div.findChildren('div')
                if sub_divs.__len__()>0:
                    for marriage_div in sub_divs:
                        singer_information.marriages.append(get_marriage_from_div(marriage_div))
                else:
                    singer_information.marriages.append(get_marriage_from_div(div))

        #print("singer")
        #print(sys.getsizeof((singer_information)))
        return

def get_marriage_from_div(marriage):
    global dashes
    print(marriage.text)
    marriage_info = Marriage()
    # if a marriage contains a link to spouse, we consider spouse to be famous
    if marriage.findChildren('a').__len__() > 0:
        marriage_info.married_famous_person = True
    # part always starts with "("
    part_with_dates = marriage.text.split("(")[1]
    print(part_with_dates)
    married = ""
    ended = ""
    # find married year and if exists, ended year, by picking numbers
    for letter in list(part_with_dates):
        if letter.isdigit():
            if len(married) == 4:
                if len(ended) == 4:
                    raise ValueError('Too many numbers in marriage text')
                ended += letter
            else:
                married += letter
        if letter == '-':
            dashes += 1
    print(married)
    print(ended)
    if len(ended)==4:
        marriage_info.ended = int(ended)
    if len(married) == 4:
        marriage_info.married_year = int(married)
    #else:
        #raise ValueError('no married date')


    #either not divorced or typed like 1946-1968
    #if len(part_wirh_dates) == 1:
    #    print("only 1 split")
    #if len(part_wirh_dates) == 2:

    ##print(part_wirh_dates)
    ##split = re.split(';|–',part_wirh_dates)
    ##print("split")
    ##print(split)
    ##ended = []
    ##if (len(split) == 1):
    ##    married = split[0]
    ##if (len(split) >1):
    ##    married = split[0]
    ##    ended = split[1]
    ##married = married.replace(')',' ')
    ##print(married.split())
    ##marriage_info.married_year = [int(s) for s in married.split() if s.isdigit()][0]
    ##if ended.__len__() > 3:
    ##    print("divorced "+ended)
    ##    endedList = [int(s) for s in ended[:ended.__len__() - 1].split() if s.isdigit()]
    ##    print(endedList)
   ## ##    ended = endedList[0]

    # find divorce info
    for abbriviation in marriage.findChildren("abbr"):
        if (abbriviation.text in divorce_possible_names):
            marriage_info.divorced = True
            marriage_info.divorced_year = ended
    #if (marriage.text.contains("divorced")):
    #    marriage_info.divorced = True
    #    #print("contains divorced")
    #print("marr")
    #print(sys.getsizeof((marriage_info)))
    return marriage_info

categories=["21st-century American singers"]
singers = process_file(categories[0])
married = 0
divorced = 0
genres = []
for singer in singers:
    genres = genres+singer.genres
    for marriage in singer.marriages:
        married += 1
        if marriage.divorced:
            divorced += 1
print(married)
print(divorced)
print(genres)
