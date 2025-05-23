from flask import Blueprint , request , jsonify
from status_codes import HTTP_400_BAD_REQUEST , HTTP_409_CONFLICT , HTTP_201_CREATED ,HTTP_500_INTERNAL_SERVER_ERROR
from app.models.course_model import Course
from app.extensions import db

#i am creating a blueprint for my model course
course = Blueprint('program', __name__, url_prefix='/api/v1/course')

#i am creating an endpoint for creating a new program
@course.route('/create', methods=['POST'])
def createCourse():

  #storing request values 
    data = request.json
    course_name = data.get('course_name')
    description = data.get('description')

#validations for the request values
    if not course_name or not description:
        return ({'Error' : 'All fields are required'}), HTTP_400_BAD_REQUEST  # Bad request due to invalid syntax or parameters
    
    if Course.query.filter_by(course_name=course_name).first() is not None:
        return jsonify({'Error' : 'The program already exists'}),HTTP_409_CONFLICT #The request could not be processed because of a conflict
    
#creating the new course
    try:
        new_course = Course (
            program_name = course_name ,
            description =  description 
        )

        db.session.add(new_course)
        db.commit()

        return jsonify ({
            'Message' : 'Course has been successfully created' ,
            'course' :  {
                'course_name' :  new_course.course_name , 
                'description' :   new_course.description
            }
        }) , HTTP_201_CREATED #successful creation

    except Exception as e:
        db.session.rollback(str)
        return jsonify({'error':str(e)}) , HTTP_500_INTERNAL_SERVER_ERROR # error message for server failures
 