# QChat
QChat is a social media application where users can log in, create, update, and delete their posts. They can upload their own profile images, and communicate with one another, to share information, resources, and jobs listings during the COVID-19 pandemic. The information on each post is validated for it's accuracy using a neural network to prevent misinformation regarding COVID-19 from spreading rampant on the platform. 

# The File Structure is as follows:

```
./
├── app
│   ├── blueprint_imports.txt
│   ├── config.py
│   ├── database.db
│   ├── errors
│   │   ├── handlers.py
│   │   ├── __init__.py
│   │   └── __pycache__
│   │       ├── handlers.cpython-38.pyc
│   │       └── __init__.cpython-38.pyc
│   ├── __init__.py
│   ├── machine_learning
│   │   ├── check.py
│   │   ├── covid19_info_validator.h5
│   │   ├── covid19.py
│   │   ├── data
│   │   │   ├── output.json
│   │   │   ├── training_data_O.json
│   │   │   └── who_pdfs.json
│   │   ├── dummy_text_data.json
│   │   ├── dummy_word_decode.json
│   │   ├── execute.py
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   │   ├── check.cpython-38.pyc
│   │   │   ├── covid19.cpython-38.pyc
│   │   │   ├── execute.cpython-38.pyc
│   │   │   ├── __init__.cpython-38.pyc
│   │   │   └── train.cpython-38.pyc
│   │   └── train.py
│   ├── main
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   │   ├── __init__.cpython-38.pyc
│   │   │   └── routes.cpython-38.pyc
│   │   └── routes.py
│   ├── models.py
│   ├── posts
│   │   ├── forms.py
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   │   ├── forms.cpython-38.pyc
│   │   │   ├── __init__.cpython-38.pyc
│   │   │   └── routes.cpython-38.pyc
│   │   └── routes.py
│   ├── __pycache__
│   │   ├── config.cpython-38.pyc
│   │   ├── __init__.cpython-38.pyc
│   │   └── models.cpython-38.pyc
│   ├── static
│   │   ├── check_0.jpg
│   │   ├── check_1.jpg
│   │   ├── check_2.jpg
│   │   ├── Covid-19.png
│   │   ├── main.css
│   │   └── profile_images
│   │       ├── 53fa8c80cb8f07d2.jpg
│   │       ├── 73933dcf6ece5589.jpg
│   │       ├── a41e8879cea4dba5.png
│   │       ├── b169d1fe59e8b623.png
│   │       ├── b57c997a27cb7a5e.png
│   │       ├── b5914111d8098e7b.jpg
│   │       ├── b82418344831a769.jpg
│   │       ├── default.jpg
│   │       ├── e7abcd9c7d0f3682.jpg
│   │       ├── ed281b648c3e8981.jpg
│   │       └── edb7154b333427af.jpg
│   ├── templates
│   │   ├── about.html
│   │   ├── account.html
│   │   ├── create_post.html
│   │   ├── errors
│   │   │   ├── 403.html
│   │   │   ├── 404.html
│   │   │   └── 500.html
│   │   ├── home.html
│   │   ├── login.html
│   │   ├── post.html
│   │   ├── register.html
│   │   ├── reset_request.html
│   │   ├── reset_token.html
│   │   ├── template.html
│   │   └── user_posts.html
│   ├── users
│   │   ├── forms.py
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   │   ├── forms.cpython-38.pyc
│   │   │   ├── __init__.cpython-38.pyc
│   │   │   ├── routes.cpython-38.pyc
│   │   │   └── utils.cpython-38.pyc
│   │   ├── routes.py
│   │   └── utils.py
│   └── web_scrape
│       ├── __init__.py
│       ├── Misinformation.json
│       ├── report.json
│       ├── scrap2.py
│       ├── scrap3.py
│       ├── scrap_pdf.py
│       └── scrap.py
├── README.md
├── requirements.txt.
└── run.py
```

# To execute our app, you will need python3.6 or greater and pip.
To run the app:

1. Navigate to the following directory:  QChat/
2. type the following: 
    
# To install all dependencies:
        
    pip install -r requirements.txt

# Enviornmental Variables: 
These are the following enviornmental path variables you will need to set up.
In QChat/app/config.py

        export SECRET_KEY="TODDKING"
        export SQLALCHEMY_DATABASE_URI="sqlite:///database.db"
        export MONGO_URI="mongodb://localhost:27017/myDatabase"
        export MAIL_USERNAME="<an email adress>"
        export MAIL_PASSWORD="<a password for that email address"

        # this will create a neural network using local static json data
        python run.py ml train covid19 json 

        # executes the web server on port 5000
        python run.py 
