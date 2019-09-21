from flask import Flask, request, Response
from flask_cors import CORS
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
from flask import jsonify
import json
import uuid

db_connect = create_engine('sqlite:///database2.db')
app = Flask(__name__)
CORS(app)
api = Api(app)

USERS_TABLE = 'Users'

# def print_table(table):
#     conn = db_connect.connect()
#     query = conn.execute("SELECT * FROM " + table)

#     print(table + ' Contents:')
#     for row in query:
#         for key in row.keys():
#             print(row[key], end='')
#         print('')

def run_setup():
    conn = db_connect.connect()
    # query = conn.execute("DROP TABLE Players")
    # query = conn.execute("DROP TABLE UserSessions")
    # query = conn.execute("DROP TABLE Days")
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
        query = conn.execute("""
            CREATE TABLE Days (
                id int,
                name varchar
            )
        """)
        query = conn.execute("""
            INSERT INTO Days (id, name) VALUES (1, 'Friday')
        """)
        query = conn.execute("""
            INSERT INTO Days (id, name) VALUES (2, 'Saturday')
        """)
        query = conn.execute("""
            INSERT INTO Days (id, name) VALUES (3, 'Sunday')
        """)
    
    # print_table('Players')

def get_standard_response(response_str):
    resp = Response(response_str)
    # resp.headers['Access-Control-Allow-Origin'] = '*'
    # resp.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, PUT, OPTIONS, DELETE, PATCH'
    # resp.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept, Authorization'
 
    return resp

def update_session_expiration(session):
    conn = db_connect.connect()
    query = conn.execute("UPDATE UserSessions SET expiration = DATETIME(DATE('now'), '+5 minutes') WHERE session = '" + session + "'")
    # conn.commit()

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
        # conn.commit()

    return session_id

@app.route('/players/<kumo_id>')
def get_player(kumo_id):
    print(kumo_id)
    conn = db_connect.connect()
    query = conn.execute('SELECT * FROM Players WHERE kumoId = %d' %int(kumo_id))
    
    result = query.fetchone()
    if result == None:
        print('Kumo ID not found...')
        response_str = json.dumps({
            'errorMsg': 'User not registered'
        })
    else:
        print('Kumo ID found!')
        response_str = json.dumps({
            'id': result.kumoId,
            'name': result.name,
            'sessionId': generate_session_id(result.kumoId)
        })

    return get_standard_response(response_str)

@app.route('/players/register', methods=['POST'])
def register_player():
    kumoId = request.form.get('id')
    name = request.form.get('name')

    print('Request to register ' + name + ' with ID ' + kumoId)
    
    if kumoId == None or name == None:
        print('User info invalid')
        response_str = json.dumps({
            'errorMsg': 'Invalid ID or Name'
        })
        return get_standard_response(response_str)
    
    conn = db_connect.connect()
    query = conn.execute('SELECT * FROM Players WHERE kumoId = %d' %int(kumoId))
    result = query.fetchone()
    print('Searching for existing user')

    if result:
        print('Existing user found')
        response_str = json.dumps({
            'id': result.kumoId,
            'name': result.name,
            'session_id': generate_session_id(result.kumoId)
        })
        return get_standard_response(response_str)

    query = conn.execute("INSERT INTO Players (kumoId, name) VALUES (" + str(int(kumoId)) + ", '" + name + "')")
    print('Adding user to database')

    response_str = json.dumps({
        'id': kumoId,
        'name': name,
        'sessionId': generate_session_id(kumoId)
    })
    return get_standard_response(response_str)

@app.route('/search/systems', methods=['GET'])
def search_systems():
    conn = db_connect.connect()

    session_id = request.headers.get('Authorization')
    print(session_id)
    # TODO: Validate session id

    # query = conn.execute('SELECT * FROM GameSystems ORDER BY name')
    # response_obj = {

    # }
    # while result = query.fetchone():
    
    response_str = json.dumps({
        'test': 'test'
    })
    return get_standard_response(response_str)

@app.route('/search/dms', methods=['GET'])
def search_dms():
    response_str = json.dumps({
        'test': 'test'
    })
    return get_standard_response(response_str)

@app.route('/search/days', methods=['GET'])
def search_days():
    conn = db_connect.connect()
    query = conn.execute('SELECT id, name FROM Days ORDER BY id')

    response_obj = {
        'results': [

        ]
    }
    rows = query.fetchall()
    for row in rows:
        response_obj['results'].append({'id': row.id, 'name': row.name})
    
    response_str = json.dumps(response_obj)
    return get_standard_response(response_str)

@app.route('/search/times', methods=['GET'])
def search_times():
    response_str = json.dumps({
        'test': 'test'
    })
    return get_standard_response(response_str)

if __name__ == '__main__':
    run_setup()
    app.run(debug=True, port='5002')