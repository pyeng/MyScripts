#!/usr/bin/env python

import sys
import time
import serial


def read_serial(console):
    """ 
    Check if there is data waiting to be read. Read and return it.
    Else return null string
    """
    
    data_bytes = console.inWaiting()
    
    if data_bytes:
        return console.read(data_bytes)
    else:
        return ""


def check_logged_in(console):
    """ Check if logged in to switch """

    console.write("\n")
    time.sleep(0.5)
    prompt = read_serial(console)
    
    if "#" in prompt:
        return True
    else:
        return False


def login(console):
    """ Login to switch """

    login_status = check_logged_in(console)
    
    if login_status:
        print "Already logged in"
        return None

    print "Logging into switch"
    
    while True:
        console.write("\n")
        time.sleep(0.5)
        input_data = read_serial(console)
    
        if not "Username" in input_data:
            continue
    
        console.write("admin\n")
        time.sleep(0.5)

        input_data = read_serial(console)
        if not "Password" in input_data:
            continue
       
        console.write("admin\n")
        time.sleep(0.5)

        login_status = check_logged_in(console)
       
        if login_status:
            print "We are logged in\n"
            break


def logout(console):
    """ Exit from console session """

    print "Logging out from switch"
 
    while check_logged_in(console):
        console.write("exit\n")
        time.sleep(.5)

    print "Successfully logged out from switch"


def send_command(console, cmd=""):
    """ Send a command down the channel. Return the output """
    
    console.write(cmd + "\n")
    time.sleep(0.5)
    return read_serial(console)


def main():
    """ Interact to Edge-Core switch via serial port using Python """

    print "\nInitializing serial connection\n"

    console = serial.Serial(
        port = "/dev/ttyUSB0",
        baudrate=115200,
        parity="N",
        stopbits=1,
        bytesize=8,
        timeout=8
    )

    setup_ip = [
                "configure", 
                "interface vlan 1",
                "ip address 10.90.90.90 255.255.255.0",
                "end",
                ]
    
    fw_name = "ecs3510_28t_v1.5.2.7.bix"

    upload_fw = [
                "copy tftp file",
                "10.90.90.100",
                "2",
                fw_name,
                fw_name
                ]

    boot_new_fw = "boot system opcode:{}".format(fw_name)
    
    apply_fw = [
                "conf",
                boot_new_fw
                ]

    if not console.isOpen():
        sys.exit()

    login(console)
    
    for command in setup_ip:
        print send_command(console, cmd=command)
    
    for command in upload_fw:
        print send_command(console, cmd=command)
    time.sleep(200)

    for command in apply_fw:
        print send_command(console, cmd=command)
    time.sleep(15)

    logout(console)

if __name__ == "__main__":
    main()
