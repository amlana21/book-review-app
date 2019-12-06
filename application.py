import os

from flask import Flask, session,render_template, request,jsonify,make_response
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import requests
from flask_bcrypt import Bcrypt

from xmlparse import parse_response

app = Flask(__name__)
bcrypt = Bcrypt(app)
bookreadsapi=os.getenv("BOOKREADS_API")

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))
#

@app.route("/",methods=['GET'])
def index():
    if session.get('user_id') is None:
        # session["user_id"] = []
        return render_template('login.html')
    else:
        return render_template('index.html')

@app.route("/login",methods=['POST'])
def login():
    input=request.get_json()
    username=input['username']
    password=input['password']
    if "'" in username:
        resp=make_response(jsonify(error=str('invalid user')),400)
        return resp
    elif '"' in username:
        resp=make_response(jsonify(error=str('invalid user')),400)
        return resp

    try:
        rep={'username':username}        
        count=db.execute("SELECT * FROM users WHERE username=:username",{"username":username}).fetchall()
        if len(count)==0:
            raise Exception('Auth Failed')
        else:
            pwd=count[0]['pssword']
            usr_id=count[0]['id']
            rep['id']=usr_id
            pw_chk=bcrypt.check_password_hash(pwd, password)            
            if pw_chk:
                resp=make_response(jsonify(login='success',details=rep),200)
                session["user_id"] = []
                session["user_id"].append(usr_id)
                return resp
            else:
                raise Exception('Auth Failed')
    except Exception as e:
        resp=make_response(jsonify(error=str(e)),400)
        return resp

    


@app.route('/logout',methods=['GET'])
def logout():
    if not session['user_id'] is None:
        session['user_id']=None
    return render_template('logout.html')



@app.route("/register",methods=['POST'])
def register():
    input=request.get_json()
    fname=input['firstname']
    lname=input['lastname']
    email=input['email']
    username=input['username']
    password=bcrypt.generate_password_hash(input['password']).decode('utf8')
    loginstatus='loggedoff'
    if "'" in username:
        resp=make_response(jsonify(error=str('invalid user')),400)
        return resp
    elif '"' in username:
        resp=make_response(jsonify(error=str('invalid user')),400)
        return resp
    try:
        db.execute("INSERT INTO users (firstname,lastname,email,username,pssword,loginstatus) values (:firstname,:lastname,:email,:username,:pssword,:loginstatus)",{"firstname":fname,"lastname":lname,"email":email,"username":username,"pssword":password,"loginstatus":loginstatus})
        db.commit()
        resp = make_response(jsonify(status='success',user=input), 200)
        return resp
    except Exception as e:
        # print("error: "+e)
        
        resp = make_response(jsonify(error=str(e)), 400)
        return resp

@app.route('/api/<isbn>',methods=['GET'])
def getbook(isbn):
    isbn=isbn
    try:
        books=db.execute('SELECT * FROM books WHERE isbn=:isbn',{'isbn':isbn}).fetchall()
        bookdir={}
        for book in books:
            bookdir['title']=book.title
            bookdir['author']=book.author
            bookdir['year']=book.year
            bookdir['isbn']=book.isbn
            bookdir['id']=book.id
            

        if len(books)>=1:
            #api call
            url="https://www.goodreads.com/book/review_counts.json?key={}&isbns={}".format(bookreadsapi,isbn)
            bookapi=requests.get(url)
            apireq=bookapi.json()
            bookdir['review_count']=apireq['books'][0]['reviews_count']
            bookdir['average_score']=apireq['books'][0]['average_rating']
            resp=make_response(jsonify(bookdir),200)
        else:
            raise Exception('No Books')
    except Exception as e:
        resp=make_response(jsonify(error=str(e)),400)
    return resp



