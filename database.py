from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
# from sqlalchemy.ext.declarative import declarative_base




SQLALCHEMY_DATABASE_URL = 'postgresql://ezgmixpr:CIUkwhxlRiSukdeR4zLFSFQApnzYJEgF@jelani.db.elephantsql.com/ezgmixpr'

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
