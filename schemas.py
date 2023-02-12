# shorter_app/schemas.py

'''
Defined what data the API expected from the client and the server.
'''


from pydantic import BaseModel


# This will be used to store the URL that the shortened URL forwards to 
class URLBase(BaseModel):
    target_url: str
 
# URL class inherits the target_url field from the URLBase   
class URL(URLBase):
    # is_active allows the deactivation of a shortened URLs
    is_active: bool
    
    # clicks allows to count the number of times a shortened URL has been visited
    clicks: int
    
    class Config:
        # Telling pydantic to work with a database (by setting orm_mode = True)
        # ORM: Object-Relational Mapping
        orm_mode = True
  
# This allows the use of the url and admin_url to be used in the API without being stored in our databse      
class URLInfo(URL):
    url: str
    admin_url: str