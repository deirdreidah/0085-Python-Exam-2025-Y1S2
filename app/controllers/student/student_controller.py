from flask import Blueprint , request , jsonify
from app.status_codes import HTTP_400_BAD_REQUEST , HTTP_409_CONFLICT, HTTP_201_CREATED , HTTP_200_OK ,HTTP_500_INTERNAL_SERVER_ERROR , HTTP_404_NOT_FOUND
from app.models.student_model import Student
from app.extensions import db

#i am creating a blueprint for my model program 
student = Blueprint('student', __name__, url_prefix='/api/v1/student')

#i am creating an endpoint for creating a new program
@student.route('/create', methods=['POST'])
def createStudent():

  #storing request values 
    data = request.json
    student_name = data.get('student_name')
    email = data.get('email')
    contact =data.get('contact')
    gender = data.get('gender')

#validations for the request values
    if not student_name or not email or not contact or not gender:
        return ({'Error' : 'All fields are required'}), HTTP_400_BAD_REQUEST  # Bad request due to invalid syntax or parameters
    
    if Student.query.filter_by(student_name=student_name).first() is not None:
        return jsonify({'Error' : 'The student already exists'}),HTTP_409_CONFLICT #The request could not be processed because of a conflict
    
    if Student.query.filter_by(email=email).first() is not None:
        return jsonify({'Error' : 'Email is already in use.'}), HTTP_409_CONFLICT #The request could not be processed because of a conflict
    
    if Student.query.filter_by(contact=contact).first() is not None:
        return jsonify({'Error' : 'Contact is already in use.'}) , HTTP_409_CONFLICT #The request could not be processed because of a conflict
    
#creating the new student
    try:
        new_student = Student (
            student_name = student_name ,
            email =  email,
            contact = contact , 
            gender = gender 
        )

        db.session.add(new_student)
        db.commit()

        return jsonify ({
            'Message' : 'Student has been successfully created' ,
            'student' :  {
                'student_name' :  new_student.student_name , 
                'email' :   new_student.email ,
                'contact' : new_student.contact,
                'gender' : new_student.gender
            }
        }) , HTTP_201_CREATED #successful creation

    except Exception as e:
        db.session.rollback(str)
        return jsonify({'error':str(e)}) , HTTP_500_INTERNAL_SERVER_ERROR # error message for server failures
 
 #getting all students
@student.get('/get_all' , endpoint= 'get_all_students')
def get_all_students():

    try:
        all_students = Student.query.all()

        student_data = []
        for student in all_students:
            student_info = {
                'student_id' : student.student_id,
                'student_name': student.sudent_name,
                'email': student.email,
                'contact': student.contact,
                'gender': student.gender
            }
            student_data.append(student_info)
        return jsonify({
            'Message': 'All students retrieved',
            'students': student_data
        }),HTTP_200_OK #data has been returned successfully
    
    except Exception as e:
        return jsonify ({
            'Error': str(e)
        }),HTTP_500_INTERNAL_SERVER_ERROR # error message for server failures
    
#delete student
@student.route('/delete/<int:student_id>', methods=['DELETE'] ,  endpoint='delete_student') # Defining a route for deleting a student 
def delete_student(student_id):
    
    try:
        
        student = Student.query.get(student_id) 
        if not student:
            return jsonify({'message': 'Student does not exist'}), HTTP_404_NOT_FOUND # The requested resource could not be found on the server
         
        else:
            db.session.delete(student)
            db.session.commit()

            return jsonify({
                'message': 'Student has been deleted successfully'
                }) , HTTP_200_OK #data has been returned successfully
    except Exception as e:
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR # error message for server failures
    