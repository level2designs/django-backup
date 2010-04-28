from django.conf import settings
from django.core.management import setup_environ
from django.utils.importlib import import_module

import os
import subprocess
import shlex

def get_manage_py():
    module = import_module(settings.SETTINGS_MODULE)
    return os.path.join(setup_environ(module, settings.SETTINGS_MODULE), 'manage.py')
    
def run_command_on_server(host, username, command, wait=False):
    full_command = str("ssh %s@%s '%s'" % (username, host, command))
    print full_command
#    print shlex.split(full_command)
    p = subprocess.Popen(shlex.split(full_command))
    if wait:
        p.wait()
    return p
    
def run_command_from_server(from_host, from_username, to_host, to_username, command, wait=False):
    to_command = str("ssh %s@%s \"%s\"") % (to_username, to_host, command)
    from_command = str("ssh %s@%s '%s'" % (from_username, from_host, to_command))
    print from_command
#    print shlex.split(from_command)
    p = subprocess.Popen(shlex.split(from_command))
    if wait:
        p.wait()
    return p
    
def run_make_backup_dir(backup_server, backup_server_path):
    command = "mkdir -p %s" % backup_server_path
    proc = run_command_on_server(backup_server.address.strip(), backup_server.username.strip(), command, True)
    
def run_directory_backup(backup_server, client, remote_path, backup_server_path):
    command = "rdiff-backup %s@%s::%s %s" % (client.username.strip(), client.address.strip(), remote_path.strip(), backup_server_path)
    proc = run_command_on_server(backup_server.address.strip(), backup_server.username.strip(), command, True)

def run_database_backup(backup_server, client, database):
    #make mysqldump dir
    command = "mkdir -p %s" % client.database_dump_path.strip()
    proc = run_command_from_server(backup_server.address.strip(), backup_server.username.strip(), client.address.strip(), client.username.strip(), command, True)
    
    #run mysql dump
    command = "mysqldump --user=%s --password=%s %s > %s/%s.sql" % (database.username.strip(), database.password.strip(), 
                                                                        database.db_name.strip(), client.database_dump_path.strip(), database.db_name.strip())
    
    proc = run_command_from_server(backup_server.address.strip(), backup_server.username.strip(), client.address.strip(), client.username.strip(), command, True);