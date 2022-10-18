# client server
# framework
# flask
# request-response

# client -> computer that is listens to server response & sends requests to server.(web browser)
# server -> processes client request then sends respond to the client. (flask app)
# framework -> make development easy by utilizing the reusable code...flask, django


from flask import *

# start
app = Flask(__name__)


# decorators(@)
# flask routing
# method -> route()
# to  bind the method route to your app object, then we use decorator @

@app.route('/home')
def home_page():
    return "Hello welcome to flask"


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/register')
def sign_up():
    return render_template('register.html')


@app.route('/')
def index():
    return "view the index page"


@app.route('/add')
def add():
    fruits = ['orange', 'pineapple', 'apple']
    return fruits


# css, js, images, bootstrap on flask
# static folder


app.run(debug=True)
# end
