from datetime import datetime
from app import db
from app.models.base import BaseModel

class Purchase(BaseModel):
    """Purchase model for storing purchase transactions."""
    __tablename__ = 'purchases'

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(20), unique=True, index=True)
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendors.id'), nullable=False)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    vendor_bill_number = db.Column(db.String(50))
    vendor_bill_date = db.Column(db.Date)
    subtotal = db.Column(db.Numeric(10, 2), default=0)
    total_tax = db.Column(db.Numeric(10, 2), default=0)
    total = db.Column(db.Numeric(10, 2), default=0)
    notes = db.Column(db.Text)
    status = db.Column(db.String(20), default='draft')  # draft, confirmed, cancelled
    created_by_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    vendor = db.relationship('Vendor', back_populates='purchases')
    lines = db.relationship('PurchaseLine', back_populates='purchase', cascade='all, delete-orphan')
    created_by = db.relationship('User', back_populates='purchases_created')

    def __repr__(self):
        return f'<Purchase {self.number}>'

class PurchaseLine(BaseModel):
    """PurchaseLine model for storing purchase line items."""
    __tablename__ = 'purchase_lines'

    id = db.Column(db.Integer, primary_key=True)
    purchase_id = db.Column(db.Integer, db.ForeignKey('purchases.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)
    tax_rate = db.Column(db.Numeric(4, 2))
    tax_amount = db.Column(db.Numeric(10, 2))
    subtotal = db.Column(db.Numeric(10, 2))
    total = db.Column(db.Numeric(10, 2))

    purchase = db.relationship('Purchase', back_populates='lines')
    item = db.relationship('Item', back_populates='purchase_lines')

    def __repr__(self):
        return f'<PurchaseLine {self.id}>'

class Invoice(BaseModel):
    """Invoice model for storing sales transactions."""
    __tablename__ = 'invoices'

    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(20), unique=True, index=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'))
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    subtotal = db.Column(db.Numeric(10, 2), default=0)
    discount = db.Column(db.Numeric(10, 2), default=0)
    total_tax = db.Column(db.Numeric(10, 2), default=0)
    total = db.Column(db.Numeric(10, 2), default=0)
    round_off = db.Column(db.Numeric(2, 2), default=0)
    notes = db.Column(db.Text)
    status = db.Column(db.String(20), default='draft')  # draft, confirmed, cancelled
    created_by_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    customer = db.relationship('Customer', back_populates='invoices')
    vehicle = db.relationship('Vehicle', back_populates='invoices')
    lines = db.relationship('InvoiceLine', back_populates='invoice', cascade='all, delete-orphan')
    payments = db.relationship('Payment', back_populates='invoice')
    created_by = db.relationship('User', back_populates='invoices_created')

    def __repr__(self):
        return f'<Invoice {self.number}>'

class InvoiceLine(BaseModel):
    """InvoiceLine model for storing invoice line items."""
    __tablename__ = 'invoice_lines'

    id = db.Column(db.Integer, primary_key=True)
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoices.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'))
    description = db.Column(db.String(255))
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)
    discount = db.Column(db.Numeric(10, 2), default=0)
    tax_rate = db.Column(db.Numeric(4, 2))
    tax_amount = db.Column(db.Numeric(10, 2))
    subtotal = db.Column(db.Numeric(10, 2))
    total = db.Column(db.Numeric(10, 2))

    invoice = db.relationship('Invoice', back_populates='lines')
    item = db.relationship('Item', back_populates='invoice_lines')
    service = db.relationship('Service', back_populates='invoice_lines')

    def __repr__(self):
        return f'<InvoiceLine {self.id}>'

class Payment(BaseModel):
    """Payment model for storing payment transactions."""
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    invoice_id = db.Column(db.Integer, db.ForeignKey('invoices.id'), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    payment_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    payment_method = db.Column(db.String(20))  # cash, card, upi, etc.
    reference = db.Column(db.String(50))
    notes = db.Column(db.Text)

    invoice = db.relationship('Invoice', back_populates='payments')

    def __repr__(self):
        return f'<Payment {self.id}>'

class StockMove(BaseModel):
    """StockMove model for tracking inventory movements."""
    __tablename__ = 'stock_moves'

    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)  # positive for in, negative for out
    reference = db.Column(db.String(50))  # purchase/invoice number
    reference_type = db.Column(db.String(20))  # purchase, sale, adjustment
    notes = db.Column(db.Text)

    item = db.relationship('Item', back_populates='stock_moves')

    def __repr__(self):
        return f'<StockMove {self.id}>'