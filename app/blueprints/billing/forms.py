from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, IntegerField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Optional, Length
from wtforms.widgets import HiddenInput

class CustomerSearchForm(FlaskForm):
    """Form for searching customers by mobile number."""
    mobile = StringField('Mobile Number', validators=[DataRequired(), Length(min=10, max=15)])

class InvoiceForm(FlaskForm):
    """Form for creating/editing invoices."""
    customer_id = IntegerField('Customer ID', widget=HiddenInput())
    vehicle_id = SelectField('Vehicle', coerce=int, validators=[Optional()])
    notes = TextAreaField('Notes', validators=[Optional(), Length(max=500)])

class InvoiceLineForm(FlaskForm):
    """Form for adding/editing invoice lines."""
    item_id = SelectField('Item', coerce=int, validators=[Optional()])
    service_id = SelectField('Service', coerce=int, validators=[Optional()])
    quantity = IntegerField('Quantity', default=1)
    unit_price = DecimalField('Unit Price', places=2)
    discount = DecimalField('Discount', places=2, default=0)

class PaymentForm(FlaskForm):
    """Form for recording payments."""
    amount = DecimalField('Amount', places=2, validators=[DataRequired()])
    payment_method = SelectField('Payment Method', 
        choices=[
            ('cash', 'Cash'),
            ('card', 'Card'),
            ('upi', 'UPI'),
            ('netbanking', 'Net Banking')
        ],
        validators=[DataRequired()]
    )
    reference = StringField('Reference', validators=[Optional(), Length(max=50)])