# form_routes.py

from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session, flash
from pymongo import MongoClient
import json
from bson.objectid import ObjectId
from datetime import datetime 

form_routes = Blueprint('form_routes', __name__)

# Load Geo Data (provinces, divisions, etc.)
with open("geo_data.json") as f:
    geo_data = json.load(f)

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["Abdullah(12)_travel_db"]
form_collection = db["form_submissions"]
fare_collection = db["fares"]

@form_routes.route("/form", methods=["GET", "POST"])
def customer_form():
    # Ensure user is logged in before accessing the form
    if "user_id" not in session:
        flash("Please log in to fill the travel form.", "warning")
        return redirect(url_for("auth.login"))

    provinces = list(geo_data.keys())

    if request.method == "POST":
        # Get form data
        name = request.form.get("name")
        source_province = request.form.get("sourceProvince")
        source_division = request.form.get("sourceDivision")
        source_district = request.form.get("sourceDistrict")
        dest_province = request.form.get("destProvince")
        destination = request.form.get("destination")
        mode = request.form.get("mode")
        fare = request.form.get("fare")
        user_id = session["user_id"] # Get the logged-in user's ID from session

        # Insert new booking into MongoDB
        form_collection.insert_one({
            "user_id": user_id, # Store user_id with the booking
            "name": name,
            "sourceProvince": source_province,
            "sourceDivision": source_division,
            "sourceDistrict": source_district,
            "destProvince": dest_province,
            "destination": destination,
            "mode": mode,
            "fare": fare
        })

        flash("Your booking has been saved successfully!", "success")
        return redirect(url_for('auth.welcome')) # Redirect to welcome page after submission

    # For GET request (when creating a new form), explicitly pass booking=None
    # This prevents the 'booking' variable from being undefined in the template
    return render_template("form.html", provinces=provinces, booking=None)


@form_routes.route("/get_divisions/<province>")
def get_divisions(province):
    divisions = list(geo_data[province]["divisions"].keys())
    return jsonify(divisions)

@form_routes.route("/get_districts/<province>/<division>")
def get_districts(province, division):
    districts = geo_data[province]["divisions"][division]
    return jsonify(districts)

@form_routes.route("/get_destinations/<province>")
def get_destinations(province):
    destinations = geo_data[province]["destinations"]
    return jsonify(destinations)


@form_routes.route('/submit', methods=['POST'])
def submit_booking():
    print("--- AJAX submit_booking route entered ---")

    if 'username' not in session:
        # If not logged in, return a JSON error response for AJAX
        return jsonify({"status": "error", "message": "Please log in to make a booking."}), 401

    data = request.json
    print(f"Received JSON data: {data}") # KEEP THIS FOR DEBUGGING NULLS

    if not data:
        return jsonify({"status": "error", "message": "Invalid request: No JSON data received."}), 400

    # Extract data using .get() for safety
    name = data.get('name')
    sourceProvince = data.get('sourceProvince')
    sourceDivision = data.get('sourceDivision')
    sourceDistrict = data.get('sourceDistrict')
    destProvince = data.get('destProvince')
    destination = data.get('destination')
    mode = data.get('mode')
    fare = data.get('fare')

    logged_in_username = session['username']

    booking_data = {
        "name": name,
        "sourceProvince": sourceProvince,
        "sourceDivision": sourceDivision,
        "sourceDistrict": sourceDistrict,
        "destProvince": destProvince,
        "destination": destination,
        "mode": mode,
        "fare": fare,
        "created_at": datetime.now(),
        "booked_by_username": logged_in_username
    }

    try:
        form_collection.insert_one(booking_data)
        print(f"Booking inserted: {booking_data}")
        # THIS IS THE ONLY RETURN ON SUCCESS
        return jsonify({"status": "success", "message": "Your booking has been submitted successfully!"}), 200
    except Exception as e:
        print(f"Error inserting booking: {e}")
        # THIS IS THE ONLY RETURN ON ERROR
        return jsonify({"status": "error", "message": f"An error occurred: {e}"}), 500


@form_routes.route("/get_fare", methods=["POST"])
def get_fare():
    data = request.json
    source = data["source"]
    destination = data["destination"]
    mode = data["mode"]

    fare_record = fare_collection.find_one({
        "source": source,
        "destination": destination,
        "mode": mode
    })

    if fare_record:
        return jsonify({"fare": fare_record["fare"]})
    else:
        return jsonify({"fare": "Not Found"}), 404
    

@form_routes.route("/update_booking/<booking_id>", methods=["POST"])
def update_booking(booking_id):
    if "user_id" not in session:
        flash("Please log in to update bookings.", "warning")
        return redirect(url_for("auth.login"))

    existing_booking = form_collection.find_one({"_id": ObjectId(booking_id), "user_id": session["user_id"]})
    if not existing_booking:
        flash("Booking not found or you do not have permission to update it.", "danger")
        return redirect(url_for("auth.welcome"))

    name = request.form.get("name")
    source_province = request.form.get("sourceProvince")
    source_division = request.form.get("sourceDivision")
    source_district = request.form.get("sourceDistrict")
    dest_province = request.form.get("destProvince")
    destination = request.form.get("destination")
    mode = request.form.get("mode")
    fare = request.form.get("fare")

    form_collection.update_one(
        {"_id": ObjectId(booking_id)},
        {"$set": {
            "name": name,
            "sourceProvince": source_province,
            "sourceDivision": source_division,
            "sourceDistrict": source_district,
            "destProvince": dest_province,
            "destination": destination,
            "mode": mode,
            "fare": fare
        }}
    )
    flash("Your booking has been updated successfully!", "success")
    return redirect(url_for("auth.welcome"))

# 

@form_routes.route("/delete_booking/<booking_id>", methods=["POST"])
def delete_booking(booking_id):
    if "username" not in session: # <-- Change from "user_id" to "username"
        flash("Please log in to delete bookings.", "warning")
        return redirect(url_for("auth.login"))

    logged_in_username = session["username"] # <-- Get the username from session

    try:
        # Change 'user_id' to 'booked_by_username' to match your saved data
        result = form_collection.delete_one(
            {
                "_id": ObjectId(booking_id),
                "booked_by_username": logged_in_username # <-- Match the field name from your saved bookings
            }
        )

        if result.deleted_count == 1:
            flash("Booking deleted successfully!", "success")
        else:
            # This happens if the booking_id doesn't exist OR
            # if booked_by_username doesn't match the current user
            flash("Booking not found or you do not have permission to delete it.", "danger")
    except Exception as e:
        # Catch potential errors like invalid ObjectId string
        flash(f"An error occurred while trying to delete the booking: {e}", "danger")
        print(f"Error during booking deletion: {e}") # Print to server terminal for debugging

    return redirect(url_for("auth.welcome"))