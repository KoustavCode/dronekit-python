"""
This script is for testing that commands that are sent are correctly uploaded and can then be retrieved unchanged.

The script adds a number of commands and then reads them back. 
This first version is not automatic. The result is validated by inspection. To make this easy all values passed to 
the commands for lat/lon etc are the same, and these differ for each command.

- Returned commands should be one item bigger than was sent (Vehicle.commands[0] is the Home location waypoint)
- Vehicle.commands[1] (and later) should correspond to the commands set. 
"""

import time
from droneapi.lib import VehicleMode, Location, Command
from pymavlink import mavutil

api             = local_connect()
v         = api.get_vehicles()[0]

print 'Create mission'
#  	
cmds = v.commands
cmds.clear()

def scommand(command, param1,param2,param3,param4,param5,param6,param7):
    """
    Short command format. Pre-fills all the values which are always the same. It also pre
    fills the frame setting to MAV_FRAME_GLOBAL_RELATIVE_ALT as in most case this is good
    to use
    """
    return Command( 0, 0, 0, mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT, 
                command, 0, 0, 
                param1, param2, param3, param4, param5, param6, param7)


#add a takeoff command
altitude=10 #target altitude
pitch=10 #take off pitch. Need to check if degrees or radians, and what is a reasonable valued.
cmd = scommand( mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, pitch, 0, 0, 0, 0, 0, altitude)
cmds.add(cmd)
			   
# Add normal waypoint
lat = -10
lon = 10
altitude = 10
cmd = scommand( mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, lat, lon, altitude)
cmds.add(cmd)

# Add normal waypoint
lat = -20
lon = 20
altitude = 20
cmd = scommand( mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 0, 0, 0, lat, lon, altitude)
cmds.add(cmd)

# Add loiter waypoint
lat = -30
lon = 30
altitude = 30
cmd = scommand( mavutil.mavlink.MAV_CMD_NAV_LOITER_UNLIM, 0, 0, 0, 0, lat, lon, altitude)
cmds.add(cmd)

# Send commands
v.flush()

#Wait 2s. Should give us a chance to read the APM response that waypoints are updated.
time.sleep(2)

#Cache original commands in a list (can't just be copied for later comparison)
original_cmds=list()
for cmd in cmds:
    original_cmds.append(cmd)

	
# Print out original commands
print "CHECK1: Print out original commands"
for cmd in original_cmds:
    print "Command", cmd

	
# Get uploaded commands and print
print "CHECK2: Download commands from drone and print"
cmds.download()
cmds.wait_valid()

for cmd in cmds:
    print "Command", cmd
print "cmds count:", cmds.count
print "cmds next:", cmds.count




