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
    query = conn.execute("DROP TABLE IF EXISTS Players")
    query = conn.execute("DROP TABLE IF EXISTS UserSessions")
    query = conn.execute("DROP TABLE IF EXISTS Days")
    query = conn.execute("DROP TABLE IF EXISTS GameSystems")
    query = conn.execute("DROP TABLE IF EXISTS DMs")
    query = conn.execute("DROP TABLE IF EXISTS Times")
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
                expiration date,
                admin int
            )
        """)
        query = conn.execute("""
            CREATE TABLE Days (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name varchar
            )
        """)
        query = conn.execute("""
            INSERT INTO Days (name) VALUES ('Friday')
        """)
        query = conn.execute("""
            INSERT INTO Days (name) VALUES ('Saturday')
        """)
        query = conn.execute("""
            INSERT INTO Days (name) VALUES ('Sunday')
        """)
        query = conn.execute("""
            CREATE TABLE GameSystems (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name varchar
            )
        """)
        query = conn.execute("""
            INSERT INTO GameSystems (name) VALUES ('D&D')
        """)
        query = conn.execute("""
            INSERT INTO GameSystems (name) VALUES ('Pathfinder')
        """)
        query = conn.execute("""
            INSERT INTO GameSystems (name) VALUES ('Starfinder')
        """)
        query = conn.execute("""
            INSERT INTO GameSystems (name) VALUES ('Shadowrun')
        """)
        query = conn.execute("""
            INSERT INTO GameSystems (name) VALUES ('DCC')
        """)
        query = conn.execute("""
            INSERT INTO GameSystems (name) VALUES ('MLP')
        """)

        query = conn.execute("""
            CREATE TABLE DMs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name varchar
            )
        """)
        conn.execute("""
            INSERT INTO DMs (name) VALUES ('Alex Loney');
        """)
        conn.execute("""
            INSERT INTO DMs (name) VALUES ('Peter');
        """)
        query = conn.execute("""
            CREATE TABLE Times (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name varchar
            )
        """)
        conn.execute("""
            INSERT INTO Times (name) VALUES ('9:00 AM');
        """)
        conn.execute("""
            INSERT INTO Times (name) VALUES ('10:00 AM');
        """)
        conn.execute("""
            INSERT INTO Times (name) VALUES ('11:00 AM');
        """)
        conn.execute("""
            INSERT INTO Times (name) VALUES ('12:00 PM');
        """)
        conn.execute("""
            INSERT INTO Times (name) VALUES ('1:00 PM');
        """)
        conn.execute("""
            INSERT INTO Times (name) VALUES ('2:00 PM');
        """)
        conn.execute("""
            INSERT INTO Times (name) VALUES ('3:00 PM');
        """)
        conn.execute("""
            INSERT INTO Times (name) VALUES ('4:00 PM');
        """)
        conn.execute("""
            INSERT INTO Times (name) VALUES ('5:00 PM');
        """)
        conn.execute("""
            INSERT INTO Times (name) VALUES ('6:00 PM');
        """)
        conn.execute("""
            INSERT INTO Times (name) VALUES ('7:00 PM');
        """)
        conn.execute("""
            INSERT INTO Times (name) VALUES ('8:00 PM');
        """)
        conn.execute("""
            INSERT INTO Times (name) VALUES ('9:00 PM');
        """)
        conn.execute("""
            INSERT INTO Times (name) VALUES ('10:00 PM');
        """)
        conn.execute("""
            INSERT INTO Times (name) VALUES ('11:00 PM');
        """)
        conn.execute("""
            INSERT INTO Times (name) VALUES ('12:00 AM');
        """)
        conn.execute("""
            INSERT INTO Times (name) VALUES ('1:00 AM');
        """)
        conn.execute("""
            INSERT INTO Times (name) VALUES ('2:00 AM');
        """)
        conn.execute("""
            INSERT INTO Times (name) VALUES ('3:00 AM');
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

    query = conn.execute("SELECT * FROM UserSessions WHERE kumoId = :i", i=int(id))
    result = query.fetchone()
    if result != None:
        session_id = result.session
        update_session_expiration(session_id)
    else:
        session_id = str(uuid.uuid1())
        query = conn.execute("INSERT INTO UserSessions (kumoId, session, expiration) VALUES (:i, :s, DATETIME(DATE('now'), '+5 minutes'))", i=int(id), s=session_id)
        # conn.commit()

    return session_id

def validate_session(session_id):
    if session_id == None:
        return False

    conn = db_connect.connect()
    query = conn.execute("SELECT * FROM UserSessions WHERE session = :s AND expiration > date('now')", s=session_id)

    result = query.fetchone()
    if result == None:
        return False
    return True

@app.route('/players/<kumo_id>')
def get_player(kumo_id):
    print('Looking up player with ID ' + kumo_id)
    conn = db_connect.connect()
    query = conn.execute('SELECT * FROM Players WHERE kumoId = :i', i=int(kumo_id))
    
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
    query = conn.execute('SELECT * FROM Players WHERE kumoId = :i', i=int(kumoId))
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

    query = conn.execute("INSERT INTO Players (kumoId, name) VALUES (:i, :n)", i=int(kumoId), n=name)
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

    if not validate_session(session_id):
        response_str = json.dumps({
            'errorMsg': 'Invalid session, please log in first.'
        })
        return get_standard_response(response_str)
    
    query = conn.execute("SELECT * FROM GameSystems ORDER BY name")
    rows = query.fetchall()

    response_obj = {
        'results': [

        ]
    }
    for row in rows:
        response_obj['results'].append({'id': row.id, 'name': row.name})
    
    response_str = json.dumps(response_obj)
    return get_standard_response(response_str)

@app.route('/search/dms', methods=['GET'])
def search_dms():
    session_id = request.headers.get('Authorization')
    print(session_id)

    conn = db_connect.connect()
    query = conn.execute('SELECT id, name FROM DMs ORDER BY id')

    response_obj = {
        'results': [

        ]
    }
    rows = query.fetchall()
    for row in rows:
        response_obj['results'].append({'id': row.id, 'name': row.name})
    
    response_str = json.dumps(response_obj)
    return get_standard_response(response_str)

@app.route('/search/days', methods=['GET'])
def search_days():
    session_id = request.headers.get('Authorization')
    print(session_id)

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
    session_id = request.headers.get('Authorization')
    print(session_id)

    conn = db_connect.connect()
    query = conn.execute('SELECT id, name FROM Times ORDER BY id')

    response_obj = {
        'results': [

        ]
    }
    rows = query.fetchall()
    for row in rows:
        response_obj['results'].append({'id': row.id, 'name': row.name})
    
    response_str = json.dumps(response_obj)
    return get_standard_response(response_str)

@app.route('/logout', methods=['POST'])
def logout():
    session_id = request.headers.get('Authorization')
    print(session_id)

    conn = db_connect.connect()
    query = conn.execute('DELETE FROM UserSessions WHERE session = :s', s=session_id)

    response_str = json.dumps({})
    return get_standard_response(response_str)

if __name__ == '__main__':
    run_setup()
    app.run(debug=True, port='5002')