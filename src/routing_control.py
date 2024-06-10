import os

def show_routes():
    os.system("route -n")

def add_fake_gateway():
    os.system("route add default gw 192.168.1.1")

if __name__ == "__main__":
    print("Current routing table:")

    show_routes()

    print("\nAdding fake gateway...")

    add_fake_gateway()

    print("New routing table:")

    show_routes()
