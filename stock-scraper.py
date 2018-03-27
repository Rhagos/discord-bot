from lxml import html
import requests
from time import sleep
import json
import argparse
from random import randint
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By

def parse_page(ticker):
    """
    Args:
        ticker (str): stock symbol
    Returns:
        dict of the data
    """
    stock_dict = {}

    headers = {
         "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding":"gzip, deflate",
        "Accept-Language":"en-GB,en;q=0.9,en-US;q=0.8,ml;q=0.7",
        "Connection":"keep-alive",
        "Host":"www.nasdaq.com",
        "Referer":"http://www.nasdaq.com",
        "Upgrade-Insecure-Requests":"1",
        "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36"
    }
    for tries in range(5):
        try:
            
            url = "https://www.nasdaq.com/symbol/{0}".format(ticker)
            """
            response = requests.get(url, headers = headers)

 #           if response.status_code != 200:
  #              raise ValueError("Invalid response from Webserver")

            print("Parsing {0}".format(url))
            with open('wtfnasdaq{0}.txt'.format(ticker), 'w') as dump:
                dump.write(response.content.decode('utf-8'))
            parser = html.fromstring(response.text)
"""
            options = webdriver.ChromeOptions()
            options.add_argument('--disable-extensions')
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')
            options.add_argument('--no-sandbox')

            driver = webdriver.Chrome(chrome_options=options)
            print("DRIVER ONLINE")
            driver.get(url)
            print("URL GOTTEN")



            #DIV TAGS
            xpath_head = "//div[@id='qwidget_pageheader']//hl//text()"
 #           xpath_key_stock_table = '//div[@class="row overview-results relativeP"]//div[contains(@class,"table-table"")]/div'
            xpath_open_price = '//b[contains(text(),"Open Price:")]/following-sibling::span/text()'
            xpath_open_date = '//b[contains(text(),"Open Date:")]/following-sibling::span/text()'
            xpath_close_price = '//b[contains(text(),"Close Price:")]/following-sibling::span/text()'
            xpath_close_date = '//b[contains(text(),"Close Date:")]/following-sibling::span/text()'
            xpath_key = './/div[@class="table-cell"]/b/text()'
            xpath_value = './/div[@class="table-cell"]/text()'

 #           raw_name = parser.xpath(xpath_head)
 #           key_stock_table = parser.xpath(xpath_key_stock_table)
 #           raw_open_price = parser.xpath(xpath_open_price)
 #           print(raw_open_price)
 #           raw_open_date = parser.xpath(xpath_open_date)
 #           raw_close_price = parser.xpath(xpath_close_price)
 #           raw_close_date = parser.xpath(xpath_close_date)
            raw_name = driver.find_element(By.XPath, xpath_head)
            raw_open_price = driver.find_element(By.XPath, xpath_open_price)
            raw_open_date = driver.find_element(By.XPath, xpath_open_date)
            raw_close_price = driver.find_element(By.XPath, xpath_close_price)
            raw_close_date = driver.find_element(By.XPath, xpath_close_date)

            name = raw_name[0].replace("Common Stock Quote & Summary Data","").strip() if raw_name else ""
            op_price = raw_open_price[0].strip() if raw_open_price else None
            op_date = raw_open_date[0].strip() if raw_open_date else None
            cl_price = raw_close_price[0].strip() if raw_close_price else None
            cl_date = raw_close_date[0].strip() if raw_close_date else None

  #          for i in key_stock_table:
  #              key = i.xpath(xpath_key)
  #              value = i.xpath(xpath_value)
  #              key = ''.join(key).strip()
  #              value = ' '.join(''.join(value).split())
  #              stock_dict[key] = value

            nasdaq_data = {

                    "company_name":name,
                    "ticker":ticker,
                    "url":url,
                    "open_price":op_price,
                    "open_date":op_date,
                    "close_price":cl_price,
                    "close_date":cl_date,
   #                 "key_stock_data":stock_dict
                }
            driver.quit()
            return nasdaq_data
        except Exception as e:
            print("Failed: {0}".format(e))


def main():
    symbol = sys.argv[1]
    print(parse_page(symbol))


if __name__ == "__main__":
    main()


