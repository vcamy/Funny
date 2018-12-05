import requests
import bs4
import re
import csv
import json
import datetime


def main(source_file):
    json_data = readJson(source_file)
    if json_data is not None:
        for value in json_data.values():
            for item in value:
                print(item)
                dataScraper(item)

def dataScraper(data):
    url_list = getUrls(data)
    keywords = getKeys(data)
    target_file = getFileName(data)
    for url in url_list:
        r = requests.get(url)
        if r.status_code == 200:
            result = ParseHtml(r.content, keywords)
            writeData(target_file, result)
        else:
            print("fail to open website %s." % url)

def readJson(filePath):
##    try:
    with open(filePath, 'r',) as f:
            data = json.load(f)
##    except:
##        data = None
##        print("Fail to read %s" % filePath)
    return data

def getUrls(data):
    url_list = data.get("urls")
    print(url_list)
    return url_list

def getFileName(data):
    path = data.get("filename")
    print(path)
    return path

def getKeys(data):
    keywords = data.get("keys")
    print(keywords)
    return keywords

def ParseHtml(content, keywords):
    soup = bs4.BeautifulSoup(content,"html.parser")
    record=datetime.date.today().strftime("%x")
    for head,value in keywords.items():
        print(head, value)
        for k, v in value.items():
            num = getLimitedNum(v)
            for item in soup.find_all(head,{k:re.compile(v)}, limit=num):
                print(item.text)
                record += "," + str(item.text).strip() 
                print(record)
    return record  


def writeData(file_name, data):
    with open(file_name, "a+") as f:
        f.write(data +'\n')
        f.close()
    return

def getLimitedNum(value):
    return len(value.split("|"))

main("C:\\Users\\Amy\\Desktop\\keys.json")

