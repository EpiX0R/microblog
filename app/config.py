"""
Contains Prod, Dev and Test config classes.
Also Custom class for logging, RequestFormatter.
"""

import os
from logging import Formatter
from dotenv import load_dotenv
from flask import request


basedir = os.path.abspath(os.path.dirname(__file__) +  "/..")
load_dotenv(os.path.join(basedir, '.env'))



class Config():
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

class ProdConfig(Config):
    """Production configuration"""
    ENV = "production"
    DEBUG = False

class DevConfig(Config):
    """Development configuration"""
    ENV = 'development' # Pointless attribut, needs to be set in environment
    DEBUG = True # Pointless attribut, needs to be set in environment
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestConfig(Config):
    """Test configuration"""
    ENV = "test"
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    # Bcrypt algorithm hashing rounds (reduced for testing purposes only!)
    BCRYPT_LOG_ROUNDS = 4
    # Disable CSRF tokens in the Forms (only valid for testing purposes!)
    WTF_CSRF_ENABLED = False



class RequestFormatter(Formatter):
    """
    Custom class for formatting logger to include url and ip
    """
    def format(self, record):
        """
        Add url and remote_addr to record
        """
        record.url = request.url
        record.remote_addr = request.remote_addr
        return super().format(record)
