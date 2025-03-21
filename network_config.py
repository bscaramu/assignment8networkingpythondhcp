#!/usr/bin/env python3

import sys
import re
import ipaddress
import json
import os

ipv4_pool = list(ipaddress.IPv4Network("192.168.1.0/24").hosts())
ipv6_subnet = "2001:db8::/64"
lease_file = "leases.json"

if os.path.exists(lease_file):
    with open(lease_file, 'r') as f:
        try:
            leases = json.load(f)
        except:
            leases = {}
else:
    leases = {}

def validate_mac(mac):
    return re.match(r"^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$", mac) is not None

def eui64(mac, subnet):
    parts = mac.split(":")
    mac_bytes = [int(part, 16) for part in parts]
    mac_bytes[0] ^= 0b00000010
    eui64_bytes = mac_bytes[:3] + [0xFF, 0xFE] + mac_bytes[3:]
    interface_id_int = int.from_bytes(eui64_bytes, byteorder='big')
    subnet_prefix = ipaddress.IPv6Network(subnet, strict=False)
    ipv6_int = int(subnet_prefix.network_address) + interface_id_int
    return str(ipaddress.IPv6Address(ipv6_int))

def save_leases():
    with open(lease_file, 'w') as f:
        json.dump(leases, f, indent=2)

def assign_ipv4(mac):
    for ip in ipv4_pool:
        ip_str = str(ip)
        if not any(lease.get("assigned_ipv4") == ip_str for lease in leases.values()):
            lease_info = {
                "mac_address": mac,
                "assigned_ipv4": ip_str,
                "lease_time": "3600 seconds",
                "subnet": "192.168.1.0/24"
            }
            leases[mac] = lease_info
            save_leases()
            return lease_info
    return {"error": "No available IPv4 addresses"}

def assign_ipv6(mac):
    ipv6 = eui64(mac, ipv6_subnet)
    lease_info = {
        "mac_address": mac,
        "assigned_ipv6": ipv6,
        "lease_time": "3600 seconds",
        "subnet": ipv6_subnet
    }
    leases[mac] = lease_info
    save_leases()
    return lease_info

if len(sys.argv) != 3:
    print(json.dumps({"error": "Usage: python3 network_config.py <MAC> <DHCPv4|DHCPv6>"}))
    sys.exit(1)

mac = sys.argv[1].upper()
dhcp_version = sys.argv[2]

if not validate_mac(mac):
    print(json.dumps({"error": "Invalid MAC address format"}))
    sys.exit(1)

if mac in leases:
    print(json.dumps(leases[mac]))
    sys.exit(0)

if dhcp_version == "DHCPv4":
    result = assign_ipv4(mac)
elif dhcp_version == "DHCPv6":
    result = assign_ipv6(mac)
else:
    result = {"error": "Invalid DHCP version"}

print(json.dumps(result))
