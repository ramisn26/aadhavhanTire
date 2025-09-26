"""Vendor models."""
from datetime import datetime
from app import db
from app.models.base import BaseModel

class Vendor(BaseModel):
    """Vendor model for storing vendor information."""
    __tablename__ = 'vendors'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True, index=True)
    name = db.Column(db.String(100), nullable=False)
    contact_person = db.Column(db.String(100))
    phone = db.Column(db.String(15))
    email = db.Column(db.String(120))
    address = db.Column(db.Text)
    gst_number = db.Column(db.String(15))
    payment_terms = db.Column(db.Integer)  # in days
    created_by_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    purchases = db.relationship('Purchase', back_populates='vendor')
    created_by = db.relationship('User', back_populates='vendors')

    def __repr__(self):
        return f'<Vendor {self.code}>'