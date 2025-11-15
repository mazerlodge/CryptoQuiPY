
specialChars = ".,!@#$%^&*()_+-="
encPhrase = "JIBBERISH"
decPhrase = ""
cmd="?"

transTable = {}
for ac in specialChars:
	transTable[ac] = ac

def showHelp(helpSection):

	match helpSection:
		case "SHOW_COMMANDS":
			print("Commands are quit, ?, A=b, ^ABC=def, showphrase, showdistro")

		case "SHOW_ASSIGN_INSTRUCTIONS":
			print("Assignments take the form A=b or ^ABC=def")

		case _:
			print(f"Help section '{helpSection}' not found.")

def DoAssign(lPart, rPart):

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


def DoQuit():
	print("Received Quit Command")
	exit()

def processCmd(cmd): 

	bValidAssignment = True 

	if "=" in cmd:
		cmdParts = cmd.split('=')
		if (len(cmdParts) == 2):
			lPart = cmdParts[0]
			rPart = cmdParts[1]

			if (len(lPart) > 0 and len(rPart) > 0):
				cmd = "DO_ASSIGN"
			else: 
				bValidAssignment = False
		else:
			bValidAssignment = False

		if (not bValidAssignment):
			showHelp("SHOW_ASSIGN_INSTRUCTIONS")
			return

	match cmd:
		case "?":
			showHelp("SHOW_COMMANDS")

		case "quit":
			DoQuit()

		case "DO_ASSIGN":
			DoAssign(lPart, rPart)

		case _:
			showHelp("SHOW_COMMANDS")


# ========== entry point 

while(cmd != "quit"):
	cmd = input("Command:")
	processCmd(cmd)

