import socket
import sys
import json
from src.orderbook import OrderBook
from  src.tradingStrategy import TradingStrategy

HOST, PORT = 'localhost', 9995
data = " ".join(sys.argv[1:])

# trader = Trader()
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((HOST, PORT))
    while True:
        encoding = 'utf-8'
        received = str(sock.recv(1024), encoding=encoding)
        print(f"Sent:    {'nothing' if not data else data}")
        # turn string
        # into a dict
        new_order = json.loads(received)
        # ob = OrderBook()
        # ts = TradingStrategy()
        # ts.get_best_order(ob)

        print(f'Received: {new_order}')
