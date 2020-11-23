#!/usr/bin/env python3

from __future__ import absolute_import, division, print_function
from getpass import getpass
import netmiko, paramiko
import json
import signal
import sys

signal.signal(signal.SIGPIPE, signal.SIG_DFL)  # IOError: Broken pipe
signal.signal(signal.SIGINT, signal.SIG_DFL)  # KeyboardInterrupt: Ctrl-C


#Initiate an connection to device via SSH given IP, device type, user, pass, enable secret
def startConnection():
    print('-'*79)
    ip_addr = input('IP Address: ')
    device = input('Device type: ')
    username = input('Username: ')
    password = getpass('Password: ')
    secret = getpass('Secret: ')
    print('-'*79)

    #stores device information in a dictionary, adds to dictlist devices
    device_info = {
        'device_type': device,
        'ip': ip_addr,
        'username': username,
        'password': password,
        'secret': secret,
    }
    print(
        'Connecting to device', device_info['ip'], 'as', device_info['username'], 
        "\nEnter a command or type 'quit' to exit program")

    #connect to device using values stored in dictionary
    connection = netmiko.ConnectHandler(**device_info)
    connection.enable() #enable mode
    return connection


#sending a specific command
def sendCommand(connection, command):
    output = connection.send_command(command)
    print(output)


#handles configuration commands sent
def sendConfig(connection, command_list):
    #gathering the commands
    config_commands = []
    config_commands += command_list.split(',')

    #showing output of the command
    output = connection.send_config_set(config_commands, exit_config_mode=False)
    print(output)


#dicsonnects from the device
def disconnectDevice(connection):
    connection.disconnect()


netmiko_exceptions = (
    netmiko.ssh_exception.NetMikoTimeoutException,
    netmiko.ssh_exception.NetMikoAuthenticationException,
    paramiko.ssh_exception.AuthenticationException,
    ValueError
    )


#runs the script
def automate_ssh_connection(running=True):
    try:
        connection = startConnection()
        while running:
            print('-'*79)
            choice = input(connection.find_prompt())
            if 'show' in choice:
                sendCommand(connection, choice)
            elif choice.lower()=='quit':
                print('Thanks for using SSH Automation. Goodbye!')
                disconnectDevice(connection)
                running = False
            else:
                sendConfig(connection, choice)
    except netmiko_exceptions as e:
        print('Error: ', e, '\nPlease try again.')
        automate_ssh_connection()


automate_ssh_connection()