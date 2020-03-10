import logging
from Sail_Logic_Functions_1 import getCurrentRelativeHeading
from Sail_Logic_Functions_1 import getCurrentHeading
from Sail_Logic_Functions_1 import pointOfSail
from Sail_Logic_Functions_1 import tack
from Sail_Logic_Functions_1 import bearOff
from Sail_Logic_Functions_1 import rudderStraight
from Sail_Logic_Functions_1 import onStarboard
from Sail_Logic_Functions_1 import sailsOut
from Sail_Logic_Functions_1 import headingCourse
from Sail_Logic_Functions_1 import headUp
from Sail_Logic_Functions_1 import sails
from Sail_Logic_Functions_1 import rudderLeeward
from Sail_Logic_Functions_1 import rudderStraight
from Sail_Logic_Functions_1 import rudderWindward
from Sail_Logic_Functions_1 import switchTack


from enum import Enum
import time

class POS(Enum):
    irons = 0
    closeHauld = 1
    closeReach = 2
    beamReach = 3
    broadReach = 4
    run = 5
    lee = 6

#The big idea here is that we can use these statics to 
#loop the gyb() method while tracking if we have crossed 
#wind or not and check if the gyb command has changed.
class GybControl:
    #desired is used to track if the gyb heading has been updated.
    desired = -1
    #start is used to determine the starting heading of this gyb command.
    #Used in gyb() to determine if we have crossed wind or not.
    start = -1
gybStatics = GybControl()
#Constants for lay line.
#Frequency you want to tune waitForLayLine() with.
LAYDELAY = 2
#How close you want to get to the way point before quitting.
LAYPRECISION = 5

class Controller:
    """
    Class used for direct control of the sailboat.

    Args:
        writer (ThreadsafeSerialWriter): The writer to send the messages too
    """
    #Added defualt value for testing
    def __init__(self, writer = None):
        self.writer = writer
    def actuate_winch(self, value):
        assert 0 <= value <= 100
        logging.info("Actuating winch: {}".format(value))
        self.writer.write(b'00', str(value).encode('utf-8'))

    def actuate_rudder(self, value):
        assert 0 <= value <= 180
        logging.info("Actuating rudder: {}".format(value))
        self.writer.write(b'SR', str(value).encode('utf-8'))
    def simple_write(self, subject, value):
        # Literally just pass messages transparently to the Mega over XBee
        self.writer.write(subject, str(value).encode('utf-8'))
    #Desired Heading tells us the direction we want to be going in.
    def gybe(self, desiredHeading):

        #If this is the first gyb command, or an updated gyb heading,
        #then update the gyb statics so we can check crossed wind.
        if (gybStatics.desired == -1 or desiredHeading != gybStatics.desired):
            gybStatics.desired = desiredHeading
            gybStatics.start = getCurrentRelativeHeading()

        #This tells us the direction we're heading in. Compass coordinates. (?)
        currentHeading = getCurrentHeading()
        #This is and enum (?) that gives our current POS.
        currentPOS = pointOfSail()

        if (currentPOS != POS.run and currentPOS == POS.closeHauld):
            #Tack and bear off.
            tack()
            #paramaters to rudder straight might need tuning.
            bearOff(desiredHeading, onStarboard(), 0, \
                (currentHeading < 195 and currentHeading > 180))
        else:
            #Check if we have crossed wind.
                #I think that crossing wind means we moved from pointing left of the direction 
                #of wind to the right of the direction of the wind or vice versa. That could
                #be completely wrong, I have no idea.
            if ((getCurrentRelativeHeading() > 180) and (gybStatics.start < 180)) or \
            ((getCurrentRelativeHeading() < 180) and (gybStatics.start > 180)):
                if (headingCourse(desiredHeading) == POS.run):
                    #let out sail, straighten out
                    rudderStraight()
                    sailsOut()

                else:
                    #hold rudder, head up
                    headUp(desiredHeading, onStarboard(), 0, 0)

            else:
                #pull in, tilt 45.
                #Theres a sails out function but not sails in, so i just jammed this together.
                if onStarboard():
                    sails(180)
                else:
                    sails(0)
                rudderLeeward(45)

    def waitForLayLine(self):
        #Get heading at start of path, this is our lay line we 
        #want to follow.
        #headingPOS = pointOfSail(getCurrentHeading())
        headingPOS = pointOfSail()
        heading = getCurrentHeading()
        #STILL NEED TO GET REAL VALUES, THESE ARE JSUT SO IT COMPILES.
        #
        wayPointPosition = 10
        getCurrentPosition = 0

        #Until we reach the waypoint, keep correcting course to 
        #stay on lay line.
        #We need a way to know if we're there or not. How do I get GPS?
        while((getCurrentPosition - wayPointPosition) > LAYPRECISION):
            #Check if we need a correction.
            if(pointOfSail() != headingPOS):
                    switchTack(heading)
            else:
                #Just keep cruisin, do I even need this?
                sailsOut()
                rudderStraight()
            #Wait to refresh.
            time.sleep(LAYDELAY)

def startAutomaticControl(state):
    """
    Code for controlling the boat based on the state object. The state object
    contains up to date information of all the sensor readings.

    It's highly important to know that this function does NOT try to modify the
    state object, as there aren't any threadsafe guarantees. It should only
    read from the state, never modifying its attributes.
    """

    logging.info("Starting automatic control thread.")
    controller = Controller(state.writer)
    controller.simple_write("00", "1") # Preemptively announce to Mega that you're online

    extreme = True

    while True:
        if state.rpi_autopilot_enabled:
            if extreme == True:
                controller.actuate_rudder(0)
                extreme = False
            else:
                controller.actuate_rudder(180)
                extreme = True

            # Do something. E.g.
            #
            # controller.actuate_winch(22)
            pass
        else:
            # Put into autopilot
            #logging.info("Not in Autopilot.")
            #controller.simple_write(b'A0', "1")
            pass

        time.sleep(2)
