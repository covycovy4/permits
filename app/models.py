
from app import db
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, text
from sqlalchemy.orm import relationship


# 🏛️ Permit Table
class Permit(db.Model):
    __tablename__ = 'permit'

    id = db.Column(Integer, primary_key=True, server_default=text("nextval('permit_id_seq'::regclass)"))
    salutation = db.Column(String(10), nullable=False)
    name = db.Column(String(100), nullable=False)
    address = db.Column(String(200), nullable=False)
    number_of_animals = db.Column(Integer, nullable=False)
    animal_type = db.Column(String(50), nullable=False)
    cattle_type = db.Column(String(50), nullable=True)  # Can be NULL
    other_animal_type = db.Column(String(100), nullable=True)  # Can be NULL
    origin = db.Column(String(100), nullable=False)
    origin_district = db.Column(String(100), nullable=False)
    destination = db.Column(String(100), nullable=False)
    destination_district = db.Column(String(100), nullable=False)
    movement_period = db.Column(String(50), nullable=False)  # Changed to String
    route = db.Column(String(200), nullable=False)
    payment_amount = db.Column(Float, nullable=False)  # Matches PostgreSQL 'double precision'
    payment_amount_in_words = db.Column(String(200), nullable=False)
    date = db.Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    status = db.Column(String(50), nullable=False, server_default=text("Submitted"))  # Corrected
    origin_status = db.Column(String(20), nullable=False, server_default=text("Pending"))  # Corrected
    destination_status = db.Column(String(20), nullable=False, server_default=text("Pending"))  # Corrected

# 🔎 Audit Log Table
class AuditLog(db.Model):
    __tablename__ = 'audit_logs'

    id = db.Column(db.Integer, primary_key=True, server_default=text("nextval('audit_logs_id_seq'::regclass)"))
    permit_id = db.Column(db.Integer, db.ForeignKey('permit.id'), nullable=False)
    action = db.Column(db.String(50), nullable=False)
    admin_id = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    reason = db.Column(db.String(255))

    permit = db.relationship('Permit', backref=db.backref('audit_logs', lazy=True))
    
    
    checked = db.Column(db.Boolean, default=False, nullable=False)
checked_by = db.Column(db.Integer, db.ForeignKey('user.id'))  # If you want to track who checked it
approved_by = db.Column(db.Integer, db.ForeignKey('user.id'))
approval_date = db.Column(db.DateTime)

 
