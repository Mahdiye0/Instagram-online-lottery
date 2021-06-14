from flask import Flask, render_template, request, redirect, url_for,session
from flask_sqlalchemy import SQLAlchemy
from scrapinsta import Scraper
from instaloader import  Instaloader, Profile, Post
# from flask_debugtoolbar import DebugToolbarExtension
import os
import shutil
import urllib
import random
from suds.client import Client



app = Flask(__name__)
app.debug = True
app.secret_key = 'any random string'
# app.config['SECRET_KEY'] = b'_5#y2L"F4Q8z\n\xec]/'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS']=False
# //toolbar = DebugToolbarExtension(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:@localhost/lottery"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(100))
    password = db.Column(db.String(100))
    email = db.Column(db.String(100))
class Member_refid(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    idmember = db.Column(db.Integer)
    refid = db.Column(db.String(100))
    
    
    
db.create_all()
db.session.commit()

@app.route("/")
def index():
    return render_template("index.html", form_action= 'login')

@app.route("/new")
def new():
    return render_template("register.html" , form_action= 'register' )


@app.route("/register")
def register():
   
    return render_template("register.html",message="1" )

@app.route("/process" , methods=["POST"])
def process():
    try:

        u = request.form["user"]
        p = request.form["password"]
        e = request.form["email"]
        r = Member.query.filter_by(user=u).first()
        if r is None:
            member = Member(user=u,password=p,email=e)
            db.session.add(member)
            db.session.commit()
            return redirect(url_for('index'))
        else:
            return redirect(url_for('register',message="2"))

    except Exception as ex:
        return ex


    

@app.route("/loginprocss" , methods=['GET', 'POST'])
def loginprocss():
    try:
        u = request.form["user"]
        p = request.form["password"]
        r = Member.query.filter_by(user=u,password=p).first()
        if r is not None:
            session['id']=r.id
            session['user']=request.form["user"]
            return redirect(url_for('login'))
            #,list=[False,False,False,False],post="",text="",count="",flag=False,flag1=False,flag2=False))

            #return render_template  ("login.html",src="",list=[False,False,False,False],post="",text="",count="",flag=False,flag1=False,flag2=False)
#یه بررسی بکمن
        else:
            return redirect(url_for('index',flag=True))

    except Exception as ex:
        return ex
@app.route("/login" )
def login():
    return render_template  ("login.html",src="",list=[False,False,False,False],post="",text="",count="",flag=False,flag1=False,flag2=False)


@app.route("/logout" )
def logout():
    try:

        session.clear()
        return redirect(url_for('index'))

    except Exception as ex:
        return ex

@app.route("/Outputprocss" , methods=["POST"])
def Outputprocss():
    try:
        dir = 'test'
        for f in os.listdir(dir):
            os.remove(os.path.join(dir, f))
        post=request.form["addresspost"]
        session['link']=post
        short=post[-40:]
        a=Scraper().scraperpost(short[0:11])
        check=[False,False,False,False]
        flagm=False
        flagl=False
        flagc=False
        flagf=False
        countmm=0
        countl=0
        countc=0
        countff=0
        session['m']=''
        session['c']=''
        session['l']=''
        session['f']=''
        if  "mention" in request.form:
            flagm=True
            check[3]=True
            countmm=Scraper().countmention(short[0:11])
            session['m']='mention'
        if   "comment" in request.form:
            flagc=True
            check[0]=True
            countc=Scraper().countcomment(post)
            session['c']='comment'
        if "like" in request.form:
            flagl=True
            check[1]=True
            countl=Scraper().countlike(post)
            session['l']='like'
        if "followers" in request.form:
            check[2]=True
            flagf=True
            countff=Scraper().countf(a)
            session['f']='follower'
        if (countff+countmm+countl+countc)==0:
            flag=False
            flag1=False
            flag2=True
        elif (countff+countmm+countl+countc)>1000:
            flag=True
            flag1=False
            flag2=False
        else:
            flag1=True
            flag=False
            flag2=False
        
        session['count']=countff+countmm+countl+countc    
        return render_template("login.html",list=check,post=post,text="owner_username: "+a,countc=countc,countl=countl,countf=countff,countm=countmm,flagm=flagm,flagc=flagc,flagf=flagf,flagl=flagl,flag=flag,flag1=flag1,flag2=flag2)
    except TypeError :
        return  ("1-Input is incorrect. Check the link address and try again.\n2-Login to instagram fail.Please wait and try again .\n3- incorrect user or password for login to instagram set config.txt")  
    except OSError :
        return  ('There is no folder Test. Create it in the current path.try again')  
    except Exception as ex :
        return  ('Login to instagram fail.Please wait a few minutes before you try again')  #render_template  ("login.html",src="",list=[False,False,False,False],post="",text="",count="",flag=False,flag1=False,flag2=False)




MMERCHANT_ID = 'f4e0d012-a688-4234-81a8-14e69f3a2642'  # Required
ZARINPAL_WEBSERVICE = 'https://www.zarinpal.com/pg/services/WebGate/wsdl'  # Required
amount = 1000  # Amount will be based on Toman  Required
description = u'توضیحات تراکنش تستی'  # Required
email = 'user@userurl.ir'  # Optional
mobile = '09123456789'  # Optional

@app.route('/request/')
def send_request():
    client = Client(ZARINPAL_WEBSERVICE)
    result = client.service.PaymentRequest(MMERCHANT_ID,
                                           amount,
                                           description,
                                           email,
                                           mobile,
                                           str(url_for('verify', _external=True)))
    if result.Status == 100:
        return redirect('https://www.zarinpal.com/pg/StartPay/' + result.Authority)
    else:
        return 'Error'

@app.route('/verify/', methods=['GET', 'POST'])
def verify():
    client = Client(ZARINPAL_WEBSERVICE)
    if request.args.get('Status') == 'OK':
        result = client.service.PaymentVerification(MMERCHANT_ID,
                                                    request.args['Authority'],
                                                    amount)
        if result.Status == 100:
            memberid = Member_refid(idmember=session['id'],refid=str(result.RefID))
            db.session.add(memberid)
            db.session.commit()
            return render_template('verify.html',refid=str(result.RefID),flag=True)
        elif result.Status == 101:
            return render_template('verify.html', refid=str(result.Status),flag1=True)
        else:
            return 'Transaction failed. Status: ' + str(result.Status)
    else:
        return 'Transaction failed or canceled by user'
    

@app.route("/report")
def report():
    try:
        return  render_template('report.html',winer="",flag=False)
    except Exception as ex:
        return ex     

@app.route("/download")
def download():
    try:
        if session['c']=='comment':
            filename=Scraper().Exportfilecomment('comment',session['link'])
            session['filec']=filename
        if session['l']=='like':
            filename=Scraper().Exportfilelike('like',session['link'])
            session['filel']=filename
        if session['f']=='follower':
            filename=Scraper().Exportfilefollower('follower',session['link'])
            session['filef']=filename
        if session['m']=='mention':
            filename=Scraper().Exportfilemention('mention',session['link'])
            session['filem']=filename
        
        return  render_template('report.html',winer="",flag=False)
    except TypeError :
        return  ('Please close the Excel file if it is open and  try again')  #render_template  ("login.html",src="",list=[False,False,False,False],post="",text="",count="",flag=False,flag1=False,flag2=False)
        
    except Exception :
        return  ('Login to instagram fail.Please wait a few minutes before you try again')  #render_template  ("login.html",src="",list=[False,False,False,False],post="",text="",count="",flag=False,flag1=False,flag2=False)
   
@app.route("/Lotterry")
def Lotterry():
    try:
        listlike=[]
        if session['l']=='like':
            listlike=Scraper().get_list_like(session['link'])
        if session['f']=='follower':
            listfollower=Scraper().get_list_follower(session['link'])
            for x in listfollower:
                listlike.append(x)
        if session['c']=='comment':
            listcomment=Scraper().get_list_comment(session['link'])
            for x in listcomment:
                listlike.append(x)
        if session['m']=='mention':
            listmention=Scraper().get_list_mention(session['link'])
            for x in listmention:
                listlike.append(x)

        if len(listlike)>0:
            n = random.randint(0,len(listlike)-1)
            winer=listlike[n]
            flag=True
            return  render_template('report.html',winer=str(winer),flag=flag)
        else: 
            return  render_template('report.html',winer="",flag=False)
    except Exception as ex:
        return  ('Login to instagram fail.Please wait a few minutes before you try again')  #render_template  ("login.html",src="",list=[False,False,False,False],post="",text="",count="",flag=False,flag1=False,flag2=False)
  

if __name__ == "__main__":
    app.run(debug=True)