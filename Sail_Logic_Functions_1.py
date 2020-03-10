#!/usr/bin/env python
# coding: utf-8

# In[ ]:


gps_speed = 5
compass_angle = 90
windvane_angle = 100
wind_speed = 10
error = 5
tacking_speed = 5
rudder_angle = 90
sails_angle = 90

# TODO: find how to use boolean values
true = 1
false = 0


class SailException(Exception):
    pass


# Points of Sail: 0 - Irons 1 - Close hauld 2 - Close reach 3 - Beam reach 4 - Broad Reach 5 - Run 6 - By the lee
def inBetween(value, lower, upper):
    if (value > lower and value < upper):
        return true
    return false


def getCurrentRelativeHeading():
    return windvane_angle


def getCurrentHeading():
    return compass_angle


def getCurrentSpeed():
    return gps_speed


# TODO
def sails(degree):
    return 1


def onStarboard():
    if getCurrentRelativeHeading() < 180:
        return true
    else:
        return false


def sailsOut():
    if onStarboard():
        sails(0)
    else:
        sails(180)


# TODO
def rudderWindward(degree):
    global rudder_angle
    d = degree
    if onStarboard():
        rudder_angle = 90 + d
    else:
        rudder_angle = 90 - d


# TODO
def rudderStraight():
    global rudder_angle
    rudder_angle = 90


# TODO
def rudderLeeward(degree):
    global rudder_angle
    d = degree
    if onStarboard():
        rudder_angle = 90 - d
    else:
        rudder_angle = 90 + d



def pointOfSail():
    # Irons
    if ((getCurrentRelativeHeading()) < 40 - error or (getCurrentRelativeHeading()) > 310 + error):
        return 0
    # Close Hauld
    elif (inBetween((getCurrentRelativeHeading()), 45 - error, 45 + error)
          or inBetween((getCurrentRelativeHeading()), 315 - error, 315 + error)):
        return 1

    # Close Reach
    elif (inBetween((getCurrentRelativeHeading()), 45, 68 + error)
          or inBetween((getCurrentRelativeHeading()), 293 - error, 315)):
        return 2
    # Beam Reach
    elif (inBetween((getCurrentRelativeHeading()), 68 - error, 113 + error)
          or inBetween((getCurrentRelativeHeading()), 248 - error, 293 + error)):
        return 3
    # Broad Reach
    elif (inBetween((getCurrentRelativeHeading()), 113 - error, 170 + error)
          or inBetween((getCurrentRelativeHeading()), 190 - error, 248 + error)):
        return 4
    # Run
    else:
        return 5


def headingCourse(heading):
    # Irons
    if heading < 40 - error or heading > 310 + error:
        return 0
    # Close Hauld
    elif inBetween(heading, 45 - error, 45 + error) or inBetween(heading, 315 - error, 315 + error):
        return 1
    # Close Reach
    elif inBetween(heading, 45, 68 + error) or inBetween(heading, 293 - error, 315):
        return 2
    # Beam Reach
    elif inBetween(heading, 68 - error, 113 + error) or inBetween(heading, 248 - error, 293 + error):
        return 3
    # Broad Reach
    elif inBetween(heading, 113 - error, 170 + error) or inBetween(heading, 190 - error, 248 + error):
        return 4
    # Run
    else:
        return 5

# TODO Add exception for when boat should bear off not head up
def headUp(heading, onStarboard, error, turnRudder):
    if turnRudder:
        rudderWindward(45)
    currentHeading = getCurrentHeading()
    while (currentHeading > heading + error and onStarboard) or (
            currentHeading < heading - error and onStarboard != True):
        # currentHeading = getCurrentHeading()
        # Pertend rudder is moving
        if onStarboard:
            currentHeading = currentHeading + 1
        else:
            currentHeading = currentHeading - 1
        global compass_angle
        compass_angle = currentHeading
        boatStatus()
    rudderStraight()


def bearOff(heading, onStarboard, error, turnRudder):
    if turnRudder:
        rudderLeeward(45)
        currentHeading = getCurrentHeading()
    while (currentHeading < heading + error and onStarboard) or (
            currentHeading > heading - error and onStarboard != True):
        currentHeading = getCurrentHeading()
    rudderStraight()


#I added a zero as the last arguement for all head up calls, not sure if thats useful.
def tack():
    if getCurrentSpeed() <= tacking_speed:
        if onStarboard():
            headUp(315, 0, true, 0)
        else:
            headUp(45, 0, true, 0)
    else:
        rudderWindward(45)
        while getCurrentRelativeHeading() < 45 or getCurrentRelativeHeading() > 315:
            headUp(0, 0, false, 0)


def switchTack(desiredHeading):
    if pointOfSail() == 1:
        if headingCourse(desiredHeading) == 5:
            gybe(desiredHeading)
        else:
            tack()
    elif pointOfSail() == 2:
        if headingCourse(desiredHeading) >= 3:
            gybe(desiredHeading)
        else:
            tack()
    else:
        gybe(desiredHeading)


def gybe(desiredHeading):
    start = getCurrentRelativeHeading()
    distanceTo = 180 - start

    while inBetween(getCurrentHeading(), desiredHeading - error, desiredHeading + error) != True:
        while abs(getCurrentHeading() - start) < abs(distanceTo):
            rudderLeeward(45)
            sails(90)
        if headingCourse(desiredHeading) == 5:
            rudderStraight()
            sailsOut()
        else:
            headUp(desiredHeading, onStarboard(), error, false)



# TODO
def feather():
    return 1


# TODO
def search():
    return 1


def boatStatus():
    print("The boat is currently going {0} knots at {1} degrees. The wind is coming from {2} degrees relative to the "
          "boat at {3} knots. The Rudder is at {4} degrees and the sails are \nat {5} "
          "degrees".format(gps_speed, compass_angle, windvane_angle, wind_speed, rudder_angle, sails_angle))


# -------------------------------------------------------------------------------
# main:


boatStatus()
headUp(115, onStarboard(), error, 5)
boatStatus()

