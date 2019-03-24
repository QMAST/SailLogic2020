# Error can be added to improve accuracy of turns.
# Points of Sail: 0 - Irons 1 - Close hauld 2 - Close reach 3 - Beam reach 4 - Broad Reach 5 - Run 6 - By the lee
def headUp(heading, error, turnRudder):
	if(turnRudder)
		rudderWindward(45)
	do:
		currentHeading = getCurrentHeading()
	while(currentHeading < heading + error && onStarboard()) || (currentHeading > heading - error && !onStarboard())
	rudderStraight()

def bearOff(heading, error, turnRudder):
	if(turnRudder)
		rudderLeward(45)
	do
		currentHeading = getCurrentHeading()
	while(currentHeading > heading + error && onStarboard()) || (currentHeading < heading - error && !onStarboard()) 
	rudderStraight()

def tack()
	if(getCurrentSpeed() <= TACKING_SPEED)
		if(onStarboard)
		headUp(315, 0, true)
		else
		headUp(45, 0, true)
	else
		rudderWindward(45)
		do:
			headup(0, 0, false)
		while (getCurrentRelativeHeading() < 45) || (getCurrentRelativeHeading())() > 315

def switchTack(desiredHeading)
	if(pointOfSail() == 1)
		if(headingCourse(desiredHeading) == 5)
			gybe(desiredHeading)
		else
			tack()
	else if(pointOfSail() == 2)
		if(headingCourse(desiredHeading) >= 3)
			gybe(desiredHeading)
		else
			tack()
	else if(pointOfSail() >= 3)
		gybe(desiredHeading)

def gybe(desiredHeading)
	start = getCurrentRelativeHeading()
	distanceTo = 180 = start

	while(!(inbetween(getCurrentHeading(), desiredHeading - error, desiredHeading + error)))
		while(abs(getCurrentHeading() - start()) < abs(distanceTo))
			rudderLeward(45)
			sails(90)
		if(headingCourse(desiredHeading) == 5)
			rudderStraight()
			sailsOut()
		else
			headUp(desiredHeading, error, false)


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
	return gps.speed

def feather()

def search

def headingCourse(heading)
# Irons
	if ((heading < 40 - error) || (heading > 310 + error))
		return 0
	# Close Hauld
	else if (inbetween((heading, 45 - error, 45 + error)) 
		|| inbetween((heading, 315 - error, 315 + error)))
		return 1
	# Close Reach
	else if (inbetween((heading, 45, 68 + error)) 
		|| inbetween((heading, 293 - error, 315)))
		return 2
	# Beam Reach
	else if (inbetween((heading, 68 - error, 113 + error)) 
		|| inbetween((heading, 248 - error, 293 + error)))
		return 3
	# Broad Reach
	else if (inbetween((heading, 113 - error, 170 + error)) 
		|| inbetween((heading, 190 - error, 248 + error)))
		return 4
	# Run
	else if (inbetween((heading, 170 - error, 190 + error)))
		return 4

def rudderWindward(degree)
	if(onStarboard())
		# Turn the rudder to (90 + degree)
	else
		# Turn the rudder to (90 - degree)

def rudderLeeward(degree)
	if(onStarboard())
		# Turn the rudder to (90 - degree)
	else
		# Turn the rudder to (90 + degree)



def pointOfSail()
	# Irons
	if ((getCurrentRelativeHeading()) < 40 - error || (getCurrentRelativeHeading()) > 310 + error)
		return 0
	# Close Hauld
	else if (inbetween((getCurrentRelativeHeading()), 45 - error, 45 + error) 
		|| inbetween((getCurrentRelativeHeading()), 315 - error, 315 + error))
		return 1
	# Close Reach
	else if (inbetween((getCurrentRelativeHeading()), 45, 68 + error) 
		|| inbetween((getCurrentRelativeHeading()), 293 - error, 315))
		return 2
	# Beam Reach
	else if (inbetween((getCurrentRelativeHeading()), 68 - error, 113 + error) 
		|| inbetween((getCurrentRelativeHeading()), 248 - error, 293 + error))
		return 3
	# Broad Reach
	else if (inbetween((getCurrentRelativeHeading()), 113 - error, 170 + error) 
		|| inbetween((getCurrentRelativeHeading()), 190 - error, 248 + error))
		return 4
	# Run
	else if (inbetween((getCurrentRelativeHeading()), 170 - error, 190 + error))
		return 4

def inBetween(value, lower, upper)
	if (value > lower && value < upper)
		return true
	return false

