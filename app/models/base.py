from datetime import datetime
from app import db

class BaseModel(db.Model):
    """Base model class that includes common fields and methods."""
    __abstract__ = True

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

    def save(self):
        """Save the current instance to the database."""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Soft delete the current instance."""
        self.is_active = False
        db.session.commit()

    def hard_delete(self):
        """Hard delete the current instance from the database."""
        db.session.delete(self)
        db.session.commit()