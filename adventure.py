import random

class Room:
	def __init__(self, description, inhabitants, inventory):
		self.description = description
		self.inhabitants = inhabitants
		self.inventory = inventory
		self.connections = {}

class Character:
	def __init__(self, description, location, inventory):
		self.description = description
		self.location = None
		self.move(location)
		self.inventory = inventory
	def move(self, new_location):
		if self.location != None:
			self.location.inventory.remove(self)
		self.location = new_location
		if self.location != None:
			self.location.inventory.append(self)

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
wizened_witch = Character("wizened old witch", grisly_chamber, [])
green_child = Character("green-skinned child", long_cave, [])
bearded_dwarf = Character("bearded dwarf", small_alcove, [])
disembodied_voice = Character("disembodied voice", chimney_room, [])

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
	print "You have a sword in your inventory!\n(Press Enter key)"
else:
	inventory.append(flashlight)
	print "You have a flashlight in your inventory!\n(Press Enter key)"

chamber_tally = 0

while True:

	raw_input()
	answer_list = []
	answer_dict = {}
	
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

	qcount = 1

	if flashlight in inventory:
		if len(location.inhabitants) != 0:
			for character in location.inhabitants:
				question = question + "\n    >Talk to the " + character.description + " (" + str(qcount) + ")"
				answer_list.append(str(qcount))
				answer_dict[qcount] = ("talk", character)
				qcount += 1
		if len(location.inventory) != 0:
			for item in location.inventory:
				question = question + "\n    >Pick up the " + item.description + " (" + str(qcount) + ")"
				answer_list.append(str(qcount))
				answer_dict[qcount] = ("pick up", item)
				qcount += 1
	else:
		question = question + "\n    >Wave your sword around (" + str(qcount) + ")\n    >Yell out hello (" + str(qcount + 1) + ")"
		answer_list.extend([str(qcount), str(qcount + 1)])
		answer_dict[qcount] = ("wave", None)
		answer_dict[qcount + 1] = ("yell", None)
		qcount += 2
	if location == entrance:
		question = question + "\n    >Leave the Haunted Cave (" + str(qcount) + ")"
		answer_list.append(str(qcount))
		answer_dict[qcount] = ("leave", None)
		qcount += 1
	question = question + "\n    >Drop something (" + str(qcount) + ")"
	answer_list.append(str(qcount))
	answer_dict[qcount] = ("drop", None)
	qcount += 1
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
