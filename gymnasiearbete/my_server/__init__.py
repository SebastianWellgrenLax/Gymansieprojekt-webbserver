from flask import Flask, redirect, render_template, request, url_for, flash
from distutils import extension
import requests, json, uuid
from bs4 import BeautifulSoup
from urllib.request import urlopen, urlretrieve
from flask_login import LoginManager, login_user, logout_user, current_user, login_required, UserMixin
from flask_sqlalchemy import SQLAlchemy

from my_server.config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
login_manager = LoginManager(app)

login_manager.login_message_category = 'info'

from my_server import routes, error
