from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
# from sqlalchemy.ext.declarative import declarative_base




SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:test1234!@localhost:6543/TodoApplicationDatabase'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()


# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker, declarative_base
# # from sqlalchemy.ext.declarative import declarative_base




# SQLALCHEMY_DATABASE_URL = 'sqlite:///./todo.sqlite'

# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# Base = declarative_base()
