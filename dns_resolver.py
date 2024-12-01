import socket
import threading
import struct

MAX_SIZE = 512

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind(('0.0.0.0', 5353))
    print("DNS server listening on port 5353...")

    while True:
        data, addr = server.recvfrom(MAX_SIZE)
        thread = threading.Thread(target=handle_request, args=(data, addr, server))
        thread.start()

def handle_request(data, addr, server):
    response = process_query(data)
    server.sendto(response, addr)

def process_query(data):
    try:
        domain_name, question_end = parse_domain_name(data, 12)

        # Load the domain map and resolve the query
        domain_map = load_myhosts()
        ip_address = domain_map.get(domain_name, None)
        if not ip_address:
            print(f"No record found for {domain_name}")
            return b''
        return build_response(data, ip_address, question_end)
    except Exception as e:
        print(f"Error processing query: {e}")
        return b''

def parse_domain_name(data, offset):
    domain_parts = []
    while True:
        length = data[offset]
        if length == 0:
            break
        domain_parts.append(data[offset + 1:offset + 1 + length].decode())
        offset += length + 1
    return ".".join(domain_parts), offset + 1

def build_response(query, resolved_ip, question_end):
    transaction_id = query[:2]
    flags = struct.pack(">H", 0x8180)  # Standard response, no error
    qdcount = struct.pack(">H", 1)  # 1 question
    ancount = struct.pack(">H", 1)  # 1 answer
    nscount = struct.pack(">H", 0)  # 0 authority records
    arcount = struct.pack(">H", 0)  # 0 additional records

    # Echo the question section
    question = query[12:question_end + 4]  # Include QTYPE and QCLASS (4 bytes)

    # Build the answer section
    answer_name = struct.pack(">H", 0xC00C)  # Pointer to the domain name in the question
    answer_type = struct.pack(">H", 1)  # Type A
    answer_class = struct.pack(">H", 1)  # Class IN
    ttl = struct.pack(">I", 300)  # TTL (300 seconds)
    data_length = struct.pack(">H", 4)  # IPv4 address is 4 bytes
    ip_parts = [int(octet) for octet in resolved_ip.split('.')]
    rdata = struct.pack(">BBBB", *ip_parts)  # Convert IP to binary

    answer = answer_name + answer_type + answer_class + ttl + data_length + rdata

    response = transaction_id + flags + qdcount + ancount + nscount + arcount + question + answer
    return response

def load_myhosts(file_path="/etc/myhosts"):
    domain_map = {}
    try:
        with open(file_path, "r") as file:
            for line in file:
                if line.strip() and not line.startswith("#"):
                    ip, domain = line.split()
                    ip = ip.strip()
                    domain = domain.strip()
                    domain_map[domain] = ip
    except FileNotFoundError:
        print("Error: /etc/myhosts file not found.")
    return domain_map

if __name__ == "__main__":
    start_server()
