from ..app import db
from sqlalchemy.sql import func


class Article(db.Model):
    __tablename__ = "Articles"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    userId = db.Column(db.Integer, db.ForeignKey("Users.id"))
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    @property
    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "created_at": self.created_at,
        }
