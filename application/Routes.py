from application import app
from application import db
from application import bcrypt
from flask import render_template, request, redirect, flash, url_for, session
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
                return redirect('/details')
        flash('Invalid email or password. Please try again.', 'error')

    return render_template('login.html', form=form)



# Routing using decorators ----- Prosthesis -----
@app.route("/details")
def patientDetails():
    prosthesis_cursor = db.Prostheses.find()
    prosthesis_list = list(prosthesis_cursor)
    return render_template("views.html", prostheses=prosthesis_list)

@app.route("/add_Prosthesis", methods=["POST", "GET"])
def prosthesis():
    if request.method == "POST":
        form = DentalProsthesis(request.form)

        prosthesis_type = form.prosthesis_type.data
        checkbox = form.checkbox.data
        # selected_date_str = form.selected_date.data.strip()  # Remove leading and trailing whitespace
        # selected_date = datetime.strptime(selected_date_str, "%Y-%m-%d").date()
        selected_date = form.selected_date.data
        # Convert selected_date to a datetime.datetime object with midnight time
        selected_datetime = datetime.datetime.combine(selected_date, datetime.time.min)


        db.Prostheses.insert_one({
            "name": prosthesis_type,
            "list": checkbox,
            "selected_date": selected_datetime
            })
        
        flash("Dental Prosthesis Added", "success")
        return redirect("/details")

    else:
        form = DentalProsthesis()
    return render_template("prosthesis.html", form=form)

@app.route("/delete_Prosthesis/<id>")
def delete_Prosthesis(id):
    db.Prostheses.find_one_and_delete({"_id": ObjectId(id)})
    flash("Prosthesis successfully deleted", "success")
    return redirect("/details")

@app.route("/update_Prosthesis/<id>", methods=["POST", "GET"])
def update_Prosthesis(id):
    if request.method == "POST":
        form = DentalProsthesis(request.form)
        prosthesis_type = form.prosthesis_type.data
        checkbox = form.checkbox.data
        selected_date = form.selected_date.data
        selected_datetime = datetime.datetime.combine(selected_date, datetime.time.min)

        db.Prostheses.find_one_and_update({"_id": ObjectId(id)}, {"$set": {
            "name": prosthesis_type,
            "list": checkbox,
            "selected_date": selected_datetime
        }})

        flash("Dental Prosthesis Updated", "success")
        return redirect("/details")
    else:
        form = DentalProsthesis()

        dental_prosthesis = db.Prostheses.find_one({"_id": ObjectId(id)})
        if dental_prosthesis:
            form.prosthesis_type.data = dental_prosthesis.get("name", None)
            form.checkbox.data = dental_prosthesis.get("list", None)
            form.selected_date.data = dental_prosthesis.get("selected_date", None)
        else:
            flash("Prosthesis not found", "error")
            return redirect("/details")  # Redirect to details page if prosthesis not found

    return render_template("prosthesis.html", form=form)