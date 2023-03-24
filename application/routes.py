from flask import jsonify, request, make_response, current_app as app, Response
from loguru import logger
from .models import tor_ip_model
from .db import get_db_session
import traceback, datetime
import requests
from bs4 import BeautifulSoup
import pandas as pd


def check_ip():
    with open('tor-ips.txt') as f:
        lines = f.readlines()
    return [items.strip() for items in lines]


@app.route("/", methods=["GET"])
def hello():
    return "hello!"

@app.route("/udger", methods=["GET", "POST"])
def udger():
    """
    GET: gather tor IP addresses from udger.com and filter out the IP addresses that overlap with those in DB
    POST: add IP address records to DB
    """
    s = get_db_session()
    if request.method == "POST":
        try:
            body = request.get_json()
            new_ip = body['ip']
            new = tor_ip_model(new_ip)
        except:
            err = 'malformed POST request form   \n'
            logger.error(err + traceback.format_exc())
            return Response(err, status=400)
        try:
            s.add(new)
            s.commit()
            return make_response(f'successfully inserted {new}\n')
        except:
            err = f'failed to insert {new}'
            logger.error(err)
            return Response(err, status=400)
        
    if request.method == "GET":
        try: 
            URL = "https://udger.com/resources/ip-list/tor_exit_node"
            page = requests.get(URL, verify=False)
        except:
            err = f'failed to get website to scrape: {URL}'
            logger.error(err)
            return Response(err, status=500)
        
        try:
            soup = BeautifulSoup(page.text, 'lxml')
            table1 = soup.find("table", id="iptab")
            headers = []
            for i in table1.find_all("th"):
                title = i.text
                headers.append(title.strip())
            headers.append('')
            scrapedData = pd.DataFrame(columns=headers)
        
            # Create a for loop to fill scrapedData
            for counter, j in enumerate(table1.find_all('tr')[1:]):
                row_data = j.find_all('td')
                row = [i.text for i in row_data]
                # Create a for loop to fill scrapedData
                scrapedData.loc[counter] = row
            # Drop and clearing unnecessary columns
            scrapedData = scrapedData.drop(columns=['Last seen', 'IP name', 'DC', 'Country', ''])
            q = s.query(tor_ip_model)
            ips = q.all()
            scrapedIPs = [str(x.strip()) for x in scrapedData['IP address']]
            storedIPs = [str(x.ip.strip()) for x in ips]
            result = []
            for items in scrapedIPs:
                if items not in storedIPs: # only return IPs not stored in DB
                    result.append(items)
        except:
            err = f'failed to parse website HTML into dataframe'
            logger.error(err)
            return Response(err, status=500)

    return make_response(f'{result}\n')


@app.route("/dan", methods=["GET", "POST"])
def dan():
    s = get_db_session()
    
    if request.method == "POST":
        try:
            body = request.get_json()
            new_ip = body['ip']
            new = tor_ip_model(new_ip)
        except:
            err = 'malformed POST request form   \n'
            logger.error(err + traceback.format_exc())
            return Response(err, status=400)
        try:
            s.add(new)
            s.commit()
            return make_response(f'successfully inserted {new}\n')
        except:
            err = f'failed to insert {new}'
            logger.error(err)
            return Response(err, status=400)
        
    if request.method == "GET":
        URL = "https://www.dan.me.uk/torlist/"
        page = requests.get(URL, verify=False)
        listOfIps = page.text.split("\n")
        listOfIps.pop(len(listOfIps) - 1)
        scrapedData = pd.DataFrame(columns=['ip'])
        # Create a for loop to fill mydata
        for counter, j in enumerate(listOfIps):
            # Create a for loop to fill mydata
            scrapedData.loc[counter] = [j]
        q = s.query(tor_ip_model)
        ips = q.all()
        new_str0 = [str(x.strip()) for x in scrapedData['ip']]
        new_str1 = [str(x.ip.strip()) for x in ips]
        result = []
        for items in new_str0:
            if items not in new_str1:
                result.append(items)
    return make_response(f'{result}\n')
