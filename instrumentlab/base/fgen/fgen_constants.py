
from enum import Enum

class FgenConstants():

    class mode(Enum):
        VOLT_DC = "volt_dc"
        VOLT_AC = "volt_ac"
        CURR_DC = "curr_dc"
        CURR_AC = "curr_ac"

    class range_(Enum):
        MIN = "min"
        MAX = "max"
        AUTO = "auto"


