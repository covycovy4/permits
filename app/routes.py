from flask import Blueprint, render_template, request, redirect, jsonify
from app import db
from app.models import Permit  # Adjust this if Permit is defined elsewhere
from datetime import datetime
from flask_login import current_user
from flask import session
import os
import psycopg2
import logging

# Create the blueprint after importing
# Create the Blueprint with an explicit template folder path
main = Blueprint('main', __name__, template_folder=os.path.join(os.getcwd(), 'templates'))


# Route for the home page
@main.route('/')
def index():
    return render_template('index.html')

# Database Configuration
DATABASE_URL = os.getenv("DATABASE_URL")
def get_db_connection():
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode="require")
        return conn
    except Exception as e:
        print("Database connection error:", e)
        return None


# Function to establish a database connection
def get_db_connection():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print("Database connection error:", e)
        return None  # Ensures the caller handles this properly
        
@main.route('/api/submissions/<int:id>', methods=['GET'])

def get_submission(id):

    permit = Permit.query.get(id)

    if permit:

        return jsonify({

            'id': permit.id,

            'salutation': permit.salutation,

            'name': permit.name,

            'address': permit.address,

            'number_of_animals': permit.number_of_animals,

            'animal_type': permit.animal_type,

            'cattle_type': permit.cattle_type,

            'other_animal_type': permit.other_animal_type,

            'origin': permit.origin,

            'origin_district': permit.origin_district,

            'destination': permit.destination,

            'destination_district': permit.destination_district,

            'movement_period': permit.movement_period,

            'route': permit.route,

            'payment_amount': permit.payment_amount,

            'payment_amount_in_words': permit.payment_amount_in_words,

            'date': permit.date.strftime('%Y-%m-%d'),

            'status': permit.status

        })

    return jsonify({'error': 'Permit not found'}), 404


# Route to submit a new permit

@main.route('/submit', methods=['POST'])
def submit_permit():
    try:
        data = request.json
        new_permit = Permit(
            salutation=data['salutation'],
            name=data['name'],
            address=data['address'],
            number_of_animals=data['numberOfAnimals'],
            animal_type=data['animalType'],
            cattle_type=data.get('cattleType', None),
            other_animal_type=data.get('otherAnimalType', None),
            origin=data['origin'],
            origin_district=data['originDistrict'],
            destination=data['destination'],
            destination_district=data['destinationDistrict'],
            movement_period=data['movementPeriod'],
            route=data['route'],
            payment_amount=data['paymentAmount'],
            payment_amount_in_words=data['paymentAmountInWords'],
            date=datetime.strptime(data['submissionDate'], '%Y-%m-%d'),
            status='Submitted'
        )

        db.session.add(new_permit)
        db.session.commit()  # ✅ Ensure commit

        return jsonify({'message': 'Permit successfully submitted!'}), 201

    except Exception as e:
        db.session.rollback()  # ✅ Rollback in case of error
        print("Error submitting permit:", e)
        return jsonify({'error': str(e)}), 400


# Create permit
@main.route('/api/submissions', methods=['POST'])
def create_submissions():
    data = request.get_json()

    # Validate required fields
    required_fields = [
        "salutation", "name", "address", "number_of_animals", "animal_type", 
        "origin", "origin_district", "destination", "destination_district", 
        "movement_period", "route", "payment_amount", "payment_amount_in_words", 
        "submission_date"
    ]

    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        insert_query = """
        INSERT INTO permit (salutation, name, address, number_of_animals, animal_type, 
                            cattle_type, other_animal_type, origin, origin_district, 
                            destination, destination_district, movement_period, route, 
                            payment_amount, payment_amount_in_words, date, status)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'Pending')
        RETURNING id;
        """

        cursor.execute(insert_query, (
            data["salutation"], data["name"], data["address"], data["number_of_animals"],
            data["animal_type"], data.get("cattle_type", ""), data.get("other_animal_type", ""),
            data["origin"], data["origin_district"], data["destination"], data["destination_district"],
            data["movement_period"], data["route"], data["payment_amount"], 
            data["payment_amount_in_words"], data["submission_date"]
        ))

        permit_id = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "Permit submitted successfully!", "permit_id": permit_id}), 201

    except Exception as e:
        print("Error submitting permit:", e)
        return jsonify({"error": "Failed to submit permit"}), 500


