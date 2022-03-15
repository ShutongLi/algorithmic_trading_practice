import heapq
import itertools

class OrderQueue:

    def __init__(self):
        self.queue = []
        self.counter = itertools.count()
        self.__remove_placeholder__ = '<removed-task>'
        self.oid_order_lookup = {}

    # push the order of a symbol into
    def push(self, new_order, priority):
        # pointer_copy =
        pass
