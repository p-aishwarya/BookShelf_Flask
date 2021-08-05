from flask import Flask, render_template,request,jsonify
from flask.globals import session
from flask.helpers import flash, url_for
from werkzeug.utils import redirect
from models import *
import pandas as pd
from operator import and_


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://gvbhuwtbvlbaky:b846d16af3e74b7b7782777b2489f647e59c45c8164d91f1d011773f08b37101@ec2-3-233-100-43.compute-1.amazonaws.com:5432/dfgjco1sf9ki1a'
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
#     return render_template("users.html",users=user)
@app.route("/home",methods=["POST","GET"])
def home():
    flag = True
    if 'username' in session:
        username = session['username']
        flag = False
        return render_template("home.html",user = username,flag = flag)

    return render_template("home.html",flag = flag)

@app.route("/register",methods=["POST","GET"])
def register():
    if request.method=="GET":
        return render_template("register.html",flag=False)
    else:
        try:
            email_id=request.form.get("email")
            # session['username']=email_id
            password=request.form.get("psw")
            repeatpassword=request.form.get("psw-repeat")
            u=Users(email=email_id,pwd=password,repeatpwd=repeatpassword)
            db.session.add(u)
            db.session.commit()
            # result=Users.query.all()
            return render_template("login.html")
        except:
            return render_template("register.html",flag=True)

        # return f" Great {email_id} Registration process is completed!!"
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

@app.route("/logout",methods=["POST","GET"])
def logout():
    session.pop('username',None)
    return redirect('home')
@app.route("/book", methods=["POST","GET"])
def book():
    if request.method == "POST":
        det = request.form['bookform_data']
        print(det)
        tag = '%'+det+'%'
        book1 = Bookdetails.query.filter(Bookdetails.id.ilike(tag)).all()
        book2 = Bookdetails.query.filter(Bookdetails.title.ilike(tag)).all()
        book3 = Bookdetails.query.filter(Bookdetails.author.ilike(tag)).all()
        book4 = Bookdetails.query.filter(Bookdetails.year.ilike(tag)).all()
        books = book1+book2+book3+book4
        books_dict=[]
        for each in books:
            context = {'isbn':each.id, 'Title':each.title,'Author':each.author, 'Year':each.year}
            # print(context)
            books_dict.append(context)
            context={}

        return jsonify(books_dict)
        # if "username" in session:
        #     username = session['username']
        #     flag = False
        #     return render_template("home.html",user = username,flag = flag,books=book)
        # else:
        #     return render_template("home.html",flag = True,books=book)
    else:
        return redirect('home')

@app.route("/book/details/<id>",methods=['POST','GET'])
def get_book_details(id):
    det = Bookdetails.query.filter(Bookdetails.id==id).all()
    total_reviews = reviews.query.filter(reviews.bookId==id).all()
    session['bookid'] = id
    flag_review = False
    book_del = True
    if 'username' in session:
        user = session['username']
        try:
            rev = reviews.query.filter(and_(reviews.bookId==id,reviews.uname==user)).first()
            if rev.uname != None:
                flag_review = False
        except Exception as e:
            print("exception while clicked on id = ",e)
            flag_review = True

        try:
            s = shelf.query.filter(and_(shelf.bookId==id, shelf.uname==user)).first()
            if s.bookId != None:
                book_del = False
        except:
            book_del = True

    
        return render_template('details.html',reviews=total_reviews,user=user,flag_review=flag_review,flag=False,details=det,book_del = book_del)
    else:
        return render_template('details.html',reviews=total_reviews,flag_review=flag_review,flag=True,details=det,book_del = book_del)


@app.route("/review", methods=['POST','GET'])
def review():
    if request.method == 'GET':
        return render_template('details.html')
    else:
        review = request.form.get('review')
        rating = request.form.get('rating')
        user = session['username']
        bookid = session['bookid']
        print("from /review , user= ",user," book = ",bookid)
        r = reviews(bookId=bookid,uname=user,review=review,rating=int(rating))
        db.session.add(r)
        db.session.commit()
        book_del= True
        try:
            s = shelf.query.filter(and_(shelf.bookId==id, shelf.uname==user)).first()
            if s.bookId != None:
                book_del = False
        except:
            book_del = True
        det = Bookdetails.query.filter(Bookdetails.id==bookid).all()
        total_reviews = reviews.query.filter(reviews.bookId==bookid).all()
        return render_template('details.html', reviews=total_reviews, flag_review=False, user=user, flag=False, details=det,book_del=book_del)

@app.route('/shelfsubmit', methods=['POST','GET'])
def shelfsubmit():
    if request.method == 'GET':
        return redirect('home')
    else:
        bookid = session['bookid']
        det = Bookdetails.query.filter(Bookdetails.id==bookid).all()
        total_reviews = reviews.query.filter(reviews.bookId==bookid).all()
        book_del = True
        flag_review = False
        if 'username' in session:
            count = request.form.get('shelf')
            user = session['username']
            
            try:
                s = shelf.query.filter(and_(shelf.bookId==bookid, shelf.uname==user)).delete()
                db.session.commit()
                print("*****",s,type(s))
                if s == 0:
                    print(s.uname)
                # print("shelf submit files = ",s.uname,s.bookId)
                flash("Book is removed from the shelf")
                book_del = True
            except Exception as e:
                print("exception from shelf submit = ",e)
                s = shelf(bookId=bookid, uname=user, bookCount=count)
                db.session.add(s)
                db.session.commit()
                book_del = False
                flash("Book is added into Shelf")
                
            try:
                rev = reviews.query.filter(and_(reviews.bookId==bookid,reviews.uname==user)).first()
                if rev.uname != None:
                    flag_review = False
            except Exception as e:
                print("exception while clicked on id = ",e)
                flag_review = True
            
            return render_template('details.html',reviews=total_reviews,user=user,flag_review=flag_review,flag=False,details=det,book_del = book_del)
            # return render_template('index.html', form=form)

        else:
            flash("Please login or register to add the book")
            return render_template('details.html',reviews=total_reviews,flag_review=flag_review,flag=True,details=det,book_del = book_del)

@app.route("/shelfpage",methods=['POST','GET'])
def shelfpage():
    if 'username' in session:
        user = session['username']
        try:
            books = shelf.query.filter(shelf.uname==user).all()
            user = session['username']
            shelfbooks = []
            for book in books:
                bookid=book.bookId
                det = Bookdetails.query.filter(Bookdetails.id==bookid).all()
                shelfbooks.append(det)

            # print("shelfbooks = ",shelfbooks)
            return render_template("shelf.html",books=shelfbooks,flag=False,user=user)
        except:
            return render_template('shelf.html',msg=True)
    else:
        pass

@app.route("/admin")
def admin():
    user = Bookdetails.query.all()
    return render_template("user.html",users=user)