# Route to get a list of all permit submissions with optional filtering

@main.route('/api/submissions', methods=['GET'])

def get_submissions():

    try:

        # Get query parameters from URL

        district_filter = request.args.get('district', '')

        start_date_filter = request.args.get('startDate', '')

        end_date_filter = request.args.get('endDate', '')


        # Build the query filter

        query = Permit.query


        # Filter by district (origin or destination)

        if district_filter:

            if district_filter != "All":

                query = query.filter(

                    (Permit.origin_district.ilike(f'%{district_filter}%')) |

                    (Permit.destination_district.ilike(f'%{district_filter}%'))

                )

        

        # Filter by start date

        if start_date_filter:

            query = query.filter(Permit.date >= datetime.strptime(start_date_filter, '%Y-%m-%d'))

        

        # Filter by end date

        if end_date_filter:

            query = query.filter(Permit.date <= datetime.strptime(end_date_filter, '%Y-%m-%d'))


        # Fetch results

        permits = query.all()

        

        results = [{

            'id': permit.id,

            'salutation': permit.salutation,

            'name': permit.name,

            'address': permit.address,

            'number_of_animals': permit.number_of_animals,

            'animal_type': permit.animal_type,

            'cattle_type': permit.cattle_type,

            'other_animal_type': permit.other_animal_type,

            'origin': permit.origin,

            'origin_district': permit.origin_district,

            'destination': permit.destination,

            'destination_district': permit.destination_district,

            'movement_period': permit.movement_period,

            'route': permit.route,

            'payment_amount': permit.payment_amount,

            'payment_amount_in_words': permit.payment_amount_in_words,

            'date': permit.date.strftime('%Y-%m-%d'),

            'status': permit.status

        } for permit in permits]


        return jsonify(results)

    except Exception as e:

        return jsonify({'error': f"An error occurred while fetching submissions: {str(e)}"}), 500




# Fetch a single permit by ID
@main.route('/api/permits/<int:permit_id>', methods=['GET'])
def get_permit_by_id(permit_id):
    conn = get_db_connection()

    if conn is None:
        return jsonify({"error": "Failed to connect to the database"}), 500

    cursor = conn.cursor()

    try:
        query = """
        SELECT id, salutation, name, number_of_animals, animal_type,
               origin_district, destination_district, movement_period,
               route, payment_amount, payment_amount_in_words, date, status
        FROM permit
        WHERE id = %s;
        """

        cursor.execute(query, (permit_id,))
        permit = cursor.fetchone()

        if not permit:
            cursor.close()
            conn.close()
            return jsonify({"error": "Permit not found"}), 404

        permit_data = {
            "id": permit[0],
            "salutation": permit[1],
            "name": permit[2],
            "numberOfAnimals": permit[3],
            "animalType": permit[4],
            "originDistrict": permit[5],
            "destinationDistrict": permit[6],
            "movementPeriod": permit[7],
            "route": permit[8],
            "paymentAmount": permit[9],
            "paymentAmountInWords": permit[10],
            "date": permit[11].strftime("%Y-%m-%d %H:%M:%S"),
            "status": permit[12]
        }

        cursor.close()
        conn.close()

        return jsonify(permit_data), 200

    except Exception as e:
        cursor.close()
        conn.close()
        print("Error fetching permit:", e)
        return jsonify({"error": "Failed to fetch permit data"}), 500




# Disapprove permit
@main.route('/disapprove/<role>/<int:permit_id>', methods=['POST'])
def disapprove(role, permit_id):
    permit = Permit.query.get(permit_id)

    if permit:
        if role == "origin":
            permit.origin_status = "Disapproved"
        elif role == "destination":
            permit.destination_status = "Disapproved"

        db.session.commit()

    return redirect(request.referrer)


