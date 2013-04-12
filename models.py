from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.schema import ForeignKey
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("mysql://root:@localhost/domychores")
Base = declarative_base()


class User(Base):
    """The User table to represent users of the application."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(75), nullable=False)
    password = Column(String(128), nullable=False)
    address = Column(String(250), nullable=False)

    def __init__(self, first_name, last_name, email, password, address):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.address = address

    def __repr__(self):
        """Return string representation of the User."""
        return "<User({0} {1})>" % (self.first_name, self.last_name)


class Chore(Base):
    """The Chore table to represent a chore posting in the application."""

    __tablename__ = "chores"

    id = Column(Integer, primary_key=True)
    task = Column(String(100), nullable=False)
    description = Column(String(250), nullable=False)
    owner_id = Column(Integer, ForeignKey('users.id'))
    worker_id = Column(Integer, ForeignKey('users.id'))
    posted_at = Column(String(50), nullable=False)

    def __init__(self, task, description, owner_id):
        self.task = task
        self.description = description
        self.owner_id = owner_id
        self.posted_at = datetime.now().isoformat()

    def __repr__(self):
        """Return string representation of the Chore."""
        return "<Chore({0})>" % (self.id)


def create_all():
    """Create all the Tables"""
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    """Create all tables upon calling as script."""
    create_all()
