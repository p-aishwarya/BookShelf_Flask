from flask.globals import session
from models import Users
from flask import Flask, render_template, request
from flask.helpers import url_for
from werkzeug.utils import redirect
from models import *
import pandas as pd
from operator import and_


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://wddkoosrokkkvx:6f57bbd8bb669eb06c9f1d8dd59546e008938cadf5b8dda97474f120170fd56e@ec2-3-233-100-43.compute-1.amazonaws.com:5432/ddmue56io1262'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
app.secret_key = "any random string"

with app.app_context():
    db.create_all()

# @app.route("/")
# def index():
#     df = pd.read_csv('books.csv', index_col='isbn')
#     for ind in df.index:
#         try:
#             b = Bookdetails(id=ind,title=df['title'][ind],author=df['author'][ind],year=str(df['year'][ind]))
#             db.session.add(b)
#         except Exception as e:
#             print("pandas ind",e)
#     db.session.commit()
#     user = Bookdetails.query.all()
#     return render_template("user.html",users=user)

@app.route("/home", methods = ["POST","GET"])
def home():
    flag = True
    if 'username' in session:
        username = session['username']
        flag = False
        return render_template("home.html",user = username,flag = flag)

    return render_template("home.html",flag=flag)

@app.route("/register", methods = ["POST","GET"])
def register():
    if request.method == "GET":
        return render_template("register.html", flag=False)

    else:
        try:
            email = request.form.get("email")
            # session['username']=email
            pwd = request.form.get("psw")
            repeatpwd = request.form.get("psw-repeat")
            u = Users(email=email,pwd=pwd, repeat=repeatpwd)
            db.session.add(u)
            db.session.commit()
            # user=Users.query.all()
            return render_template("login.html")
        except:
            return render_template("register.html", flag=True)

@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html',flag=False)
    if request.method == 'POST':
        name = request.form.get('username') 
        password = request.form.get("password")
        # time=datetime.now()
        try:
            login_check = Users.query.filter(and_(Users.email==name,Users.pwd==password)).first()
            session['username'] = login_check.email
            return redirect('home')

            # return render_template("home.html",user=login_check.username,flag=False)
        except Exception as e: 
            print("exception in login page",e)
            return render_template("login.html",flag=True)

@app.route("/logout", methods = ["POST","GET"])
def logout():
    session.pop('username',None)

    return redirect('home')

@app.route("/book", methods=["POST","GET"])
def book():
    if request.method == "POST":
        det = request.form.get("bookvalue")
        tag = '%'+det+'%'
        book1 = Bookdetails.query.filter(Bookdetails.id.ilike(tag)).all()
        book2 = Bookdetails.query.filter(Bookdetails.title.ilike(tag)).all()
        book3 = Bookdetails.query.filter(Bookdetails.author.ilike(tag)).all()
        book4 = Bookdetails.query.filter(Bookdetails.year.ilike(tag)).all()
        book = book1+book2+book3+book4
        username = session['username']
        flag = False
        return render_template("home.html",user = username,flag = flag,books=book)
    else:
        return redirect('home')

