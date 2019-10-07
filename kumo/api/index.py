from flask import Flask, request, Response
from flask_cors import CORS
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
from flask import jsonify
import json
import uuid

db_connect = create_engine('sqlite:///database3.db')
# mysql+mysqlconnector://<user>:<password>@<host>:<port>/<default_db>
# db_connect = create_engine('mysql+mysqldb://')
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
    query = conn.execute("DROP TABLE IF EXISTS Games")
    query = conn.execute("DROP TABLE IF EXISTS GameRegister")
    query = conn.execute("SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'Players'")
    result = query.fetchone()
    if result == None:
        conn.execute("""
            CREATE TABLE Players (
                kumoId Int,
                name varchar,
                admin INTEGER,
                dm INTEGER
            )""")
        conn.execute("""
            INSERT INTO Players (kumoId, name, admin, dm) VALUES (1, 'Alex Loney', 1, 1)
        """)
        conn.execute("""
            INSERT INTO Players (kumoId, name, admin, dm) VALUES (2, 'Peter H', 0, 1)
        """)
        conn.execute("""
            CREATE TABLE UserSessions (
                kumoId Int,
                session varchar,
                expiration date,
                admin int,
                FOREIGN KEY(kumoId) REFERENCES Players(kumoId)
            )
        """)
        conn.execute("""
            CREATE TABLE Days (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name varchar,
                sort INTEGER
            )
        """)
        conn.execute("""
            INSERT INTO Days (name, sort) VALUES ('Friday', 1)
        """)
        conn.execute("""
            INSERT INTO Days (name, sort) VALUES ('Saturday', 2)
        """)
        conn.execute("""
            INSERT INTO Days (name, sort) VALUES ('Sunday', 3)
        """)
        conn.execute("""
            CREATE TABLE GameSystems (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name varchar, 
                sort INTEGER
            )
        """)
        conn.execute("""
            INSERT INTO GameSystems (name, sort) VALUES ('D&D', 1)
        """)
        conn.execute("""
            INSERT INTO GameSystems (name, sort) VALUES ('Pathfinder', 2)
        """)
        conn.execute("""
            INSERT INTO GameSystems (name, sort) VALUES ('Starfinder', 3)
        """)
        conn.execute("""
            INSERT INTO GameSystems (name, sort) VALUES ('Shadowrun', 4)
        """)
        conn.execute("""
            INSERT INTO GameSystems (name, sort) VALUES ('DCC', 5)
        """)
        conn.execute("""
            INSERT INTO GameSystems (name, sort) VALUES ('MLP', 6)
        """)
        conn.execute("""
            CREATE TABLE Times (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name varchar,
                sort INTEGER
            )
        """)
        conn.execute("""
            INSERT INTO Times (name, sort) VALUES ('9:00 AM', 1);
        """)
        conn.execute("""
            INSERT INTO Times (name, sort) VALUES ('10:00 AM', 2);
        """)
        conn.execute("""
            INSERT INTO Times (name, sort) VALUES ('11:00 AM', 3);
        """)
        conn.execute("""
            INSERT INTO Times (name, sort) VALUES ('12:00 PM', 4);
        """)
        conn.execute("""
            INSERT INTO Times (name, sort) VALUES ('1:00 PM', 5);
        """)
        conn.execute("""
            INSERT INTO Times (name, sort) VALUES ('2:00 PM', 6);
        """)
        conn.execute("""
            INSERT INTO Times (name, sort) VALUES ('3:00 PM', 7);
        """)
        conn.execute("""
            INSERT INTO Times (name, sort) VALUES ('4:00 PM', 8);
        """)
        conn.execute("""
            INSERT INTO Times (name, sort) VALUES ('5:00 PM', 9);
        """)
        conn.execute("""
            INSERT INTO Times (name, sort) VALUES ('6:00 PM', 10);
        """)
        conn.execute("""
            INSERT INTO Times (name, sort) VALUES ('7:00 PM', 11);
        """)
        conn.execute("""
            INSERT INTO Times (name, sort) VALUES ('8:00 PM', 12);
        """)
        conn.execute("""
            INSERT INTO Times (name, sort) VALUES ('9:00 PM', 13);
        """)
        conn.execute("""
            INSERT INTO Times (name, sort) VALUES ('10:00 PM', 14);
        """)
        conn.execute("""
            INSERT INTO Times (name, sort) VALUES ('11:00 PM', 15);
        """)
        conn.execute("""
            INSERT INTO Times (name, sort) VALUES ('12:00 AM', 16);
        """)
        conn.execute("""
            INSERT INTO Times (name, sort) VALUES ('1:00 AM', 17);
        """)
        conn.execute("""
            INSERT INTO Times (name, sort) VALUES ('2:00 AM', 18);
        """)
        conn.execute("""
            INSERT INTO Times (name, sort) VALUES ('3:00 AM', 19);
        """)
        conn.execute("""
            CREATE TABLE Games (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR,
                description VARCHAR,
                systemid INTEGER,
                dayid INTEGER,
                timeid INTEGER,
                dmid INTEGER,
                seats INTEGER,
                waitlist INTEGER,
                FOREIGN KEY(systemid) REFERENCES GameSystems(id),
                FOREIGN KEY(dayid) REFERENCES Days(id),
                FOREIGN KEY(timeid) REFERENCES Times(id),
                FOREIGN KEY(dmid) REFERENCES Players(id)
            )
        """)
        conn.execute("""
            INSERT INTO Games (name, description, systemid, dayid, timeid, dmid, seats, waitlist) VALUES ('DDEX1-08 Tales Trees Tell', 'Despite the shaky alliance that exists with the elves of the Quivering Forest, they do not suffer trespass in their realm lightly, especially from common folk from nearby Phlan. A woodworker''s recent blunder into the forest might set off a diplomatic incident. Can you help find him and mollify the aggravated elves?', 1, 1, 1, 1, 7, 4)
        """)
        conn.execute("""
            INSERT INTO Games (name, description, systemid, dayid, timeid, dmid, seats, waitlist) VALUES ('DDEX1-09 Outlaws of the Iron Route', 'The Iron Route, an important trade road east of Phlan, is beset by competing bandits. An exiled Black Fist officer leads his band of mercenaries turned cloaked ruffians, while a mysterious dragonborn sorcerer commands screaming savages from the north. In this war over the trade route, the beleaguered merchants are the victims, and Phlan suffers from a lack of supplies. It''s up to adventurers to strike out and reopen this vital route.', 1, 1, 1, 2, 7, 4)
        """)
        conn.execute("""
            CREATE TABLE GameRegister (
                kumoId INTEGER,
                gameId INTEGER,
                registered DATETIME,
                FOREIGN KEY(kumoId) REFERENCES Players(kumoId),
                FOREIGN KEY(gameId) REFERENCES Games(id)
            )
        """)
        conn.execute("""
            INSERT INTO GameRegister (kumoId, gameId, registered) VALUES (1, 1, date('now'))
        """)
        conn.execute("""
            INSERT INTO GameRegister (kumoId, gameId, registered) VALUES (1, 1, date('now'))
        """)
        conn.execute("""
            INSERT INTO GameRegister (kumoId, gameId, registered) VALUES (1, 1, date('now'))
        """)
        conn.execute("""
            INSERT INTO GameRegister (kumoId, gameId, registered) VALUES (1, 1, date('now'))
        """)
        conn.execute("""
            INSERT INTO GameRegister (kumoId, gameId, registered) VALUES (1, 1, date('now'))
        """)
        conn.execute("""
            INSERT INTO GameRegister (kumoId, gameId, registered) VALUES (1, 1, date('now'))
        """)
        conn.execute("""
            INSERT INTO GameRegister (kumoId, gameId, registered) VALUES (1, 1, date('now'))
        """)
        conn.execute("""
            INSERT INTO GameRegister (kumoId, gameId, registered) VALUES (1, 1, date('now'))
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
    print('Generating Session ID')
    conn = db_connect.connect()

    print('Deleting expired sessions')
    query = conn.execute("DELETE FROM UserSessions WHERE expiration < date('now')")
    query.close()

    print('Finding the users session')
    query = conn.execute("SELECT * FROM UserSessions WHERE kumoId = :i", i=int(id))
    result = query.fetchone()
    query.close()

    if result != None:
        print('Existing session found, reusing')
        session_id = result.session
        update_session_expiration(session_id)
    else:
        print('Generating new session')
        session_id = str(uuid.uuid1())
        query = conn.execute("INSERT INTO UserSessions (kumoId, session, expiration) VALUES (:i, :s, DATETIME(DATE('now'), '+5 minutes'))", i=int(id), s=session_id)
        # conn.commit()

    return session_id

def validate_session(session_id):
    
    # Debug code REMOVE WHEN I NPRODUCTION
    return True

    if session_id == None:
        return False

    conn = db_connect.connect()
    query = conn.execute("SELECT * FROM UserSessions WHERE session = :s AND expiration > date('now')", s=session_id)
    result = query.fetchone()
    query.close()

    if result == None:
        return False
    return True

def session_is_admin(player_id):

    if player_id == None:
        return False

    conn = db_connect.connect()
    query = conn.execute('SELECT COUNT(*) AS cnt FROM Players WHERE kumoId = :i AND admin = 1', i = player_id)
    result = query.fetchone()
    query.close()

    if result == None:
        return False
    
    if int(result['cnt']) == 1:
        return True
    
    return False

def get_player_id(session_id):
    if session_id == None:
        return False
    
    conn = db_connect.connect()
    query = conn.execute('SELECT kumoId FROM UserSessions WHERE session = :s', s=session_id)
    result = query.fetchone()
    query.close()

    if result == None:
        return False
    
    return result['kumoId']

@app.route('/players/<kumo_id>')
def get_player(kumo_id):
    print('Looking up player with ID ' + kumo_id)
    conn = db_connect.connect()
    query = conn.execute('SELECT * FROM Players WHERE kumoId = :i', i=int(kumo_id))
    result = query.fetchone()
    query.close()
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
            'admin': result.admin,
            'dm': result.dm,
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
    query.close()
    print('Searching for existing user')

    if result:
        print('Existing user found')
        response_str = json.dumps({
            'id': result.kumoId,
            'name': result.name,
            'session_id': generate_session_id(result.kumoId)
        })
        return get_standard_response(response_str)

    query = conn.execute("INSERT INTO Players (kumoId, name, admin, dm) VALUES (:i, :n, 0, 0)", i=int(kumoId), n=name)
    query.close()
    print('Adding user to database')

    response_str = json.dumps({
        'id': kumoId,
        'name': name,
        'sessionId': generate_session_id(kumoId)
    })
    return get_standard_response(response_str)

@app.route('/search/systems', methods=['GET'])
def search_systems():
    session_id = request.headers.get('Authorization')
    print(session_id)

    if not validate_session(session_id):
        response_str = json.dumps({
            'errorMsg': 'Invalid session, please log in first.'
        })
        return get_standard_response(response_str)
    
    conn = db_connect.connect()

    query = conn.execute("SELECT * FROM GameSystems ORDER BY name")
    rows = query.fetchall()
    query.close()

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

    if not validate_session(session_id):
        response_str = json.dumps({
            'errorMsg': 'Invalid session, please log in first.'
        })
        return get_standard_response(response_str)

    conn = db_connect.connect()
    query = conn.execute('SELECT kumoId, name FROM Players WHERE dm = 1 ORDER BY name')
    rows = query.fetchall()
    query.close()

    response_obj = {
        'results': [

        ]
    }
    for row in rows:
        response_obj['results'].append({'id': row.kumoId, 'name': row.name})
    
    response_str = json.dumps(response_obj)
    return get_standard_response(response_str)

@app.route('/search/days', methods=['GET'])
def search_days():
    session_id = request.headers.get('Authorization')
    print(session_id)

    if not validate_session(session_id):
        response_str = json.dumps({
            'errorMsg': 'Invalid session, please log in first.'
        })
        return get_standard_response(response_str)

    conn = db_connect.connect()
    query = conn.execute('SELECT id, name FROM Days ORDER BY id')
    rows = query.fetchall()
    query.close()

    response_obj = {
        'results': [

        ]
    }
    for row in rows:
        response_obj['results'].append({'id': row.id, 'name': row.name})
    
    response_str = json.dumps(response_obj)
    return get_standard_response(response_str)

@app.route('/search/times', methods=['GET'])
def search_times():
    session_id = request.headers.get('Authorization')
    print(session_id)

    if not validate_session(session_id):
        response_str = json.dumps({
            'errorMsg': 'Invalid session, please log in first.'
        })
        return get_standard_response(response_str)

    conn = db_connect.connect()
    query = conn.execute('SELECT id, name FROM Times ORDER BY id')
    rows = query.fetchall()
    query.close()

    response_obj = {
        'results': [

        ]
    }
    for row in rows:
        response_obj['results'].append({'id': row.id, 'name': row.name})
    
    response_str = json.dumps(response_obj)
    return get_standard_response(response_str)

@app.route('/games/all', methods=['GET'])
def get_all_games():
    session_id = request.headers.get('Authorization')
    print(session_id)

    if not validate_session(session_id):
        response_str = json.dumps({
            'errorMsg': 'Invalid session, please log in first.'
        })
        return get_standard_response(response_str)

    conn = db_connect.connect()
    query = conn.execute("""
        SELECT a.id,
               a.name,
               a.description,
               a.seats,
               a.waitlist,
               b.name AS system,
               b.id AS systemid,
               c.name AS day,
               c.id AS dayid,
               d.name AS time,
               d.id AS timeid,
               e.name AS dm,
               e.kumoId AS dmid
          FROM Games a 
          JOIN GameSystems b 
            ON a.systemid = b.id
          JOIN Days c
            ON a.dayid = c.id
          JOIN Times d
            ON a.timeid = d.id
          JOIN Players e
            ON a.dmid = e.kumoId
         ORDER BY c.sort, d.sort, b.sort
    """)
    rows = query.fetchall()
    query.close()

    response_obj = {
        'results': [

        ]
    }
    for row in rows:
        print('Row ID: ' + str(row.id))
        obj = {'id': row.id,
            'name': row.name,
            'description': row.description,
            'seats': row.seats,
            'waitlist': row.waitlist,
            'system': {
                'id': row.systemid,
                'name': row.system
            },
            'day': {
                'id': row.dayid,
                'name': row.day
            },
            'time': {
                'id': row.timeid,
                'name': row.time
            },
            'dm': {
                'id': row.dmid,
                'name': row.dm
            },
            'players': []}
        query = conn.execute("""
            SELECT a.kumoId, b.name
              FROM GameRegister a
              JOIN Players b
                ON a.kumoId = b.kumoId
             WHERE gameId = :g
            ORDER BY registered
        """, g=row.id)
        players = query.fetchall()
        query.close()

        for player in players:
            player = {
                'id': player.kumoId,
                'name': player.name
            }
            obj['players'].append(player)

        response_obj['results'].append(obj)
    
    response_str = json.dumps(response_obj)
    return get_standard_response(response_str)

@app.route('/games/id/<id>', methods=['GET'])
def get_game_by_id(id):
    session_id = request.headers.get('Authorization')
    print(session_id)

    if not validate_session(session_id):
        response_str = json.dumps({
            'errorMsg': 'Invalid session, please log in first.'
        })
        return get_standard_response(response_str)
    
    conn = db_connect.connect()
    query = conn.execute("""
        SELECT a.id,
               a.name,
               a.description,
               a.seats,
               a.waitlist,
               b.name AS system,
               b.id AS systemid,
               c.name AS day,
               c.id AS dayid,
               d.name AS time,
               d.id AS timeid,
               e.name AS dm,
               e.kumoId AS dmid
          FROM Games a 
          JOIN GameSystems b 
            ON a.systemid = b.id
          JOIN Days c
            ON a.dayid = c.id
          JOIN Times d
            ON a.timeid = d.id
          JOIN Players e
            ON a.dmid = e.kumoId
         WHERE a.id = :g
         ORDER BY c.sort, d.sort, b.sort
    """, g=id)
    row = query.fetchone()
    query.close()

    if not row:
        response_str = json.dumps({
            'errorMsg': 'Unable to locate game with id ' + str(id)
        })
        return get_standard_response(response_str)

    response_obj = {
        'results': [

        ]
    }
    obj = {'id': row.id,
        'name': row.name,
        'description': row.description,
        'seats': row.seats,
        'waitlist': row.waitlist,
        'system': {
            'id': row.systemid,
            'name': row.system
        },
        'day': {
            'id': row.dayid,
            'name': row.day
        },
        'time': {
            'id': row.timeid,
            'name': row.time
        },
        'dm': {
            'id': row.dmid,
            'name': row.dm
        },
        'players': []}
    query = conn.execute("""
        SELECT a.kumoId, b.name
            FROM GameRegister a
            JOIN Players b
            ON a.kumoId = b.kumoId
            WHERE gameId = :g
        ORDER BY registered
    """, g=row.id)
    players = query.fetchall()
    query.close()
    for player in players:
        player = {
            'id': player.kumoId,
            'name': player.name
        }
        obj['players'].append(player)

    response_obj['results'].append(obj)
    
    response_str = json.dumps(response_obj)
    return get_standard_response(response_str)

@app.route('/games/mine')
def get_my_games():
    session_id = request.headers.get('Authorization')
    print(session_id)

    if not validate_session(session_id):
        response_str = json.dumps({
            'errorMsg': 'Invalid session, please log in first.'
        })
        return get_standard_response(response_str)

    player_id = get_player_id(session_id)
    if player_id == False:
        response_str = json.dumps({
            'errorMsg': 'Invalid session, please log in first.'
        })
        return get_standard_response(response_str)
    
    conn = db_connect.connect()
    query = conn.execute("""
        SELECT DISTINCT
               a.id,
               a.name,
               a.description,
               a.seats,
               a.waitlist,
               b.name AS system,
               b.id AS systemid,
               c.name AS day,
               c.id AS dayid,
               d.name AS time,
               d.id AS timeid,
               e.name AS dm,
               e.kumoId AS dmid
          FROM Games a 
          JOIN GameSystems b 
            ON a.systemid = b.id
          JOIN Days c
            ON a.dayid = c.id
          JOIN Times d
            ON a.timeid = d.id
          JOIN Players e
            ON a.dmid = e.kumoId
          JOIN GameRegister f
            ON a.id = f.gameId
         WHERE f.kumoId = :i
         ORDER BY c.sort, d.sort, b.sort
    """, i = player_id)
    rows = query.fetchall()
    query.close()

    response_obj = {
        'results': [

        ]
    }
    for row in rows:
        obj = {'id': row.id,
            'name': row.name,
            'description': row.description,
            'seats': row.seats,
            'waitlist': row.waitlist,
            'system': {
                'id': row.systemid,
                'name': row.system
            },
            'day': {
                'id': row.dayid,
                'name': row.day
            },
            'time': {
                'id': row.timeid,
                'name': row.time
            },
            'dm': {
                'id': row.dmid,
                'name': row.dm
            },
            'players': []}
        query = conn.execute("""
            SELECT a.kumoId, b.name
              FROM GameRegister a
              JOIN Players b
                ON a.kumoId = b.kumoId
             WHERE gameId = :g
            ORDER BY registered
        """, g=row.id)
        players = query.fetchall()
        query.close()

        for player in players:
            player = {
                'id': player.kumoId,
                'name': player.name
            }
            obj['players'].append(player)

        response_obj['results'].append(obj)
    
    response_str = json.dumps(response_obj)
    return get_standard_response(response_str)


@app.route('/games/register/<id>', methods=['POST'])
def registerForGame(id):
    session_id = request.headers.get('Authorization')
    print(session_id)

    if not validate_session(session_id):
        response_str = json.dumps({
            'errorMsg': 'Invalid session, please log in first.'
        })
        return get_standard_response(response_str)

    player_id = get_player_id(session_id)
    if player_id == False:
        response_str = json.dumps({
            'errorMsg': 'Invalid session, please log in first.'
        })
        return get_standard_response(response_str)
    
    conn = db_connect.connect()
    query = conn.execute('SELECT COUNT(*) AS cnt FROM GameRegister WHERE kumoId = :k AND gameId = :g', k=player_id, g=id)
    result = query.fetchone()
    query.close()

    if result == None:
        response_str = json.dumps({
            'errorMsg': 'Unable to determine registration'
        })
        return get_standard_response(response_str)
    
    if int(result['cnt']) != 0:
        response_str = json.dumps({
            'errorMsg': 'User already registered'
        })
        return get_standard_response(response_str)

    query = conn.execute("INSERT INTO GameRegister (kumoId, gameId, registered) VALUES (:k, :g, date('now'))", k=player_id, g=id)
    query.close()

    response_str = json.dumps({
        'success': True
    })
    return get_standard_response(response_str)

@app.route('/games/deregister/<id>', methods=['POST'])
def deRegisterForGame(id):
    session_id = request.headers.get('Authorization')
    print(session_id)

    if not validate_session(session_id):
        response_str = json.dumps({
            'errorMsg': 'Invalid session, please log in first.'
        })
        return get_standard_response(response_str)

    player_id = get_player_id(session_id)
    if player_id == False:
        response_str = json.dumps({
            'errorMsg': 'Invalid session, please log in first.'
        })
        return get_standard_response(response_str)
    
    conn = db_connect.connect()
    query = conn.execute('SELECT COUNT(*) AS cnt FROM GameRegister WHERE kumoId = :k AND gameId = :g', k=player_id, g=id)
    result = query.fetchone()
    query.close()

    if result == None:
        response_str = json.dumps({
            'errorMsg': 'Unable to determine registration'
        })
        return get_standard_response(response_str)
    
    if int(result['cnt']) != 0:
        conn.execute("DELETE FROM GameRegister WHERE kumoId = :k AND gameId = :g", k=player_id, g=id)
        query.close()

    query = conn.execute('SELECT COUNT(*) AS cnt FROM GameRegister WHERE kumoId = :k AND gameId = :g', k=player_id, g=id)
    result = query.fetchone()
    query.close()

    if result == None:
        response_str = json.dumps({
            'errorMsg': 'Unable to determine registration'
        })
        return get_standard_response(response_str)
    elif int(result['cnt']) != 0:
        response_str = json.dumps({
            'errorMsg': 'Failed to remove registration'
        })
        return get_standard_response(response_str)

    response_str = json.dumps({
        'success': True
    })
    return get_standard_response(response_str)

@app.route('/games/registered/<id>', methods=['GET'])
def is_user_registered(id):
    session_id = request.headers.get('Authorization')
    print(session_id)

    if not validate_session(session_id):
        response_str = json.dumps({
            'errorMsg': 'Invalid session, please log in first.'
        })
        return get_standard_response(response_str)

    player_id = get_player_id(session_id)
    if player_id == False:
        response_str = json.dumps({
            'errorMsg': 'Invalid session, please log in first.'
        })
        return get_standard_response(response_str)
    
    conn = db_connect.connect()
    query = conn.execute('SELECT COUNT(*) AS cnt FROM GameRegister WHERE kumoId = :k AND gameId = :g', k=player_id, g=id)
    result = query.fetchone()
    query.close()

    if result == None:
        response_str = json.dumps({
            'errorMsg': 'Unable to determine registration'
        })
        return get_standard_response(response_str)
    
    if int(result['cnt']) == 0:
        response_str = json.dumps({
            'registered': False
        })
        return get_standard_response(response_str)
    
    response_str = json.dumps({
        'registered': True
    })
    return get_standard_response(response_str)

@app.route('/games/update/<id>', methods=['POST'])
def update_game(id):
    session_id = request.headers.get('Authorization')
    print(session_id)

    print('Validating Session ID')
    if not validate_session(session_id):
        response_str = json.dumps({
            'errorMsg': 'Invalid session, please log in first.'
        })
        return get_standard_response(response_str)
    
    print('Getting player ID')
    player_id = get_player_id(session_id)
    if player_id == False:
        response_str = json.dumps({
            'errorMsg': 'Invalid session, please log in first.'
        })
        return get_standard_response(response_str)

    print('Validating that user is an admin')
    if not session_is_admin(player_id):
        response_str = json.dumps({
            'errorMsg': 'Only Admin may perform this action.'
        })
        return get_standard_response(response_str)
    
    data = request.get_json()
    print(data)

    conn = db_connect.connect()

    if int(data['system']['id']) == 0:
        query = conn.execute("""
            SELECT id, name FROM GameSystems WHERE name = :n
        """, n = data['system']['name'])
        result = query.fetchone()
        query.close()

        if result:
            data['system']['id'] = result['id']
        else:
            query = conn.execute("""
                INSERT INTO GameSystems (name) VALUES (:n)
            """, n = data['system']['name'])
            query.close()

            query = conn.execute("""
                SELECT id, name FROM GameSystems WHERE name = :n
            """, n = data['system']['name'])
            result = query.fetchone()
            query.close()

            if result:
                data['system']['id'] = result['id']
            else:
                response_str = json.dumps({
                    'errorMsg': 'Unable to create new game system.'
                })
                return get_standard_response(response_str)

    
    query = conn.execute("""
        SELECT kumoId, name FROM Players WHERE kumoId = :i
    """, i = data['dm']['id'])
    result = query.fetchone()
    query.close()

    if not result:
        query = conn.execute("""
            INSERT INTO Players (kumoId, name, dm) VALUES (:i, :n, 1)
        """, i = data['dm']['id'], n = data['dm']['name'])
        query.close()

        query = conn.execute("""
            SELECT kumoId, name FROM Players WHERE kumoId = :i AND dm = 1
        """, i = data['dm']['id'])
        result = query.fetchone()

        if not result:
            response_str = json.dumps({
                'errorMsg': 'Unable to create new DM.'
            })
            return get_standard_response(response_str)

    if int(data['day']['id']) == 0:
        query = conn.execute("""
            SELECT id, name FROM Days WHERE name = :n
        """, n = data['day']['name'])
        result = query.fetchone()
        query.close()

        if result:
            data['day']['id'] = result['id']
        else:
            query = conn.execute("""
                INSERT INTO Days (name) VALUES (:n)
            """, n = data['day']['name'])
            query.close()

            query = conn.execute("""
                SELECT id, name FROM Days WHERE name = :n
            """, n = data['day']['name'])
            result = query.fetchone()
            query.close()

            if result:
                data['day']['id'] = result['id']
            else:
                response_str = json.dumps({
                    'errorMsg': 'Unable to create new day.'
                })
                return get_standard_response(response_str)


    if int(data['time']['id']) == 0:
        query = conn.execute("""
            SELECT id, name FROM Times WHERE name = :n
        """, n = data['time']['name'])
        result = query.fetchone()
        query.close()

        if result:
            data['time']['id'] = result['id']
        else:
            query = conn.execute("""
                INSERT INTO Times (name) VALUES (:n)
            """, n = data['time']['name'])
            query.close()

            query = conn.execute("""
                SELECT id, name FROM Times WHERE name = :n
            """, n = data['time']['name'])
            result = query.fetchone()
            query.close()

            if result:
                data['time']['id'] = result['id']
            else:
                response_str = json.dumps({
                    'errorMsg': 'Unable to create time.'
                })
                return get_standard_response(response_str)

    query = conn.execute("""
        UPDATE Games
           SET name = :n,
               description = :d,
               systemid = :s,
               dayid = :a,
               timeid = :t,
               dmid = :m,
               seats = :e,
               waitlist = :w
         WHERE id = :i
    """, n = data['name'],
    d = data['description'],
    s = data['system']['id'],
    a = data['day']['id'],
    t = data['time']['id'],
    m = data['dm']['id'],
    e = data['seats'],
    w = data['waitlist'],
    i = data['id'])

    player_ids = []
    for player in data['players']:
        player_ids.append(player['id'])
    
    query = conn.execute("SELECT kumoId FROM GameRegister WHERE gameId = :g AND kumoId IN (" + ', '.join(str(x) for x in player_ids) + ")", g = data['id'])
    rows = query.fetchall()
    query.close()

    remove_ids = []
    for player in data['players']:
        found = False
        for row in rows:
            if row['kumoId'] == player['id']:
                found = True
        
        if not found:
            remove_ids.append(player['id'])

    # TODO: Should we also allow adding users here?

    if len(remove_ids) > 0:
        query = conn.execute("DELETE FROM GameRegister WHERE gameId = :g AND kumoId IN (" + ', '.join(str(x) for x in player_ids) + ")", g = data['id'])

    response_str = json.dumps({
        'success': True
    })
    return get_standard_response(response_str)

@app.route('/logout', methods=['POST'])
def logout():
    session_id = request.headers.get('Authorization')
    print(session_id)

    conn = db_connect.connect()
    query = conn.execute('DELETE FROM UserSessions WHERE session = :s', s=session_id)
    query.close()

    response_str = json.dumps({})
    return get_standard_response(response_str)

if __name__ == '__main__':
    run_setup()
    app.run(debug=True, port='5002')