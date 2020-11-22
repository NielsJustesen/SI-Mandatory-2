from flask import Flask, Blueprint
from SkatUser import SkatUser
from SkatYear import SkatYear

app = Flask(__name__)

app.register_blueprint(SkatUser)
app.register_blueprint(SkatYear)