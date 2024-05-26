from application import app
from application import db
from flask import render_template, request, redirect, flash
import datetime
from .Prostheses import DentalProsthesis 

# Routing using decorators
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

        print(selected_date)

        db.Prostheses.insert_one({
            "name": prosthesis_type,
            "list": checkbox,
            "selected_date": selected_datetime
            })
        
        print(selected_date)
        flash("Dental Prosthesis Added", "success")
        return redirect("/details")

    else:
        form = DentalProsthesis()
    return render_template("prosthesis.html", form=form)