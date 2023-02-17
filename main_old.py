# shorter_app/main.py

import validators
from fastapi import FastAPI, HTTPException


from . import schemas
# Instantiating the FastAPI class
app = FastAPI()

'''
Using a path operation decorator to associate the root path with read_root() by registering it in FastAPI. Now FastAPI listens to the root path and delegates all income GET requests to the read_root() function
'''

# The Path Operation Decorator is to associate the root path with read_root() by registering it in FastAPI.
@app.get("/")
def read_root():
    return "Welcome to the URL shortener API :)"