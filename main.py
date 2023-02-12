# shortener_app/main.py

# To generate randomness
import secrets

# Package to check that the string used is a valid URL
import validators
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

# Importing the .py files I created
from . import models, schemas

# Importing the database.py file and importing Session and engine functions
from .database import SessionLocal, engine

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

from . import schemas

def raise_bad_request(message):
    raise HTTPException(status=400, detail=message)


@app.get("/")
def read_root():
    return "Welcome to the URL shortener API :)"

@app.post("/url", response_model=schemas.URLInfo)
def create_url(url: schemas.URLBase, db: Session = Depends(get_db)):
    
    # If provided URL isn't valid the exception function is used/raised
    if not validators.url(url.target_url):
        raise_bad_request(message="You provided URL is not valid")
        
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    
    # Create key using random generator
    key = "".join(secrets.choice(chars) for _ in range(5))
    
    # Create secret_key using random generator
    secret_key = "".join(secrets.choice(chars) for _ in range(8))
    
    
    db_url = models.URL(
        
        # Create db entry for target_url
        target_url = url.target_url,
        
        # Add key to db
        key=key,
        
        # Add secret_key to db
        secret_key = secret_key
    )
    
    db.add(db_url)
    db.commit()
    db.refresh(db_url)
    db_url.url = key
    db_url.admin_url = secret_key
    
    return db_url