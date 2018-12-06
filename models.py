import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
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
    """ define the name of the table in the database the remaining class variables are the attribute
    of the model, defined as instances of the db.Column class"""
    id = db.Column(db.Integer,primary_key=True) #the first argument given to the db.Column constructor 
    # is the type of the database column and the model attribute, the remaining arguments specify 
    #configuration for each attribute(pimary_key, unique, index, nullable, default)
    
    name = db.Column(db.Text)
    
    # one to many relationships(one puppy could have many toys)
    toys = db.relationship('Toy',backref='puppy',lazy='dynamic')
    """The toys attribute added to model Puppy represents the object oriented view of the relationship
    Given an instance of class Puppy,the toys attribute will return the list of toys associated with
    that puppies,so the first argument <Toy> indicates what model is on the other side of the relation
    ship. the backref argument define the reverse direction of the relationship by adding a puppy_id
    attribute to the Toy model, """
    
    # one to one : one Puppy to one owner
    owner = db.relationship('Owner',backref='puppy',uselist=False)
    
    def __init__(self, name):
        self.name= name
    # it's not strictly necessry, the two models include a __repr__() method to give them a readable
    #string representation that can be used for debugging and testing purpose 
    
    def __repr__(self):
        if self.owner:
            return "Puppy name is %s and owner is %s" %(self.name,self.owner.name)
            #return f"Puppy name is {self.name} and owner is {self.owner.name}"
        else:
            return "Puppy name is %s and has no owner yet!" % self.name
    
    #let add one more method to this class in order to report back the number of toys that the puppy has
    def report_toys(self):
        print("Here are my toys!")
        for toy in self.toys:
            print(toy.item_name) # item_name will be an attribute that will create inside Toy model

class Toy(db.Model):
    
    __tablename__ = 'toys'
    
    id = db.Column(db.Integer,primary_key=True)
    item_name = db.Column(db.Text)
    puppy_id = db.Column(db.Integer,db.ForeignKey('puppies.id'))
    #the puppy_id column added to the Toy model is defined as a foreign key,and that establish
    #the relationship, the puppies.id arguments pecifies that the column should be interpreted as having
    #id values from rows in the puppies table
    
    def __init__(self,item_name,puppy_id):
        self.item_name = item_name
        self.puppy_id = puppy_id
    
class Owner(db.Model):
    __tablename__ = 'owner'
    
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.Text)
    puppy_id = db.Column(db.Integer,db.ForeignKey('puppies.id')) # now we have the owner connected to
    # the column puppies.id in table puppies
    
    def __init__(self,name,puppy_id):
        self.name = name
        self.puppy_id = puppy_id

# so we're going to connect all of this together and perform a migrations as well as create some
# puppies some toys and some owners and see how that all plays out.
    
    