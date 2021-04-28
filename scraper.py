import requests
from bs4 import BeautifulSoup
import pandas
import argparse
import sqlite3

def connect(dbname):
    conn = sqlite3.connect(dbname)
    conn.execute("CREATE TABLE IF NOT EXISTS FLIPKART_PHONES (NAME TEXT, PRICE INT, DISCOUNT TEXT, RATING TEXT)")
    print("Table created sucessdully!")
    conn.close()
def insert_into_table(db_name, values):
    conn = sqlite3.connect(dbname)
    conn.execute("INSERT INTO FLIPKART_PHONES VALUES (?, ?, ?, ?)",(tuple(values)))
    conn.commit()
    conn.close()
def get_hotel_info(dbname):
    conn = sqlite3.connect(dbname)
    cur=conn.cursor()
    cur.execute("SELECT * FROM FLIPKART_PHONES")
    table_data=cur.fetchall()
    for record in table_data:
        print(record)
    conn.close()
parser=argparse.ArgumentParser()
parser.add_argument("--page_num_max", help="Enter the number of pages to parse", type=int)
dbname="flipkart"
args=parser.parse_args()
flipkart_url="https://www.flipkart.com/mobiles/pr?sid=tyy%2C4io&p%5B%5D=facets.brand%255B%255D%3DRealme&otracker=nmenu_sub_Electronics_0_Realme&page="
page_num_MAX = args.page_num_max
scraped_info_list=[]
connect(dbname)
for page_num in range(1, page_num_MAX):
    req =requests.get(flipkart_url + str(page_num))
    content=req.content
    soup=BeautifulSoup(content, "html.parser")
    all_phones=soup.find_all("div", {"class": "_3pLy-c row"})
    for phone in all_phones:
        phone_dict={}
        phone_dict["name"]=phone.find("div", {"class": "_4rR01T"}).text
        phone_dict["price"]=phone.find("div", {"itemprop": "_30jeq3 _1_WHN1"})
        phone_dict["discount"]=phone.find("div", {"class": "_3Ay6Sb"}).text
        try:
            phone_dict["rating"]=phone.find("div", {"class": "_3LWZlK"}).text
        except AttributeError:
            pass
        scraped_info_list.append(phone_dict)
        insert_into_table(dbname, phone_dict.values())
dataframe = pandas.DataFrame(scraped_info_list)
dataframe.to_csv("flipkart.csv")
get_hotel_info(dbname)
print(scraped_info_list)