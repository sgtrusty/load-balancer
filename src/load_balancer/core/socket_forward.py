# least connections policy
class SocketForwardPolicy:
    def deliver(self, route, content):
        pass

class SocketForwardPolicyHTTP(SocketForwardPolicy):
    def deliver(self, route, content):
        pass
class SocketForwardPolicySocket(SocketForwardPolicy):
    def deliver(self, route, content):
        pass
class SocketForwardPolicyBucket(SocketForwardPolicy):
    def deliver(self, route, content):
        pass
class SocketForwardPolicyObjectPool(SocketForwardPolicy):
    def deliver(self, route, content):
        pass
class SocketForwardPolicyFile(SocketForwardPolicy):
    FILE_POOL = '.objs/'
    def deliver(self, route, content):
        #file1 = open(self.FILE_POOL + route, "a")
        #file1.write(content)
        #file1.close()
        pass

FORWARD_POLICIES = {
    "HTTP": SocketForwardPolicyHTTP,
    "Socket": SocketForwardPolicySocket,
    "Bucket": SocketForwardPolicyBucket,
    "ObjectPool": SocketForwardPolicyObjectPool,
    "File": SocketForwardPolicyFile
}
class SocketForwardHandler:
    def __init__(self, forwarder_type):
        self.__forwarder_type = forwarder_type
    def forward(self, route, content):
        self.__forwarder = self.__forwarder_type()
        self.__forwarder.deliver(route, content)