#----------------------------------------------------SQL CORE-----------------------------------------------------------------
from sqlalchemy import create_engine, text

engine = create_engine('sqlite:///mydatabase.db', echo = True) #sqlite code is run in files, completely different for postgres, the file "mydatabase.db" comes from this code

conn = engine.connect()

conn.execute(text("CREATE TABLE IF NOT EXISTS people (name str, age int)")) #pure sql lines, not typical - basic test

conn.commit()

#----------------------------------------------------SQL ORM-----------------------------------------------------------------

from sqlalchemy.orm import Session

session = Session(engine)

session.execute(text('INSERT INTO people (name, age) VALUES ("Mike", 30);'))

session.commit()