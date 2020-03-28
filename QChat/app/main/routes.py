from flask import render_template, request, Blueprint
from app.models import Post


main = Blueprint('main', __name__)

'''
posts = [
    {
        'author': 'Rehman Arshad',
        'title': 'Blog Post 1',
        'content': 'Hello World!',
        'date_posted': 'April 20, 2020'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'This is Sparta!',
        'date_posted': 'April 21, 2020'
    }
]

'''

# This is just dummy data I can test out without having to 
# use sqlite, and then lose my hair debuging issues! 
# I honestly never even realized I should have done this when starting most of my projects! 


@main.route('/')
@main.route('/home')
def home():                                                                                                         # Testing Complete. I no longer need to use dummy data! Horray!!! :D 
    page = request.args.get('page', 1, type=int)                                                                    # We request a page, the default page is 1, of type int
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)                            # Instead of using query.all(), I've changed this to query.paginate() ... 
                                                                                                                    # By using .query.order_by(Post.date_posted.desc())  I am able to show posts in a descending order of creation.
                                                                                                                    # Translation: The newer posts will be seen on the top, while the older posts will sink to the bottom and eventually to other paginated pages! 
    return render_template('home.html', posts=posts)                                                                



@main.route('/about')
def about():
    return render_template('about.html', title='About us')