@app.route('/submit/review',methods=['POST'])
def submit_review():
    if session.get('user_id') is None:
        return render_template('login.html')
    inpt=request.get_json()
    rating=inpt['rating']
    review=inpt['review']
    user_id=session['user_id'][0]
    book_id=inpt['book_id']
    try:
        inserted=db.execute("INSERT INTO reviews (rating,review,user_id,book_id) values (:rating,:review,:user_id,:book_id) RETURNING id",{"rating":rating,"review":review,"user_id":user_id,"book_id":book_id})
        recid = inserted.fetchone()[0]
        db.commit()
        # get username
        usrname=db.execute("SELECT * FROM users where id=:user_id",{"user_id":user_id}).fetchall()
        usrid=[]
        for usr in usrname:
            usrid.append(usr.username)
        resp=make_response(jsonify(record_id=recid,username=usrid[0]),200)
    except Exception as e:
        resp=make_response(jsonify(error=str(e)),400)
    return resp
    
@app.route('/review/<bookid>',methods=['GET'])
def getreview(bookid):
    try:
        
        review=db.execute("select rev.*,usrs.* from reviews rev join users usrs on rev.user_id = usrs.ID and rev.book_id=:bookid",{"bookid":bookid}).fetchall()
        revs=[]
        for indx,rev in enumerate(review):
            tmprv={}
            tmprv['id']=rev.id
            tmprv['rating']=rev.rating
            tmprv['review']=rev.review
            tmprv['user_id']=rev.user_id
            tmprv['book_id']=rev.book_id
            tmprv['username']=rev.username
            revs.append(tmprv)

        if len(review)==0:
            resp=make_response(jsonify(error='no book found'),400)
        else:
            resp=make_response(jsonify(revs),200)
    except Exception as e:
        resp=make_response(jsonify(error=str(e)),400)
    return resp


@app.route('/books/search',methods=['GET'])
def booksearch():
    args=request.args
    for arg in args:
        srch=args[arg]

    try:
        # search in isbn 
        qry1="SELECT * FROM books WHERE isbn LIKE '%"+srch+"%'"
        srch1=db.execute(qry1).fetchall()
        if len(srch1)>=1:
            rslts=[]
            for s in srch1:
                srchrslt={}
                srchrslt['title']=s.title
                srchrslt['author']=s.author
                srchrslt['year']=s.year
                srchrslt['isbn']=s.isbn
                srchrslt['id']=s.id
                
                img_urls=parse_response("https://www.goodreads.com/search.xml?key={}&q={}".format(bookreadsapi,s.isbn))
                srchrslt['pics']=img_urls
                
                # picrslts=picout.json()
                rslts.append(srchrslt)
            # resp=make_response(jsonify(results=rslts,pics="{}".format(tree)),200)
            resp=make_response(jsonify(results=rslts),200)
            return resp
        
        # search in name
        qry1="SELECT * FROM books WHERE title LIKE '%"+srch+"%'"
        srch1=db.execute(qry1).fetchall()
        if len(srch1)>=1:
            rslts=[]
            for s in srch1:
                srchrslt={}
                srchrslt['title']=s.title
                srchrslt['author']=s.author
                srchrslt['year']=s.year
                srchrslt['isbn']=s.isbn
                srchrslt['id']=s.id
                img_urls=parse_response("https://www.goodreads.com/search.xml?key={}&q={}".format(bookreadsapi,s.isbn))
                srchrslt['pics']=img_urls
                rslts.append(srchrslt)
            resp=make_response(jsonify(results=rslts),200)
            return resp
    
        # search in author
        qry1="SELECT * FROM books WHERE author LIKE '%"+srch+"%'"
        srch1=db.execute(qry1).fetchall()
        if len(srch1)>=1:
            rslts=[]
            for s in srch1:
                srchrslt={}
                srchrslt['title']=s.title
                srchrslt['author']=s.author
                srchrslt['year']=s.year
                srchrslt['isbn']=s.isbn
                srchrslt['id']=s.id
                img_urls=parse_response("https://www.goodreads.com/search.xml?key={}&q={}".format(bookreadsapi,s.isbn))
                srchrslt['pics']=img_urls
                rslts.append(srchrslt)
            resp=make_response(jsonify(results=rslts),200)
            return resp
        resp=make_response(jsonify(found='none'),404)
        return resp
    except Exception as e:
        resp=make_response(jsonify(error=str(e)),400)
        return resp

@app.route('/details',methods=['GET'])
def detailspage():
    args=request.args
    return render_template('details.html',bookid=args['isbn'],picurl=args['picarr'])