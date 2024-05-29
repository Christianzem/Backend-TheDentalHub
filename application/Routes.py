from application import app
from application import db
from application import bcrypt
from flask import render_template, request, redirect, flash, url_for, session, jsonify
import datetime
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import  jwt_required, create_access_token, get_jwt_identity
from .Prostheses import DentalProsthesis 
from .User import RegisterForm, LoginForm
from .Patient import PatientForm
from bson import ObjectId


# Routing ----- User -----
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    email = request.json.get('email')
    password = request.json.get('password')

    # Hash the password before storing it
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    # Check if the user already exists
    if db.users.find_one({'email': email}):
        return jsonify({'message': 'User already exists'}), 400

    # Insert the new user into the database
    db.users.insert_one({'email': email, 'password': hashed_password})

    return jsonify({'message': 'User created successfully'}), 201

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    email = request.json.get('email')
    password = request.json.get('password')

    # Check if the user exists in the database
    user = db.users.find_one({'email': email})
    if not user or not bcrypt.check_password_hash(user['password'], password):
        return jsonify({'message': 'Invalid email or password'}), 401

    # Generate JWT token for the authenticated user
    access_token = create_access_token(identity=email)

    return jsonify({'access_token': access_token}), 200

# Routing using decorators ----- Prosthesis -----
@app.route("/prosthesis")
def patientDetails():
    prosthesis_cursor = db.Prostheses.find()
    # prosthesis_list = list(prosthesis_cursor)
        # Convert ObjectId objects to strings
    prosthesis_list = [
        {
            '_id': str(prosthesis.get('_id')),
            'name': prosthesis.get('name'),
            'lab': prosthesis.get('lab'),
            'arrival': prosthesis.get('arrival'),
            'resent': prosthesis.get('resent'),
            'delivered': prosthesis.get('delivered'),
            'selected_date1': prosthesis.get('selected_date1'),
            'selected_date2': prosthesis.get('selected_date2'),
            'selected_date3': prosthesis.get('selected_date3'),
            'selected_date4': prosthesis.get('selected_date4')
        }
        for prosthesis in prosthesis_cursor
    ]
    return jsonify(prostheses=prosthesis_list)

# @app.route("/patients/<patient_id>/prostheses", methods=["GET"])
# def get_patient_prostheses(patient_id):
#     # Check if the patient exists
#     patient = db.Patient.find_one({"_id": ObjectId(patient_id)})
#     if patient:
#         # Retrieve all prosthesis associated with the patient's ObjectId
#         prostheses = list(db.Prostheses.find({"patient_id": patient_id}))
#         # Convert ObjectId to string for JSON serialization
#         for prosthesis in prostheses:
#             prosthesis["_id"] = str(prosthesis["_id"])
#         return jsonify(status="success", prostheses=prostheses)
#     else:
#         return jsonify(status="error", message="Patient not found"), 404

@app.route("/prosthesis/<id>")
def get_prosthesis(id):
    prosthesis = db.Prosthesis.find_one({"_id": ObjectId(id)})
    if prosthesis:
        prosthesis_data = {
            '_id': str(prosthesis.get('_id')),
            'name': prosthesis.get('name'),
            'lab': prosthesis.get('lab'),
            'arrival': prosthesis.get('arrival'),
            'resent': prosthesis.get('resent'),
            'delivered': prosthesis.get('delivered'),
            'selected_date1': prosthesis.get('selected_date1'),
            'selected_date2': prosthesis.get('selected_date2'),
            'selected_date3': prosthesis.get('selected_date3'),
            'selected_date4': prosthesis.get('selected_date4')
        }
        return jsonify(prosthesis=prosthesis_data)
    else:
        return jsonify(error="Prosthesis not found"), 404

@app.route("/add_Prosthesis", methods=["POST"])
def prosthesis():
        data = request.json  # Access JSON data sent from frontend
        if data:

            prosthesis_type = data.get('prosthesis_type')
            checkbox1 = data.get('checkbox1', False)  # Default value if checkbox1 is not present
            checkbox2 = data.get('checkbox2', False)
            checkbox3 = data.get('checkbox3', False)
            checkbox4 = data.get('checkbox4', False)

            selected_date1 = data.get('selected_date1')
            selected_date2 = data.get('selected_date2')
            selected_date3 = data.get('selected_date3')
            selected_date4 = data.get('selected_date4')

            # Perform necessary conversions and validations here

            # Insert data into MongoDB
            db.Prostheses.insert_one({
                "name": prosthesis_type,
                "lab": checkbox1,
                "arrival": checkbox2,
                "resent": checkbox3,
                "delivered": checkbox4,
                "selected_date1": selected_date1,
                "selected_date2": selected_date2,
                "selected_date3": selected_date3,
                "selected_date4": selected_date4
            })
        
            return jsonify(status="success", message="Dental Prosthesis Added successfully")
        else:
            return jsonify(status="error", message="No data received"), 400 #Bad Request


@app.route("/delete_Prosthesis/<id>", methods = ["DELETE"])
def delete_Prosthesis(id):
    db.Prostheses.find_one_and_delete({"_id": ObjectId(id)})
    return jsonify(status="success", message="Dental Prosthesis Deleted successfully")

