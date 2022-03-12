import socket
import sys
import json
from src.trader import Trader

HOST, PORT = 'localhost', 9995
data = " ".join(sys.argv[1:])

trader = Trader()
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((HOST, PORT))
    while True:
        encoding = 'utf-8'
        received = str(sock.recv(1024), encoding=encoding)
        print(f"Sent:    {'nothing' if not data else data}")
        # turn string
        # into a dict
        new_order = json.loads(received)
        # trader.react_to_new_order(new_order)
        print(f'Received: {new_order}')