# Filter permits based on district
@main.route('/api/submissions', methods=['GET'])
def filter_permits():
    """Filter permits based on district"""
    district = request.args.get('district', '')

    if district:
        permits = Permit.query.filter(
            (Permit.origin_district == district) | 
            (Permit.destination_district == district)
        ).all()
    else:
        permits = Permit.query.all()

    permit_list = []
    for permit in permits:
        permit_list.append({
            'id': permit.id,
            'name': permit.name,
            'date': permit.date,
            'origin_district': permit.origin_district,
            'destination_district': permit.destination_district,
            'number_of_animals': permit.number_of_animals,
            'payment_amount': permit.payment_amount,
            'status': permit.status
        })

    return jsonify(permit_list)


# Route to delete a permit
@main.route('/api/delete/<int:id>', methods=['DELETE'])
def delete_permit(id):
    """Delete a permit"""
    permit = Permit.query.get(id)

    if permit:
        db.session.delete(permit)
        db.session.commit()
        return jsonify({'message': 'Permit deleted successfully'})
    
    return jsonify({'error': 'Permit not found'}), 404



# Route to edit an existing permit submission by ID

@main.route('/edit/<int:id>', methods=['PUT'])

def edit_permit(id):

    try:

        data = request.json

        permit = Permit.query.get(id)

        if permit:

            # Update permit fields with the provided data

            permit.name = data['name']
            permit.origin = data['origin']
            permit.destination = data['destination']
            permit.number_of_animals = data['numberOfAnimals']
            permit.payment_amount = data['paymentAmount']
            permit.status = data.get('status', permit.status)

            # Commit the changes to the database

            db.session.commit()

            return jsonify({'message': 'Permit updated successfully!'}), 200

        return jsonify({'error': 'Permit not found'}), 404

    except Exception as e:

        return jsonify({'error': str(e)}), 400


# routes.py (or wherever your routes are defined)


# Route to approve a permit
@main.route('/permit/<int:permit_id>/approve', methods=['POST'])
def approve_permit(permit_id):
    permit = Permit.query.get(permit_id)

    if permit:
        permit.status = 'Approved'
        db.session.commit()
        return jsonify({"message": "Permit approved successfully!"}), 200
    
    return jsonify({"message": "Permit not found!"}), 404


# Route to disapprove a permit
@main.route('/permit/<int:permit_id>/disapprove', methods=['POST'])
def disapprove_permit(permit_id):
    permit = Permit.query.get(permit_id)

    if permit:
        permit.status = 'Disapproved'
        db.session.commit()
        return jsonify({"message": "Permit disapproved successfully!"}), 200
    
    return jsonify({"message": "Permit not found!"}), 404

# Route to delete a permit by ID
@main.route('/delete/<int:id>', methods=['DELETE'])
def delete_permit_by_id(id):
    try:
        permit = Permit.query.get(id)

        if permit:
            db.session.delete(permit)
            db.session.commit()
            return jsonify({'message': 'Permit deleted successfully!'}), 200
        
        return jsonify({'error': 'Permit not found'}), 404
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Routes to render submissions pages for various locations
@main.route('/chimanimani_submissions')
def chimanimani_submissions_page():
    return render_template('chimanimani_submissions.html')


@main.route('/buhera_submissions')
def buhera_submissions_page():
    return render_template('buhera_submissions.html')


@main.route('/chipinge_submissions')
def chipinge_submissions_page():
    return render_template('chipinge_submissions.html')


@main.route('/makoni_submissions')
def makoni_submissions_page():
    return render_template('makoni_submissions.html')


@main.route('/mutasa_submissions')
def mutasa_submissions_page():
    return render_template('mutasa_submissions.html')


@main.route('/nyanga_submissions')
def nyanga_submissions_page():
    return render_template('nyanga_submissions.html')


@main.route('/mutare_submissions')
def mutare_submissions_page():
    return render_template('mutare_submissions.html')


# Route to render the permit form page
@main.route('/form')
def form_page():
    return render_template('permit.html')


