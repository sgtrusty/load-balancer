'''
 # SpinachSocket - a metric load balancer with multi-threading
 # Copyright (C) 2022  Santiago González <https://github.com/sgtrusty>
 #             ~ Assembled through trust in coffee. ~
 #
 # This program is free software; you can redistribute it and/or modify
 # it under the terms of the CC BY-NC-ND 4.0 as published by
 # the Creative Commons; either version 2 of the License, or
 # (at your option) any later version.
 #
 # This program is distributed in the hope that it will be useful,
 # but WITHOUT ANY WARRANTY; without even the implied warranty of
 # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 # CC BY-NC-ND 4.0 for more details.
 #
 # You should have received a copy of the CC BY-NC-ND 4.0 along
 # with this program; if not, write to the  Creative Commons Corp.,
 # PO Box 1866, Mountain View, CA 94042.
 #
'''
import random

class ScalePolicy:
    def route(self):
        pass

    def update(self, *arg):
        pass

# n to 1 policy
class N2One(ScalePolicy):
    def __init__(self, servers):
        self.servers = servers

    def route(self):
        return self.servers[0]

# round robin policy
class RoundRobin(ScalePolicy):
    def __init__(self, servers):
        self.servers = servers

    def _interpolate(self, r, x):
        c = x % r[1] + r[0]
        return c

    def route(self):
        return self.servers[self.__meta]
    
    def update(self, *arg):
        if(len(arg) == 0):
            return -1

        meta = arg[0]
        self.__meta = self._interpolate([0, len(self.servers)], meta+1)
        return self.__meta

# least connections policy
class LeastConnections(ScalePolicy):
    def __init__(self, servers):
        self.servers = servers

    def route(self):
        return self.servers[self.__meta['current']]

    def update(self, *arg):
        if(len(arg) == 0):
            return {'current':0, 'polls':[0 for _ in range(len(self.servers))]}

        self.__meta = arg[0]
        least = [i for i, x in enumerate(self.__meta['polls']) if x == min(self.__meta['polls'])]
        self.__meta['current'] = random.choice(least)
        self.__meta['polls'][self.__meta['current']] = self.__meta['polls'][self.__meta['current']]+1
        return self.__meta

# least response time
class LeastResponseTime(ScalePolicy):
    def __init__(self, servers):
        self.servers = servers

    def update(self, *arg):
        # ping all output destinations based on forward_policy
        # store outcome in state holder
        pass

# random
class RandomChoice(ScalePolicy):
    def __init__(self, servers):
        self.servers = servers

    def route(self):
        return random.choice(self.servers)

SCALE_POLICIES = {
    "N2One": N2One,
    "RoundRobin": RoundRobin,
    "LeastConnections": LeastConnections,
    "LeastResponseTime": LeastResponseTime,
    "Random": RandomChoice
}

class ScalingHandler(ScalePolicy):
    def __new__(self, scaling_type, routes):
        return scaling_type(routes)