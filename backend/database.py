from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database connection URL (replace with your PostgreSQL connection string)
SQLALCHEMY_DATABASE_URL = "postgresql://funny_comments_db_user:NJAt6qYv07RiSK3M93LMNqkdMgMQzyVU@dpg-d1psmk49c44c738vmr2g-a.oregon-postgres.render.com/funny_comments_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
