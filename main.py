from app import create_app, db

app = create_app()

# Create all tables in the database
with app.app_context():
    db.create_all()  # This ensures all your models (tables) are created in PostgreSQL
    
app.register_blueprint(main)

if __name__ == "__main__":
    app = create_app()
   app.run(debug=False, host="0.0.0.0", port=5000)


