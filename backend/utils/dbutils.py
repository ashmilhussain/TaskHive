from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine  # Add this import for task completion status
from models.base import Base


class DBUtils:
    def __init__(self):
        self.DATABASE_URL = "sqlite:///./taskhive.db"
        self.engine = create_engine(self.DATABASE_URL, connect_args={"check_same_thread": False})
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        Base.metadata.create_all(bind=self.engine)

    def get_db(self):
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()