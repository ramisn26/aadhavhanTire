from decimal import Decimal
from flask import render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy.orm import joinedload
from app import db
from app.blueprints.billing import bp
from app.blueprints.billing.forms import CustomerSearchForm, InvoiceForm, InvoiceLineForm, PaymentForm
from app.models import Customer, Vehicle, Item, Service, Invoice, InvoiceLine, Payment
from app.auth.decorators import permission_required

@bp.route('/quick-bill', methods=['GET'])
@login_required
@permission_required('create_invoice')
def quick_bill():
    """Display the quick bill creation screen."""
    customer_form = CustomerSearchForm()
    invoice_form = InvoiceForm()
    line_form = InvoiceLineForm()
    payment_form = PaymentForm()
    
    # Populate the vehicle dropdown
    invoice_form.vehicle_id.choices = [(-1, 'Select Vehicle')]
    
    # Populate item and service dropdowns
    items = Item.query.filter_by(is_active=True).all()
    services = Service.query.filter_by(is_active=True).all()
    line_form.item_id.choices = [(-1, 'Select Item')] + [(i.id, f'{i.name} - {i.size}') for i in items]
    line_form.service_id.choices = [(-1, 'Select Service')] + [(s.id, s.name) for s in services]
    
    return render_template('billing/quick_bill.html',
                         customer_form=customer_form,
                         invoice_form=invoice_form,
                         line_form=line_form,
                         payment_form=payment_form)

@bp.route('/api/customer/search', methods=['POST'])
@login_required
def search_customer():
    """Search for a customer by mobile number."""
    form = CustomerSearchForm()
    if form.validate_on_submit():
        customer = Customer.query.filter_by(
            mobile=form.mobile.data,
            is_active=True
        ).first()
        
        if customer:
            vehicles = Vehicle.query.filter_by(
                customer_id=customer.id,
                is_active=True
            ).all()
            
            return jsonify({
                'success': True,
                'customer': {
                    'id': customer.id,
                    'name': customer.name,
                    'mobile': customer.mobile,
                    'email': customer.email,
                    'address': customer.address,
                    'gst_number': customer.gst_number
                },
                'vehicles': [
                    {
                        'id': v.id,
                        'registration_number': v.registration_number,
                        'make': v.make,
                        'model': v.model,
                        'year': v.year
                    } for v in vehicles
                ]
            })
        
        return jsonify({
            'success': False,
            'message': 'Customer not found'
        })
    
    return jsonify({
        'success': False,
        'message': 'Invalid form data'
    })

@bp.route('/api/item/<int:item_id>', methods=['GET'])
@login_required
def get_item_details(item_id):
    """Get item details including price and stock."""
    item = Item.query.get_or_404(item_id)
    return jsonify({
        'id': item.id,
        'name': item.name,
        'description': item.description,
        'selling_price': float(item.selling_price),
        'stock_qty': item.stock_qty,
        'gst_rate': float(item.gst_rate)
    })

@bp.route('/api/service/<int:service_id>', methods=['GET'])
@login_required
def get_service_details(service_id):
    """Get service details including price."""
    service = Service.query.get_or_404(service_id)
    return jsonify({
        'id': service.id,
        'name': service.name,
        'description': service.description,
        'price': float(service.price),
        'gst_rate': float(service.gst_rate)
    })

@bp.route('/invoice/create', methods=['POST'])
@login_required
@permission_required('create_invoice')
def create_invoice():
    """Create a new invoice."""
    form = InvoiceForm()
    
    if form.validate_on_submit():
        # Start a database transaction
        try:
            invoice = Invoice(
                customer_id=form.customer_id.data,
                vehicle_id=form.vehicle_id.data if form.vehicle_id.data != -1 else None,
                notes=form.notes.data,
                created_by_id=current_user.id,
                status='draft'
            )
            db.session.add(invoice)
            db.session.flush()  # Get the invoice ID
            
            # Process invoice lines from the form data
            lines_data = request.json.get('lines', [])
            for line_data in lines_data:
                line = InvoiceLine(
                    invoice_id=invoice.id,
                    item_id=line_data.get('item_id'),
                    service_id=line_data.get('service_id'),
                    quantity=line_data['quantity'],
                    unit_price=Decimal(str(line_data['unit_price'])),
                    discount=Decimal(str(line_data.get('discount', 0))),
                    tax_rate=Decimal(str(line_data['tax_rate'])),
                    description=line_data.get('description', '')
                )
                
                # Calculate line totals
                line.subtotal = line.quantity * line.unit_price
                line.tax_amount = (line.subtotal - line.discount) * (line.tax_rate / 100)
                line.total = line.subtotal - line.discount + line.tax_amount
                
                db.session.add(line)
            
            # Update invoice totals
            invoice.calculate_totals()
            invoice.status = 'confirmed'
            
            # Process payment if provided
            payment_form = PaymentForm()
            if payment_form.validate_on_submit():
                payment = Payment(
                    invoice_id=invoice.id,
                    amount=payment_form.amount.data,
                    payment_method=payment_form.payment_method.data,
                    reference=payment_form.reference.data
                )
                db.session.add(payment)
            
            db.session.commit()
            flash('Invoice created successfully!', 'success')
            return jsonify({
                'success': True,
                'invoice_id': invoice.id,
                'message': 'Invoice created successfully'
            })
            
        except Exception as e:
            db.session.rollback()
            return jsonify({
                'success': False,
                'message': f'Error creating invoice: {str(e)}'
            })
    
    return jsonify({
        'success': False,
        'message': 'Invalid form data'
    })