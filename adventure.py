import random

class Room:
	def __init__(self, description, inhabitants, inventory):
		self.description = description
		self.inhabitants = inhabitants
		self.inventory = inventory
		self.connections = {}

class Character:
	def __init__(self, description, location, inventory, friendly):
		self.description = description
		self.location = None
		self.move(location)
		self.inventory = inventory
		self.friendly = friendly
	def move(self, new_location):
		if self.location != None:
			self.location.inhabitants.remove(self)
		self.location = new_location
		if self.location != None:
			self.location.inhabitants.append(self)
	def talk(self):
		if self.friendly == True:
			print "The " + self.description + " wishes you a nice day."
		else:
			print "The " + self.description + " threatens your bodily integrity."

class Item:
	def __init__(self, description, owner):
		self.description = description
		self.owner = None
		self.move(owner)
	def move(self, new_owner):
		if self.owner != None:
			self.owner.inventory.remove(self)
		self.owner = new_owner
		if self.owner != None:
			self.owner.inventory.append(self)

#Rooms
entrance = Room("cold, bare entrance chamber", [], [])
grisly_chamber = Room("grisly chamber", [], [])
long_cave = Room("long, echoing cave", [], [])
small_alcove = Room("tiny rock alcove", [], [])
glass_chamber = Room("chamber with glassy walls", [], [])
chimney_room = Room("very tall room like a chimney", [], [])

entrance.connections = {"north": grisly_chamber, "south": long_cave, "east": small_alcove}
grisly_chamber.connections = {"south": entrance, "north": glass_chamber, "east": chimney_room}
long_cave.connections = {"north": entrance}
small_alcove.connections = {"west": entrance, "north": chimney_room}
glass_chamber.connections = {"south": grisly_chamber}
chimney_room.connections = {"west": grisly_chamber, "south": small_alcove}

#Characters
wizened_witch = Character("wizened old witch", grisly_chamber, [], True)
green_child = Character("green-skinned child", long_cave, [], False)
bearded_dwarf = Character("bearded dwarf", small_alcove, [], True)
disembodied_voice = Character("disembodied voice", chimney_room, [], False)

#Items
peas = Item("bag of peas", None)
goblet = Item("golden goblet", None)
mallet = Item("mallet of iron", None)
chips = Item("bag of tortilla chips", None)
necklace = Item("glass bead necklace", None)
tortoise = Item("small green tortoise", None)
sword = Item("sword", None)
flashlight = Item("flashlight", None)

room_list = [entrance, grisly_chamber, long_cave, small_alcove, glass_chamber, chimney_room]
character_list = [wizened_witch, green_child, bearded_dwarf, disembodied_voice, None, None]
item_list = [peas, goblet, mallet, chips, necklace, tortoise]

#Shuffle the lists
random.shuffle(room_list)
random.shuffle(character_list)
random.shuffle(item_list)

#Make room-character-item tuples and move characters and items into the rooms
for x in zip(room_list, character_list, item_list):
	if x[1] != None:
		x[1].move(x[0])
	if x[2] != None:
		x[2].move(x[0])

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
	inventory.append(sword)
	print "You have a sword in your inventory!"
else:
	inventory.append(flashlight)
	print "You have a flashlight in your inventory!"

