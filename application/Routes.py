from application import app
from application import db
from application import bcrypt
from flask import render_template, request, redirect, flash, url_for, session, jsonify
import datetime
from .Prostheses import DentalProsthesis 
from .User import RegisterForm, LoginForm
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
        return redirect("/prosthesis")

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