@app.route("/update_Prosthesis/<id>", methods=["POST", "GET", "PUT"])
def update_Prosthesis(id):
        data = request.json  # Access JSON data sent from frontend
        if data:

            prosthesis_type = data.get('prosthesis_type')
            checkbox1 = data.get('checkbox1', False)  # Default value if checkbox1 is not present
            checkbox2 = data.get('checkbox2', False)
            checkbox3 = data.get('checkbox3', False)
            checkbox4 = data.get('checkbox4', False)

            selected_date1 = data.get('selected_date1')
            selected_date2 = data.get('selected_date2')
            selected_date3 = data.get('selected_date3')
            selected_date4 = data.get('selected_date4')

            db.Prostheses.find_one_and_update({"_id": ObjectId(id)}, {"$set": {
                "name": prosthesis_type,
                "lab": checkbox1,
                "arrival": checkbox2,
                "resent": checkbox3,
                "delivered": checkbox4,
                "selected_date1": selected_date1,
                "selected_date2": selected_date2,
                "selected_date3": selected_date3,
                "selected_date4": selected_date4
            }})

            return jsonify(status="success", message="Dental Prosthesis Added successfully")
        else:
            return jsonify(status="error", message="No data received"), 400 #Bad Request
 
# Routing ---- Patient -----

@app.route("/patients")
def patients():
    # provider_id = session.get('user_id')  # Example: Get provider ID from session
    patient_cursor = db.Patient.find()
    patient_list = [
        {
            '_id': str(patient.get('_id')),
            'first_name': patient.get('first_name'),
            'last_name': patient.get('last_name'),
            'birth_date': patient.get('birth_date'),
            'patient_number': patient.get('patient_number'),
            'provider_id': patient.get('provider_id'), 
        }
        for patient in patient_cursor
    ]
    return jsonify(patient=patient_list)


@app.route("/patients/<id>")
def get_patient(id):
    patient = db.Patient.find_one({"_id": ObjectId(id)})
    print(patient)
    if patient:
        patient_data = {
            '_id': str(patient.get('_id')),
            'first_name': patient.get('first_name'),
            'last_name': patient.get('last_name'),
            'birth_date': patient.get('birth_date'),
            'patient_number': patient.get('patient_number'),
        }
        return jsonify(patient=patient_data)
    else:
        return jsonify(error="Patient not found"), 404
    


@app.route("/add_patient", methods=["POST"])
def add_patient():
    data = request.json  # Get JSON data from the request body
    if data:  # Check if data is received
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        birth_date = data.get('birth_date')
        patient_number = data.get('patient_number')
        provider_id = data.get("provider_id") 

        db.Patient.insert_one({
            "first_name": first_name,
            "last_name": last_name,
            "birth_date": birth_date,
            "patient_number": patient_number,
            "provider_id": provider_id  # Assign the ID of the selected provider
        })

        return jsonify(status="success", message="Dental Patient Added successfully")
    else:
        return jsonify(status="error", message="No data received"), 400  # Bad Request
    
# @app.route("/add_patient", methods=["POST", "GET"])
# def patient():
#     if request.method == "POST":
#         form = PatientForm(request.form)

#         first_name = form.first_name.data
#         last_name = form.last_name.data
#         birth_date = form.birth_date.data
#         if birth_date:
#             date_birth = datetime.datetime.combine(birth_date, datetime.time.min)
#         else:
#             date_birth = None
#         patient_number = form.patient_number.data

#         db.Patient.insert_one({
#             "first_name" : first_name,
#             "last_name": last_name,
#             "birth_date": date_birth,
#             "patient_number": patient_number
#         })

#         flash("Dental Patient Added", "Success")
#         return jsonify(status="success", message="Dental Patient Added successfully")
    
@app.route("/delete_patient/<id>", methods=["DELETE"])
def delete_patient(id):
    db.Patient.find_one_and_delete({"_id": ObjectId(id)})
    return jsonify(status="Success", message="Dental Patient Deleted")

@app.route("/update_patient/<id>", methods=["POST", "GET"])
def update_patient(id):
    data = request.json  # Get JSON data from the request body
    if data:  # Check if data is received
        # Retrieve existing provider_id associated with the patient
        patient = db.Patient.find_one({"_id": ObjectId(id)})
        if patient:
            existing_provider_id = patient.get("provider_id")

            first_name = data.get('first_name')
            last_name = data.get('last_name')
            birth_date = data.get('birth_date')
            patient_number = data.get('patient_number')

            db.Patient.find_one_and_update({"_id": ObjectId(id)},{"$set": {
                "first_name" : first_name,
                "last_name": last_name,
                "birth_date": birth_date,
                "patient_number": patient_number,
                "provider_id": existing_provider_id  # Preserve the existing provider_id
            }})
            return jsonify(status="success", message="Dental Patient Updated successfully")
        else:
            return jsonify(status="error", message="Patient not found"), 404
    else:
        return jsonify(status="error", message="No data received"), 400  # Bad Request

# @app.route("/update_patient/<id>", methods=["POST", "GET"])
# def update_patient(id):
#     if request.method == "POST":
#         form = PatientForm(request.form)

#         first_name = form.first_name.data
#         last_name = form.last_name.data
#         birth_date = form.birth_date.data
#         date_birth = datetime.datetime.combine(birth_date, datetime.time.min)
#         patient_number = form.patient_number.data
    
#         db.Patient.find_one_and_update({"_id": ObjectId(id)},{"$set": {
#             "first_name" : first_name,
#             "last_name": last_name,
#             "birth_date": date_birth,
#             "patient_number": patient_number
#         }})

#         return jsonify(status="success", message="Dental Patient Updated")
    