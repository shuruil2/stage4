from app import db

def user_validation(email, password):
    conn = db.connect()
    query = 'SELECT * FROM Users WHERE Email = "{}" AND Password = "{}";'.format(email, password)
    query_results = conn.execute(query).fetchall()
    conn.close()
    if len(query_results) == 0:
        return False
    else:
        return True
    
def user_signup(email, password, gender, age):
    conn = db.connect()

    # Get the maximum user ID
    query = 'SELECT MAX(UserId) FROM Users;'
    result = conn.execute(query).fetchone()
    max_id = result[0] if result[0] else 'user000'

    # Generate new user ID
    base_id = int(max_id[4:])
    new_id = 'user' + str(base_id + 1).zfill(3)

    # Insert new user
    query = 'INSERT INTO Users (UserId, Email, Password, Gender, Age, Role) VALUES ("{}", "{}", "{}", "{}", {}, "user");'.format(new_id, email, password, gender, age)
    conn.execute(query)
    conn.close()

def get_user_info(email):
    conn = db.connect()
    query = 'SELECT * FROM Users WHERE Email = "{}";'.format(email)
    query_rusults = conn.execute(query).fetchall()
    conn.close()
    if query_rusults:
        return query_rusults[0]
    else:
        return None