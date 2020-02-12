import logging
import time

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
    def __init__(self, writer):
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


def waitForLayLine():
    #Get heading at start of path, this is our lay line we 
    #want to follow.
    headingPOS = pointOfSail(getCurrentHeading())
    heading = getCurrentHeading()

    #Until we reach the waypoint, keep correcting course to 
    #stay on lay line.
    #We need a way to know if we're there or not. How do I get GPS?
    while((getCurrentPosition - wayPointPosition) > LAYPRECISION):
        #Check if we need a correction.
        if(pointOfSail(getCurrentHeading()) != headingPOS):
                switchTack(heading)
        else
            #Just keep cruisin, do I even need this?
            sailsOut()
            rudderStraight()
        #Wait to refresh.
        time.sleep(LAYDELAY)
                      