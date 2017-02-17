# Tools for linux-arm boards used in [PlatformIO](http://platformio.org)

* uploader.py 
	
	*upload and run/debug the program to the board using SCP or GDB. 

	*upload.py need 3 argvs: 

		*upload_port: the information up target. user_name:password@target_addr:gdb_server_port
		
		*target_bin: the target file need to be uploaded
		
		*uploader: the path/program used to upload the target file. (SCP or GDB)
