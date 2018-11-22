import os
from flask import Flask
from flask_sqlachemy import SQLAlchemy
from flask_migrate import Migrate

# setup of sqlite database
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app,db)

#create a couple of classes or models

class Puppy(db.Model):
    __tablename__ = 'puppies'
    
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.Text)
    #one to many relationships(one puppy could have many toys)
    #so we have 3 parameters: Toy(is just connecting it to the other model, toys is a relationships with 
    # the toy model), backref is going to add a back reference in the other model in the relationship
    # so it's going to add a reference to the toy model to remember that's also related to Puppy through
    #this relationship column
    toys = db.relationship('Toy',backref='puppy',lazy=dynamic)
    # one to one : one Puppy to one owner
    owner = db.relationship('Owner',backref='puppy',uselist=False)
    def __init__(self, name):
        self.name= name
    
    def __repr__(self):
        if self.owner:
            return f"Puppy name is {self.name} and owner is {self.owner.name}"
        else:
            f"Puppy name is {self.name} and has no owner yet!"
    #let add one more method to this class in order to report back the number of toy that the puppy has
    def report_toys(self):
        print("Here are my toys!")
        for toy in self.toys:
            print(toy.item_name)

class Toy(db.Model):
    
    