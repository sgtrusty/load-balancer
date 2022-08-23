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