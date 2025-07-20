from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, ForeignKey, func

#engine = create_engine('sqlite:///mydatabase.db', echo = True) #sqllite version
engine = create_engine('postgresql+psycopg2://postgres:4641@localhost:5432/satutorialdatabase', echo = True) #postgres version
#syntax of above line: postgresql + psycopg2 (something i installed to make this work)://<username>:<password>@localhost:<port>/<namefordatabase>
#before running said line, you need to createdb satutorialdatabase
meta = MetaData()

people = Table( #creates table in database called people
    "people",
    meta,
    Column('id', Integer, primary_key=True),
    Column('name', String, nullable=False), #makes it a required field
    Column('age', Integer) 
)

things = Table( #creates table in database called people
    "things",
    meta,
    Column('id', Integer, primary_key=True),
    Column('description', String, nullable=False), 
    Column('price', Float),
    Column('owner', Integer, ForeignKey("people.id")) #creates a one to many relationship - each item is mapped to a person
)
meta.create_all(engine)

conn = engine.connect()

#inserting data - commented out because you dont always want to insert when running this code
'''
insert_statement = people.insert().values(name ='Mike',age=30)
result = conn.execute(insert_statement)
conn.commit() 

insert_statement = people.insert().values(name ='Jane',age=32)
result = conn.execute(insert_statement)
conn.commit()

insert_people = people.insert().values([
    {'name' : "Josh", 'age':35},
    {'name' : "Mary", 'age':70},
    {'name' : "Benedict", 'age':65},
    {'name' : "Thomas", 'age':22},
    {'name' : "Jones", 'age':18}
    ])
insert_things = things.insert().values([
    {'description' : "table", 'price':35.0, 'owner':3}, #bad practice to pick owner ids manually
    {'description' : "tv", 'price':100.0, 'owner':4},
    {'description' : "laptop", 'price':1500.50, 'owner':4},
    {'description' : "pen", 'price':1.0, 'owner':5},
    {'description' : "water bottle", 'price':10.0, 'owner':6},
    {'description' : "tissues", 'price':5.0, 'owner':7}
    ])

conn.execute(insert_people)
conn.commit() #have to commit before executing things because those 'people' ids need to exist in the database before mapping 'things' to them
conn.execute(insert_things)
conn.commit()
'''

#selecting data
select_statement = people.select().where(people.c.age> 30)
result = conn.execute(select_statement)

#for row in result.fetchall():
#    print(row)

#updating data - commenting out because of commit, same as inserting
'''
update_statement = people.update().where(people.c.id == 2).values(name = 'James', age = 52)
result = conn.execute(update_statement)
conn.commit()
'''

#delete statement
'''
delete_statement = people.delete().where(people.c.id == 2)
result = conn.execute(delete_statement)
conn.commit()
'''

#join statement
join_statement = people.join(things, people.c.id == things.c.owner) #inner join - people who dont own something aren't included
#join_statement = people.outerjoin(things, people.c.id == things.c.owner) #outer join - everyone included, even if they don't own something
select_statement = people.select().with_only_columns(people.c.name, things.c.description).select_from(join_statement) #include name, description
result = conn.execute(select_statement)
for row in result.fetchall():
    print(row)


#group statement
group_by_statement = things.select().with_only_columns(things.c.owner, func.sum(things.c.price)).group_by(things.c.owner).having(func.sum(things.c.price) > 25) 
    #when you group, you have to decide what you are doing with the values
    #for example, if people own multiple items, and they only get one row, what are you gonna do with all their sums
        #this example code sums up all their sums, only displaying if that sum is > 35
result = conn.execute(group_by_statement)
for row in result.fetchall():
    print(row)