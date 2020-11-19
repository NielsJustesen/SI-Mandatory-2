from flask import Flask, Blueprint
from address import address
from borger import borger

app = Flask(__name__)

app.register_blueprint(address)
app.register_blueprint(borger)