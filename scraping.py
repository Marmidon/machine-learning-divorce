import requests
import json
import time
import pickle

def get_list_of_subcategories(master_category):
    result=[];
    r = requests.get("https://en.wikipedia.org/w/api.php?action=query&list=categorymembers&cmtype=subcat&cmtitle=Category:" + master_category + "&cmlimit=500&format=json")
    data = r.json()
    if "categorymembers" in data["query"]:
        result = data["query"]["categorymembers"]
        for subcat in result:
            subcat_name = subcat['title'][9:]
            print(subcat_name)
            subcat_results = get_list_of_subcategories(subcat_name)
            #if (subcat_results.__len__()>0)
            result += subcat_results
    return result;

def get_categories_page_titles(categories):
    result=[];
    for cat in categories:
        result = result + get_catergory_page_titles(cat)
    return result


def get_catergory_page_titles(category, cmcontinue=""):
    result=[];
    if cmcontinue.__len__()>0:
        cmcontinue = "&cmcontinue=" + cmcontinue
    r = requests.get("https://en.wikipedia.org/w/api.php?action=query&list=categorymembers&cmtitle=Category:" + category + "&cmlimit=500&format=json"+cmcontinue)
    data = r.json()
    if "categorymembers" in data["query"]:
        result = data["query"]["categorymembers"]
    if "continue" in data and "cmcontinue" in data["continue"]:
        result = result + get_catergory_page_titles(category, data["continue"]["cmcontinue"])
    return result;

def get_page_contents(pageTitle):
    #/w//api.php?action=query&prop=revisions&rvlimit=1&rvprop=content&titles=
    get_pages_query = "https://en.wikipedia.org/wiki/" + pageTitle
    r = requests.get(get_pages_query)
    return r.text

def put_category_to_file(caterogy_name):
    pages_info = get_catergory_page_titles(caterogy_name)
    pages = []
    i = 0
    for page in pages_info:
        i += 1
        pages.append(get_page_contents(page["title"]))
        if i>300:
            time.sleep(10)
            i = 0
    f = open(caterogy_name+".pkl", "wb")
    pickle.dump(pages, f, pickle.HIGHEST_PROTOCOL)


#subcats = get_list_of_subcategories('Singers_by_century')
#print(subcats)
categories=["21st-century American singers"]
#result1 = get_categories_page_titles(catergories)

put_category_to_file(categories[0])

#import wikipedia
#print(wikipedia.WikipediaPage(title=result1[0]["title"]).sections)
#



#firstPage = get_page_contents(result1[1]["title"])
#print(firstPage)