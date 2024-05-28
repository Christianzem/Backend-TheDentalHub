from application import app
from application import db
from application import bcrypt
from flask import render_template, request, redirect, flash, url_for, session, jsonify
import datetime
from .Prostheses import DentalProsthesis 
from .User import RegisterForm, LoginForm
from .Patient import PatientForm
from bson import ObjectId


# Routing ----- User -----
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if request.method == "POST":
        if form.validate_on_submit():
        # Process the form data (e.g., save user to database)
            email = form.email.data
            hashed_password = bcrypt.generate_password_hash(form.password.data) 

            db.User.insert_one({
                "Email": email,
                "Password": hashed_password,
            })

            flash('Account created successfully!', 'success')
            return redirect(url_for('login'))  # Redirect to login page after successful signup
    return render_template('signup.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        # Check if the user exists in the database
        user = db.User.find_one({"Email": email})
        if user:
            # Verify the password
            if bcrypt.check_password_hash(user['Password'], form.password.data):
                # Log the user in
                session['user_id'] = str(user['_id'])  # Assuming _id is a BSON object
                flash('Login successful!', 'success')
                return redirect('/prosthesis')
        flash('Invalid email or password. Please try again.', 'error')

    return render_template('login.html', form=form)



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
    # return render_template("views.html", prostheses=prosthesis_list)

@app.route("/add_Prosthesis", methods=["POST", "GET"])
def prosthesis():
    if request.method == "POST":
        # data = request.json  # Access JSON data sent from frontend

        # prosthesis_type = data.get('type')
        # checkbox1 = data.get('checkbox1', False)  # Default value if checkbox1 is not present
        # checkbox2 = data.get('checkbox2', False)
        # checkbox3 = data.get('checkbox3', False)
        # checkbox4 = data.get('checkbox4', False)

        # selected_date1 = data.get('selected_date1')
        # selected_date2 = data.get('selected_date2')
        # selected_date3 = data.get('selected_date3')
        # selected_date4 = data.get('selected_date4')

        # # Perform necessary conversions and validations here

        # # Insert data into MongoDB
        # db.Prostheses.insert_one({
        #     "name": prosthesis_type,
        #     "lab": checkbox1,
        #     "arrival": checkbox2,
        #     "resent": checkbox3,
        #     "delivered": checkbox4,
        #     "selected_date1": selected_date1,
        #     "selected_date2": selected_date2,
        #     "selected_date3": selected_date3,
        #     "selected_date4": selected_date4
        # })
        
        # return jsonify(status="success", message="Dental Prosthesis Added successfully")
        form = DentalProsthesis(request.form)

        prosthesis_type = form.prosthesis_type.data
        checkbox1 = form.checkbox1.data
        checkbox2 = form.checkbox2.data
        checkbox3 = form.checkbox3.data
        checkbox4 = form.checkbox4.data

        selected_date1 = form.selected_date1.data
        # Convert selected_date to a datetime.datetime object with midnight time
        if selected_date1:
            selected_datetime1 = datetime.datetime.combine(selected_date1, datetime.time.min)
        else:
            selected_datetime1 = None
        selected_date2 = form.selected_date2.data
        if selected_date2:
            selected_datetime2 = datetime.datetime.combine(selected_date2, datetime.time.min)
        else:
            selected_datetime2 = None
        selected_date3 = form.selected_date3.data
        if selected_date3:
            selected_datetime3 = datetime.datetime.combine(selected_date3, datetime.time.min)
        else: 
            selected_datetime3 = None
        selected_date4 = form.selected_date4.data
        if selected_date4:
            selected_datetime4 = datetime.datetime.combine(selected_date4, datetime.time.min)
        else:
            selected_datetime4 = None


        db.Prostheses.insert_one({
            "name": prosthesis_type,
            "lab": checkbox1,
            "arrival": checkbox2,
            "resent": checkbox3,
            "delivered": checkbox4,
            "selected_date1": selected_datetime1,
            "selected_date2": selected_datetime2,
            "selected_date3": selected_datetime3,
            "selected_date4": selected_datetime4
            })
        
        flash("Dental Prosthesis Added", "success")
        return jsonify(status="success", message="Dental Patient Added successfully")

    else:
        form = DentalProsthesis()
    return render_template("prosthesis.html", form=form)

@app.route("/delete_Prosthesis/<id>")
def delete_Prosthesis(id):
    db.Prostheses.find_one_and_delete({"_id": ObjectId(id)})
    flash("Prosthesis successfully deleted", "success")
    return redirect("/prosthesis")

@app.route("/update_Prosthesis/<id>", methods=["POST", "GET"])
def update_Prosthesis(id):
    if request.method == "POST":
        form = DentalProsthesis(request.form)
        prosthesis_type = form.prosthesis_type.data
        checkbox1 = form.checkbox1.data
        checkbox2 = form.checkbox2.data
        checkbox3 = form.checkbox3.data
        checkbox4 = form.checkbox4.data

        selected_date1 = form.selected_date1.data
        # Convert selected_date to a datetime.datetime object with midnight time
        if selected_date1:
            selected_datetime1 = datetime.datetime.combine(selected_date1, datetime.time.min)
        else:
            selected_datetime1 = None
        selected_date2 = form.selected_date2.data
        if selected_date2:
            selected_datetime2 = datetime.datetime.combine(selected_date2, datetime.time.min)
        else:
            selected_datetime2 = None
        selected_date3 = form.selected_date3.data
        if selected_date3:
            selected_datetime3 = datetime.datetime.combine(selected_date3, datetime.time.min)
        else: 
            selected_datetime3 = None
        selected_date4 = form.selected_date4.data
        if selected_date4:
            selected_datetime4 = datetime.datetime.combine(selected_date4, datetime.time.min)
        else:
            selected_datetime4 = None

        db.Prostheses.find_one_and_update({"_id": ObjectId(id)}, {"$set": {
            "name": prosthesis_type,
            "lab": checkbox1,
            "arrival": checkbox2,
            "resent": checkbox3,
            "delivered": checkbox4,
            "selected_date1": selected_datetime1,
            "selected_date2": selected_datetime2,
            "selected_date3": selected_datetime3,
            "selected_date4": selected_datetime4
        }})

        flash("Dental Prosthesis Updated", "success")
        return redirect("/prosthesis")
    else:
        form = DentalProsthesis()

        dental_prosthesis = db.Prostheses.find_one({"_id": ObjectId(id)})
        if dental_prosthesis:
            form.prosthesis_type.data = dental_prosthesis.get("name", None)
            form.checkbox1.data = dental_prosthesis.get("lab", None)
            form.checkbox2.data = dental_prosthesis.get("arrived", None)
            form.checkbox3.data = dental_prosthesis.get("resent", None)
            form.checkbox4.data = dental_prosthesis.get("delivered", None)
            form.selected_date1.data = dental_prosthesis.get("selected_date1", None)
            form.selected_date2.data = dental_prosthesis.get("selected_date2", None)
            form.selected_date3.data = dental_prosthesis.get("selected_date3", None)
            form.selected_date4.data = dental_prosthesis.get("selected_date4", None)
        else:
            flash("Prosthesis not found", "error")
            return redirect("/prosthesis")  # Redirect to details page if prosthesis not found

    return render_template("prosthesis.html", form=form)

# Routing ---- Patient -----

@app.route("/patients")
def patients():
    patient_cursor = db.Patient.find()
    patient_list = [
        {
            '_id': str(patient.get('_id')),
            'first_name': patient.get('first_name'),
            'last_name': patient.get('last_name'),
            'birth_date': patient.get('birth_date'),
            'patient_number': patient.get('patient_number'),
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

        db.Patient.insert_one({
            "first_name": first_name,
            "last_name": last_name,
            "birth_date": birth_date,
            "patient_number": patient_number
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
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        birth_date = data.get('birth_date')
        patient_number = data.get('patient_number')

        db.Patient.find_one_and_update({"_id": ObjectId(id)},{"$set": {
            "first_name" : first_name,
            "last_name": last_name,
            "birth_date": birth_date,
            "patient_number": patient_number
        }})
        return jsonify(status="success", message="Dental Patient Updated successfully")
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
    