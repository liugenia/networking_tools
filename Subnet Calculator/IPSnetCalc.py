#!/usr/bin/env python3

from __future__ import absolute_import, division, print_function
from random import randint
import signal

# signal.signal(signal.SIGPIPE, signal.SIG_DFL)  # IOError: Broken pipe
signal.signal(signal.SIGINT, signal.SIG_DFL)  # KeyboardInterrupt: Ctrl-C

#dict of the 9 possible values of each octet of a subnet mask
subnet_dict = {0:0, 1:128, 2:192, 3:224, 4:240, 5:248, 6:252, 7:254, 8:255}


def getKey(val, dicto):
    for key,value in dicto.items():
        if val == value:
            return key


#Given DDN/CIDR notation, converts to the other
def snMaskConverter(subnet_mask):
    #Converts DDN to CIDR
    if '.' in subnet_mask:
        subnet = subnet_mask.split('.')
        prefix_sum = 0
        for octet in subnet:
            prefix_sum += getKey(int(octet), subnet_dict)
        converted_subnet = '/' + str(prefix_sum)
    #Converts CIDR to DDN
    if '/' in subnet_mask:
        subnet = getPrefixMask(subnet_mask)
        q,r = divmod(subnet,8)
        converted_subnet = (['255']*q) + [str(subnet_dict[r])]
        if len(converted_subnet)<4:
            converted_subnet += ('0'*(4-len(converted_subnet)))
    return '.'.join(converted_subnet[0:4]) #ensures 4 octets only, gets rid of extra 0 if r=0


#keeps or converts to CIDR notation when necessary
def getPrefixMask(subnet_mask):
    if '.' in subnet_mask:
        subnet_mask = snMaskConverter(subnet_mask)
    return int(subnet_mask[1:])


#keeps or converts to DDN when necessary
def getDecMask(subnet_mask):
    if '/' in subnet_mask:
        subnet_mask = snMaskConverter(subnet_mask)
    return subnet_mask


#calculates wildcard mask given subnet mask decimal
def getWildcardMask(subnet_mask):
    snet_dec = getDecMask(subnet_mask).split('.')
    wildcard_dec = [str(255-int(octet)) for octet in snet_dec]
    return  '.'.join(wildcard_dec)


#calculates the total number of usable addresses
def getNumAddr(subnet_mask):
    subnet_mask = getPrefixMask(subnet_mask)
    host_bits = 32-subnet_mask
    num_hosts = pow(2,host_bits)
    return num_hosts


#Given DDN IP Address, converts to binary address  (each octet decimal is an 8 digit binary value)
def getBinAddr(ip_addr):
    ip_addr = ip_addr.split('.')
    binary_addr = ''
    for octet in ip_addr:
        binary_addr += format(int(octet), '08b')
    return binary_addr


#Given binary IP Address and subnet mask, gets the network and broadcast address
def getNetBcastBin(ip_addr, subnet_mask):
    binary_addr = getBinAddr(ip_addr)
    subnet_mask = getPrefixMask(subnet_mask)
    net_addr = ''
    bcast_addr = ''
    for digits in binary_addr[:subnet_mask]:
        net_addr += digits
        bcast_addr += digits
    if subnet_mask<32:
        net_addr += ('0'*(32-subnet_mask))
        bcast_addr += ('1'*(32-subnet_mask))
    return [net_addr, bcast_addr]


#Converts a binary value to decimal
def binToDec(ip_addr):
    octets = []
    n=8
    for octet in range (0,len(ip_addr),n):
        octets.append(ip_addr[octet:(octet+n)])
    dec_addr = [str(int(octet,2)) for octet in octets]
    return '.'.join(dec_addr)
    

#gets the network and brodacast address in DDN
def getNetBcastDec(ip_addr, subnet_mask):
    net_dec = binToDec(getNetBcastBin(ip_addr,subnet_mask)[0])
    bcast_dec = binToDec(getNetBcastBin(ip_addr,subnet_mask)[1])
    return [net_dec, bcast_dec]


#given network and bcast decimal, returns list of first and lat address in usable range
def getUsableRange(ip_addr, subnet_mask):
    net_dec = [str(octet) for octet in getNetBcastDec(ip_addr,subnet_mask)[0].split('.')]
    bcast_dec = [str(octet) for octet in getNetBcastDec(ip_addr,subnet_mask)[1].split('.')]
    if abs(int(net_dec[-1])-int(bcast_dec[-1]))<=2: #if there are 2 or less addresses, return addresses as is
        return [('.'.join(net_dec)), ('.').join(bcast_dec)]
    else: #otherwise return net+1, bcast-1 as the usable range
        net_dec[-1] = str(int(net_dec[-1])+1) 
        bcast_dec[-1] = str(int(bcast_dec[-1])-1)
        return [('.'.join(net_dec)), ('.').join(bcast_dec)]


#calculates the total subnets you can have
def getNumSubnets(subnet_mask):
    subnet_mask = getDecMask(subnet_mask).split('.')
    nonzero_digit_index = 0
    for index, octet in enumerate(subnet_mask, 0):
        if octet!='0' and index>nonzero_digit_index: #finding last non-zero octet
            nonzero_digit_index=index
    borrowed_bits = getKey(int(subnet_mask[nonzero_digit_index]), subnet_dict)
    total_subnets = pow(2,borrowed_bits)
    return total_subnets
    

#displays all relevant information given IP (DDN) and subnet mask (DDN or CIDR)
def SubnetCalculator():
    print()
    while True:
        choice = input('Would you like to enter an IP? (1) Yes, (2) Surprise me!, (3) Quit\n')
        if choice=='1':
            ip_addr = input('IP Address: ')
            subnet_mask = input('Subnet mask (x.x.x.x or /x): ')
        elif choice=='2':
            ip_addr = '.'.join([str(randint(0,255)) for x in range(4)])
            subnet_mask = '/' + str(randint(0,32))
        elif choice=='3':
            print('Thanks for using IP Subnet Calculator. Goodbye!')
            break
        net = getNetBcastDec(ip_addr,subnet_mask)[0]
        bcast = getNetBcastDec(ip_addr,subnet_mask)[1]
        usable = getUsableRange(ip_addr,subnet_mask)
        addrs = int(getNumAddr(subnet_mask))
        print()
        print('CIDR notation: ' + ip_addr + '/' + str(getPrefixMask(subnet_mask)))
        print('Subnet Mask: /' + str(getPrefixMask(subnet_mask)) + ' or ' + getDecMask(subnet_mask))
        print('Wildcard Mask: '  + getWildcardMask(getDecMask(subnet_mask)))
        print('Network address: ' + net)
        print('Usable IP Range: ' + str(usable[0]) + ' - ' + str(usable[1]))
        print('Broadcast address: ' + bcast)
        print('Number of Addresses: ' + str(addrs))
        print('Number of Hosts: ' + str(max(0, addrs-2))) #does not display negative host addresses
        print('Max Number of Subnets: ' + str(getNumSubnets(subnet_mask)))
        print()


SubnetCalculator()