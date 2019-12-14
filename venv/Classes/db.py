import hashlib
from random import randrange
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlsoup import SQLSoup
from var_dump import var_dump

Base = declarative_base()

class Account(Base):
    __tablename__ = "accounts"

    id = Column('id', Integer, primary_key=True)
    email = Column('email', String, nullable=False)
    username = Column('username', String, nullable=False)
    password = Column('password', String, nullable=False)
    salt = Column('salt', String, nullable=False)
    admin_level = Column('admin_level', Integer, nullable=False)


class String(Base):
    __tablename__ = "strings"

    id = Column('id', Integer, primary_key=True)
    account_id = Column('account_id', Integer, nullable=False)
    stringfile = Column('stringFile', String, nullable=False)
    index = Column('index', Integer, nullable=False)
    name = Column('name', String, nullable=False)
    value = Column('value', String, nullable=False)


engine = create_engine('mysql://sredit:123456@localhost:3306/sredit', echo=True)
Session = sessionmaker(bind=engine)
session = Session()


class Query:

    def __init__(self):
        print("Query Engine Initialized")

    def create_account(self, params):
        db = SQLSoup(engine)

        # Generate a random 32 character number and get it's md5 hash
        random_num = randrange(100000000000000000000000000000000, 999999999999999999999999999999999, 2)
        salt = hashlib.md5(str(random_num).encode())

        # Concatenate the users password and salt, then hash it with sha256
        concat = str(params['password']) + str(salt.hexdigest())
        pass_hash = hashlib.sha256(concat.encode())

        db.accounts.insert(project_name=params['project_name'], email=params['email'], username=params['username'], password=pass_hash.hexdigest(), salt=salt.hexdigest())
        db.commit()
        
    def get_hash(self, password, salt):
        concat = str(password) + str(salt)
        pass_hash = hashlib.sha256(concat.encode())
        return pass_hash.hexdigest()

    def check_username(self, username):
        db = SQLSoup(engine)
        try:
            result = db.accounts.filter(db.accounts.username==username).one()
            return "found"
        except:
            return "not found"

    def check_email(self, email):
        db = SQLSoup(engine)
        try:
            result = db.accounts.filter(db.accounts.email==email).one()
            return "found"
        except:
            return "not found"

    def get_account(self, username):
        db = SQLSoup(engine)
        try:
            result = db.accounts.filter(db.accounts.username==username).one()
            return result
        except:
            return -1

    def get_stringfiles_by_account_id(self, account_id):
        return session.query(String).filter_by(stringfile='string/en/aprilfools.stf')
