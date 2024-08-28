from sqlmodel import create_engine, Session, SQLModel
import os, traceback
from dotenv import load_dotenv
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Create engine
engine = create_engine(DATABASE_URL, pool_size=20, pool_pre_ping=True)


def create_table():
    try:
        SQLModel.metadata.create_all(engine)
    except:
        traceback.print_exc()
        print(f"Error in creating init tables.")

# Dependency to get the database session
def get_session():
    with Session(engine) as session:
        yield session