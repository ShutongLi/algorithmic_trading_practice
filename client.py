import socket
import sys
import json
from src.orderbook import OrderBook
import itertools

HOST, PORT = 'localhost', 9995
data = " ".join(sys.argv[1:])

counter = itertools.count()
ob = OrderBook()
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((HOST, PORT))

    while True:
        encoding = 'utf-8'
        received = str(sock.recv(1024), encoding=encoding)
        try:
            print(f'received order {received}')
            # turn string
            # into a dict
            new_order = json.loads(received)
            decision = ob.react_to_market_order(new_order)
            if (next(counter) + 1) % 100 == 0:
                print(ob.tm)
            package = decision.encode('utf-8')
            print(f'sending {package}')
            sock.sendall(package)
        except (json.decoder.JSONDecodeError, KeyError) as e:
            print(e)
            print(f'you fucked up! {received}')
            break
    print(ob.tm)
