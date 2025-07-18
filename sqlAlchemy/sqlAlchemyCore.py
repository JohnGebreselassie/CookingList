from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String

#engine = create_engine('sqlite:///mydatabase.db', echo = True) #sqllite version
engine = create_engine('postgresql+psycopg2://postgres:4641@localhost:5432/satutorialdatabase', echo = True) #postgres version
#syntax of above line: postgresql + psycopg2 (something i installed to make this work)://<username>:<password>@localhost:<port>/<namefordatabase>
#before running said line, you need to createdb satutorialdatabase
meta = MetaData()

people = Table( #creates table in database called people
    "people",
    meta,
    Column('id', Integer, primary_key=True),
    Column('name', String, nullable=False)
)

meta.create_all(engine)