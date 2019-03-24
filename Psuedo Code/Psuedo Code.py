# Error can be added to improve accuracy of turns.
# Points of Sail: 0 - Irons 1 - Close hauld 2 - Close reach 3 - Beam reach 4 - Broad Reach 5 - Run 6 - By the lee
def headUp(heading, onStarboard, error, turnRudder):
	if(turnRudder)
		rudderWindward(45)
	do:
		currentHeading = getCurrentHeading()
	while(currentHeading < heading + error && onStarboard) || (currentHeading > heading - error && !onStarboard)
	rudderStraight()

def bearOff(heading, onStarboard, error, turnRudder):
	if(turnRudder)
		rudderLeward(45)
	do
		currentHeading = getCurrentHeading()
	while(currentHeading > heading + error && onStarboard) || (currentHeading < heading - error && !onStarboard) 
	rudderStraight()

def tack(onStarboard)
	if(getCurrentSpeed() <= TACKING_SPEED)
		if(onStarboard)
		headUp(315, onStarboard, 0, true)
		else
		headUp(45, onStarboard, 0, true)
	else
		rudderWindward(45)
		do:
			headup(0, onStarboard, 0, false)
		while getCurrentRelativeHeading() < 45 || getCurrentRelativeHeading() > 315

def gybe()
	if()

def onStarbord()
	if (getCurrentRelativeHeading() < 180)
		return true
	else
		return false


def getCurrentRelativeHeading()
	return windvane_angle

def getCurrentHeading()
	return compass_angle

def getCurrentSpeed()
	return speed??

def feather()

def search

def pointOfSail()
	# Irons
	if (getCurrentRelativeHeading < 45 - error || getCurrentRelativeHeading > 315 + error)
		return 0
	# Close Hauld
	else if (inbetween(getCurrentRelativeHeading, 45 - error, 45 + error) 
		|| inbetween(getCurrentRelativeHeading, 315 - error, 315 + error))
		return 1
	# Close Reach
	else if (inbetween(getCurrentRelativeHeading, 45 + error, 90 + error) 
		|| inbetween(getCurrentRelativeHeading, 315 - error, 270 - error))
		return 2
	# Beam Reach
	else if (inbetween(getCurrentRelativeHeading, 90 + error, 90 + error) 
		|| inbetween(getCurrentRelativeHeading, 315 - error, 270 - error))
		return 3
	# Run
	else if (inbetween(getCurrentRelativeHeading, 90 + error, 90 + error) 
		|| inbetween(getCurrentRelativeHeading, 315 - error, 270 - error))
		return 4
	# By the Lee
	else if (inbetween(getCurrentRelativeHeading, 90 + error, 90 + error) 
		|| inbetween(getCurrentRelativeHeading, 315 - error, 270 - error))
		return 4

def inBetween(value, lower, upper)
	if (value > lower && value < upper)
		return true
	return false

