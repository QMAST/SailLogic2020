import logging
import time


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

def hold_course(self, destination, epsilon):
    """
    PLEASE MOVE TO THE APPROPIATE spot IN startAutomaticControl RELATIVE TO
    OTHER FUNCTIONS.
    
    given a destination in the form of a tuple with lat and long coordinates
    margin of acceptable error for the berring, the adjusts the rudder to hold
    course as per the "holding course until at location" function on the
    sailflow.png logic loop on the basecamp.  This function does not return
    anything.
    
    Assumes only small adjustments to rudder are needed.
    Function does not check wind direction or adjust sail.
    
    Assumes compass angle is mapped from North to 0 degrees,
    east to 90 degrees, etc.  Confirm or edit as appropriate.
    """
    desired_heading = state.Determine_Heading(destination)
        
    if abs(state.compass_angle - desired_heading) > epsilon:
        controller.actuate_rudder(90 - (state.compass_angle - desired_heading) / 2) #Assumes back of rudder points port at 0 degrees

        logging.info("Changing rudder direction to hold course")
    else:
        controller.actuate_rudder(90)
        logging.info("Continuing straight to hold course")