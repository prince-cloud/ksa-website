import secrets

def generate_password(length=8)-> str:
    password = secrets.token_urlsafe(length)
    return password