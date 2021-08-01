import requests
from requests.auth import HTTPBasicAuth
import pandas as pd
import os

pd.set_option("display.max_rows", None, "display.max_columns", None)


# api-endpoint
URL = "https://zccgainthehouse.zendesk.com/api/v2/tickets.json"

# sending get request and saving the response as response object
r = requests.get(url = URL,auth = HTTPBasicAuth('gagarwal8@wisc.edu', '9967323080'))

# extracting data in json format
data = r.json()
df=pd.DataFrame(data["tickets"])


# Restrucutre DataFrame
df=df.drop(['url','via',"raw_subject"], axis=1)
df=df.set_index('id')
df=df.dropna(axis='columns')
columns=list(df.columns)
for i in columns:
    
    typ=type(df.loc[1,i])
    value0=df.loc[1,i]
    value1=df.loc[2,i]
    if typ==type("hi"):
        values=["None",None,"","NaN"]
        if value0 in values or value1 in values:
            df=df.drop(i, axis=1)
    if typ==type(list([])):
        if len(value0)==0 or len(value1)==0:
            df=df.drop(i, axis=1)
    if typ==type(None): 
        df=df.drop(i, axis=1)


        

choice=0
id=0        
        
# infinite while loop
while True:
    print("Hello! user choose your tool")
    print("-> Press 1 to view all tickets")
    print("-> Press 2 to view a particular ticket")
    print("-> Press 3 to exit",end=' ')
    

    p = input()

    if (p=="1"):

        print("OK user\n")
        choice=1
    elif (p=="2"):
        print("OK user\n")
        print("Please enter ticket id")
        choice=2
        id=int(input())
    elif (("quit" in p) or ("exit" in p) or ("stop" in p) or ("close" in p) or ("deactivate" in p) or ("terminate" in p) or (p=="3")):
        print("Thank You!")
        break
    else :
        print("don't support")
    if choice == 1:
        print(df)
        choice=0
    if choice == 2:
        data=df.loc[df["id"]==id]
        print(data)
        choice=0
        id=0
