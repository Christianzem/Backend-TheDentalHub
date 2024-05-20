from flask import Flask, render_template
from flask_pymongo import PyMongo
from Prostheses import DentalProsthesis


app = Flask(__name__) #Flask Instance
app.config['SECRET_KEY'] = '0f5b00205ff5796fcd5e2362b9dbb227ec5c79bb'
app.config['MONGO_URI'] = 'mongodb+srv://chriz24:Elnegro24@cluster0.xs9s6dd.mongodb.net/Dental-Prostheses?retryWrites=true&w=majority&appName=Cluster0'

# Setup mongodb
mongodb_client = PyMongo(app)
db = mongodb_client.db

# Routing using decorators
@app.route("/")
def hello():
    return "<h1>Home Page</h1>"

@app.route("/add_Prosthesis")
def prosthesis():
    form = DentalProsthesis()
    return render_template("prosthesis.html", form=form ) 

# Conditional to set application into debug mode
if __name__ == '__main__':
    app.run(debug=True)