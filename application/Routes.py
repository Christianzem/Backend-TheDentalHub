from application import app 

# Routing using decorators
@app.route("/")
def hello():
    return "<h1>Home Page</h1>"

@app.route("/about")
def about():
    return "<h1>About Page</h1>"