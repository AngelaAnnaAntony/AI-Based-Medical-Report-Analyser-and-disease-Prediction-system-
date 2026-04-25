import hashlib
from modules.database import create_connection

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def signup_user(name, email, username, password):
    conn=create_connection()
    cursor=conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO users(name, email, username, password) VALUES(?,?,?,?)",
            (name, email, username, hash_password(password))
        )
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()

def login_user(email, password):
    conn=create_connection()
    cursor=conn.cursor()
    cursor.execute(
        "SELECT * FROM users WHERE email=? AND password=?",
        (email, hash_password(password))
    )
    user=cursor.fetchone()
    conn.close()
    return user

def get_user_by_email(email):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM users WHERE email=?",
        (email,)
    )
    user = cursor.fetchone()
    conn.close()
    return user

def reset_password(email, new_password):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET password=? WHERE email=?",
        (hash_password(new_password), email)
    )
    conn.commit()
    updated = cursor.rowcount
    conn.close()
    return updated > 0