from app import db
from app.models.base import BaseModel

class Customer(BaseModel):
    """Customer model for storing customer information."""
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    mobile = db.Column(db.String(15), unique=True, index=True)
    email = db.Column(db.String(120))
    address = db.Column(db.Text)
    gst_number = db.Column(db.String(15))
    loyalty_points = db.Column(db.Integer, default=0)

    vehicles = db.relationship('Vehicle', back_populates='customer')
    invoices = db.relationship('Invoice', back_populates='customer')

    def __repr__(self):
        return f'<Customer {self.name}>'

class Vehicle(BaseModel):
    """Vehicle model for storing vehicle information."""
    __tablename__ = 'vehicles'

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    registration_number = db.Column(db.String(20), unique=True, index=True)
    make = db.Column(db.String(50))
    model = db.Column(db.String(50))
    year = db.Column(db.Integer)
    vehicle_type = db.Column(db.String(20))  # car, bike, truck, etc.
    tire_size = db.Column(db.String(20))

    customer = db.relationship('Customer', back_populates='vehicles')
    invoices = db.relationship('Invoice', back_populates='vehicle')

    def __repr__(self):
        return f'<Vehicle {self.registration_number}>'