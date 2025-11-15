

# Setting to be ingested via config file (TODO)
bOverwriteTranslations = True
bClearTransTableOnSetPhrase = False 
maxLineLength = 40
specialChars = ".,!@#$%^&*()_+-='"


# Working global variables
encPhrase = ""
decPhrase = ""
transTable = {}
cmd="?"


def applyTranslation(): 
	# rewrite the decPhrase based on contents of encPhrase 
	#   translated according to values in transTable 

	global decPhrase 

	decPhrase = ""
	for ac in encPhrase: 
		decPhrase += transTable.get(ac, " ")

def clearTransTable():

	global transTable

	transTable = {}
	for ac in specialChars:
		transTable[ac] = ac


def showHelp(helpSection):

	match helpSection:
		case "SHOW_COMMANDS":
			print("Commands are quit, ?, A=b, ^ABC=def, $phrase (sets phrase), show, show trans")

		case "SHOW_ASSIGN_INSTRUCTIONS":
			print("Assignments take the form A=b or ^ABC=def")

		case _:
			print(f"Help section '{helpSection}' not found.")


def doAssign(lPart, rPart):

	global transTable

	if ((lPart[0] == "^") and (len(lPart) > 1)):
		# Do multi assignment 
		# Cut the caret(^) indicator off before starting
		lPart = lPart[1:]
		for idx in range(len(lPart)):
			transTable[lPart[idx]] = rPart[idx]
	else:
		# Do single assignment 
		transTable[lPart[0]] = rPart[0]
		
	for aKey in transTable:
		if (not (aKey in specialChars)):
			print(f"{aKey} = {transTable[aKey]}")

	applyTranslation() 


def setPhrase(phrase):

	global encPhrase 
	global decPhrase 

	print(f"Setting phrase length = {len(phrase)}")
	encPhrase = phrase 
	decPhrase = " " * len(encPhrase)

	if (bClearTransTableOnSetPhrase): 
		clearTransTable()

	applyTranslation() 


def showPhrase():
	# display the decrypted text above the encrypted form. 
	# break lines at whitespace closest to the value maxLineLength

	breakLineLimit = len(encPhrase)
	if breakLineLimit > maxLineLength:
		breakLineLimit = getLineLimit(encPhrase)

	# TODO: Break line limit needs to be recomputed for each segment
	#         to avoid breaking second+ segments mid-word.

	# Create outputArray of decPhrase segments stacked on top of encPhrase 
	#   and broken at breakLineLimit
	outputArray = []
	startIdx = 0
	endIdx = breakLineLimit
	bDoneBuilding = False 
	while (not bDoneBuilding): 
		currDecSegment = decPhrase[startIdx:endIdx] 
		currEncSegment = encPhrase[startIdx:endIdx]
		outputArray.append(currDecSegment)
		outputArray.append(currEncSegment)
		startIdx = endIdx
		if (endIdx > len(encPhrase)+1):
			bDoneBuilding = True 
		else: 
			endIdx += breakLineLimit

	for aLine in outputArray: 
		print(f"[{aLine}]")

def showTransTable(): 
	
	for at in transTable: 
		if specialChars.find(at) == -1:
			print(f"{at} = {transTable[at]}")


def doQuit():
	print("Received Quit Command")
	exit()


def getLineLimit(encPhrase):
	# return index of last space before maxLineLength
	limit = len(encPhrase) 

	idx = encPhrase.rfind(' ', 0, maxLineLength)
	if (idx != -1):
		limit = idx

	return limit

def parseAssignCmd(cmd): 

	rval = ['','']
	bValidAssignment = True 

	cmdParts = cmd.split('=')
	if (len(cmdParts) == 2):
		lPart = cmdParts[0]
		rPart = cmdParts[1]

		if (len(lPart) > 0 and len(rPart) > 0):
			rval = [lPart, rPart]
		else: 
			bValidAssignment = False
	else:
		bValidAssignment = False

	if (not bValidAssignment):
		showHelp("SHOW_ASSIGN_INSTRUCTIONS")
	
	return rval

def processCmd(cmd): 

	bValidAssignment = True 

	if len(cmd) == 0:
		return

	if "=" in cmd:
		cmdParts = parseAssignCmd(cmd)
		cmd = "DO_ASSIGN"

		# if the command parts are invalid quit processing
		if ((len(cmdParts[0]) == 0) or (len(cmdParts) < 2)):
			return 
		
	rawPhrase = ""
	if cmd[0] == '$': 
		if (len(cmd) > 1):
			rawPhrase = cmd[1:]
			cmd = "DO_SET_PHRASE"
		
	if (cmd.upper() == "SHOW"):
		cmd = "DO_SHOW"

	if (cmd.upper() == "SHOW TRANS"):
		cmd = "DO_SHOW_TRANS"

	match cmd:
		case "?":
			showHelp("SHOW_COMMANDS")

		case "quit":
			doQuit()

		case "DO_SET_PHRASE": 
			setPhrase(rawPhrase)
			showPhrase()

		case "DO_ASSIGN":
			doAssign(cmdParts[0], cmdParts[1])
			showPhrase()

		case "DO_SHOW": 
			showPhrase()

		case "DO_SHOW_TRANS":
			showTransTable()

		case _:
			showHelp("SHOW_COMMANDS")


# ========== entry point 
if __name__ == "__main__":
	clearTransTable()
	while(cmd != "quit"):
		cmd = input("Command:")
		processCmd(cmd)

