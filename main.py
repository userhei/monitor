# -*- coding: UTF-8 -*-

from flask import Flask, render_template, redirect, request
import os,sys,socket,time,re,telnetlib,codecs,datetime,shutil
from collections import OrderedDict

login = 'Enter password'
password = '.com'
prompt = 'Coredump Menu'
CLI = 'CLI>'
CLI_Conflit = 'Another session owns the CLI'

log_dir = 'log_file'

exec_comm = OrderedDict()
exec_comm['Mirror_status'] = 'mirror'
exec_comm['Path_status'] = 'conmgr status'
status_comm_desc = exec_comm.keys()
status_comm_comm = exec_comm.values()

fail_info = [['BAD','EXP','DEG','RBL'],'N']
fail_num = [2,4]

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))

def get_engine_list():
    engine_list = []
    for i in range(1,len(sys.argv)):
        engine_list.append(sys.argv[i])
        i += 1
    return engine_list

def get_engine_status_list(engine_list):
    PORT = "25000"
    engine_status_list = []
    for i in range(len(engine_list)):
        print engine_list[i]
        sh = socket.socket()
        sh.settimeout(1)
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

def in_or_not(fail_info_list,x):
    for i in range(len(fail_info_list)):
        print str(fail_info_list[i]) in x
        if str(fail_info_list[i]) in x:
            break
        return 0
    return 1  
    
def get_system_status_to_list(system_status_list,host_list,engine_status_list,log_dir,comm_desc_list,comm_comm_list,fail_info,fail_num):    
    
    for i in range(len(host_list)):
        system_status_list[0].append(host_list[i])
        system_status_list[1].append([])
        
        if int(engine_status_list[i]) == 0:
            tn = telnetlib.Telnet(host_list[i])
            tn.read_until(login, timeout = 2)
            tn.write('\r')
            tn.read_until(prompt, timeout = 2)
            tn.write("7")
            e = tn.read_until(CLI, timeout = 2)
            if int(e.find(CLI)) > 0:
                time.sleep(0.05)
            elif int(e.find(CLI_Conflit)) > 0:
                tn.write("y" + '\r')
                e = tn.read_until(CLI, timeout = 2)
                if  int(e.find(CLI)) > 0:
                    pass
            else:
                print "------Goto the CLI Failed For Engine: " + host_list[i]
                sys.exit(0)
            
            for x in range(len(comm_desc_list)):
                tn.write(comm_comm_list[x] + '\r')
                result = tn.read_until(CLI, timeout = 10)
                if in_or_not(fail_info[x],result):
                    system_status_list[1][i].append(fail_num[x])
                else:
                    system_status_list[1][i].append(0)
                time.sleep(0.05)
            tn.close
        else:
            for x in range(len(comm_desc_list)):
                system_status_list[1][i].append(99)
        print system_status_list
        
        system_status_list[2].append(sum(system_status_list[1][i]))
        
            
    print system_status_list
        
#    for x in range(len(system_status_list[0]):
#        system_status_list[2][x].append(sum(system_status_list[1][x]))
        


@app.route("/")
def home():
    
    engine_list = get_engine_list()
    engine_num = int(len(engine_list))
    print engine_list
    engine_status_list = get_engine_status_list(engine_list)
    print engine_status_list
    system_status_list = [[],[],[]]
    get_system_status_to_list(system_status_list,engine_list,engine_status_list,log_dir,status_comm_desc,status_comm_comm,fail_info,fail_num)
    print system_status_list
    
    return render_template("monitor.html",engine_list = engine_list,engine_num = engine_num,engine_status_list = engine_status_list,system_status_list = system_status_list)

if __name__ == "__main__":
    app.run(debug=True)
