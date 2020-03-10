from automatic_control import Controller
from Sail_Logic_Functions_1 import gps_speed
from Sail_Logic_Functions_1 import rudder_angle
from Sail_Logic_Functions_1 import sails_angle
from Sail_Logic_Functions_1 import boatStatus
from Sail_Logic_Functions_1 import rudderLeeward
import pytest

def test_gybe():
    boatStatus()
    cont = Controller(None)
    #cont.gybe(359)
    rudderLeeward(20)
    assert rudder_angle == 90
    boatStatus()