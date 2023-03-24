from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from loguru import logger
import os


def get_db_eng():
    db_uri = os.environ['SQLALCHEMY_DATABASE_URI']
    logger.info(f'connecting to {db_uri}')
    eng = create_engine(db_uri, echo=True)
    return eng

eng = get_db_eng()
Session = sessionmaker(eng)

def get_db_session():
    return Session()