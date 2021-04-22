# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import ipaddress
import json
from fileinput import filename
from ipaddress import IPv6Address

import psutil
import platform
from datetime import datetime
import os
import platform

from contextlib import redirect_stdout

import socket


def get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

uname = platform.uname()
#CPU
cpufreq = psutil.cpu_freq()

# print(f"Processor: {uname.processor}")
# print(f"Max Frequency: {(cpufreq.max/1000):.2f}Ghz")
# print("Physical cores:", psutil.cpu_count(logical=False))

CPU = [
      {
   "Description": uname.processor + ' @' + " {} Ghz".format(cpufreq.max/1000),
  "NumberOfCores": psutil.cpu_count(logical=False)
}
]

finalarray = [{}]
finalarray[0]["CPUs"] = CPU




#Memory
svmem = psutil.virtual_memory()
# print(f"Total: {get_size(svmem.total)}")
# print(f"Available: {get_size(svmem.available)}")

Memory = [
      {
   "InstalledGB": get_size(svmem.total),
  "AvailableGB": get_size(svmem.available)
}
]


finalarray[0]["Memory"] = Memory
#print(finalarray)

#Storage


storagearray = []

# Disk Information
# print("="*40, "Disk Information", "="*40)
# print("Partitions and Usage:")
# get all disk partitions
partitions = psutil.disk_partitions()
for partition in partitions:
    storage = {}

    # print(f"=== Device: {partition.device} ===")
    storage["Description"] = partition.device
    try:
        partition_usage = psutil.disk_usage(partition.mountpoint)
    except PermissionError:
        # this can be catched due to the disk that
        # isn't ready
        continue
    storage["CapacityGB"] = get_size(partition_usage.total)
    storage["AvailableGB"] = get_size(partition_usage.free)
    storagearray.append(storage)

    # print(f"  Total Size: {get_size(partition_usage.total)}")
    # print(f"  Free: {get_size(partition_usage.free)}")

finalarray[0]["Storage"] = storagearray
# finalarray.append({"Storage": storagearray})
#print(finalarray)

networkarray = []

#
# Network information
# print("="*40, "Network Information", "="*40)
# get all network interfaces (virtual and physical)
if_addrs = psutil.net_if_addrs()
for interface_name, interface_addresses in if_addrs.items():
    for address in interface_addresses:
        network = {}
        # print(f"=== Interface: {interface_name} ===")
        network["Description"] = interface_name
        if str(address.family) == 'AddressFamily.AF_INET':
            network["IP"] = address.address
            network["Netmask"] = address.netmask
            networkarray.append(network)
            # print(f"  IP Address: {address.address}")
            # print(f"  Netmask: {address.netmask}")
        elif str(address.family) == 'AddressFamily.AF_PACKET':
            network["Netmask"] = address.netmask
            networkarray.append(network)
            # print(f"  Netmask: {address.netmask}")
    networkarray.append(network)
# get IO statistics since boot
net_io = psutil.net_io_counters()
finalarray[0]["Network"] = networkarray

# finalarray.append({"Network": networkarray})
#print(finalarray)

#print json nicely as shown in example

# print(json.dumps(finalarray, indent=4, sort_keys=False))

# with open('machinedata.json', 'w') as f:
#     print(json.dumps(finalarray, indent=4, sort_keys=False), filename, file=f)
#     #print('Filename:', filename, file=f)  # Python 3.x

#print to JSON file
with open('machinedata.json', 'w') as f:
    with redirect_stdout(f):
        print(json.dumps(finalarray, indent=4, sort_keys=False))


# f = open("machinedata.json", "r")
# clearnewlines = f.read().splitlines()
# for x in clearnewlines:
#   print(x)


# part 2
# with open('machinedata.json') as json_file:
#     data = json.load(json_file)
#     # print(data[0]['Network'])
#     network_size = len(data[0]['Network'])
#     for i in range(0, network_size):
#         if "IP" in data[0]['Network'][i]:
#             print(data[0]['Network'][i])
#             IPv4 = data[0]['Network'][i]["IP"]
            # numbers = list(map(int, IPv4.split('.')))
            # hex = '2002:{:02x}{:02x}:{:02x}{:02x}::'.format(*numbers)
            # IPv6 = IPv6Address(ipaddress.ip_address(hex))
            # ipaddress.ip_address(hex)
            # print(IPv6)
            # IPv6 = IPv6Address(ipaddress.ip_address(hex))
            # print(IPv6)
            # s = socket()
            # s.getaddrinfo(IPv4, None, socket.AF_INET6)




