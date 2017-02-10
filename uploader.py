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
	f = open(join(project_path, ".pioenvs", "target"), "w")
	f.write("spawn scp %s %s@%s:~/scp_program" % (target_bin, user_name, target_addr))
	f.write("\nexpect \"%s@%s's password:\"" % (user_name, target_addr))
	f.write("\nsend \"%s\\r\"" % (password))
	f.write("\nspawn ssh %s@%s \"./scp_program\"" % (user_name, target_addr))
	f.write("\nexpect \"password\"")
	f.write("\nsend \"%s\\r\"" % (password))
	f.write("\ninteract\n")
	f.close()
	
	os.system("gnome-terminal -x bash -c \"expect ./.pioenvs/target; read -s -n1 \"")

else:
	f = open(join(project_path, ".pioenvs", "upload.gdb"), "w")
	f.write("target extended-remote %s:%s" % (target_addr, upload_port))
	f.write("\nremote put %s ./gdb/program" % (target_bin))
	f.write("\nfile %s" % (target_bin))
	f.write("\nset remote exec-file "+"./gdb/program")
	f.write("\nbreak main\nrun\n")
	f.close()

	f = open(join(project_path, ".pioenvs", "target"), "w")
	f.write("spawn ssh %s@%s \"mkdir gdb;gdbserver --multi :%s\"" % (user_name, target_addr, upload_port))
	f.write("\nexpect \"password\"")
	f.write("\nsend \"%s\\r\"" % (password))
	f.write("\ninteract\n")
	f.close()

	os.system("gnome-terminal -x bash -c \"expect ./.pioenvs/target;\"")
	os.system("gnome-terminal -x bash -c \"%s -x %s/.pioenvs/upload.gdb\"" % (uploader, project_path))