while True:

	raw_input("(Press Enter key)")

	question = "\nYou are in a " + location.description + "."
	if flashlight in inventory:
		if len(location.inhabitants) != 0:
			for character in location.inhabitants:
				question = question + "\nThere is a " + character.description + " here."
		if len(location.inventory) != 0:
			for item in (location.inventory):
				question = question + "\nOn the floor you see a " + item.description + "."
	else:
		question = question + "\nIt's too dark to see anything in here."
	question = question + "\nWhat do you want to do?"

	answer_dict = {}
	qcount = 1

	if flashlight in inventory:
		if len(location.inhabitants) != 0:
			for character in location.inhabitants:
				question = question + "\n    >Talk to the " + character.description + " (" + str(qcount) + ")"
				answer_dict[qcount] = ("talk", character)
				qcount += 1
		if len(location.inhabitants) != 0:
			for character in location.inhabitants:
				question = question + "\n    >Pick up the " + character.description + " (" + str(qcount) + ")"
				answer_dict[qcount] = ("pick up", character)
				qcount += 1
		if len(location.inventory) != 0:
			for item in location.inventory:
				question = question + "\n    >Pick up the " + item.description + " (" + str(qcount) + ")"
				answer_dict[qcount] = ("pick up", item)
				qcount += 1
	else:
		question = question + "\n    >Wave your sword around (" + str(qcount) + ")\n    >Yell out hello (" + str(qcount + 1) + ")"
		answer_dict[qcount] = ("wave", None)
		answer_dict[qcount + 1] = ("yell", None)
		qcount += 2
	if location == entrance:
		question = question + "\n    >Leave the Haunted Cave (" + str(qcount) + ")"
		answer_dict[qcount] = ("leave", None)
		qcount += 1
	question = question + "\n    >Drop something (" + str(qcount) + ")"
	answer_dict[qcount] = ("drop", None)
	qcount += 1
	for direction in location.connections.keys():
		question = question + "\n    >Go " + direction + " (" + str(qcount) + ")"
		answer_dict[qcount] = ("go", direction)
		qcount += 1

	answer = ""
	while not answer in answer_dict.keys():
		try:
			answer = int(raw_input(question + "\n>"))
		except:
			print "Please enter a number."

	if answer_dict[answer][0] == "talk":
		#print "The " + answer_dict[answer][1].description + " tells you a long and preposterous story."
		answer_dict[answer][1].talk()
		continue
	if answer_dict[answer][0] == "pick up":
		if isinstance(answer_dict[answer][1], Character):
			if answer_dict[answer][1].friendly == True:
				print "The " + answer_dict[answer][1].description + " chides you for your rudeness."
			else:
				print "The " + answer_dict[answer][1].description + " beats you soundly about the head."
		else:
			print "You have a " + answer_dict[answer][1].description + " in your inventory!"
			inventory.append(answer_dict[answer][1])
			answer_dict[answer][1].move(None)
		continue
	if answer_dict[answer][0] == "wave":
		print "You swing your sword wildly about."
		if len(location.inhabitants) != 0:
			for character in location.inhabitants:
				print "There is a shout very close to you.\nYou find an injured " + character.description + " on the floor."
		else:
			print "After a while you feel quite silly and put it away again."
		continue
	if answer_dict[answer][0] == "yell":
		print "You hear the echo of your own voice."
		if len(location.inhabitants) != 0:
			print "There are footsteps running away."
			for character in location.inhabitants:
				direction = random.choice(location.connections.keys())
				character.move(location.connections[direction])
		if len(location.inventory) != 0:
			for item in location.inventory:
				print "On the floor you find a " + item.description + ". You pick it up."
				inventory.append(item)
				item.move(None)
		continue
	if answer_dict[answer][0] == "leave":
		print "You leave the cave and start the journey home.\n\nYour inventory is:\n"
		for n in inventory:
			print ">" + n.description
		print "\nWell done! You have made the clan of " + pants_colour.capitalize() + "-pants proud.\n"
		break
	if answer_dict[answer][0] == "drop":
		if inventory == []:
			print "You have nothing to drop!"
		else:
			dcount = 1
			drop_dict = {}
			drop_selection = "What do you want to drop?\n    >Nothing (" + str(dcount) + ")"
			drop_dict[dcount] = "nothing"
			dcount += 1
			for item in inventory:
				drop_selection = drop_selection + "\n    >" + item.description + " (" + str(dcount) + ")"
				drop_dict[dcount] = item
				dcount += 1
			drop_answer = ""
			while not drop_answer in drop_dict.keys():
				try:
					drop_answer = int(raw_input(drop_selection + "\n>"))
				except:
					print "Please enter a number."
			if drop_dict[drop_answer] == "nothing":
				continue
			else:
				print "You drop the " + drop_dict[drop_answer].description + " onto the floor."
				inventory.remove(drop_dict[drop_answer])
				drop_dict[drop_answer].move(location)
				continue

	print "You go " + answer_dict[answer][1] + " to the next chamber."
	location = location.connections[answer_dict[answer][1]]
