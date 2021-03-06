"""
This test represents a simple demo for testing.
Feel free to copy and modify at your leisure.
"""

from droneapi.lib import VehicleMode
from pymavlink import mavutil
import time
import sys
import os
from testlib import assert_equals

# This test runs first!
def test_parameter(local_connect):
    v = local_connect().get_vehicles()[0]

    # Perform a simple parameter check
    assert_equals(type(v.parameters['THR_MIN']), float)

# This test runs second. Add as many tests as you like
def test_mode(local_connect):
    v = local_connect().get_vehicles()[0]

    # Ensure Mode is an instance of VehicleMode
    assert isinstance(v.mode, VehicleMode)
