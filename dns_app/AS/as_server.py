import socket
import json

DNS_DB_FILE = 'dns_records.json'

def load_dns_records():
    try:
        with open(DNS_DB_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_dns_records(records):
    with open(DNS_DB_FILE, 'w') as file:
        json.dump(records, file)

def handle_registration(data):
    records = load_dns_records()
    hostname = data[1].split('=')[1]
    ip_address = data[2].split('=')[1]
    ttl = data[3].split('=')[1]

    records[hostname] = {'ip': ip_address, 'ttl': ttl}
    save_dns_records(records)

def handle_query(data):
    records = load_dns_records()
    hostname = data[1].split('=')[1]

    if hostname in records:
        record = records[hostname]
        response = f"TYPE=A\nNAME={hostname}\nVALUE={record['ip']}\nTTL={record['ttl']}\n"
        return response
    else:
        return None

def start_udp_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.bind(('0.0.0.0', 53533))
    
    while True:
        data, addr = server.recvfrom(1024)
        data = data.decode().split('\n')
        
        if data[0] == 'TYPE=A':
            if len(data) == 4:
                # Registration Request
                handle_registration(data)
            else:
                # Query Request
                response = handle_query(data)
                if response:
                    server.sendto(response.encode(), addr)

if __name__ == '__main__':
    start_udp_server()
