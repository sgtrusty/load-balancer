import random

# n to 1 policy
class N2One:
    def __init__(self, servers):
        self.servers = servers  

    def route(self):
        return self.servers[0]

    def update(self, *arg):
        pass


# round robin policy
class RoundRobin:
    def __init__(self, servers):
        self.servers = servers

    def route(self):
        pass
    
    def update(self, *arg):
        pass


# least connections policy
class LeastConnections:
    def __init__(self, servers):
        self.servers = servers

    def route(self):
        pass

    def update(self, *arg):
        pass


# least response time
class LeastResponseTime:
    def __init__(self, servers):
        self.servers = servers

    def route(self):
        pass

    def update(self, *arg):
        pass


# random
class RandomChoice:
    def __init__(self, servers):
        self.servers = servers

    def route(self):
        return random.choice(self.servers)

    def update(self, *arg):
        pass


SCALE_POLICIES = {
    "N2One": N2One,
    "RoundRobin": RoundRobin,
    "LeastConnections": LeastConnections,
    "LeastResponseTime": LeastResponseTime,
    "Random": RandomChoice
}