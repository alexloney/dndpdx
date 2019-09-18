from flask import Flask, request, Response
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
from flask import jsonify
import json
import uuid

db_connect = create_engine('sqlite:///database.db')
app = Flask(__name__)
api = Api(app)

USERS_TABLE = 'Users'

def run_setup():
    conn = db_connect.connect()
    query = conn.execute("SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'Players'")
    result = query.fetchone()
    if result == None:
        query = conn.execute("""
            CREATE TABLE Players (
                kumoId Int,
                name varchar
            )""")
        query = conn.execute("""
            CREATE TABLE UserSessions (
                kumoId Int,
                session varchar,
                expiration date
            )
        """)
        

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

def update_session_expiration(session):
    conn = db_connect.connect()
    query = conn.execute("UPDATE UserSessions SET expiration = DATETIME(DATE('now'), '+5 minutes') WHERE session = '" + session + "'")

def generate_session_id(id):
    conn = db_connect.connect()
    query = conn.execute("DELETE FROM UserSessions WHERE expiration < date('now')")

    query = conn.execute("SELECT * FROM UserSessions WHERE kumoId = %d" % int(id))
    result = query.fetchone()
    if result != None:
        session_id = result.session
        update_session_expiration(session_id)
    else:
        session_id = str(uuid.uuid1())
        query = conn.execute("INSERT INTO UserSessions (kumoId, session, expiration) VALUES (" + str(int(id)) + ", '" + session_id + "', DATETIME(DATE('now'), '+5 minutes'))")

    return session_id

@app.route('/players/<kumo_id>')
def get_player(kumo_id):
    conn = db_connect.connect()
    query = conn.execute('SELECT * FROM Players WHERE kumoId = %d' %int(kumo_id))
    result = query.fetchone()
    if result == None:
        response_str = json.dumps({
            'errorMsg': 'User not registered'
        })
    else:
        response_str = json.dumps({
            'id': result.kumoId,
            'name': result.name,
            'sessionId': generate_session_id(result.kumoId)
        })

    resp = Response(response_str)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route('/players/register', methods=['POST'])
def register_player():
    kumoId = request.form.get('id')
    name = request.form.get('name')
    
    if kumoId == None or name == None:
        response_str = json.dumps({
            'errorMsg': 'Invalid ID or Name'
        })
        resp = Response(response_str)
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
    
    conn = db_connect.connect()
    query = conn.execute('SELECT * FROM Players WHERE kumoId = %d' %int(kumoId))
    result = query.fetchone()

    if result:
        response_str = json.dumps({
            'id': result.kumoId,
            'name': result.name,
            'session_id': generate_session_id(result.kumoId)
        })
        resp = Response(response_str)
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
    
    query = conn.execute("INSERT INTO Players (kumoId, name) VALUES (" + str(int(kumoId)) + ", '" + name + "')")

    response_str = json.dumps({
        'id': kumoId,
        'name': name,
        'sessionId': generate_session_id(kumoId)
    })
    resp = Response(response_str)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

if __name__ == '__main__':
    run_setup()
    app.run(debug=True, port='5002')