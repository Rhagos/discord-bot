from lxml import html
import requests
from time import sleep
import json
import argparse
from random import randint
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions


sel = False

def parse_yahoo(ticker):
    """
    Parses Yahoo by retrieving a json output and parsing data out of that.
    """
    url = 'https://query1.finance.yahoo.com/v8/finance/chart/{}?region=US&lang=en-US&includePrePost=false&interval=2m&range=1d&corsDomain=finance.yahoo.com&.tsrc=finance'.format(ticker)
    for tries in range(2):
        try:
            response = requests.put(url, headers={'Content-type':'application/json'}, data='')
            parse = html.fromstring(requests.get('https://finance.yahoo.com/quote/{0}?p={0}'.format(ticker), headers={'Content-type':'application/json'}).text)
            xpath_title="/html/head/title/text()"
            company_name = parse.xpath(xpath_title)[0][:-35]

            output = json.loads(response.text)
            current_price = output['chart']['result'][0]['meta']['regularMarketPrice']
            last_price = output['chart']['result'][0]['meta']['previousClose']

            change = round(current_price - last_price,3)
            change_per = str(round(change/last_price,3)*100) + "%"
            stock_data = {
                'company_name':company_name,
                'price':current_price,
                'change':change,
                'change_percent':change_per
            }
            return stock_data
        except Exception as e:
            print("Error retrieving stocks, {0}".format(e))

def parse_page(ticker):
    """
    Parses NASDAQ by retrieving the http response and then parsing through it with xpath to scrape out the data.
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
    for tries in range(2):
        try:
            url = "https://www.nasdaq.com/symbol/{0}".format(ticker)
            response = requests.get(url, headers = headers)

            print("Parsing {0}".format(url))
            parser = html.fromstring(response.text)

            #DIV TAGS
            # Nasdaq scraping tags
            xpath_head = "//*[@id='qwidget_pageheader']/h1/text()"
            xpath_price = "//*[@id='qwidget_lastsale']/text()"


            xpath_change_up_val = "//*[@id='qwidget_netchange'][@class='qwidget-cents qwidget-Green']/text()"
            xpath_change_up_per = "//*[@id='qwidget_percent'][@class='qwidget-percent qwidget-Green']/text()"
            xpath_change_dn_val = "//*[@id='qwidget_netchange'][@class='qwidget-cents qwidget-Red']/text()"
            xpath_change_dn_per = "//*[@id='qwidget_percent'][@class='qwidget-percent qwidget-Red']/text()"
            raw_name = parser.xpath(xpath_head)
            raw_price = parser.xpath(xpath_price)

            raw_change_val = parser.xpath(xpath_change_up_val) if parser.xpath(xpath_change_up_val) != [] else parser.xpath(xpath_change_dn_val)
            raw_change_per = parser.xpath(xpath_change_up_per) if parser.xpath(xpath_change_up_per) != [] else parser.xpath(xpath_change_dn_per)

            if sel:
                name = raw_name.replace("Common Stock ({0}) Quote & Summary Data".format(ticker),"").strip() if raw_name else ""
                price = raw_price.strip() if raw_price else None
                change_val = raw_change_val.strip() if raw_change_val else None
                change_per = raw_change_per.strip() if raw_change_per else None
            else:
                name = raw_name[0].replace("Common Stock ({0}) Quote & Summary Data".format(ticker),"").strip() if raw_name else ""
                price = raw_price[0].strip() if raw_price else None

                change_val = raw_change_val[0].strip() if raw_change_val else None
                change_per = raw_change_per[0].strip() if raw_change_per else None
            change_val = '-'+change_val if raw_change_val == parser.xpath(xpath_change_dn_val) else change_val
            change_per = '-'+change_per if raw_change_per == parser.xpath(xpath_change_dn_per) else change_per
 #           op_price = raw_open_price.strip() if raw_open_price else None
 #           op_date = raw_open_date.strip() if raw_open_date else None
 #           cl_price = raw_close_price.strip() if raw_close_price else None
 #           cl_date = raw_close_date.strip() if raw_close_date else None

  #          for i in key_stock_table:
  #              key = i.xpath(xpath_key)
  #              value = i.xpath(xpath_value)
  #              key = ''.join(key).strip()
  #              value = ' '.join(''.join(value).split())
  #              stock_dict[key] = value

   #         nasdaq_data = {

   #                 "company_name":name,
   #                 "ticker":ticker,
   #                 "url":url,
   #                 "open_price":op_price,
   #                 "open_date":op_date,
   #                 "close_price":cl_price,
   #                 "close_date":cl_date,
   #                 "key_stock_data":stock_dict
   #             }
            nasdaq_data = {
                    "company_name":name,
                    "price":price,
                    "change":change_val,
                    "change_percent":change_per
                    }
 #           driver.quit()
            return nasdaq_data
        except Exception as e:
            print("Failed: {0}".format(e))

def webdriver_scraper(ticker):
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-extensions')
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')

        driver = webdriver.Chrome(chrome_options=options)
        print("DRIVER ONLINE")
        url = "https://finance.yahoo.com/quote/{0}?p={1}".format(ticker,ticker)
        driver.get(url)
        print(driver.current_url)
        print("Idling...")

        with open('wtfnasdaq{0}.txt'.format(ticker), 'w') as dump:
            dump.write(driver.page_source)


        xpath_head = "//*[@class='D(ib) Fz(18px)'][@data-reactid='7']"
        xpath_price = "//*[@class='Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)'][@data-reactid='35']"
        xpath_change = "//*[contains(@class, 'Trsdu(0.3s) Fw(500) Pstart(10px) Fz(24px)')][@data-reactid='37']"


        raw_name = driver.find_element(By.XPATH,xpath_head).text
        raw_price = driver.find_element(By.XPATH, xpath_price).text
        raw_change = driver.find_element(By.XPATH, xpath_change).text

        print(raw_name)
        print(raw_price)
        print(raw_change)

        name = raw_name.strip() if raw_name else ""
        price = raw_price.strip() if raw_price else None
        change_val = raw_change_val.strip() if raw_change_val else None
        change_per = raw_change_per.strip() if raw_change_per else None

        nasdaq_data = {
                "company_name":name,
                "price":price,
                "change":change_val,
                "change_percent":change_per
            }
        driver.quit()
        return nasdaq_data
    except Exception as e:
        print("Failed {0}".format(e))

def main():
    symbol = sys.argv[1]
    print(parse_yahoo(symbol))
    #print(parse_page(symbol))
    #print(webdriver_scraper(symbol))


if __name__ == "__main__":
    main()


