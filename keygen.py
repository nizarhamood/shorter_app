# shorter_app/keygen.py

import secrets
import string


from sqlalchemy.orm import Session

from . import crud 
def create_random_key(length: int = 5) -> str:
    # Using the string modules 
    chars = string.ascii_uppercase + string.digits
    return "".join(secrets.choice(chars) for _ in range(length))

def create_unique_random_key(db: Session) -> str:
    key = create_random_key()
    # Calling create_random_key() if key already exists in database, this makes sure every shortened URL exists only once.
    while crud.get_db_url_by_key(db, key):
        key = create_random_key()
    return key