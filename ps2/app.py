from flask import Flask, render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap
import json
import os

app = Flask(__name__)
bootstrap = Bootstrap(app)  # Initialize Bootstrap with the app

DATA_FILE = 'data.json'

# Function to save data into a JSON file
def save_data(data):
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r+') as file:
            try:
                existing_data = json.load(file)
            except json.JSONDecodeError:
                existing_data = []
            existing_data.append(data)
            file.seek(0)
            json.dump(existing_data, file, indent=4)
    else:
        with open(DATA_FILE, 'w') as file:
            json.dump([data], file, indent=4)

@app.route("/", methods=["GET", "POST"])
def index():
    success_message = "Data is posted successfully."  

    if request.method == "POST":
        # Get data from the form
        first_name = request.form.get('first_name')
        middle_name = request.form.get('middle_name')
        last_name = request.form.get('last_name')
        contact_number = request.form.get('contact_number')
        address = request.form.get('address')
        email = request.form.get('email')

        # Basic server-side validation
        if not first_name or not last_name or not contact_number or not email:
            return redirect(url_for('index'))

        # Structure the data as a dictionary
        user_data = {
            "first_name": first_name,
            "middle_name": middle_name,
            "last_name": last_name,
            "contact_number": contact_number,
            "address": address,
            "email": email
        }

        # Save data to JSON file
        try:
            save_data(user_data)
            success_message = "Data submitted successfully!"  # Set success message
        except Exception as e:
            # Handle the error, for example logging it
            print(f"An error occurred: {str(e)}")

        return redirect(url_for('index'))

    return render_template("index.html", success_message=success_message)

if __name__ == "__main__":
    app.run(debug=True)
