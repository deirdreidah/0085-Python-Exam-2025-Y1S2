from app.extensions import db
from datetime import datetime

class Student(db.Model):
    __tablename__ = 'students'
    student_id = db.Column(db.Integer , primary_key = True , nullable = False)
    student_name = db.Column(db.String(255) , nullable= False)
    email = db.Column(db.String(255) , nullable = False , unique = True)
    contact = db.Column(db.String(255), nullable = False , unique = True)
    gender = db.Column(db.String(255), nullable = False)
    program_id = db.Column(db.Integer , db.ForeignKey('programs.program_id'), nullable = False)
    program = db.relationship('Program', backref = 'students')
    course_id = db.Column(db.Integer , db.ForeignKey('courses.course_id'), nullable = False)
    course = db.relationship('Course', backref = 'students')
    created_at = db.Column(db.DateTime , default=datetime.utcnow)
    updated_at = db.Column(db.DateTime , default=datetime.utcnow)

    def __init__(self , student_id , student_name , email , contact , gender , created_at, updated_at):
        super(Student , self).__init__()
        self.student_id = student_id
        self.student_name = student_name
        self.email = email
        self.contact = contact
        self.gender = gender
        self.created_at = created_at
        self.updated_at = updated_at

    def __repr__(self) -> str: 
        return f'{self.student_name} {self.email}'