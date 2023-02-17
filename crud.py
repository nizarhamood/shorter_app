# shorter_app/crud.py

from sqlalchemy.orm import Session
from . import keygen, models, schemas

def create_db_url(db: Session, url: schemas.URLBase) -> models.URL:
    # To ensure there are no duplicates in the database
    key = keygen.create_unique_random_key(db)
    # Still ensures uniques by prefixing the string with the value of key
    secret_key = f"{key}_{keygen.create_random_key(length=8)}"
    db_url = models.URL(target_url=url.target_url, key=key, secret_key=secret_key)
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    return db_url

def get_db_url_by_key(db: Session, url_key: str) -> models.URL:
    return (
        db.query(models.URL)
        .filter(models.URL.key == url_key, models.URL.is_active)
        .first()
    )