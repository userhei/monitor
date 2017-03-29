
import os,sys,socket

engine_list = []
for i in range(1,len(sys.argv)):    
    engine_list.append(sys.argv[i])
    i += 1

print engine_list