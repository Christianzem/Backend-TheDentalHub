# from flask import Flask, render_template, request, flash, redirect
# from flask_pymongo import PyMongo
# from pymongo.errors import PyMongoError
# import os
# import datetime
# from Prostheses import DentalProsthesis  # Import the form class
# from dotenv import load_dotenv

# load_dotenv()

# app = Flask(__name__)
# # Assignment of secret key inside of my .env
# app.secret_key = os.environ.get("SECRET_KEY")

# # Connect to MongoDB
# mongo_uri = os.getenv("MONGODB_URI") # Assignment of my URI inside of my .env
# print(os.getenv("MONGODB_URI"))
# try:
#     mongo_client = PyMongo(app, uri=mongo_uri)
#     if mongo_client.db is None:
#         raise ValueError("MongoDB connection failed: Database is None")
# except Exception as e:
#     print(os.getenv("MONGODB_URI"))
#     print(f"Error connecting to MongoDB: {e}")
#     # You can also use flash messages to inform the user about the error
#     flash("Error connecting to MongoDB. Please try again later.", "error")

# # Access the database
# db = mongo_client.db

# Routing using decorators
# @app.route("/details")
# def patientDetails():
#     prosthesis_cursor = db.Prostheses.find()
#     prosthesis_list = list(prosthesis_cursor)
#     return render_template("views.html", prostheses=prosthesis_list)

# @app.route("/add_Prosthesis", methods=["POST", "GET"])
# def prosthesis():
#     if request.method == "POST":
#         form = DentalProsthesis(request.form)

#         prosthesis_type = form.prosthesis_type.data
#         checkbox = form.checkbox.data
#         # selected_date_str = form.selected_date.data.strip()  # Remove leading and trailing whitespace
#         # selected_date = datetime.strptime(selected_date_str, "%Y-%m-%d").date()
#         selected_date = form.selected_date.data
#         # Convert selected_date to a datetime.datetime object with midnight time
#         selected_datetime = datetime.datetime.combine(selected_date, datetime.time.min)

#         print(selected_date)

#         db.Prostheses.insert_one({
#             "name": prosthesis_type,
#             "list": checkbox,
#             "selected_date": selected_datetime
#             })
        
#         print(selected_date)
#         flash("Dental Prosthesis Added", "success")
#         return redirect("/details")

#     else:
#         form = DentalProsthesis()
#     return render_template("prosthesis.html", form=form)

# # Conditional to set application into debug mode
# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=8000, debug=True)
