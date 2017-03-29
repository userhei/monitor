# -*- coding: UTF-8 -*-

from flask import Flask, render_template, redirect, request
import os,sys,socket,time

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

engine_num = "int(len(sys.argv))"

#status_engine = 0
#status_AH = 0
#status_mirror = 0
#status_drvstate = 0
#status_drive_path = 0
#status_engine_path = 0
#status_initiator_path = 0

def get_engine_list():
    engine_list = []
    for i in range(1,len(sys.argv)):
        engine_list.append(sys.argv[i])
        i += 1
    return engine_list

def get_engine_status_list(engine_list):
    PORT = "80"
    engine_status_list = []
    for i in range(len(engine_list)):
        print engine_list[i]
        sh = socket.socket()
        sh.settimeout(1)
#        for i in range (0,1):
        engine_status = sh.connect_ex((engine_list[i], int(PORT)))
        print engine_status
        sh.close()
        time.sleep(0.25)
        if engine_status > 0:
            engine_status = 1
        else:
            engine_status == 0
        engine_status_list.append(engine_status)
    return engine_status_list

@app.route("/")
def home():
    engine_list = get_engine_list()
    engine_num = int(len(engine_list))
    print engine_list
    engine_status_list = get_engine_status_list(engine_list)
    return render_template("monitor.html",engine_list = engine_list,engine_num = engine_num,engine_status_list = engine_status_list)

if __name__ == "__main__":
    app.run(debug=True)
