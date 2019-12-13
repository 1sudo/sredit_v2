from flask import Flask, session
from flask_session import Session
from flask_redis import FlaskRedis

class SRSession:

    def __init__(self):
        print("Session Init")

    def set(self, key, value):
        session[key] = value
    
    def get(self, key):
        return session.get(key, 'no')
