from web import app

if __name__ == "__main__":
    app.run(debug=True)

# run.py > __init__.py > routes.py > models.py > forms.py

### DB COMMAND LINE##
# python
# db.create.all() --> to create model from models.py
#>>> from web import db (web is folder name)
#>>>from web import db
#>>> from web.models import User 
#>>> user = User.query.first()
#>>> user
#User('admin', 'admin@localhost.loc', 'default.jpg')
#>>> user.password
#'$2b$12$M2Xph7EqnxIPMGZavqoaSuPKirpnXOLUyNV8xbiqC1Wun4w1vwGgO'

#SQL-ALCHEMY
# db.create.all()
# from <folder_name> import <tables> // eq : from webflask import User, Post
# <var_name> = <tables_name>(<key> : <value>, <key2> : value2) // eq: User_1 = User(username:'faizal', email='faizal@kusmawan.com')
# db.session.add(<var_name>) //  eq: db.session.add(User_1)
# if you want add next item to tables repeat var_name and db.session.add() process
# db.session.commit() --> to commit data change(s)
# User.query.all() --> to query all data
# User.query.first() --> to query fist row of data
# User.query.filter_by(<key>=<value>) // eq : User.query.filter_by(Username='faizal')


### package install ###
# pip install Flask
# pip install wtform
# pip install flask-wtf
# pip install email_validator
# pip install flask-sqlalchemy
# pip install flask_bcrypt


### bcrypt ##
# bcrypt.generate_password_hash('stringvalue')
# bcrypt.generate_password_hash('stringvalue').decode('utf-8')
# hashed_pw = bcrypt.generate_password_hash('stringvaldue').decode('utf-8')
# bcrypt.check_password_hash(hashed_pw, 'stringvalue')