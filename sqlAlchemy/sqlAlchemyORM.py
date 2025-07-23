from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, func
import pandas as pd
from sqlalchemy.orm import declarative_base, sessionmaker, relationship #declarative_base replaces metadata from Core, and sessionmaker cause ORM uses sessions, not connections

#orm maps python classes to database
engine = create_engine('postgresql+psycopg2://postgres:4641@localhost:5432/satutorialdatabase', echo = True) #postgres version
    #can read more about this in sqlAlchemyCore

Base = declarative_base() #this lets you map your databases in here to real databases

class Person(Base):
    __tablename__ = 'people' #name of database
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer)

    things = relationship('Thing',back_populates='person') #defines a relationship between person/thing

class Thing(Base):
    __tablename__ = 'things' #name of database
    id = Column(Integer, primary_key=True)
    description = Column(String, nullable=False)
    price = Column(Float)
    owner = Column(Integer, ForeignKey("people.id")) 

    person = relationship('Person', back_populates="things")

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

#creating a new person and thing mapped to a person
'''
newPerson = Person(name = 'Charlie', age = '70')
session.add(newPerson)
session.flush()

newThing = Thing(description = 'lamp', price = '500', owner = newPerson.id) #much better practice to not manually put ids
session.add(newThing)
session.commit()

#super convenient way to get things from the database using python, advantage of ORM 
print([i.description for i in newPerson.things]) #put it in a list - some generator object bs that i forgot from cse20 lol!
print(newThing.person.name)
'''
#select
result = session.query(Person.name, Person.age).filter(Person.age>50).all() #.all() = all results that you get
#if you were to put .query(Person), you would get a list of Person objects with attributes
#print(result)

#delete
'''
result = session.query(Person.name, Person.age).filter(Person.age>50).delete()
session.commit()
'''

#update 
'''
result = session.query(Person).filter(Person.name == 'Charlie').update({'name':'Charles'}) #you have to put person cause you're updating the object
session.commit()
result = session.query(Person.name, Person.age).filter(Person.name == 'Charles').all() 
print(result)
'''

#join
result = session.query(Person.name, Thing.description).join(Person).all() #fun fact: in this query person and thing are interchangeable
#print(result)

result = session.query(Thing.owner, func.sum(Thing.price)).group_by(Thing.owner).having(func.sum(Thing.price) > 50).all() #fun fact: in this query person and thing are interchangeable
#print(result)

#pandas incorporation
df = pd.read_sql("Select * from people", con = engine)
print(df)
#can also inser pandas dataframes into the database, but i didn't write that here - look at the vid if want
session.close()