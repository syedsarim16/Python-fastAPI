#it is SQLALchemy ORM model for a Post entity in a blogging application.
from sqlalchemy import Column, Integer, String, Boolean,func, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from.database import Base
from sqlalchemy.orm import relationship

class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=True)
    content = Column(String, nullable=True)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False, server_default=text('now()'))
    owner_id= Column(Integer,ForeignKey("y_users.id",ondelete="CASCADE") ,nullable=False)  # Foreign key to the user who created the post
    owner=relationship("User")
class User(Base):
    __tablename__ = "y_users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())  #  This line is essential

class Vote(Base):
    __tablename__="votes"
    user_id=Column(Integer,ForeignKey("y_users.id",ondelete="CASCADE"),primary_key=True)
    post_id=Column(Integer,ForeignKey("posts.id",ondelete="CASCADE"),primary_key=True)



