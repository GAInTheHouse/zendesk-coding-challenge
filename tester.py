import pytest
import pandas as pd
from flask import Flask, request, jsonify, Response
import re
import matplotlib
from matplotlib import pyplot as plt
from io import StringIO
import requests
from requests.auth import HTTPBasicAuth
import os
from bs4 import BeautifulSoup
import main


##TODO: Test All Functions Individuals
##TODO: Test the integrations - If a next button is clicked, does it work?
##TODO:                       - If an id is entered in the form does it update the code
##TODO:                       - Befroe any id is entered what does the webpage do?
##TODO:                       - After any id is entered what does the webpage do?    

#Checks if the home function correctly reads html file
def test_home(name):
    #authentication()
    print(name)
    main.username=name[0]
    main.password=name[1]
    with open("index.html") as f:
        html = f.read()
    htmlObj=main.home()
    assert(main.page==0)
    assert(htmlObj==html)

#Checks the length of the df returned by the helper function
def test_get_all_data():
    # api-endpoint
    URL = "https://zccgainthehouse.zendesk.com/api/v2/tickets.json"
    # sending get request and saving the response as response object
    r = requests.get(url = URL,auth = HTTPBasicAuth(main.username, main.password))
    # extracting data in json format
    data = r.json()
    df=pd.DataFrame(data["tickets"])
    assert len(main.get_all_data())==len(df)

#Test if there's 1 table with 25 rows
def test_all_tickets_01():
    output=main.all_tickets()
    assert(main.page==1)
    #print(output)
    assert(output.count("/table")==1)
    assert(output.count("/tr")==27) ## 25 rows of data and 2 rows for column name
    
#Test if there's 1 table with 25 rows and if 2 calls give the same html code
def test_all_tickets_02():
    output=main.all_tickets()
    soup = BeautifulSoup(output,features="html.parser")
    table = soup.find("table")

    # The first 2 tr contains the field names.
    headings = [th.get_text() for th in table.find("tr").find_all("th")]
    headings.insert(0,"id")

    datasets = []
    for row in table.find_all("tr")[2:]:
        dataset = zip(headings, (td.get_text() for td in row.find_all("td")))
        datasets.append(dataset)

    assert(len(datasets)==25)
    
    output2=main.all_tickets()
    assert(output2!=output)
    assert(main.page==3)
    
def test_get_one_ticket():
    
    main.id=1
    output=main.get_one_ticket()
    assert(output.count("/ul")>=1)
    assert(output.count("/li")<30)
    
def test_browser():
    
    output=main.browse()
    assert(output.count("/ul")>=1)
    assert(output.count("/li")<30)
    
    main.id=0
    output=main.browse()
    assert("Please enter an id in the previous page!" in output)
    

