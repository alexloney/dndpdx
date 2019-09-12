from flask import Flask, request, Response
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
from flask import jsonify
import json

db_connect = create_engine('sqlite:///database.db')
app = Flask(__name__)
api = Api(app)

USERS_TABLE = 'Users'

def run_setup():
    conn = db_connect.connect()
    query = conn.execute("SELECT name FROM sqlite_master WHERE type = 'table' AND name = '" + USERS_TABLE + "'")
    result = query.fetchone()
    if result == None:
        print('Creating tables')

        

class Employees(Resource):
    def get(self):
        return {'test': 'string'}
        # conn = db_connect.connect() # connect to database
        # query = conn.execute("select * from employees") # This line performs query and returns json result
        # return {'employees': [i[0] for i in query.cursor.fetchall()]} # Fetches first column that is Employee ID

class Tracks(Resource):
    def get(self):
        # conn = db_connect.connect()
        # query = conn.execute("select trackid, name, composer, unitprice from tracks;")
        # result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        # return jsonify(result)
        return {'test2': 'string2'}

class Employees_Name(Resource):
    def get(self, employee_id):
        # conn = db_connect.connect()
        # query = conn.execute("select * from employees where EmployeeId =%d "  %int(employee_id))
        # result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        # return jsonify(result)
        return {'test3': employee_id}
        
class Users(Resource):
    def get(self, user_id):
        response_str = json.dumps({
            'id': user_id,
            'name': 'Alex Loney'
        })
        resp = Response(response_str)
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp

api.add_resource(Users, '/users/<user_id>')

api.add_resource(Employees, '/employees') # Route_1
api.add_resource(Tracks, '/tracks') # Route_2
api.add_resource(Employees_Name, '/employees/<employee_id>') # Route_3


if __name__ == '__main__':
    run_setup()
    app.run(port='5002')