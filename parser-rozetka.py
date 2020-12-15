from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd
import re
import os
import urllib.request
import argparse
# Initiate the parser
parser = argparse.ArgumentParser()

# Add long and short argument
parser.add_argument("-s", "--search", help="SEARCH phraze")
parser.add_argument("-I", "--image",  help="save images to the file /images", action="store_true")
parser.add_argument("-a", "--articule",  help="product articule or id", action="store_true")
parser.add_argument( "-l", "--link", help="product link", action="store_true")
parser.add_argument("-t", "--title", help="product title", action="store_true")
parser.add_argument("-i","--imagelink", help="save image link", action="store_true")
parser.add_argument("-r", "--rating", help="product rating", action="store_true")
parser.add_argument("-R", "--reviews", help="Amount of reviews", action="store_true")
parser.add_argument("-p", "--price", help="price without promo", action="store_true")
parser.add_argument("-o", "--oldprice", help="if promo price exists in o ther case 0", action="store_true")
parser.add_argument("-d", "--description", help="description of the product", action="store_true")
parser.add_argument("-f", "--file", help="read url list from FILE")
parser.add_argument("-w", "--write", help="Write to file name")

args=parser.parse_args()
proxy = "socks4://200.24.80.2:4145"
#parse url's
url_rozetka='https://rozetka.com.ua/search/?text=%s&page=1'

page = 1
rozetka_list = []
link_list = []
cwd = os.getcwd()

#load the page in chrome browser
def run_chrome () : 
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
#    chrome_options.add_argument('--proxy-server={}'.format(proxy))
    browser = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver', options=chrome_options)
    return browser

def browsepage (browser, url):
    browser.get(url)
    time.sleep(10)
    data = browser.page_source
    return data

#parsing rozetka web page for the description and price
def parse_page_rozetka(data) :
    soup = BeautifulSoup(data, "html.parser")
    for div in soup.findAll("div", {"class" : "goods-tile"}):
        if div.find("div", {"class" : "goods-tile__availability goods-tile__availability_type_available"}) :
            list = {}
            if args.title: list["product"] = div.find("span", {"class" : "goods-tile__title"}).get_text(strip=True)
            if args.price: list["price"] = div.find("span" , {"class" : "goods-tile__price-value"}).get_text(strip=True).replace("\xa0", "")
            if args.imagelink: list["imagelink"] = div.find("img", {"class" : "lazy_img_hover display-none"}).get('src')
            if args.articule: list["articule"] = div.find("div", {"class" : "g-id display-none"}).get_text(strip=True)
            if args.link: list["link"] = div.find("a", {"class" : "goods-tile__heading"}).get("href")
            if args.rating: list["rating"] = div.find("div", {"class" : "goods-tile__stars"}).find("svg").get('aria-label')
            if args.reviews: 
                try: list["reviews"] = div.find("span", {"class" : "goods-tile__reviews-link"}).get_text(strip=True)
                except : list ["reviews"]= "0"
            if args.oldprice: 
                try: list["oldprice"] = div.find("div", {"class" : "goods-tile__price goods-tile__price_type_old"}).get_text(strip=True).replace("\xa0", "")[0:-1:]
                except: list["oldprice"] = 0
            if args.description: list["description"] = div.find("div", {"class" : "goods-tile__hidden-content"}).get_text(strip=True)
            if args.image: 
                image = div.find("img", {"class" : "lazy_img_hover display-none"}).get('src')
                image_name = cwd+"/images/"+image.split("/")[-1]
#                print (image)
                if not os.path.exists(cwd+"/images/"):
                    os.makedirs(cwd+"/images/")
                try: urllib.request.urlretrieve(image, image_name)
                except: print ("Download image error")
            rozetka_list.append(list)
    return rozetka_list



#does not work looking for the next page for rozetka parsing
def next_page_rozetka (data) :
    soup = BeautifulSoup(data, "html.parser")
    link_next_page = False
    try: link_next_page = soup.find("a" , {"class" : "button button_color_gray button_size_medium pagination__direction pagination__direction_type_forward"}).get("href")
    except: link_next_page = False
    return link_next_page

#convert list of data and save to file
def write_data (list, file):
    df = pd.DataFrame(list)
#    print (df)
    df.to_csv(file, mode="a", index = False, header = False) #save to file

if __name__ == '__main__':

    if args.write:
        file =  arg.write
    else: file ="rozetka.csv"


    if args.search:
        url_rozetka =url_rozetka % (args.search)
        browser = run_chrome()
        while url_rozetka:
            print ('start parsing page:', url_rozetka)
            data = browsepage(browser, url_rozetka)
            rozetka_list = parse_page_rozetka(data) #parse data 
            write_data (rozetka_list, cwd+"/"+file)
            rozetka_list=[]
            page = page +1
            page_text = "&page=%s"
            if next_page_rozetka(data): url_rozetka = next_page_rozetka(data).replace(page_text % (page-1), page_text % (page))
#                print (url_rozetka)
            else:  url_rozetka = False 
        browser.quit()
    elif args.file:
        url_rozetka =url_rozetka % (args.search)
        browser = run_chrome()
        with open(args.file, 'r', encoding='utf-8') as f:
            link_list = f.read().split('\n')
        for link in link_list:
            url_rozetka = link
            while url_rozetka:
                print ('start parsing page:', url_rozetka)
                data = browsepage(browser, url_rozetka)
                rozetka_list = parse_page_rozetka(data) #parse data 
                write_data (rozetka_list, cwd+"/"+file)
                rozetka_list=[]
                if next_page_rozetka(data): url_rozetka = next_page_rozetka(data) 
                else:  url_rozetka = False 
