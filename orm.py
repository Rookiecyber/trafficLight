from sqlalchemy import Boolean, Float
from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy import DateTime
from sqlalchemy import event
from sqlalchemy import exc
from sqlalchemy import ForeignKey
from sqlalchemy import inspect
from sqlalchemy import Integer
from sqlalchemy import MetaData
from sqlalchemy import or_
from sqlalchemy import select
from sqlalchemy import Table
from sqlalchemy import Unicode
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref
from sqlalchemy.orm import interfaces
from sqlalchemy.orm import object_session
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from sqlalchemy.sql.expression import bindparam
from sqlalchemy.types import LargeBinary
from sqlalchemy.types import Text
from sqlalchemy.types import TypeDecorator
from tornado.log import app_log

meta = MetaData(
    naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }
)

Base = declarative_base(metadata=meta)
Base.log = app_log


class User(Base):
    """User Roles"""

    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Unicode(255), unique=True)

    def __repr__(self):
        return "<{} {} >".format(
            self.__class__.__name__,
            self.name,
        )

    @classmethod
    def find(cls, db, name):
        """Find a role by name.
        Returns None if not found.
        """
        return db.query(cls).filter(cls.name == name).first()

    @classmethod
    def findById(cls, db, id):
        """Find a user by name.
        Returns None if not found.
        """
        return db.query(cls).filter(cls.id == id).first()


class Car(Base):
    """User Roles"""

    __tablename__ = 'car'
    id = Column(Integer, primary_key=True, autoincrement=True)
    direction = Column(Unicode(255))
    flow = Column(Integer)
    time = Column(Unicode(255))

    def __repr__(self):
        return "<{} {} {} {}>".format(
            self.__class__.__name__,
            self.direction,
            self.flow,
            self.time
        )

    @classmethod
    def findByFlow(cls, db, flow):
        """Find a role by flow.
        Returns None if not found.
        """
        return db.query(cls).filter(cls.flow == flow).first()

    @classmethod
    def findById(cls, db, id):
        """Find a user by id.
        Returns None if not found.
        """
        return db.query(cls).filter(cls.id == id).first()

    @classmethod
    def findByDirection(cls, db, direction):
        """Find a user by direction.
        Returns None if not found.
        """
        return db.query(cls).filter(cls.direction == direction).first()

    @classmethod
    def findByTime(cls, db, time):
        """Find a user by time.
        Returns None if not found.
        """
        return db.query(cls).filter(cls.time == time).first()


# 可信度知识
class Knowledge(Base):
    """Knowledge Roles"""

    __tablename__ = 'knowledge'
    # ID
    id = Column(Integer, primary_key=True, autoincrement=True)
    # 前提
    E = Column(Unicode(255))
    # 结论
    H = Column(Unicode(255))
    # 前提可信度
    CFE = Column(Float)
    # 知识可信度
    CFHE = Column(Float)

    def __repr__(self):
        return "<{} {} {} {} {}>".format(
            self.__class__.__name__,
            self.E,
            self.H,
            self.CFE,
            self.CFHE
        )

    @classmethod
    def findByID(cls, db, id):
        """Find a role by ID.
        Returns None if not found.
        """
        return db.query(cls).filter(cls.id == id).first()

    @classmethod
    def findByE(cls, db, E):
        """Find a role by E.
        Returns None if not found.
        """
        return db.query(cls).filter(cls.E == E).first()

    @classmethod
    def findByH(cls, db, H):
        """Find a user by H.
        Returns None if not found.
        """
        return db.query(cls).filter(cls.H == H).first()

    @classmethod
    def findByCFE(cls, db, CFE):
        """Find a user by CFE.
        Returns None if not found.
        """
        return db.query(cls).filter(cls.CFE == CFE).first()

    @classmethod
    def findByCFHE(cls, db, CFHE):
        """Find a user by CFHE.
        Returns None if not found.
        """
        return db.query(cls).filter(cls.CFHE == CFHE).first()


# Fuzzy Knowledge Roles
class Fuzzy(Base):
    __tablename__ = 'fuzzy'
    # ID
    id = Column(Integer, primary_key=True, autoincrement=True)
    # Name.
    name = Column(Unicode(255))
    # 输入参数到隶属度向量映射关系.
    map_input_2_membership_vec = Column(Text)
    # 模糊矩阵.
    matrix_r = Column(Text)

    def __repr__(self):
        return "<{} {} {} {}>".format(
            self.__class__.__name__,
            self.name,
            self.map_input_2_membership_vec,
            self.matrix_r,
        )

    @classmethod
    def findByID(cls, db, id):
        """Find a role by ID.
        Returns None if not found.
        """
        return db.query(cls).filter(cls.id == id).first()

    @classmethod
    def findByName(cls, db, name):
        """Find a role by E.
        Returns None if not found.
        """
        return db.query(cls).filter(cls.name == name).first()


# Weather
class Weather(Base):
    __tablename__ = 'weather'
    # ID
    id = Column(Integer, primary_key=True, autoincrement=True)
    # Name.
    name = Column(Unicode(255))
    # 输入参数到隶属度向量映射关系.
    rain = Column(Integer)
    # 输入参数到隶属度向量映射关系.
    snow = Column(Integer)
    # 输入参数到隶属度向量映射关系.
    wind = Column(Integer)

    def __repr__(self):
        return "<{} {} {} {} {}>".format(
            self.__class__.__name__,
            self.name,
            self.rain,
            self.snow,
            self.wind,
        )

    @classmethod
    def get(cls, db, id):
        """Find a role by ID.
        Returns None if not found.
        """
        return db.query(cls).filter(cls.id == id).first()


class Result(Base):
    __tablename__ = 'result'
    # ID
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Unicode(255))

    weather_rain = Column(Integer)
    weather_snow = Column(Integer)
    weather_wind = Column(Integer)


    # Total Args.
    base_pass_time = Column(Integer)
    public_time = Column(Integer)

    car_numbers = Column(Unicode(255))

    public_allocated_times = Column(Unicode(255))
    weather_add_times = Column(Unicode(255))

    final_results = Column(Unicode(255))
    time = Column(Unicode(255))

    def __repr__(self):
        return "<{} {} {} {} {} {} {} {} {} {} {} {}>".format(
            self.__class__.__name__,
            self.name,
            self.base_pass_time,
            self.weather_rain,
            self.weather_snow,
            self.weather_wind,
            self.public_time,
            self.car_numbers,
            self.public_allocated_times,
            self.weather_add_times,
            self.final_results,
            self.time,
        )
