# -*- coding: UTF-8 -*-

from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
import os,sys

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

num = "1"
host = "192.168.1.1"
status = int(sys.argv[1])

@app.route("/")
def home():
    return render_template("monitor.html",num = num,status = status,host = host)

if __name__ == "__main__":
    app.run(debug=True)
