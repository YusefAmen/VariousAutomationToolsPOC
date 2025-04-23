import heapq
from collections import defaultdict
from datetime import datetime

class RateLimiter:
    def __init__(self, name='default', time_window=60, limit=10):
        self.name = name
        self.queue = []
        self.time_window = time_window
        self.limit = limit

    def is_allowed(self, user_id: str, timestamp: int) -> bool:

        # first i need to check if the item can be added to the heapq which maintaisn the smallest timestamp at the front 
        now = datetime.now()
        while len(self.queue) > sel.limit and now - timestamp > now - self.time_window:
            heapq.heappop(self.queue)


        # then need to add new tiem stamp
        if now - timestamp > self.queue[0]:
            heapq.heappush(self.queue, timestamp)


        return True

    def __str__(self):
        return self.name + ": [" + ",".join(str(x) for x in self.queue) + "]"




def main():
    rl = RateLimiter()

    print(rl)

if __name__ == '__main__':
    main()
