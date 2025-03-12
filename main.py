import os
from app import create_app, db
from flask_migrate import Migrate

# Create the app using the factory function
app = create_app()

# Initialize Flask-Migrate with the app and db
migrate = Migrate(app, db)

# The rest of your app setup follows

if __name__ == "__main__":
    # Running the Flask app in development mode
    app.run(debug=False, host="0.0.0.0", port=5000)

