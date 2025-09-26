from app import db
from app.models.base import BaseModel

class Item(BaseModel):
    """Item model for storing tyre inventory."""
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True, index=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    size = db.Column(db.String(20))
    brand = db.Column(db.String(50))
    pattern = db.Column(db.String(50))
    purchase_price = db.Column(db.Numeric(10, 2))
    selling_price = db.Column(db.Numeric(10, 2))
    gst_rate = db.Column(db.Numeric(4, 2))
    stock_qty = db.Column(db.Integer, default=0)
    reorder_level = db.Column(db.Integer, default=5)
    category = db.Column(db.String(50))  # tube, tyre, etc.

    purchase_lines = db.relationship('PurchaseLine', back_populates='item')
    invoice_lines = db.relationship('InvoiceLine', back_populates='item')
    stock_moves = db.relationship('StockMove', back_populates='item')

    def __repr__(self):
        return f'<Item {self.code}>'

class Service(BaseModel):
    """Service model for storing service offerings."""
    __tablename__ = 'services'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(20), unique=True, index=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(10, 2))
    gst_rate = db.Column(db.Numeric(4, 2))
    duration = db.Column(db.Integer)  # in minutes
    category = db.Column(db.String(50))  # alignment, balancing, etc.

    invoice_lines = db.relationship('InvoiceLine', back_populates='service')

    def __repr__(self):
        return f'<Service {self.code}>'