#!/usr/bin/python3

import os, shutil, configparser, hashlib, time
from subprocess import Popen, PIPE
from datetime import datetime
from git import Repo

config = configparser.ConfigParser()
log_content = ''

#utility function to get SHA-256 checksums
def sha256_checksum(filename, block_size=65536):
	sha256 = hashlib.sha256()
	with open(filename, 'rb') as f:
		for block in iter(lambda: f.read(block_size), b''):
			sha256.update(block)
	return sha256.hexdigest()


#function to check if script should be updated
def is_update_time(subdir, file, freq):
	should_run_update = True
	try:
		f = open(os.path.join(subdir, file)+'.lastlog', 'r')
		timestamp = int(float(f.readline()))
		prev_time = datetime.fromtimestamp(timestamp)
		f.close()
		diff = datetime.now() - prev_time		
		if diff.seconds/60/60<int(freq):
			should_run_update = False
	except Exception:
		 pass
	return should_run_update


#function to write to last log details
def write_last_log(subdir, file):
	f = open(os.path.join(subdir, file)+'.lastlog', 'w')
	f.write(log_content)
	f.close()


#function for cloning remote git repo locally and checking for changes
def update_from_git(git_remote, localpath):
	is_new = False
	try:
		repo = Repo(localpath+ '/remote-git')
	except:
		repo = Repo.init(localpath+ '/remote-git')
		remote = repo.create_remote('origin', git_remote)
		remote.fetch() 
		repo.create_head('master', remote.refs.master).set_tracking_branch(remote.refs.master).checkout()
		is_new = True
	
	origin = repo.remotes.origin
	origin.fetch()
	checksum_remote = origin.refs.master.commit
	checksum_local = repo.head.commit
	
	if checksum_remote!=checksum_local or is_new:
		repo.config_writer().set_value('user', 'name', 'default.repo').release()
		repo.config_writer().set_value('user', 'email', 'default.repo').release()
		repo.git.stash()
		repo.git.merge()


#function for taking files from git repo and copying to local folder
def copy_updated_files(localpath):
	global log_content
	full_remote_path = localpath+ '/remote-git/'
	#get .gitignore files & folders
	ignored_folders = set()
	ignored_files = set()
	for item in open(full_remote_path + '.gitignore').read().split('\n'):
		if item.endswith('/'):
			ignored_folders.add(item)
		else:
			ignored_files.add(item)
	ignored_files.add('.gitignore')
	ignored_folders.add('.git/')

	for subdir, dirs, files in os.walk(full_remote_path, topdown=True):
		this_subdir = subdir.replace(full_remote_path,'') + '/' 

		if this_subdir in ignored_folders:
			[dirs.remove(d) for d in list(dirs)]
			continue

		for file in files:
			this_file = (os.path.join(subdir, file)).replace(full_remote_path,'')
			if this_file not in ignored_files:
				git_file = os.path.join(subdir, file)
				local_file = git_file.replace('/remote-git/', '/')
				local_dir = subdir.replace('/remote-git/', '/')
				new_checksum = sha256_checksum(git_file)
				ex_checksum = ''
				if os.path.exists(local_file):
					ex_checksum = sha256_checksum(local_file)
				
				if new_checksum != ex_checksum:
					if not os.path.exists(local_dir):
						os.mkdir(local_dir)
					shutil.copy(git_file, local_file)
					log_content += '\nCopying new file ' + local_file


#function for calling post-install script if config parameter is given
def call_post_install_script(params_text):
	global log_content
	args = params_text.split()
	log_content +='\nPost-update script: ' + params_text
	proc = Popen(args, stdout=PIPE, stderr=PIPE)
	out, err = proc.communicate()
	if len(err)>0:
		log_content += '\nsubprocess error: ' + err


#main function - loops through found .properties files and triggers further actions
def process_properties_files():
	global log_content
	for subdir, dirs, files in os.walk(os.path.dirname(os.path.abspath(__file__))):
		for file in files:
			ext = os.path.splitext(file)[-1].lower()
			
			if ext == '.properties' and '/remote-git' not in subdir:
				config.read(os.path.join(subdir, file))
				script_name = os.path.splitext(file)[0].lower()
				should_update = is_update_time(subdir, script_name, config['DEFAULT']['check_frequency'])
				if should_update:
					log_content = str(time.time())
					log_content += '\nRunning update based on ' + file
					log_content += '\nTime (UTC): ' + datetime.utcnow().strftime("%d-%m-%Y @ %H:%M:%S")

					try:
						update_from_git(config['DEFAULT']['git_remote'], config['DEFAULT']['local_path'])
					except Exception as e:
						log_content += '\nupdate_from_git error: ' + str(e)
					try:
						copy_updated_files(config['DEFAULT']['local_path'])
					except Exception as e:
						log_content += '\ncopy_updated_files error: ' + str(e)
					try:
						if len(config['DEFAULT']['post_update'])>1:
							call_post_install_script(config['DEFAULT']['post_update'])
					except Exception as e:
						log_content += '\ncall_post_install_script error: ' + str(e)
					write_last_log(subdir, script_name)


#run script
if __name__== "__main__":
	process_properties_files()
