#!/usr/bin/env python3

from __future__ import absolute_import, division, print_function
from getpass import getpass
import json
import netmiko, paramiko
import signal
import sys

signal.signal(signal.SIGPIPE, signal.SIG_DFL)  # IOError: Broken pipe
signal.signal(signal.SIGINT, signal.SIG_DFL)  # KeyboardInterrupt: Ctrl-C


#Initiate an connection to device via SSH given IP, device type, user, pass, enable secret
def startConnection():
    #getting device info
    print('-'*79)
    ip_addr = input('IP Address: ')
    device = input('Device type: ')
    username = input('Username: ')
    password = getpass('Password: ')
    secret = getpass('Secret: ')
    print('-'*79)

    #storing device info in dict
    device_info = {
        'device_type': device,
        'ip': ip_addr,
        'username': username,
        'password': password,
        'secret': secret,
    }
    print(
        'Connecting to', device_info['ip'], 'as', device_info['username'], 
        "\nEnter a command (commands sep by comma) or type 'quit' to exit program")

    #establishing the connection with given information from device_info
    connection = netmiko.ConnectHandler(**device_info)
    connection.enable() #enters enable mode with provided password
    return connection


#handles configuration commands sent, parses into list
def sendConfig(connection, command_list):
    config_commands = []
    config_commands += command_list.split(',')
    connection.send_config_set(config_commands, exit_config_mode=False)


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
                output = connection.send_command(choice)
                print(output)
            elif choice.lower()=='quit':
                print('Thanks for using SSH Automation. Goodbye!')
                connection.disconnect()
                running = False
            else:
                sendConfig(connection, choice)
    except netmiko_exceptions as e:
        print('Error: ', e, '\nPlease try again.')
        automate_ssh_connection()


automate_ssh_connection()