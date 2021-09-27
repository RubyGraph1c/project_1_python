from db.run_sql import run_sql
from models.session import Session
from models.member import Member
from models.booking import Booking 
import repos.member_repo as member_repo
import repos.session_repo as session_repo
import repos.booking_repo as booking_repo

def save(session):
    sql = "INSERT INTO sessions(name, category) VALUES ( %s, %s ) RETURNING id"
    values = [session.name, session.category]
    results = run_sql( sql, values )
    session.id = results[0]['id']
    return session

def select_all():
    sessions = []

    sql = "SELECT * FROM sessions"
    results = run_sql(sql)

    for row in results:
        session = session(row['name'], row['category'], row['id'])
        sessions.append(session)
    return sessions


def select(id):
    session = None
    sql = "SELECT * FROM sessions WHERE id = %s"
    values = [id]
    result = run_sql(sql, values)[0]

    if result is not None:
        session = session(result['name'], result['category'], result['id'] )
    return session


def delete_all():
    sql = "DELETE FROM sessions"
    run_sql(sql)

def members(session):
    members = []
    sql = "SELECT members.* FROM members INNER JOIN visits ON visits.member_id = members.id WHERE session_id = %s"
    values = [session.id]
    results = run_sql(sql, values)
    
    for row in results: 
        member = member(row['name'], row['id'])
        members.append(member)
    return members