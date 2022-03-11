import socket
import sys
import json
from src.orderbook import OrderBook

HOST, PORT = 'localhost', 9995
data = " ".join(sys.argv[1:])

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((HOST, PORT))
    while True:
        encoding = 'utf-8'
        received = str(sock.recv(1024), encoding=encoding)
        print(f"Sent:    {'nothing' if not data else data}")
        order = json.loads(received)
        print(f'Received: {order}')
