#!/usr/bin/python

# -*- coding: utf-8 -*-
import sys, os

join = os.path.join
project_path = os.getcwd()

upload_port = sys.argv[1]
target_bin = join(project_path, sys.argv[2])
uploader = sys.argv[3]

l = upload_port.index(":")
user_name = upload_port[:l]
upload_port = upload_port[l+1:]

l = upload_port.index("@")
password = upload_port[:l]
upload_port = upload_port[l+1:]

try:
	l = upload_port.index(":")
	target_addr = upload_port[:l]
	upload_port = upload_port[l+1:]
except:
	target_addr = upload_port
	upload_port = "5678"
if uploader == 'scp':
	f = open(join(project_path, ".pioenvs", "target.sh"), "w")
	f.write("spawn scp "+target_bin+" "+user_name+"@"+target_addr+":~/gdb")
	f.write("\nexpect \""+user_name+"@"+target_addr+"'s password:\"")
	f.write("\nsend \""+password+"\\r\"")

	f.write("\nspawn ssh "+user_name+"@"+target_addr+" \"./gdb/program\"")
	f.write("\nexpect \"password\"")
	f.write("\nsend \""+password+"\\r\"")
	f.write("\ninteract\n")
	f.close()
	# os.system("expect ./.pioenvs/target.sh")
	os.system("gnome-terminal -x bash -c \"expect ./.pioenvs/target.sh; read -s -n1 \"")

else:
	f = open(join(project_path, ".pioenvs", "upload.gdb"), "w")
	f.write("target extended-remote "+target_addr+":"+upload_port)
	f.write("\nremote put "+target_bin+" ./gdb/program")
	f.write("\nfile "+target_bin)
	f.write("\nset remote exec-file "+"./gdb/program")
	f.write("\nbreak main\nrun\n")
	f.close()

	f = open(join(project_path, ".pioenvs", "target.sh"), "w")
	f.write("spawn ssh root@"+target_addr+" \"mkdir gdb;gdbserver --multi :"+upload_port+"\"")
	f.write("\nexpect \"password\"")
	f.write("\nsend \""+password+"\\r\"")
	f.write("\ninteract\n")
	f.close()

	os.system("gnome-terminal -x bash -c \"expect ./.pioenvs/target.sh;\"")

	os.system("gnome-terminal -x bash -c \""+uploader+" -x "+project_path+"/.pioenvs/upload.gdb\"")
