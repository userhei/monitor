# -*- coding: UTF-8 -*-

from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
import os,sys,socket

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

num = "int(len(sys.argv))"
host = "192.168.1.1"
#status = int(sys.argv[1])
status_engine = 0
status_AH = 0
status_mirror = 0
status_drvstate = 0
status_drive_path = 0
status_engine_path = 0
status_initiator_path = 0

def get_status_engine
    PORT = "25000"
#    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sh = socket.socket()
    sh.settimeout(1)    ## set a timeout of 1 sec
    for i in range (0, 1): # try once
        result = sh.connect_ex((engine_ip, int(PORT)))  # connect to the remote host on port 25000
                                                    ## (port 25000 is always open for HA-AP engine)
#        print ".... ", result
        if result > 0:
            dbg.printDBG2(file_name, "can not connect to engine: %s port: %s, retry=%s" %(engine_ip, PORT, i))
        else:           # everything is OK!
            dbg.printDBG2(file_name, "connected to engine: %s port: %s, retry=%s" %(engine_ip, PORT, i))
            sh.close()
            return True
    sh.close()
    return False

@app.route("/")
def home():
    return render_template("monitor.html",num = num,status = status,host = host)

if __name__ == "__main__":
    app.run(debug=True)
