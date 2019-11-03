from flask import Flask, render_template,jsonify
import read_data
import pandas as pd
import os
import json
import models
import pandas as pd
import helper
import wiki

steps=10
present_dir=os.path.dirname(os.path.abspath(__file__))
path="\data\data_ub.csv"
dname=""

data = pd.read_csv(present_dir+path, error_bad_lines=False,header=0, parse_dates=[1], index_col=0, squeeze=True)
data["Adj Close"] = data["Adj Close"].astype(float)
data=data.loc[:,"Adj Close"]
data=data[:1000]
data=pd.Series(data)

app = Flask(__name__)

@app.route("/amazon",methods=["get"])
def amazon():
    
       path="\data\AMZN.csv"
       global dname
       dname="Amazon"
       return "Success"
   
@app.route("/apple",methods=["get"])
def apple():
    try:
       path="\data\AAPL.csv"
       global dname
       dname="Apple"
       return "Success"
    except:
        return  json.dumps({}) 

@app.route("/ubhack",methods=["get"])
def ub():
    try:
       path="\data\data_ub.csv"
       global dname
       dname="UB"
       return "Success"
    except:
        return  json.dumps({})    

@app.route("/slstm",methods=["post"])
def baseline():   
    try: 
        obj=models.Models()
        x=obj.uni_baseline(data,steps)
        x["company"]=dname
        print(x)
        return x
    except:        
        return json.dumps({}) 

@app.route("/sarima",methods=["post"])
def sarima():
    try:
        obj=models.Models()
        x=json.dumps(obj.uni_sarima(data,steps))
        x["company"]=dname
        print(x)          
        return x              
    except:
        return json.dumps({}) 

@app.route("/baseline",methods=["post"])
def lstm():
    try:
        x=(helper.lstm(data,steps))
        x["company"]=dname
        print(x)    
        return x    
    except:
        return json.dumps({}) 

@app.route("/wiki",methods=["post"])
def wiki_():
    try:
        wiki_ = wiki.Wiki()        
        wiki_results = wiki_.get_wiki(dname)
        p=wiki_results["query"]["pages"]
        q=list(p.keys())
        print(q)
        return json.dumps({"desc":p[q[0]]["extract"]})
    except:
        return json.dumps({"desc":"Wiki not found about"+dname})
@app.route("/news",methods=["post"])
def news_():
    try:
        news = wiki.News()
        news_results = news.get_news(dname+"news")  
        print(news_results)   
        #return {}  
        return json.dumps({"desc":news_results["articles"][0]["title"]})   
    except:
        return json.dumps({"desc":"News not found about"+dname})

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')

if __name__ == "__main__":
    app.run(debug=True,threaded=False)
