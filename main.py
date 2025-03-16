import os
from app import create_app, db
from flask_migrate import Migrate
from flask_cors import CORS

# Create the app using the factory function
app = create_app()

# Enable CORS (Cross-Origin Resource Sharing)
CORS(app)

# Initialize Flask-Migrate with the app and db
migrate = Migrate(app, db)

if __name__ == "__main__":
    # Running the Flask app in development mode
    app.run(debug=False, host="0.0.0.0", port=5000)

