#!/usr/bin/python3
"""New engine DBStorage"""
from sqlalchemy import (create_engine)
from os import getenv
from models.base_model import Base
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker


class DBStorage:
    """Database storage"""
    __engine = None
    __session = None

    def __init__(self):
        """Initialize DBStorage instance"""
        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}/{}".
                                      format(getenv("HBNB_MYSQL_USER"),
                                             getenv("HBNB_MYSQL_PWD"),
                                             getenv("HBNB_MYSQL_HOST"),
                                             getenv("HBNB_MYSQL_DB")),
                                      pool_pre_ping=True)

        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """query on the current database session (self.__session) all
        objects depending of the class name"""
        classes = [User, State, Place, City, Amenity, Review]
        result = {}
        if cls in classes:
            search = self.__session.query(cls)
            for object in search:
                key = "{}.{}".format(type(object).__name__,
                                     object.id)
                result[key] = object
        elif cls is None:
            for class_ in classes:
                search = self.__session.query(class_)
                for object in search:
                    key = "{}.{}".format(type(object).__name__,
                                         object.id)
                    result[key] = object
        return result

    def new(self, obj):
        """Add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables in the database"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(
            bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """
        Call remove() method on the private session attribute
        (self.__session) or close() on the class Session
        """
        self.__session.close()
