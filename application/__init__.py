from flask import Flask, render_template, request, flash, redirect
from flask_pymongo import PyMongo
from pymongo.errors import PyMongoError
import os
# import datetime
# from Prostheses import DentalProsthesis  # Import the form class
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
# Assignment of secret key inside of my .env
app.secret_key = os.environ.get("SECRET_KEY")

# Connect to MongoDB
mongo_uri = os.getenv("MONGODB_URI") # Assignment of my URI inside of my .env
print(os.getenv("MONGODB_URI"))
try:
    mongo_client = PyMongo(app, uri=mongo_uri)
    if mongo_client.db is None:
        raise ValueError("MongoDB connection failed: Database is None")
except Exception as e:
    print(os.getenv("MONGODB_URI"))
    print(f"Error connecting to MongoDB: {e}")
    # You can also use flash messages to inform the user about the error
    flash("Error connecting to MongoDB. Please try again later.", "error")

# Access the database
db = mongo_client.db

from application import Routes