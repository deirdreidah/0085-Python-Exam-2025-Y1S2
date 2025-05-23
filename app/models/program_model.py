from app.extensions import db
from datetime import datetime

class Program(db.Model): 
    __tablename__ = 'programs'
    program_id = db.Column(db.Integer , primary_key = True, nullable = False)
    program_name = db.Column(db.String(255), nullable = False)
    description = db.Column(db.String(255), nullable = False)
    created_at = db.Column(db.DateTime , default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def __init__(self, program_id, program_name , description , created_at , updated_at):
        super(Program , self).__init__()
        self.program_id = program_id
        self.program_name = program_name
        self.description = description
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self) -> str:
        return f'{self.program_name} {self.description}'
