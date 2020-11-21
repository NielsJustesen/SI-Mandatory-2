from flask import Flask, Blueprint
from SkatUser import SkatUser

app = Flask(__name__)

app.register_blueprint(SkatUser)