# Route to render the submissions page
@main.route('/submissions')
def submissions_page():
    return render_template('permit2.html')

# API to fetch Chimanimani-specific submissions
@main.route('/api/chimanimani_submissions', methods=['GET'])
def get_chimanimani_submissions():
    try:
        permits = Permit.query.filter(
            (Permit.origin_district.ilike('%Chimanimani%')) |
            (Permit.destination_district.ilike('%Chimanimani%'))
        ).all()

        results = [{
            'id': permit.id,
            'salutation': permit.salutation,
            'name': permit.name,
            'address': permit.address,
            'number_of_animals': permit.number_of_animals,
            'animal_type': permit.animal_type,
            'cattle_type': permit.cattle_type,
            'other_animal_type': permit.other_animal_type,
            'origin': permit.origin,
            'origin_district': permit.origin_district,
            'destination': permit.destination,
            'destination_district': permit.destination_district,
            'movement_period': permit.movement_period,
            'route': permit.route,
            'payment_amount': permit.payment_amount,
            'payment_amount_in_words': permit.payment_amount_in_words,
            'date': permit.date.strftime('%Y-%m-%d'),
            'status': permit.status
        } for permit in permits]

        return jsonify(results)
    
    except Exception as e:
        return jsonify({'error': f"An error occurred while fetching Chimanimani submissions: {str(e)}"}), 500


# API to fetch Buhera-specific submissions
@main.route('/api/buhera_submissions', methods=['GET'])
def get_buhera_submissions():
    try:
        permits = Permit.query.filter(
            (Permit.origin_district.ilike('%Buhera%')) |
            (Permit.destination_district.ilike('%Buhera%'))
        ).all()

        results = [{
            'id': permit.id,
            'salutation': permit.salutation,
            'name': permit.name,
            'address': permit.address,
            'number_of_animals': permit.number_of_animals,
            'animal_type': permit.animal_type,
            'cattle_type': permit.cattle_type,
            'other_animal_type': permit.other_animal_type,
            'origin': permit.origin,
            'origin_district': permit.origin_district,
            'destination': permit.destination,
            'destination_district': permit.destination_district,
            'movement_period': permit.movement_period,
            'route': permit.route,
            'payment_amount': permit.payment_amount,
            'payment_amount_in_words': permit.payment_amount_in_words,
            'date': permit.date.strftime('%Y-%m-%d'),
            'status': permit.status
        } for permit in permits]

        return jsonify(results)

    except Exception as e:
        return jsonify({'error': f"An error occurred while fetching Buhera submissions: {str(e)}"}), 500


# API to fetch Chipinge-specific submissions
@main.route('/api/chipinge_submissions', methods=['GET'])
def get_chipinge_submissions():
    try:
        permits = Permit.query.filter(
            (Permit.origin_district.ilike('%Chipinge%')) |
            (Permit.destination_district.ilike('%Chipinge%'))
        ).all()

        results = [{
            'id': permit.id,
            'salutation': permit.salutation,
            'name': permit.name,
            'address': permit.address,
            'number_of_animals': permit.number_of_animals,
            'animal_type': permit.animal_type,
            'cattle_type': permit.cattle_type,
            'other_animal_type': permit.other_animal_type,
            'origin': permit.origin,
            'origin_district': permit.origin_district,
            'destination': permit.destination,
            'destination_district': permit.destination_district,
            'movement_period': permit.movement_period,
            'route': permit.route,
            'payment_amount': permit.payment_amount,
            'payment_amount_in_words': permit.payment_amount_in_words,
            'date': permit.date.strftime('%Y-%m-%d'),
            'status': permit.status
        } for permit in permits]

        return jsonify(results)

    except Exception as e:
        return jsonify({'error': f"An error occurred while fetching Chipinge submissions: {str(e)}"}), 500


