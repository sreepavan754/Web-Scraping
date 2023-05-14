import pandas as pd
from flask import Flask,render_template,session,request,redirect
import json
import math

with open('main.json','r') as c:
    params = json.load(c)['params']



app = Flask(__name__)
app.secret_key = params['secret_key']

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        print(username,password)
        if username == params['username'] and password == params['password']:
            session['u_name'] = params['username']
            return redirect("/")

        else:
            return redirect("/login")

    else:
        return render_template("login.html")
@app.route("/")
def home():
    # print(data)
    if "u_name" in session:
        scrapped_data = pd.read_csv('Scraped data2.csv')
        data = []
        Model = list(scrapped_data['Name'])
        Price = list(scrapped_data['Price'])
        rating = list(scrapped_data['Reviews'])
        url = list(scrapped_data['Image'])
        for i in range(len(Model)):
            k = (Model[i],Price[i],rating[i],url[i])
            data.append(k)
        return render_template('index.html',data=data,account=params['username'])
    else:
        return redirect('/login')

@app.route("/compare/<pageno>")
def compare(pageno):
    if "u_name" in session:
        amazon_data = pd.read_csv('Scraped data2.csv')
        flipkart = pd.read_csv('Scraped data.csv')
        flipkartdata =  []
        amazondata = []
        numofproducts = 10

        model = list(flipkart['Item'])
        Price = list(flipkart['Price'])
        Reviews = list(flipkart['Reviews'])
        Image = list(flipkart['Image'])

        model1 = list(amazon_data['Name'])
        Price1 = list(amazon_data['Price'])
        Reviews1 = list(amazon_data['Reviews'])
        Image1 = list(amazon_data['Image'])
        count = 0
        for i in range(len(model)):
            count+=1
            k = (model[i],Price[i],Reviews[i],Image[i],count)
            flipkartdata.append(k)
        count = 0
        for i in range(len(model1)):
            count+=1
            k = (model1[i],Price1[i],Reviews1[i],Image1[i],count)
            amazondata.append(k)

        # last = math.ceil(len(amazondata)/numofproducts)
        last= math.ceil(len(flipkartdata)/numofproducts)

        if int(pageno)<=0:
            prev = 0
            next = int(pageno)+1
        elif int(pageno) == last:
            prev = int(pageno)-1
            next = last
        else:
            prev = int(pageno)-1
            next = int(pageno)+1

        amazondata = amazondata[(int(pageno)*numofproducts):(int(pageno)*numofproducts+numofproducts)]
        flipkartdata = flipkartdata[(int(pageno)*numofproducts):(int(pageno)*numofproducts+numofproducts)]

        return render_template("compare.html",flipkartdata=flipkartdata,amazondata=amazondata,prev=prev,next=next,pageno=pageno,account=params['username'])

    else:
        return redirect("/login")
@app.route("/logout")
def logout():
    session.pop('u_name')
    return redirect("/")


app.run(debug=True)




