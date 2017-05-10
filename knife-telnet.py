#!/usr/bin/env python

import telnetlib
import time
import yaml

def import_vars():
    # Import yaml file with VARIABLES

    with open("knife_telnet_vars.yaml") as f:
        vars = yaml.load(f)
        return vars


def disable_paging():
    # Disable paging on a Cisco router

        tn.write("disable clipaging" + "\n")
        print tn.read_until("NeverMatches",delay)

def enable_paging():
    # Enable paging on a Cisco router

        tn.write("enable clipaging" + "\n")
        #print tn.read_until("NeverMatches",delay)


def exec_commands(command):
    # Let's try to send the device commands

    for command in commands:
        # running actual command
        tn.write(command + "\n")
        print tn.read_until("NeverMatches",delay)


if __name__ == '__main__':

    delay    = 0.3
    port     = 23
    vars     = import_vars()
    hosts    = vars["hosts"]
    username = vars["username"]
    password = vars["password"]
    commands = vars["commands"]

    for host in hosts:

        tn = telnetlib.Telnet(str(host),port,delay)

        print tn.read_until("NeverMatches",delay)
        # passing username
        tn.write(username + "\n")
        # passing password
        print tn.read_until("NeverMatches",delay)
        tn.write(password + "\n")
        
        # Turn off paging
        disable_paging()

        # Exec commands
        exec_commands(commands)

        # Turn on paging
        enable_paging()

        #tn.write("exit\n")       