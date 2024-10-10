
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 # Add this import

# Create the database table
Base = declarative_base()