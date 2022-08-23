# least connections policy
class ForwardPolicy:
    __upstream = None
    def deliver(self, content):
        pass
    def hasSocket(self):
        return __upstream is not None
    def getSocket(self):
        return __upstream

class ForwardPolicyHTTP(ForwardPolicy):
    def deliver(self, content):
        pass
class ForwardPolicySocket(ForwardPolicy):
    def __init__(self, route):
        __upstream = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        __upstream.connect(route)
        __upstream.setblocking(False)
        pass
    def deliver(self, content):
        __upstream.send(content)
        pass
class ForwardPolicyBucket(ForwardPolicy):
    hasResponse = True
    def deliver(self, content):
        pass
class ForwardPolicyObjectPool(ForwardPolicy):
    hasResponse = True
    def deliver(self, content):
        pass
class ForwardPolicyFile(ForwardPolicy):
    hasResponse = True
    FILE_POOL = '.objs/'
    def __init__(self, route):
        self.__route = route
    def deliver(self, content):
        try:
            file1 = open(self.FILE_POOL + self.__route, "a")
            file1.write(content)
            file1.close()
            return {'status': 200, 'message': "Done"}
        except Exception as err:
            return {'status': 500, 'message': "Received exception", "exception": err}

FORWARD_POLICIES = {
    "HTTP": ForwardPolicyHTTP,
    "Socket": ForwardPolicySocket,
    "Bucket": ForwardPolicyBucket,
    "ObjectPool": ForwardPolicyObjectPool,
    "File": ForwardPolicyFile
}
class ForwardHandler(ForwardPolicy):
    def __new__(self, forwarder_type, route):
        return forwarder_type(route)