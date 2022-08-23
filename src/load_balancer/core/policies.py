# n to 1 policy
class N2One:
    def __init__(self, servers):
        self.servers = servers  

    def select_server(self):
        return self.servers[0]

    def update(self, *arg):
        pass


# round robin policy
class RoundRobin:
    def __init__(self, servers):
        self.servers = servers

    def select_server(self):
        pass
    
    def update(self, *arg):
        pass


# least connections policy
class LeastConnections:
    def __init__(self, servers):
        self.servers = servers

    def select_server(self):
        pass

    def update(self, *arg):
        pass


# least response time
class LeastResponseTime:
    def __init__(self, servers):
        self.servers = servers

    def select_server(self):
        pass

    def update(self, *arg):
        pass


POLICIES = {
    "N2One": N2One,
    "RoundRobin": RoundRobin,
    "LeastConnections": LeastConnections,
    "LeastResponseTime": LeastResponseTime
}