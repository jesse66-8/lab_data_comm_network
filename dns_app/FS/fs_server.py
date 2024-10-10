from flask import Flask, request, jsonify
import socket
import json

app = Flask(__name__)

def register_to_as(hostname, ip, as_ip, as_port):
    message = f"TYPE=A\nNAME={hostname}\nVALUE={ip}\nTTL=10\n"
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(message.encode(), (as_ip, as_port))
    sock.close()

def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

@app.route('/register', methods=['PUT'])
def register():
    data = request.get_json()
    hostname = data.get('hostname')
    ip = data.get('ip')
    as_ip = data.get('as_ip')
    as_port = data.get('as_port')

    if not all([hostname, ip, as_ip, as_port]):
        return "Bad Request", 400

    # Register with Authoritative Server
    register_to_as(hostname, ip, as_ip, int(as_port))
    return "Registered", 201

@app.route('/fibonacci', methods=['GET'])
def get_fibonacci():
    number = request.args.get('number')
    
    try:
        num = int(number)
    except ValueError:
        return "Bad Request: Invalid number", 400

    result = fibonacci(num)
    return jsonify({'fibonacci': result}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9090)
