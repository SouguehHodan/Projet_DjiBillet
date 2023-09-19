from flask import Flask,render_template,redirect,session,url_for,request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column,Integer,String,ForeignKey
from sqlalchemy.orm import relationship
from flask_mysqldb import MySQL,MySQLdb
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
import bcrypt
import mysql.connector


app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+mysqlconnector://root:@localhost/Projet_Final"
db=SQLAlchemy()
db.init_app(app)
app.secret_key = 'secret_key'
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Projetdb.db"
# mydb = mysql.connector.connect(
#   host="localhost",
#   user="root",
#   password="",
#   database="Projet_Final"
# )
# print(mydb)
# app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:''@localhost/Project_Final"
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


class  Events(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nameE = db.Column(db.String(200))
    type = db.Column(db.String(200),  nullable=False)
    dates = db.Column(db.DateTime())
    adress = db.Column(db.String(200), nullable=False)
    prix = db.Column(db.Integer, nullable=False)
    Nb_place = db.Column(db.Integer, nullable=False)
    # fileimage = db.Column(db.String(20), nullable=False)
    following = relationship("User", secondary='reserver',backref='follower')

    def __init__(self,nameE,type,dates,adress,prix,Nb_place):
        self.nameE=nameE
        self.type=type
        self.dates=dates
        self.adress=adress
        self.prix=prix
        self.Nb_place=Nb_place
        # self.image=image

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200),nullable=False)
    email = db.Column(db.String(200),unique=True,nullable=False)
    password = db.Column(db.String(200))

    def __init__(self,email,password,name):
        self.name=name
        self.email=email
        self.password= bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    def check_password(self,password):
        return bcrypt.checkpw(password.encode('utf-8'),self.password.encode('utf-8'))

class Reserver(db.Model):
    id1 = db.Column(db.Integer,primary_key=True)
    qte=db.Column(db.Integer)
    events_id = db.Column(db.Integer, ForeignKey('events.id'))
    user_id = db.Column(db.Integer, ForeignKey('user.id'))
  

with app.app_context():
    db.create_all()

@app.route("/Inscription",methods=["GET","POST"])
def register():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        new_user = User(name=name,email=email,password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect("/Connection")        
    return render_template("inscrip.html")

@app.route("/Connection",methods=["GET","POST"])
def login():
    if request.method == "POST":
        email=request.form['email']
        password=request.form['password']

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            session['email'] = user.email
            session['password'] = user.password
            return redirect("/List_2")
        else:
            return render_template('connexion.html',error='invalid user')
    
    return render_template("connexion.html")

@app.route("/Deconnection")
def deconnection():
    if session['email']:
        user =  db.session.execute(db.select(User).order_by(User.id)).scalars()
        return render_template('deconnection.html',vafid=user)
        # user =  db.session.execute(db.select(User).order_by(User.id)).scalars()
        # return render_template("deconnection.html", vafid=user)
    return redirect(url_for('out'))     

@app.route('/logout')
def out():
    session.pop('email',None)
    return render_template("connexion.html")

@app.route("/App_Event",methods=["GET","POST"])
def addevent():
    if request.method == "POST":
        nameE = request.form['nameE']
        type = request.form['type']
        dates = request.form['dates']
        adress = request.form['adress']
        prix = request.form['prix']
        Nb_place = request.form['nbrs']
        # image = request.files['image']

        # events = Events(fileimage=image.fileimage, data=image.read())
        new_event = Events(nameE=nameE,type=type,dates=dates,adress=adress,prix=prix,Nb_place=Nb_place)
        db.session.add(new_event)
        db.session.commit()
        return redirect("/List")        
    return render_template("app_event.html")
        
@app.route("/List")
def list():
    # event =  Events.query.all()
    events =  db.session.execute(db.select(Events).order_by(Events.id)).scalars()
    return render_template("events_admin.html", vafid=events)

@app.route("/List_2")
def list_2():
    # event =  Events.query.all()
    events =  db.session.execute(db.select(User).order_by(User.id)).scalars()
    return render_template("user_admin.html", vafid=events)

@app.route("/")
def index():
    return render_template("Accueil.html")


@app.route("/Evenement")
def even():
    return render_template("evenement.html")

@app.route("/Paiement")
def conta():
    return render_template("paiement.html")

@app.route("/consert&spectacle")
def consec():
    return render_template("con_spec.html")

@app.route("/Sport")
def sport():
    return render_template("sport.html")

@app.route("/Conpherence")
def conpher():
    return render_template("conpherence.html")

@app.route("/Theatre")
def theat():
    return render_template("theatre.html")

@app.route("/Festival")
def festi():
    return render_template("festival.html")

@app.route("/Anime")
def ani():
    return render_template("anime.html")

@app.route("/Reserve")
def reser():
    return render_template("reserve.html")

@app.route("/Panier")
def panie():
    return render_template("panier.html")

@app.route("/Admin")
def admi():
    return render_template("dashboard.html")

@app.route("/Event_admin")
def even_admi():
    return render_template("events_admin.html")

@app.route("/User_admin")
def user_admin():
    return render_template("user_admin.html")

@app.route("/Aid")
def aide():
    return render_template("aide.html")

@app.route("/Profile_admin")
def profile():
    return render_template("profil.html")

# @app.route("/Inscription")
# def instription():
#     return render_template("inscrip.html")

# @app.route("/Connection")
# def connec():
#     return render_template("connexion.html")

# @app.route("/Deconnection")
# def donnec():
#     return render_template("deconnection.html")

# @app.route("/App_Event")
# def addevent():
#     return render_template("Accueil.html")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=9000)