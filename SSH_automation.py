#!/usr/bin/env python3

from __future__ import absolute_import, division, print_function

import netmiko
import json
import getpass


#Initiate an connection to device via SSH given IP, device type, user and pass
def startConnection():
    print()
    print('.....CONNECTING TO A DEVICE.....')
    print()
    ip_addr = input('IP Address: ')
    device = input('Device type: ')
    username = input('Username: ')
    password = getpass.getpass('Password: ')
    secret = getpass.getpass('Secret:')
    print()

    #stores device information in a dictionary, adds to dictlist devices
    device_info = {
        'device_type': device,
        'ip': ip_addr,
        'username': username,
        'password': password,
        'secret': secret
    }

    #connect to device using values stored in dictionary
    connection = netmiko.ConnectHandler(**device_info)
    connection.enable() #enable mode

    #verify SSH connection established
    print(connection.find_prompt())
    return connection


#sending a specific command
def sendCommand(connection):
    command = input('Enter Command:\n')
    output = connection.send_command(command)
    print(output)


#handles configuration commands sent
def sendConfig(connection):
    #gathering the commands
    config_commands = []
    command = input('Enter config:\n')
    while command != "quit":
        config_commands += config_commands

    #showing output of the command
    output = connection.send_config_set(config_commands)
    print(output)


#dicsonnects from the device
def disconnectDevice(connection):
    connection.disconnect()


#runs the script
def automate_ssh_connection(running=True):
    connection = startConnection()
    while running:
        print('What would you like to do?')
        choice = input('(1) Show device config, (2) Configure device, (3) Quit\n')
        if choice=='1':
            sendCommand(connection)
        elif choice=='2':
            sendConfig(connection)
        elif choice=='3':
            print('Thanks for using SSH Automation. Goodbye!')
            disconnectDevice(connection)
            running = False


automate_ssh_connection()