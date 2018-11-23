# is for Create entries INTO the TABLES

from models import db,Puppy,Toy,Owner

# Creating 2 puppies

patu = Puppy('Patu')
fido = Puppy('Fido')

# Add database to DATABASE
db.session.add_all([patu,fido])
db.session.commit()

#check!
print(Puppy.query.all())

patu = Puppy.query.filter_by(name='Patu').first()

# Create Owner Object
hamada = Owner('hamada',patu.id)
# Give patu some toys
toy1 = Toy('bones',patu.id)
toy2 = Toy('Ball',patu.id)
db.session.add_all([hamada,toy1,toy2])
db.session.commit()

#Grab patu after those additions

patu = Puppy.query.filter_by(name='Patu').first()
print(patu)
print(patu.report_toys())

