import pandas as pd
from flask import Flask, request, jsonify, Response
import re
import matplotlib
from matplotlib import pyplot as plt
from io import StringIO
import requests
from requests.auth import HTTPBasicAuth
import os
import sys

matplotlib.use('Agg')

app = Flask(__name__)
id = 0
page=0
username=""
password=""
def highlight(s):
    if s.status == 'open':
        return ['background-color: cyan']*len(s)
    elif s.status == 'solved':
        return ['background-color: light-green']*len(s)
    else:
        return ['background-color: yellow']*len(s)

@app.route('/')
def home():
    global page
    page=0
    
    with open("index.html") as f:
        html = f.read()
    return html

@app.route('/all.html')
def all_tickets():
    
    with open("all.html") as f:
        html = str(f.read())
    
    global page
    print(page)
    df=get_all_data()
    if type(df)==str:
        return html.replace("{}",df) 
    limit=int(len(df.index)/25)
    print(limit)
    if(len(df.index)%25!=0):
        limit+=1
    print(limit)    
    
        
    if page == limit:
        df=df.loc[(page-1)*25+1:,:]
        html=html.replace("next","page 1")
        page=0
    else:
        page+=1
        df=df.loc[(page-1)*25+1:page*25,:]
    
    df=df.style.apply(highlight, axis=1)
    
    with pd.option_context("display.max_rows", None, "display.max_columns", None):
        return html.replace("{}",df._repr_html_())
    
@app.route('/browse.html')
def browse():
    global page
    page=0
    html = """
    <html><body>
    <h1>Browse</h1>
    {}
    </body></html>
    """
    print(type(html))
    if id==0:
        return html.format("Please enter an id in the previous page!")
    htmlObj=get_one_ticket()
    return html.format(htmlObj)

    
@app.route('/id', methods=["POST"])
def get_id():
    global id
    global page
    if page !=0:
        page-=1
    
    inp = str(request.data, "utf-8")
    if re.match(r"\d+", inp): # 1
        id=int(inp)
        return jsonify("Thanks, the #id is {}!".format(id))
    return jsonify("bad, bad, bad!") # 3

def printitems(dictObj, indent=0):
    p=[]
    p.append('<ul>\n')
    for k in dictObj:
        v=dictObj[k]
        if isinstance(v, dict):
            p.append('<li>'+ k+ ':')
            p.append(printitems(v))
            p.append('</li>')
        else:
            typ=type(v)
            values=["None",None,"","NaN",[]]
            if v in values:
                continue
            p.append('<li>'+ k+ ':'+ str(v)+ '</li>')
    p.append('</ul>\n')
    return '\n'.join(p)

def get_one_ticket():
    
    URL = "https://zccgainthehouse.zendesk.com/api/v2/tickets/"+str(id)
    # sending get request and saving the response as response object
    r = requests.get(url = URL,auth = HTTPBasicAuth(username, password))

    # extracting data in json format
    data = r.json()
    data=data["ticket"]
    data.pop('raw_subject')
    htmlObj=printitems(data)
    return htmlObj


##TODO: Make the error better
def get_all_data():
    # api-endpoint
    try:
        URL = "https://zccgainthehouse.zendesk.com/api/v2/tickets.json"
        # sending get request and saving the response as response object
        r = requests.get(url = URL,auth = HTTPBasicAuth(username, password))
    except:
        return "API Authentication Error/API unavailable"

    # extracting data in json format
    data = r.json()
    df=pd.DataFrame(data["tickets"])

    df=df.set_index('id')
    df=df.dropna(axis='columns')
    df=df[["subject","status"]]    
    return df

def main():
    global username
    global password
    try:
        username=str(sys.argv[1])
        password=str(sys.argv[2])
    except:
        print("Failed to detect username or password.\n")
        print("Correct usage: python3 main.py USERNAME PASSWORD")
        sys.exit(0)


## Make the error more specific
if __name__ == '__main__':
    
    main()
    app.run(host="0.0.0.0", debug=True) # don't change this line!
            
    
    
