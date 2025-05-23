from flask import Blueprint , request , jsonify
from app.status_codes import HTTP_400_BAD_REQUEST , HTTP_409_CONFLICT , HTTP_201_CREATED , HTTP_500_INTERNAL_SERVER_ERROR , HTTP_404_NOT_FOUND , HTTP_200_OK
from app.models.program_model import Program   
from app.extensions import db

#i am creating a blueprint for my model program 
program = Blueprint('program', __name__, url_prefix='/api/v1/program')

#i am creating an endpoint for creating a new program
@program.route('/create', methods=['POST'])
def createProgram():

  #storing request values 
    data = request.json
    program_name = data.get('program_name')
    description = data.get('description')

#validations for the request values
    if not program_name or not description:
        return ({'Error' : 'All fields are required'}), HTTP_400_BAD_REQUEST  # Bad request due to invalid syntax or parameters
    
    if Program.query.filter_by(program_name=program_name).first() is not None:
        return jsonify({'Error' : 'The program already exists'}),HTTP_409_CONFLICT #The request could not be processed because of a conflict
    
#creating the new program
    try:
        new_program = Program (
            program_name = program_name ,
            description =  description 
        )

        db.session.add(new_program)
        db.commit()

        return jsonify ({
            'Message' : 'Program has been successfully created' ,
            'program' :  {
                'program_name' :  new_program.program_name , 
                'description' :   new_program.description
            }
        }) , HTTP_201_CREATED #successful creation

    except Exception as e:
        db.session.rollback(str)
        return jsonify({'error':str(e)}) , HTTP_500_INTERNAL_SERVER_ERROR # error message for server failures
    
#Updating a program   
@program.route('/update/<int:program_id>', methods=['PUT'] ,  endpoint='update_program') # Defining a route for updating a program 
def update_program(program_id):
    
    try:
        
        program = Program.query.get(program_id) # Querying the database for the program  with the specified id
     
        if not program:
            return jsonify({'message': 'Program does not exist'}), HTTP_404_NOT_FOUND # The requested resource could not be found on the server
        
        else:
            data = request.get_json() # Extracting the JSON data
            program_name = data.get('program_name', program.program_name) # Extracting the program name from the JSON data
            description = data.get('description', program.description) # Extracting the description of the program from the JSON data
                 
            program.program_name = program_name
            program.description = description

            db.session.commit() # Committing the changes to the database
            
            return jsonify({
                'Message': program_name + ' has been updated successfully',
                'program': {
                    'program_name' : program.program_name,
                    'description' : program.description,
                    'updated_at' : program.updated_at}
                }), HTTP_200_OK #data has been returned successfully
            
    except Exception as e:
        return jsonify({'error': str(e)}), HTTP_500_INTERNAL_SERVER_ERROR # error message for server failures
 