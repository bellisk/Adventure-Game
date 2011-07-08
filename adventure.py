class Room:
	def __init__(self, description, inhabitant, item):
		self.description = description
		self.inhabitant = inhabitant
		self.item = item
		self.connections = {}

entrance = Room("cold, bare entrance chamber", None, None)
grisly_chamber = Room("grisly chamber", "wizened old witch", "golden goblet")
long_cave = Room("long, echoing cave", "green-skinned child", "bag of peas")
small_alcove = Room("tiny rock alcove", "bearded dwarf", "iron mallet")
glass_chamber = Room("chamber with glassy walls", None, "sack of coal")
chimney_room = Room("very tall room like a chimney", "disembodied voice", None)

entrance.connections = {"north": grisly_chamber, "south": long_cave, "east": small_alcove}
grisly_chamber.connections = {"south": entrance, "north": glass_chamber, "east": chimney_room}
long_cave.connections = {"north": entrance}
small_alcove.connections = {"west": entrance, "north": chimney_room}
glass_chamber.connections = {"south": grisly_chamber}
chimney_room.connections = {"west": grisly_chamber, "south": small_alcove}

location = entrance

print "WELCOME TO THE HAUNTED CAVE".center(80)

name = raw_input("What is your name, bold adventurer?\n> ")
print "Welcome, " + name + "!"

pants_colour = raw_input("What colour are your pants?\n> ").lower()

if pants_colour in ["red", "green", "blue", "orange", "pink", "black", "white"]:
	print "You shall be known as " + name + " " + pants_colour.capitalize() + "-pants."
else:
	pants_colour = "no"
	print "That's not a real colour. You shall be known as " + name + " " + pants_colour.capitalize() + "-pants."

age = -1
while age == -1:
    try:
        age = int(raw_input("How old are you?\n> "))
    except:
        pass

answer = ""
while not answer in ["1", "2"]:
    answer = raw_input(
"""What do you want to take with you into the cave?
	1. A sword
	2. A flashlight
> """)

inventory = []

if answer == "1":
	inventory.append("sword")
	print "You have a sword in your inventory!\n(Press any key)"
else:
	inventory.append("flashlight")
	print "You have a flashlight in your inventory!\n(Press any key)"

chamber_tally = 0

while True:

	raw_input()
	answer_list = []
	
	question = "\nYou are in a " + location.description + "."
	if "flashlight" in inventory:
		if location.inhabitant != None:
			question = question + "\nThere is a " + location.inhabitant + " here."
		if location.item != None:
			question = question + "\nOn the floor you see a " + location.item + "."
	else:
		question = question + "\nIt's too dark to see anything in here."
	question = question + "\nWhat do you want to do?"

	if "flashlight" in inventory:
		if location.inhabitant != None:
			question = question + "\n    >Talk to the " + location.inhabitant + " (talk)"
			answer_list.append("talk")
		if location.item != None:
			question = question + "\n    >Pick up the " + location.item + " (pick up)"
			answer_list.append("pick up")
	else:
		question = question + "\n    >Wave your sword around (wave)\n    >Yell out hello (yell)"
		answer_list.extend(["wave", "yell"])
	if location == entrance:
		question = question + "\n    >Leave the Haunted Cave (leave)"
		answer_list.append("leave")
	question = question + "\n    >Drop something (drop)"
	answer_list.append("drop")
	for direction in location.connections.keys():
		question = question + "\n    >Go " + direction + " (" + direction + ")"
		answer_list.append(direction)

	answer = ""
	while not answer in answer_list:
	    answer = raw_input(question + "\n>")

	if answer == "talk":
		print "The " + location.inhabitant + " tells you a long and preposterous story."
		continue
	if answer == "pick up":
		print "You have a " + location.item + " in your inventory!"
		inventory.append(location.item)
		location.item = None
		continue
	if answer == "wave":
		print "You swing your sword wildly about."
		if location.inhabitant != None:
			print "There is a shout very close to you.\nYou find an injured " + location.inhabitant + " on the floor."
		else:
			print "After a while you feel quite silly and put it away again."
		continue
	if answer == "yell":
		print "You hear the echo of your own voice."
		if location.inhabitant != None:
			print "There are footsteps running away."
			location.inhabitant = None
		if location.item != None:
			print "On the floor you find a " + location.item + ". You pick it up."
			inventory.append(location.item)
			location.item = None
		continue
	if answer == "leave":
		print "You leave the cave and start the journey home.\n\nYour inventory is:"
		for n in inventory:
			print n
		print "\nWell done! You have made the clan of " + pants_colour.capitalize() + "-pants proud."
		break
	if answer == "drop":
		if inventory == []:
			print "You have nothing to drop!"
		else:
			drop_list = ["nothing"]
			drop_selection = "What do you want to drop?\n    >Nothing (nothing)"
			for item in inventory:
				drop_selection = drop_selection + "\n    >" + item + " (" + item + ")"
				drop_list.append(item)
			drop_answer = ""
			while not drop_answer in drop_list:
				drop_answer = raw_input(drop_selection + "\n>")
			if drop_answer == "nothing":
				continue
			else:
				print "You drop the " + drop_answer + " onto the floor."
				inventory.remove(drop_answer)
				location.item = drop_answer
				continue
	print "You go " + answer + " to the next chamber."
	location = location.connections[answer]