# API to fetch Mutasa-specific submissions
@main.route('/api/mutasa_submissions', methods=['GET'])
def get_mutasa_submissions():
    try:
        permits = Permit.query.filter(
            (Permit.origin_district.ilike('%Mutasa%')) |
            (Permit.destination_district.ilike('%Mutasa%'))
        ).all()

        results = [{
            'id': permit.id,
            'salutation': permit.salutation,
            'name': permit.name,
            'address': permit.address,
            'number_of_animals': permit.number_of_animals,
            'animal_type': permit.animal_type,
            'cattle_type': permit.cattle_type,
            'other_animal_type': permit.other_animal_type,
            'origin': permit.origin,
            'origin_district': permit.origin_district,
            'destination': permit.destination,
            'destination_district': permit.destination_district,
            'movement_period': permit.movement_period,
            'route': permit.route,
            'payment_amount': permit.payment_amount,
            'payment_amount_in_words': permit.payment_amount_in_words,
            'date': permit.date.strftime('%Y-%m-%d'),
            'status': permit.status
        } for permit in permits]

        return jsonify(results)

    except Exception as e:
        return jsonify({'error': f"An error occurred while fetching Mutasa submissions: {str(e)}"}), 500


# API to fetch Mutare-specific submissions
@main.route('/api/mutare_submissions', methods=['GET'])
def get_mutare_submissions():
    try:
        permits = Permit.query.filter(
            (Permit.origin_district.ilike('%Mutare%')) |
            (Permit.destination_district.ilike('%Mutare%'))
        ).all()

        results = [{
            'id': permit.id,
            'salutation': permit.salutation,
            'name': permit.name,
            'address': permit.address,
            'number_of_animals': permit.number_of_animals,
            'animal_type': permit.animal_type,
            'cattle_type': permit.cattle_type,
            'other_animal_type': permit.other_animal_type,
            'origin': permit.origin,
            'origin_district': permit.origin_district,
            'destination': permit.destination,
            'destination_district': permit.destination_district,
            'movement_period': permit.movement_period,
            'route': permit.route,
            'payment_amount': permit.payment_amount,
            'payment_amount_in_words': permit.payment_amount_in_words,
            'date': permit.date.strftime('%Y-%m-%d'),
            'status': permit.status
        } for permit in permits]

        return jsonify(results)

    except Exception as e:
        return jsonify({'error': f"An error occurred while fetching Mutare submissions: {str(e)}"}), 500


# API to fetch Nyanga-specific submissions
@main.route('/api/nyanga_submissions', methods=['GET'])
def get_nyanga_submissions():
    try:
        permits = Permit.query.filter(
            (Permit.origin_district.ilike('%Nyanga%')) |
            (Permit.destination_district.ilike('%Nyanga%'))
        ).all()

        results = [{
            'id': permit.id,
            'salutation': permit.salutation,
            'name': permit.name,
            'address': permit.address,
            'number_of_animals': permit.number_of_animals,
            'animal_type': permit.animal_type,
            'cattle_type': permit.cattle_type,
            'other_animal_type': permit.other_animal_type,
            'origin': permit.origin,
            'origin_district': permit.origin_district,
            'destination': permit.destination,
            'destination_district': permit.destination_district,
            'movement_period': permit.movement_period,
            'route': permit.route,
            'payment_amount': permit.payment_amount,
            'payment_amount_in_words': permit.payment_amount_in_words,
            'date': permit.date.strftime('%Y-%m-%d'),
            'status': permit.status
        } for permit in permits]

        return jsonify(results)

    except Exception as e:
        return jsonify({'error': f"An error occurred while fetching Nyanga submissions: {str(e)}"}), 500




# Corrected code:

def log_action(permit_id, action, admin_id, reason=None):
    # The body of the log_action function should be indented
    # For example, if you want to log the action to a file or database
    print(f"Action: {action}, Permit ID: {permit_id}, Admin ID: {admin_id}, Reason: {reason}")
    # Additional code for logging actions can go here
    # If you are interacting with a database, you can insert logs into your logs table, for example.
        



# Register the blueprint with the app
def create_app():
    app = Flask(__name__)
    app.register_blueprint(main)  # This is indented properly
    return app


logging.basicConfig(level=logging.DEBUG)


