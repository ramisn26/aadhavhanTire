"""Utility script to manage users in the database."""
from flask import Flask
from app import create_app, db
from app.models import User, Role

app = create_app()

def list_users():
    """List all users in the database."""
    with app.app_context():
        users = User.query.all()
        roles = Role.query.all()
        
        print("\nRoles:")
        for role in roles:
            print(f"  {role.id}: {role.name} - {role.permissions}")
        
        print("\nUsers:")
        for user in users:
            print(f"  {user.id}: {user.name} ({user.email}) - Role: {user.role.name if user.role else 'None'}")

def create_admin():
    """Create an admin user."""
    with app.app_context():
        admin_role = Role.query.filter_by(name='Admin').first()
        if not admin_role:
            print("Admin role not found!")
            return
        
        admin = User(
            name='Admin',
            email='admin@example.com',
            is_active=True,
            role_id=admin_role.id
        )
        admin.password = 'admin123'
        
        db.session.add(admin)
        db.session.commit()
        print(f"Created admin user: {admin.email} with password: admin123")

def verify_login(email, password):
    """Verify if login credentials work."""
    with app.app_context():
        user = User.query.filter_by(email=email).first()
        if not user:
            print(f"No user found with email: {email}")
            return
        
        if user.verify_password(password):
            print("Password is valid!")
        else:
            print("Password is invalid!")

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Available commands:")
        print("  list - List all users")
        print("  create-admin - Create admin user")
        print("  verify email password - Verify login credentials")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'list':
        list_users()
    elif command == 'create-admin':
        create_admin()
    elif command == 'verify' and len(sys.argv) == 4:
        verify_login(sys.argv[2], sys.argv[3])
    else:
        print("Unknown command. Use: list, create-admin, or verify email password")