This file is intended to document my journey as I build this over the summer.
Hopefully I update this every day from learning something new.
Note - This is the up to date journal, not the ones in the branches.

1. 7/12
    a. Watched 1hr git breakdown, created repo with initial readme commits
2. 7/13
    a. Created the venv
    b. updated the readme with actual project guidelines
    c. Created this journal :)
    d. Had a lot of problems with the venv and fastapi
    e. restarted the venv and installed fastapi
    f. ran a fastapi test on a branch - it worked
    g. more fastapi learning tomorrow
3. 7/14
    a. Finished the fastapi tutorial. Key concepts:
        aa. Basic API function ('Hello World')
        ab. Main types of requests - GET, POST, PUT, DELETE
        ac. Pydantic Schemes and Data Validation
        ad. Wrote everything reflecting a list of dictionaries, need to learn PostgreSQL for database
        ae. HTTP Exceptions and /docs 
4. 7/15  
    a. Started Postgres - installed Postico2 as my editor, using pgadmin4 to control databases  
    b. tutorial finished by tomorrow, but its all in Postico so nothing new in this repository  
5. 7/16  
    a. Finished PostgreSQL tutorial on Postico
        aa. basic tables, entities, keywords  
        ab. Create, Read, Update, Delete (CRUD) functions  
        ac. Relational tables  
    b. Knowing this, I can start thinking through some basic database design for my project  
        ba. Table of users with table of recipes, a user can have many recipes (one-to-many)  
    c. SQLAlchemy starts tomorrow, goal is to finish by Saturday and start endpoints over the weekend
6. 7/17
    a. Started SQLAlchemy tutorial
    b. Found out along the way that i needed a PostgreSQL adapter for python to use SQLAlchemy Core
    c. Installed psycopg2 off a video recommendation, was a nightmare to install
    d. Finally connected to the database(createdb database) and created a table in there from python, pretty cool
    e. SQL Alchemy tutorial done tomorrow hopefully, trying to finish both Core and ORM and decide which is best for the project
7. 7/19
    a. Took the day off yesterday - leetcode
    b. Finished SQL Alchemy core/ORM tutorial
    c. gonna be using the ORM when i create my api, seems much more intuitive to use
    d. Only goal tomorrow is to start creating and testing endpoints, but it might be more difficult then i think
    e. Im giving myself all of next week to finish the CRUD
    