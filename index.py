from logging import basicConfig
from flask import Flask,render_template,redirect,url_for,send_from_directory,request,jsonify,session
from flask.helpers import flash
from pymongo import MongoClient
import ssl
import requests
import os
import json 
import datetime
import pandas as pd
from datetime import datetime,timedelta
from dateutil import parser
import time
# os.environ['TZ'] = 'Asia/Kolkata' # set new timezone
# time.tzset()
# time.localtime()
admins = {"bzadmin":"admin@beingzero"}
# from requests.api import request
client = MongoClient("mongodb+srv://admin:bzhandles@datastore.rzoau.mongodb.net/myFirstDatabase&retryWrites=true&w=majority",ssl_cert_reqs=ssl.CERT_NONE)
db = client['Contest']
col = db['CollegeDetails']
dictionary = {}
for i in col.find():
  dictionary[i['collegeId']] = i['batchSlug']
print(dictionary)
app = Flask(__name__)
app.secret_key = "1234"

@app.route("/")
def home():
  flag = False
  if "username" in session:
    flag = True
  db = client['Contest']
  col = db['CollegeDetails']
  dictionary = {}
  for i in col.find():
    dictionary[i['collegeId']] = i['batchSlug']
  return render_template("home.html",d = dictionary,flag = flag)

@app.route('/favicon.ico') 
def favicon(): 
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

def status(l):
  l1 = []
  l2 = l
  l=l['model']
  l=l['challenges']
  #print(l)
  ta=0
  try:
    for i in range(len(l)):
      if l[i]['attempted1']:
        ta+=1
    if ta==0:
      l1.append("Not Participated")
    else:
      l1.append("Solved - "+str(ta))
    t1 = l2['model']['challenges']
    l1.append(float(t1[0]['score1'])+float(t1[1]['score1']))
  except:
    l1.append("Not Participated")
    l1.append(0)
  if l1[0] == "Not Participated":
    l1 = -100
  else:
    l1 = l1[1]
  d1 = {}
  d1["-".join((l2['model']['contest']['starttime'].split("T")[0]).split("-")[::-1])] = l1
  return d1

