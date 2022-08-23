from core.socket_forward import SocketForwardHandler

class SocketBalancer:
    def __new__(self, routes, scale_policy, forward_policy, content):
        scaler = scale_policy(routes)
        route = scaler.route()
        
        forwarder = SocketForwardHandler(forward_policy)
        forwarder.forward(route, content)
        return route