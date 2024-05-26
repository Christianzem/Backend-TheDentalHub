from application import app
from application import db
from flask import render_template, request, redirect, flash
import datetime
from .Prostheses import DentalProsthesis 
from bson import ObjectId

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
