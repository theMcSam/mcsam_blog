from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker
import os

load_dotenv()

Base = declarative_base()

engine = create_engine(
    os.environ.get('RENDER_POSTRGRESS_DB_URL'), echo=True
)

Session = sessionmaker(bind=engine)
db_session = Session()