from flask import Flask, url_for, request, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/<string:name>")
def page2(name):
    return f"Hi {name}"

@app.route("/login", methods=['POST', 'GET'])
def login():
    name = ""
    if request.method == 'POST':
        name = request.form['name']
    else:
        name = request.args.get('name')
    return f'Hi {name}'

if __name__ == '__main__':
    app.run(port=1617, debug=True)
