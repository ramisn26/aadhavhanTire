from app import db
from app.models.base import BaseModel

class Setting(BaseModel):
    """Setting model for storing business configuration."""
    __tablename__ = 'settings'

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(50), unique=True, nullable=False)
    value = db.Column(db.Text)
    data_type = db.Column(db.String(20))  # string, integer, float, json, etc.
    description = db.Column(db.String(255))
    category = db.Column(db.String(50))  # general, invoice, notification, etc.

    def __repr__(self):
        return f'<Setting {self.key}>'

class Reminder(BaseModel):
    """Reminder model for customer follow-ups."""
    __tablename__ = 'reminders'

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'))
    type = db.Column(db.String(20))  # alignment, balancing, general, etc.
    due_date = db.Column(db.Date, nullable=False)
    message = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending')  # pending, sent, cancelled
    sent_via = db.Column(db.String(20))  # whatsapp, sms, both

    customer = db.relationship('Customer', backref='reminders')
    vehicle = db.relationship('Vehicle', backref='reminders')

    def __repr__(self):
        return f'<Reminder {self.id}>'