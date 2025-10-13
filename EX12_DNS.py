import socket
import struct

def dns_query(domain):
    # Build DNS query packet
    transaction_id = b'\xaa\xbb'   # ID
    flags = b'\x01\x00'            # Standard query
    questions = b'\x00\x01'        # QDCOUNT (1 question)
    answer_rrs = b'\x00\x00'
    authority_rrs = b'\x00\x00'
    additional_rrs = b'\x00\x00'

    # Encode domain (e.g., example.com -> 7example3com0)
    query = b''.join(
        (bytes([len(part)]) + part.encode() for part in domain.split('.'))
    ) + b'\x00'

    qtype = b'\x00\x01'   # Type A
    qclass = b'\x00\x01'  # Class IN

    packet = transaction_id + flags + questions + answer_rrs + authority_rrs + additional_rrs + query + qtype + qclass

    # Send UDP packet
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(5)
    sock.sendto(packet, ("8.8.8.8", 53))  # Google Public DNS
    data, _ = sock.recvfrom(512)
    sock.close()

    # Parse response
    ip_list = []
    answer_offset = 12 + len(query) + 4
    while answer_offset < len(data):
        atype = struct.unpack("!H", data[answer_offset+2:answer_offset+4])[0]
        length = struct.unpack("!H", data[answer_offset+10:answer_offset+12])[0]
        if atype == 1 and length == 4:  # IPv4
            ip_bytes = data[answer_offset+12:answer_offset+16]
            ip = ".".join(str(b) for b in ip_bytes)
            ip_list.append(ip)
        answer_offset += 16
    return ip_list


# -------- Main program --------
domain = input("Enter domain name: ")
ips = dns_query(domain)
print(f"Resolved IPs for {domain}: {ips if ips else 'No IP found'}")
