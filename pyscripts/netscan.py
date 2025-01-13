# Import required packages from the Scapy library
from scapy.all import ARP, Ether, srp, conf
import csv
import socket
import ipaddress

# Confirm if npcap is well configured
print(conf.ifaces)


# Get the local IP Address of your device
def getLocalIp():
    # Gets the local IP address of the machine
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Connect to Google's DNS server
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        print(local_ip)
        return local_ip
    except Exception as e:
        print(f"Error getting local IP: {e}")
        return None


# getLocalIp()


# Get the network range
def getNetworkRange(ipAddress):
    # Gets the network range based on the Ip Address
    if not ipAddress:
        return None
    try:
        network = ipaddress.ip_network(ipAddress + "/24", strict=False)
        print(network)
        return str(network)
    except Exception as e:
        print(f"Error getting network range: {e}")
        return None


# getNetworkRange('192.168.62.10')


# Function to scan network and get the connected devices
def scanNetwork(network):
    print("scanning network", network)
    # Create an ARP request
    arp = ARP(pdst=network)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp

    # Send the packet and capture the responses
    # conf.L3socket = L3RawSocket
    result = srp(packet, timeout=3, verbose=0)[0]

    devices = []
    for sent, received in result:
        devices.append({"IP": received.psrc, "MAC": received.hwsrc})

    print(devices)
    return devices


# scanNetwork("192.168.62.0/24")


# Save devices found to a csv
def saveToCsv(devices, filename):
    # Saves the scanned devices to a CSV file.
    with open(filename, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["IP", "MAC"])
        writer.writeheader()
        for device in devices:
            writer.writerow(device)


# Execute all the functions from the block below.


def scan():
    # Get IP Address for my network
    ipAddress = getLocalIp()

    # Return if no IP found
    if not ipAddress:
        print("Failed to get local IP. Exiting.")
        return

    # Get the network range
    networkRange = getNetworkRange(ipAddress)

    # Scan the network using the network range found
    print("Scanning the network...")
    devices = scanNetwork(networkRange)
    # devices = scanNetwork("192.168.13.0/24")
    if devices:
        print(f"Found {len(devices)} devices on the network.")
        for device in devices:
            print(f"IP: {device['IP']}, MAC: {device['MAC']}")
        # Save results to a CSV file
        filename = "network_scan_report.csv"
        saveToCsv(devices, filename)
        print(f"Report saved to {filename}.")
    else:
        print("No devices found on the network.")


scan()
