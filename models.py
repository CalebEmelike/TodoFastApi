from database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey


class User(Base):
    __tablename__ = 'users' # This is the name of the table in the database
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String)
    
    
class Todos(Base):
    __tablename__ = 'todos' # This is the name of the table in the database
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50), nullable=False)
    description = Column(String(100), nullable=False)
    priority = Column(Integer)
    completed = Column(Boolean, default=False)
    ower_id = Column(Integer, ForeignKey("users.id"))
   
   
   
   
   

