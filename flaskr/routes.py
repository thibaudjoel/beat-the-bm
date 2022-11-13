from app import app
from flask import request

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World!"

@app.route("/<string:name>")
def name_page(name):
    return f"Hi {name}"

@app.route("/login", methods=['POST', 'GET'])
def login():
    name = ""
    if request.method == 'POST':
        name = request.form['name']
    else:
        name = request.args.get('name')
    return f'Hi {name}'

@app.route("/<string:name>")
def page2(name):
    return f"Hi {name}"