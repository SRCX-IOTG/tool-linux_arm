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
	with open(join(project_path, ".pioenvs", "target"), "w") as f:
		f.write('\
			set user "%s"\n\
			set password "%s"\n\
			set targetAddr "%s"\n\
			set targetBin "%s"\n\
			spawn scp $targetBin $user@$targetAddr:~/scp_program\n\
			expect {\n\
				"(yes/no)?" {\n\
					send "yes\\r "; \n\
					exp_continue;\n\
				}\n\
				"*assword:" {\n\
					send "$password\\r"; \n\
				}\n\
			}\n\
			\n\
			spawn ssh $user@$targetAddr "./scp_program"\n\
			expect {\n\
				"*assword:" {\n\
					send "$password\\r"; \n\
				}\n\
			}\n\
			interact'
			% (user_name, password, target_addr, target_bin)
		)

	os.system("gnome-terminal -x bash -c \"expect ./.pioenvs/target; read -s -n1 \"")

else:
	with open(join(project_path, ".pioenvs", "upload.gdb"), "w") as f:
		f.write("target extended-remote %s:%s" % (target_addr, upload_port))
		f.write("\nremote put %s ./gdb/program" % (target_bin))
		f.write("\nfile %s" % (target_bin))
		f.write("\nset remote exec-file "+"./gdb/program")
		f.write("\nbreak main\nrun\n")
		
	with open(join(project_path, ".pioenvs", "target"), "w") as f:
		f.write('\
			set user "%s"\n\
			set password "%s"\n\
			set targetAddr "%s"\n\
			set targetBin "%s"\n\
			set uploadPort "%s"\n\
			spawn ssh $user@$targetAddr "mkdir gdb;gdbserver --multi :$uploadPort"\n\
			expect {\n\
				"(yes/no)?" {\n\
					send "yes\\r "; \n\
					exp_continue;\n\
				}\n\
				"*assword:" {\n\
					send "$password\\r"; \n\
				}\n\
			}\n\
			interact'
			% (user_name, password, target_addr, target_bin, upload_port)
		)


	os.system("gnome-terminal -x bash -c \"expect ./.pioenvs/target;\"")
	os.system("gnome-terminal -x bash -c \"%s -x %s/.pioenvs/upload.gdb\"" % (uploader, project_path))
