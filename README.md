# QChat
A social media application that provides verified information regarding the Corona Virus, COVID-19.

To execute our app, you need python and pip.
To run the app:

1. move to QChat/QChat/
2. type the following: 

`   # installs all dependencies
    pip install -r requirements.txt
    
    export SECRET_KEY="TODDKING"
    export SQLALCHEMY_DATABASE_URI="sqlite:///database.db"
    export MONGO_URI="mongodb://localhost:27017/myDatabase"
    export MAIL_USERNAME="<an email adress>"
    export MAIL_PASSWORD="<a password for that email address"
    
    # this will create a neural network using local static json data
    python run.py ml train covid19 json 
    
    # executes the web server on port 5000
    python run.py 
