from flask import Flask, render_template, request, redirect, url_for, flash
import json
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flashing messages

DATA_FILE = os.path.join('data', 'users.json')

def load_users():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_user(user):
    users = load_users()
    users.append(user)
    with open(DATA_FILE, 'w') as f:
        json.dump(users, f, indent=4)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get form data
        first_name = request.form.get('first_name').strip()
        middle_name = request.form.get('middle_name').strip()
        last_name = request.form.get('last_name').strip()
        contact_number = request.form.get('contact_number').strip()
        address = request.form.get('address').strip()
        email = request.form.get('email').strip()

        # Basic validation
        if not first_name or not last_name or not contact_number or not email:
            flash('Please fill in all required fields.', 'error')
            return redirect(url_for('index'))

        # Create user dictionary
        user = {
            'first_name': first_name,
            'middle_name': middle_name,
            'last_name': last_name,
            'contact_number': contact_number,
            'address': address,
            'email': email
        }

        # Save user to JSON file
        save_user(user)

        flash('User information saved successfully!', 'success')
        return redirect(url_for('index'))

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
