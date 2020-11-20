'''
Subnet Calculator (currently only IPv4...working on IPv6)
takes IP and Subnet, returns relevant information
by Eugenia Liu
'''

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
        subnet = int(subnet_mask[1:])
        q,r = divmod(subnet,8)
        converted_subnet = ('255.'*q) + str(subnet_dict[r])
        octet_count = converted_subnet.count('.')
        if octet_count<3:
            converted_subnet += ('.0'*(3-octet_count))
    return converted_subnet


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


#Given DDN IP Address, converts to binary address each octet decimal is an 8 digit binary value)
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
    net_dec[-1] = str(int(net_dec[-1])+1)
    bcast_dec[-1] = str(int(bcast_dec[-1])-1)
    return [('.'.join(net_dec)), ('.').join(bcast_dec)]


#displays all relevant information given IP (DDN) and subnet mask (CIDR or prefix)
def SubnetCalculator():
    ip_addr = input('IP Address: ')
    subnet_mask = input('Subnet mask (x.x.x.x or /x): ')
    wildcard_bits = 32-getPrefixMask(subnet_mask)
    net = getNetBcastDec(ip_addr,subnet_mask)[0]
    bcast = getNetBcastDec(ip_addr,subnet_mask)[1]
    usable = getUsableRange(ip_addr,subnet_mask)
    hosts = int(getNumAddr(subnet_mask))
    print()
    print()
    print('CIDR notation: ' + ip_addr + '/' + str(getPrefixMask(subnet_mask)))
    print('Subnet Mask: /' + str(getPrefixMask(subnet_mask)) + ' or ' + getDecMask(subnet_mask))
    print('Wildcard Mask: /'  + str(wildcard_bits) + ' or ' + getWildcardMask(getDecMask(subnet_mask)))
    print('Network address: ' + net)
    print('Usable IP Range: ' + str(usable[0]) + ' - ' + str(usable[1]))
    print('Broadcast address: ' + bcast)
    print('Number of Addresses: ' + str(hosts))
    print('Number of Usable Hosts: ' + str(hosts-2))


SubnetCalculator()