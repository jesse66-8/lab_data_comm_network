from flask import Flask, request, jsonify
import requests
import socket

app = Flask(__name__)

def query_dns(hostname, as_ip, as_port):
    message = f"TYPE=A\nNAME={hostname}\n"
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(message.encode(), (as_ip, as_port))
    response, _ = sock.recvfrom(1024)
    sock.close()

    lines = response.decode().split('\n')
    if lines[0] == "TYPE=A":
        return lines[2].split('=')[1]  # Extract IP address from VALUE field
    return None

@app.route('/fibonacci', methods=['GET'])
def get_fibonacci():
    hostname = request.args.get('hostname')
    fs_port = request.args.get('fs_port')
    number = request.args.get('number')
    as_ip = request.args.get('as_ip')
    as_port = request.args.get('as_port')

    if not all([hostname, fs_port, number, as_ip, as_port]):
        return "Bad Request: Missing parameters", 400

    try:
        int(number)
    except ValueError:
        return "Bad Request: Invalid number", 400

    # Query the Authoritative Server for hostname IP
    fs_ip = query_dns(hostname, as_ip, int(as_port))
    if not fs_ip:
        return "DNS Query Failed", 500

    # Call Fibonacci Server
    fibonacci_url = f"http://{fs_ip}:{fs_port}/fibonacci?number={number}"
    response = requests.get(fibonacci_url)
    
    if response.status_code == 200:
        return response.content, 200
    else:
        return "Error from Fibonacci Server", response.status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
