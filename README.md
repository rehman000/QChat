# QChat
QChat is a social media application where users can log in, create, update, and delete their posts. They can upload their own profile images, and communicate with one another, to share information, resources, and jobs listings during the COVID-19 pandemic. The information on each post is validated for it's accuracy using a neural network to prevent misinformation regarding COVID-19 from spreading rampant on the platform. 

# The File Structure is as follows:

```
./
├── Dear Judges
├── Password_Reset.jpg
├── QChat
│   ├── app
│   │   ├── blueprint_imports.txt
│   │   ├── config.py
│   │   ├── database.db
│   │   ├── errors
│   │   │   ├── handlers.py
│   │   │   ├── __init__.py
│   │   │   └── __pycache__
│   │   │       ├── handlers.cpython-38.pyc
│   │   │       └── __init__.cpython-38.pyc
│   │   ├── __init__.py
│   │   ├── machine_learning
│   │   │   ├── check.py
│   │   │   ├── covid19_info_validator.h5
│   │   │   ├── covid19.py
│   │   │   ├── data
│   │   │   │   ├── mongo_migrate.py
│   │   │   │   ├── output2.json
│   │   │   │   ├── output.json
│   │   │   │   ├── __pycache__
│   │   │   │   │   └── mongo_migrate.cpython-38.pyc
│   │   │   │   ├── text_data.json
│   │   │   │   ├── who_pdfs.json
│   │   │   │   └── word_decode.json
│   │   │   ├── execute.py
│   │   │   ├── __init__.py
│   │   │   ├── __pycache__
│   │   │   │   ├── check.cpython-38.pyc
│   │   │   │   ├── covid19.cpython-38.pyc
│   │   │   │   ├── execute.cpython-38.pyc
│   │   │   │   ├── __init__.cpython-38.pyc
│   │   │   │   └── train.cpython-38.pyc
│   │   │   ├── train.py
│   │   │   └── word_decode.json
│   │   ├── main
│   │   │   ├── __init__.py
│   │   │   ├── __pycache__
│   │   │   │   ├── __init__.cpython-38.pyc
│   │   │   │   └── routes.cpython-38.pyc
│   │   │   └── routes.py
│   │   ├── models.py
│   │   ├── posts
│   │   │   ├── forms.py
│   │   │   ├── __init__.py
│   │   │   ├── __pycache__
│   │   │   │   ├── forms.cpython-38.pyc
│   │   │   │   ├── __init__.cpython-38.pyc
│   │   │   │   └── routes.cpython-38.pyc
│   │   │   └── routes.py
│   │   ├── __pycache__
│   │   │   ├── config.cpython-38.pyc
│   │   │   ├── __init__.cpython-38.pyc
│   │   │   └── models.cpython-38.pyc
│   │   ├── static
│   │   │   ├── check_0.jpg
│   │   │   ├── check_1.jpg
│   │   │   ├── check_2.jpg
│   │   │   ├── Covid-19.png
│   │   │   ├── GitHub.png
│   │   │   ├── main.css
│   │   │   └── profile_images
│   │   │       ├── 53fa8c80cb8f07d2.jpg
│   │   │       ├── 73933dcf6ece5589.jpg
│   │   │       ├── a41e8879cea4dba5.png
│   │   │       ├── b169d1fe59e8b623.png
│   │   │       ├── b57c997a27cb7a5e.png
│   │   │       ├── b5914111d8098e7b.jpg
│   │   │       ├── b82418344831a769.jpg
│   │   │       ├── default.jpg
│   │   │       ├── e7abcd9c7d0f3682.jpg
│   │   │       ├── ed281b648c3e8981.jpg
│   │   │       └── edb7154b333427af.jpg
│   │   ├── templates
│   │   │   ├── about.html
│   │   │   ├── account.html
│   │   │   ├── create_post.html
│   │   │   ├── errors
│   │   │   │   ├── 403.html
│   │   │   │   ├── 404.html
│   │   │   │   └── 500.html
│   │   │   ├── home.html
│   │   │   ├── login.html
│   │   │   ├── post.html
│   │   │   ├── register.html
│   │   │   ├── reset_request.html
│   │   │   ├── reset_token.html
│   │   │   ├── template.html
│   │   │   └── user_posts.html
│   │   ├── users
│   │   │   ├── forms.py
│   │   │   ├── __init__.py
│   │   │   ├── __pycache__
│   │   │   │   ├── forms.cpython-38.pyc
│   │   │   │   ├── __init__.cpython-38.pyc
│   │   │   │   ├── routes.cpython-38.pyc
│   │   │   │   └── utils.cpython-38.pyc
│   │   │   ├── routes.py
│   │   │   └── utils.py
│   │   └── web_scrape
│   │       ├── __init__.py
│   │       ├── Misinformation.json
│   │       ├── __pycache__
│   │       │   └── scrap_pdf.cpython-38.pyc
│   │       ├── report.json
│   │       ├── scrap2.py
│   │       ├── scrap3.py
│   │       ├── scrap_pdf.py
│   │       └── scrap.py
│   ├── requirements.txt
│   └── run.py
└── README.md
```

# To execute our app, 
- you will need python3.6 or greater, mongodb and pip.

To run the app:

1. Navigate to the following directory:  QChat/QChat
2. type the following: 
    
# To install all dependencies:
        
    pip install -r requirements.txt

# Enviornmental Variables: 
These are the following enviornmental path variables:

        export SECRET_KEY="mysecretkey"
        export SQLALCHEMY_DATABASE_URI="sqlite:///database.db"
        export MONGO_URI="mongodb://localhost:27017/myDatabase"
        export MAIL_USERNAME="<an email adress>"
        export MAIL_PASSWORD="<a password for that email address>"

#### Information about the environment variables
* SQLALCHEMY_DATABASE_URI represents the url to an SQL database
* MONGO_URI represents the url to a mongodb database
* SECRET_KEY represents your secret key
* MAIL_USERNAME represents an email address
* MAIL_PASSWORD represents an email password


An important note, in order for the password reset functionality to properly work. 
You need to provide a valid Gmail username, and password, BUT also enable this:

https://myaccount.google.com/lesssecureapps

Or else it will not work. Google by default disables this feature, since most people are not developers.
This is mostly to allow developers to debug their applications, before deploying it to any cloud service.

# The following command: 
will send the training data to your mongodb database
    
    python run.py ml data json_mongo 

# To create a neural network: 
this command will create a neural network using mongodb data:
    
    python run.py ml train covid19 mongo 

# To start the application: 
In the QChat Directory run the following command:

    python run.py 

# The Web Server is starting on port 5000:
On your browser navigate to:

    http://localhost:5000/
