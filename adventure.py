import random

class Room:
	def __init__(self, description, inhabitants, inventory):
		self.description = description
		self.inhabitants = inhabitants
		self.inventory = inventory
		self.connections = {}

class Character:
	def __init__(self, description, location, inventory, friendly, embodied):
		self.description = description
		self.location = None
		self.move(location)
		self.inventory = inventory
		self.friendly = friendly
		self.embodied = embodied
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
wizened_witch = Character("wizened old witch", grisly_chamber, [], True, True)
green_child = Character("green-skinned child", long_cave, [], False, True)
bearded_dwarf = Character("bearded dwarf", small_alcove, [], True, True)
disembodied_voice = Character("disembodied voice", chimney_room, [], False, False)
player = Character("you", entrance, [], True, True)

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
item_list = [peas, goblet, mallet, chips, necklace, tortoise, sword, flashlight]

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


print "WELCOME TO THE HAUNTED CAVE".center(80)

name = raw_input("What is your name, bold adventurer?\n> ")
print "Welcome, " + name + "!"

pants_colour = raw_input("What colour are your pants?\n> ").lower()

if pants_colour in ["red", "green", "blue", "orange", "pink", "black", "white"]:
	print "You shall be known as " + name + " " + pants_colour.capitalize() + "-pants."
else:
	pants_colour = "no"
	print "That's not a real colour. You shall be known as " + name + " " + pants_colour.capitalize() + "-pants."

friendly = ""
while not friendly.lower() in ["yes", "no"]:
    try:
        friendly = raw_input("Are you an amiable type?\n> ")
    except:
	print "Answer yes or no."
        pass

if friendly.lower() == "no":
	player.friendly = False

answer = ""
while not answer in ["1", "2"]:
    answer = raw_input(
"""What do you want to take with you into the cave?
	1. A sword
	2. A flashlight
> """)

inventory = []

if answer == "1":
	sword.move(player)
	print "You have a sword in your inventory!"
else:
	flashlight.move(player)
	print "You have a flashlight in your inventory!"

while True:

	raw_input("(Press Enter key)")

	question = "\nYou are in a " + player.location.description + "."
	if flashlight in player.inventory:
		if len(player.location.inhabitants) != 0:
			for character in player.location.inhabitants:
				if character != player:
					question = question + "\nThere is a " + character.description + " here."
		if len(player.location.inventory) != 0:
			for item in (player.location.inventory):
				question = question + "\nOn the floor you see a " + item.description + "."
	else:
		question = question + "\nIt's too dark to see anything in here."
	question = question + "\nWhat do you want to do?"

	answer_dict = {}
	qcount = 1

	if flashlight in player.inventory:
		if len(player.location.inhabitants) != 0:
			for character in player.location.inhabitants:
				if character != player:
					question = question + "\n    >Talk to the " + character.description + " (" + str(qcount) + ")"
					answer_dict[qcount] = ("talk", character)
					qcount += 1
		if len(player.location.inhabitants) != 0:
			for character in player.location.inhabitants:
				if character != player:
					question = question + "\n    >Pick up the " + character.description + " (" + str(qcount) + ")"
					answer_dict[qcount] = ("pick up", character)
					qcount += 1
		if len(player.location.inventory) != 0:
			for item in player.location.inventory:
				question = question + "\n    >Pick up the " + item.description + " (" + str(qcount) + ")"
				answer_dict[qcount] = ("pick up", item)
				qcount += 1
	else:
		question = question + "\n    >Yell out hello (" + str(qcount) + ")"
		answer_dict[qcount] = ("yell", None)
		qcount += 1
		question = question + "\n    >Feel your way around the room (" + str(qcount) + ")"
		answer_dict[qcount] = ("feel", None)
		qcount += 1
	if sword in player.inventory:
		question = question + "\n    >Wave your sword around (" + str(qcount) + ")"
		answer_dict[qcount] = ("wave", None)
		qcount += 1
	if player.location == entrance:
		question = question + "\n    >Leave the Haunted Cave (" + str(qcount) + ")"
		answer_dict[qcount] = ("leave", None)
		qcount += 1
	question = question + "\n    >Drop something (" + str(qcount) + ")"
	answer_dict[qcount] = ("drop", None)
	qcount += 1
	for direction in player.location.connections.keys():
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
		answer_dict[answer][1].talk()
		continue
	if answer_dict[answer][0] == "pick up":
		if isinstance(answer_dict[answer][1], Character):
			if player.friendly == True:
				if answer_dict[answer][1].friendly == True:
					print "You pick up the " + answer_dict[answer][1].description + "."
					answer_dict[answer][1].move(None)
					player.inventory.append(answer_dict[answer][1])
				else:
					if len(player.inventory) != 0:
						thing = random.choice(player.inventory)
						thing.move(answer_dict[answer][1])
						print "When you try to pick up the " + answer_dict[answer][1].description + ", they steal your " + thing.description + "."
					else:
						print "The " + answer_dict[answer][1].description + " beats you soundly about the head."
			else:
				if answer_dict[answer][1].friendly == True:
					print "The " + answer_dict[answer][1].description + " chides you for your rudeness."
				else:
					print "The " + answer_dict[answer][1].description + " beats you soundly about the head."
		else:
			print "You have a " + answer_dict[answer][1].description + " in your inventory!"
			answer_dict[answer][1].move(player)
		continue
	if answer_dict[answer][0] == "wave":
		print "You swing your sword wildly about."
		if len(player.location.inhabitants) != 0:
			for character in player.location.inhabitants:
				if character != player and character.embodied == True:
					print "There is a shout very close to you.\nYou find an injured " + character.description + " on the floor."
		else:
			print "After a while you feel quite silly and put it away again."
		continue
	if answer_dict[answer][0] == "yell":
		print "You hear the echo of your own voice."
		if len(player.location.inhabitants) > 1:
			print "There are footsteps running away."
			for character in player.location.inhabitants:
				if character != player:
					direction = random.choice(player.location.connections.keys())
					character.move(player.location.connections[direction])
		continue
	if answer_dict[answer][0] == "feel":
		if len(player.location.inventory) != 0:
			for item in player.location.inventory:
				print "On the floor you find a " + item.description + ". You pick it up."
				item.move(player)
		else:
			print "You find nothing of interest in the room."
		continue
	if answer_dict[answer][0] == "leave":
		print "You leave the cave and start the journey home.\n\nYour inventory is:\n"
		for n in player.inventory:
			print ">" + n.description
		print "\nWell done! You have made the clan of " + pants_colour.capitalize() + "-pants proud.\n"
		break
	if answer_dict[answer][0] == "drop":
		if player.inventory == []:
			print "You have nothing to drop!"
		else:
			dcount = 1
			drop_dict = {}
			drop_selection = "What do you want to drop?\n    >Nothing (" + str(dcount) + ")"
			drop_dict[dcount] = "nothing"
			dcount += 1
			for item in player.inventory:
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
				drop_dict[drop_answer].move(player.location)
				continue

	print "You go " + answer_dict[answer][1] + " to the next chamber."
	player.location = player.location.connections[answer_dict[answer][1]]
