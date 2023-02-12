# shorter_app/models.py

from sqlalchemy import Boolean, Column, Integer, String

from .database import Base

class URL(Base):
    __tablename__ = 'urls'

    '''
    By setting the primary_key argument to True, you don’t need to provide a unique argument, as it defaults to True for primary keys anyway.
    '''
    id = Column(Integer, primary_key=True)
    
    # key field will contain the random string that'll be part of the shortened URL
    key = Column(String, unique=True, index=True)
    
    # secret_key the user can manage their shortened URL and see stats
    secret_key = Column(String, unique=True, index=True)
    
    # To store the url strings
    # NOTE: if unique values is set to True different users would be prevented from forwarding to the same URL
    target_url = Column(String, index=True)
    
    # When users want to delete a shortened URL the entry will become inactive instead 
    is_active = Column(Boolean, default=True)
    
    # Will increase by one each time someone clicks the shortened link
    clicks = Column(Integer, default=0)