def autoUpdateParticipationUtil(name):
  batch = name
  print(batch)
  db = client['Contest']
  col = db['CollegeDetails']
  # l12 = []
  # for i in col.find():
  #   l12.append(i)
  # l12 = l12[0]
  # dictionary = {}
  # for i in col.find():
  #   dictionary[i['collegeId']] = i['batchSlug']
  college = list(col.find({"collegeId":batch}))[0]
  contest_slug = college['batchSlug']
  db = client["Contest"]
  collection = db[batch]
  l = []
  for i in collection.find():
    l.append(i)
  ml = []
  for i in l:
    agent = {"User-Agent":'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
    url="https://www.hackerrank.com/rest/compare?&contest_slug="+contest_slug+"&hacker_slug_1="+str(i['hackerrank_handle'])+"&hacker_slug_2=&_=1638202112967"
    r=requests.get(url,headers=agent)
    q=r.json()
    ctime = datetime.now()
    stime = q['model']['contest']['endtime']
    stime = parser.parse(stime.split("T")[0]+ " "+ stime.split("T")[-1].split('.')[0]) 
    etime = q['model']['contest']['endtime']
    etime = parser.parse(etime.split("T")[0]+ " "+ etime.split("T")[-1].split('.')[0]) 
    etime = etime + timedelta(hours = 5) + timedelta(minutes = 30)
    print(etime,ctime)
    if (ctime<=etime):
      return {"Succes":False}
    # print(stime,etime,l[0]['Hackerrank contests'])
    # print(q)
    ml.append(status(q))
    if list(ml[0])[0] in college['contestDates']:
      return {"Success":False}
  for i in range(len(l)):
    l[i]['Hackerrank contests'][list(ml[0])[0]] = ml[i][list(ml[0])[0]]
    try:
      l[i]["Hackerrank contests score"] += float(list(ml[i].values())[0])
    except:
      l[i]["Hackerrank contests score"] += -100
  for i in l:
    filter = { 'hackerrank_handle': i['hackerrank_handle']}
    newvalues = { "$set": { 'Hackerrank contests': i['Hackerrank contests'],"Hackerrank contests score" : i["Hackerrank contests score"] } } 
    collection.update_one(filter, newvalues)
  college['contestDates'].append(ml[0][0])
  col.update_one({"collegeId":batch},{"$set":college['contestDates']})
  return {"Success":True}

@app.route("/autoupdtest")
def autoUpdateParticipation():
  db = client['Contest']
  col = db['CollegeDetails']
  dictionary = {}
  for i in col.find():
    dictionary[i['collegeId']] = i['batchSlug']
  for i in dictionary:
    print(autoUpdateParticipationUtil(i))
  return {"Success":True}

def updateparticipation(name):
  batch = name
  print(batch)
  db = client['Contest']
  col = db['CollegeDetails']
  l12 = []
  for i in col.find():
    l12.append(i)
  l12 = l12[0]
  dictionary = l12['colleges']
  contest_slug = dictionary[batch]
  db = client["Contest"]
  collection = db[batch]
  l = []
  for i in collection.find():
    l.append(i)
  ml = []
  for i in l:
    agent = {"User-Agent":'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
    url="https://www.hackerrank.com/rest/compare?&contest_slug="+contest_slug+"&hacker_slug_1="+str(i['hackerrank_handle'])+"&hacker_slug_2=&_=1638202112967"
    r=requests.get(url,headers=agent)
    q=r.json()
    # print(q)
    ml.append(status(q))
    if list(ml[0])[0] in l[0]['Hackerrank contests']:
      return {"Success":False}
  for i in range(len(l)):
    l[i]['Hackerrank contests'][list(ml[0])[0]] = ml[i][list(ml[0])[0]]
    try:
      l[i]["Hackerrank contests score"] += float(list(ml[i].values())[0])
    except:
      l[i]["Hackerrank contests score"] += -100
  for i in l:
    filter = { 'hackerrank_handle': i['hackerrank_handle']}
    newvalues = { "$set": { 'Hackerrank contests': i['Hackerrank contests'],"Hackerrank contests score" : i["Hackerrank contests score"] } } 
    collection.update_one(filter, newvalues)
  return {"Success":True}

@app.route("/forceupd/<name>")
def forceupdateparticipation(name):
  batch = name
  print(batch)
  db = client['Contest']
  col = db['CollegeDetails']
  l12 = []
  for i in col.find():
    l12.append(i)
  l12 = l12[0]
  dictionary = l12['colleges']
  contest_slug = dictionary[batch]
  db = client["Contest"]
  collection = db[batch]
  l = []
  for i in collection.find():
    l.append(i)
  ml = []
  for i in l:
    agent = {"User-Agent":'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
    url="https://www.hackerrank.com/rest/compare?&contest_slug="+contest_slug+"&hacker_slug_1="+str(i['hackerrank_handle'])+"&hacker_slug_2=&_=1638202112967"
    r=requests.get(url,headers=agent)
    q=r.json()
    # print(q)
    ml.append(status(q))
  for i in range(len(l)):
    l[i]['Hackerrank contests'][list(ml[0])[0]] = ml[i][list(ml[0])[0]]
    try:
      l[i]["Hackerrank contests score"] += float(list(ml[i].values())[0])
    except:
      l[i]["Hackerrank contests score"] += -100
  for i in l:
    filter = { 'hackerrank_handle': i['hackerrank_handle']}
    newvalues = { "$set": { 'Hackerrank contests': i['Hackerrank contests'],"Hackerrank contests score" : i["Hackerrank contests score"] } } 
    collection.update_one(filter, newvalues)
  return {"Success":True}

@app.route('/logout')
def logout():
   session.pop('username', None)
   return redirect(url_for('home'))

@app.route('/login', methods = ['GET', 'POST'])
def login():
   if request.method == 'POST':
        user = request.form['username']
        password = request.form['password']
        if user in admins and admins[user] == password:
          session['username'] = user
          return redirect(url_for('home'))
        else:
            return redirect(url_for('login'))
   return render_template("login.html")


@app.route("/handles/<name>",methods = ["GET","POST"])
def updatehandles(name):
  if request.method=="POST":
    print(list(request.files))
    df = request.files['file']
    df = pd.read_excel(df)
    d = []
    for i in range(len(df['name'])):
      d1 = {"name":df['name'][i]}
      col = df.columns
      for j in col[2::2]:
        if df[j+"_valid"][i] == True or df[j+"_valid"][i] == 1.0:
          d1[j] = df[j][i]
        else:
          d1[j] = None
      d.append(d1)
    db = client["Contest"]
    col = db[name]
    l = {}
    for i in col.find():
      l[i['name']] = i['hackerrank_handle']
    c = 0
    for i in d:
      if i['name'] in l and l[i['name']] != i['hackerrank_handle']:
        c+=1
        print(i['name'])
        col.update_one({'name':i['name']},{"$set":{"hackerrank_handle":i['hackerrank_handle']}})
    flash("Updated "+str(c)+" handles")
  return redirect(url_for("home"))

@app.route("/insert/<name>",methods = ["GET","POST"])
def insertstudents(name):
  if request.method=="POST":
    print(list(request.files))
    df = request.files['file']
    df = pd.read_excel(df)
    d = []
    db = client["Contest"]
    collection = db[name]
    l = {}
    c = 0
    for i in collection.find():
      l[i['name']] = i['hackerrank_handle']
    for i in range(len(df['name'])):
      d1 = {"name":df['name'][i]}
      if d1["name"] in l:
        continue
      c+=1
      col = df.columns
      for j in col[2::2]:
        if df[j+"_valid"][i] == True or df[j+"_valid"][i] == 1.0:
          d1[j] = df[j][i]
        else:
          d1[j] = None
      d1['Hackerrank contests score'] = 0
      d1["Hackerrank contests"] = {}
      d1['isRemoved'] = False
      d.append(d1)
    collection.insert_many(d)
    flash("Inserted "+str(c)+" Students")
  return redirect(url_for("home"))

@app.route("/newregistration",methods = ["GET","POST"])
def newregistration():
    flag = False
    if "username" in session:
      flag = True
    if request.method == "POST":
        db = client['Contest']
        col = db['CollegeDetails']
        l12 = []
        for i in col.find():
          l12.append(i)
        l12 = l12[0]
        dictionary = l12['colleges']
        db = client["Contest"]
        df = request.files['file']
        df = pd.read_excel(df)
        d = []
        for i in range(len(df['name'])):
            d1 = {"name":df['name'][i]}
            col = df.columns
            for j in col[2::2]:
                if df[j+"_valid"][i] == True or df[j+"_valid"][i] == 1.0:
                    d1[j] = df[j][i]
                else:
                    d1[j] = None
            d1['Hackerrank contests score'] = 0
            d1["Hackerrank contests"] = {}
            d1['isRemoved'] = False
            d.append(d1)
        collegecode  =request.form['clgcode']
        phase = "".join(list(request.form['phase'].split("-"))) 
        print(phase)
        batchyear = "".join(list(request.form['batch'].split("-"))) 
        s = 'BZ'+collegecode+batchyear+"P"+phase[-1]
        hackerrank_url = request.form['hackerrankurl']
        hackerrank_url = hackerrank_url.split("/")[4]
        print(s)
        if s in dictionary:
          flash("This Batch is already present in the Site")
          return redirect(url_for("home"))
        col = db[s]
        col.insert_many(d)
        dictionary[s] = hackerrank_url
        col1 = db['CollegeDetails']
        col1.update_one({"_id":l12['_id']},{"$set":{"colleges":dictionary}})
        json.dump(dictionary,open("batches.txt",'w'))
        return redirect(url_for("home"))
    return render_template("newbatch.html",flag = flag)
# @app.route("/input/<name>",methods = ["GET","POST"])
# def inp(name):
#   print(name)
  # if request.method == "POST":
  #   n = request.form['hidden_skills']
  #   print(n.split(","))
  # db = client["Handles"]
  # collection = db['BZCMRTC2024P1']
  # l = []
  # for i in collection.find():
  #   l.append(i)
  # for i in range(len(l)):
  #   l[i] = l[i]['name']
  # return render_template("input.html")

@app.route("/add/<name>",methods = ["GET","POST"])
def addfromblockedlist(name):
  if request.method == "POST":
    db = client["Contest"]
    collection = db[name]
    n = request.form['names_for_addition']
    n = n.split(",")
    print(n)
    for i in n:
      collection.update_one({"name":i},{"$set":{"isRemoved":False}})
    print("done")
    # flash("Students have been Added")
    return {"Success":True}
  return redirect(url_for("home"))

@app.route("/rm/<name>",methods = ["GET","POST"])
def moveToBlockedList(name):
  if request.method == "POST":
    db = client["Contest"]
    collection = db[name]
    n = request.form['hidden_skills']
    n = n.split(",")
    for i in n:
      collection.update_one({"name":i},{"$set":{"isRemoved":True}})
    print("done")
    # flash("Students have been removed")
    return {"Success":True}
  return redirect(url_for("home"))

@app.route("/erasedate/<name>",methods = ['GET','POST'])
def erasedate(name):
  if request.method == "POST":
    date = request.form['date']
    db = client['Contest']
    col = db[name]
    l = []
    for i in col.find():
      l.append(i)
    for i in range(len(l)):
      if date in l[i]['Hackerrank contests']:
        del l[i]['Hackerrank contests'][date]
      col.update_one({'name':l[i]['name']},{"$set":{'Hackerrank contests':l[i]['Hackerrank contests']}})
    return redirect(name)
  return redirect(url_for('home'))

@app.route("/<name>",methods = ["GET","POST"])
def getleaderboard(name):
    if name[0:2]!='BZ':
      return redirect(url_for("home"))
    flag = False
    if "username" in session:
      flag = True
    # if name[0:3] == "new":
    #     newparticipation(name.split("$")[-1])
    db = client["Contest"]
    collection = db[name]
    if request.method == "POST":
      n = request.form['hidden_skills']
      n = n.split(",")
      for i in n:
        collection.update_one({"name":i},{"$set":{"isRemoved":True}})
      print("done")
      flash("Students have been removed")
      return redirect(url_for("home"))
    l = []
    l2 = []
    removed_students = []
    for i in collection.find():
      if i['isRemoved']==False:
        l.append(i)
        l2.append(i['name'])
      else:
        removed_students.append(i['name'])
    l = sorted(l, key=lambda k: k['Hackerrank contests score'], reverse=True)
    #print(removed_students)
    # print(l[0]['Hackerrank contests'],name)
    if 'Hackerrank contests' in l[0]:
        dates = [datetime.strptime(ts, "%d-%m-%Y") for ts in l[0]['Hackerrank contests']]
        dates.sort()
        sorteddates = [datetime.strftime(ts, "%d-%m-%Y") for ts in dates]
        for i in range(len(l)):
          s = 0
          for j in sorteddates:
            if j not in l[i]['Hackerrank contests']:
              l[i]['Hackerrank contests'][j] = -100
            s+=l[i]['Hackerrank contests'][j]
          l[i]['Hackerrank contests score'] = s
        l = sorted(l, key=lambda k: k['Hackerrank contests score'], reverse=True)
        return render_template("leaderboard.html",l = l,l1 = sorteddates,le = len(sorteddates)+3,name = name,l2 = l2,l3 = removed_students,flag = flag)
    return render_template("leaderboard.html",l = l,l1 = {},name = name,l2 = l2,l3 = removed_students,flag = flag)

if __name__ == "__main__":
    app.run(debug=True)