from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.blueprints.auth import bp
from app.models import User
from app.blueprints.auth.forms import RegistrationForm, LoginForm

@bp.route('/register', methods=['GET', 'POST'])
def register():
    """Handle user registration."""
    if current_user.is_authenticated:
        return redirect(url_for('billing.quick_bill'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(name=form.name.data, email=form.email.data)
        user.password = form.password.data
        user.save()
        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html', form=form)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login."""
    if current_user.is_authenticated:
        return redirect(url_for('billing.quick_bill'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or not next_page.startswith('/'):
                next_page = url_for('billing.quick_bill')
            return redirect(next_page)
        flash('Invalid email or password', 'danger')
    
    return render_template('auth/login.html', form=form)

@bp.route('/logout')
@login_required
def logout():
    """Handle user logout."""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))

@bp.route('/profile')
@login_required
def profile():
    """Display user profile."""
    return render_template('auth/profile.html')

@bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    """Handle password change."""
    from app.blueprints.auth.forms import ChangePasswordForm
    form = ChangePasswordForm()
    
    if form.validate_on_submit():
        if not current_user.check_password(form.current_password.data):
            flash('Current password is incorrect.', 'danger')
        else:
            current_user.password = form.new_password.data
            current_user.save()
            flash('Your password has been successfully updated.', 'success')
            return redirect(url_for('auth.profile'))
    
    return render_template('auth/change_password.html', form=form)