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
from enum import Enum

from core.forward import FORWARD_POLICIES, ForwardHandler
from core.scaling import SCALE_POLICIES, ScalingHandler
from core.reader import READER_POLICIES

# policies
class POLICIES(Enum):
    NONE = 0

    FORWARD = 1
    SCALE = 2
    READER = 3

    LAST = 3
    INVALID = 16


DEFAULT_POLICIES = {
    POLICIES.FORWARD: FORWARD_POLICIES['File'],
    POLICIES.SCALE: SCALE_POLICIES['LeastConnections'],
    POLICIES.READER: READER_POLICIES['Generic']
}