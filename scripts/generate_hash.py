"""Generate password hash."""
from werkzeug.security import generate_password_hash

password = 'admin123'
password_hash = generate_password_hash(password)
print(f"Password hash for '{password}':")
print(password_hash)