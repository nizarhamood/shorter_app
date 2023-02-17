# shorter_app/main.py



'''
uvicorn shorter_app.main:app --reload
'''

# Package to check that the string used is a valid URL
import validators
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from . import crud, models, schemas

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
    raise HTTPException(
        status=400, 
        detail=message
    )

def raise_not_found(request):
    message = f"URL '{request.url}' does not exits"
    raise HTTPException(
        status_code=404, 
        detail=message
    )


@app.get("/")
def read_root():
    return "Welcome to the URL shorter API :)"

@app.post("/url", response_model=schemas.URLInfo)
def create_url(url: schemas.URLBase, db: Session = Depends(get_db)):
    
    # If provided URL isn't valid the exception function is used/raised
    if not validators.url(url.target_url):
        raise_bad_request(message="You provided URL is not valid")
    
    db_url = crud.create_db_url(db=db, url=url)
    db_url.url = db_url.key
    db_url.admin_url = db_url.secret_key
    
    return db_url

# To forward the user to the shortened URL
'''
The decorator uses the get function from FastAPI and I've added extra functionality to it with the forward_to_target function
'''
@app.get("/{url_key}")
def forward_to_target(
    url_key: str,
    request: Request,
    db: Session = Depends(get_db)
):
    db_url = (
        db.query(models.URL)
        .filter(models.URL.key == url_key, models.URL.is_active)
        .first()
    )
    if db_url := crud.get_db_url_by_key(db=db,url_key=url_key):
        return RedirectResponse(db_url.target_url)
    else:
        # If the provided URL.key doesn't match what's in the database
        raise_not_found(request)