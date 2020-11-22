#!/usr/bin/env python

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
    command = input('Enter Command: ')
    output = connection.send_command(command)
    print(output)


#handles configuration commands sent
def sendConfig(connection):
    #gathering the commands
    config_commands = []
    command = input('Enter config: ')
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
        choice = input('[ Show device config | Configure device | Quit ]')
        if 'show' in choice.lower():
            sendCommand(connection)
        elif 'config' in choice.lower():
            sendConfig(connection)
        elif 'qu' in choice.lower():
            print('Thanks for using network config. Goodbye!')
            disconnectDevice(connection)
            running = False


# startConnection()
automate_ssh_connection()