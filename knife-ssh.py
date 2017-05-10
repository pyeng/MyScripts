#!/usr/bin/env python

import paramiko
import time
import yaml

def import_vars():
    # Import yaml file with VARIABLES

    with open("knife_vars.yaml") as f:
        vars = yaml.load(f)
        return vars


def disable_paging(remote_conn):
    # Disable paging on a Cisco router

    remote_conn.send("terminal length 0\n")
    time.sleep(0.5)

    # Clear the buffer on the screen
    output = remote_conn.recv(1000)

    return output


def exec_commands(command):
    # Let's try to send the device commands

    for command in commands:
        remote_conn.send("\n")
        remote_conn.send("{}\n".format(command))

        # Wait for the command to complete
        time.sleep(0.5)
            
        output = remote_conn.recv(5000)
        print output


if __name__ == '__main__':

    vars     = import_vars()
    ip_list  = vars["ip"]
    username = vars["username"]
    password = vars["password"]
    commands = vars["commands"]

    # Create instance of SSHClient object
    remote_conn_pre = paramiko.SSHClient()

    # Automatically add untrusted hosts (make sure okay for security policy in your environment)
    remote_conn_pre.set_missing_host_key_policy(
         paramiko.AutoAddPolicy())

    for ip in ip_list:

        # Initiate SSH connection
        remote_conn_pre.connect(ip, username=username, password=password, look_for_keys=False, allow_agent=False)
        print "SSH connection established to %s" % ip

        # Use invoke_shell to establish an 'interactive session'
        remote_conn = remote_conn_pre.invoke_shell()
        print "Interactive SSH session established"

        # Turn off paging
        disable_paging(remote_conn)

        # Exec commands
        exec_commands(commands)