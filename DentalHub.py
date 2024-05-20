from flask import Flask
app = Flask(__name__)


# Routing using decorators
@app.route("/")
def hello():
    return "<h1>Home Page</h1>"

@app.route("/about")
def about():
    return "<h1>About Page</h1>"



# Conditional to set application into debug mode
if __name__ == '__main__':
    app.run(debug=True)