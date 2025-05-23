from app.extensions import db
from datetime import datetime

class Course(db.Model):
    __tablename__ = "courses"
    course_id = db.Column(db.Integer , primary_key = True , nullable = False)
    course_name = db.Column(db.String(255) , nullable = False)
    description = db.Column(db.String(255) , nullable = False)
    program_id = db.Column(db.Integer , db.ForeignKey('programs.program_id'), nullable = False)
    program = db.relationship('Program', backref = 'courses')
    created_at = db.Column(db.DateTime , default=datetime.utcnow)
    updated_at = db.Column(db.DateTime , default=datetime.utcnow)

    def __init__(self , course_id , course_name , description , created_at , updated_at):
        super(Course , self).__init__()
        self.course_id = course_id
        self.course_name = course_name
        self.description = description
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self) ->str:
        return f'{self.course_name} {self.description}'
    

