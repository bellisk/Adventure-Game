import random

class World:
	def __init__(self):
		self.player = None
		self.rooms = []
		self.characters = []
		self.items = []

class Room:
	def __init__(self, world, description, inhabitants, inventory):
		self.world = world
		self.description = description
		self.inhabitants = inhabitants
		self.inventory = inventory
		self.connections = {}

class Character:
	def __init__(self, world, description, owner, location, inventory, friendly = True, embodied = True, visible = True):
		self.world = world
		self.description = description
		self.owner = None
		self.location = None
		self.move_to_room(location)
		self.inventory = inventory
		self.friendly = friendly
		self.embodied = embodied
		self.visible = visible
	def move_to_character(self, new_owner):
		if self.owner != None:
			self.owner.inventory.remove(self)
		if self.location != None:
			self.location.inhabitants.remove(self)
			self.location = None
		self.owner = new_owner
		if self.owner != None:
			self.owner.inventory.append(self)
	def move_to_room(self, new_location):
		if self.owner != None:
			self.owner.inventory.remove(self)
			self.owner = None
		if self.location != None:
			self.location.inhabitants.remove(self)
		self.location = new_location
		self.location.inhabitants.append(self)
		if self == world.player and flashlight in self.inventory:
			for character in self.location.inhabitants:
				character.visible = True
			for item in self.location.inventory:
				item.visible = True
		else:
			for character in self.location.inhabitants:
				character.visible = False
			for item in self.location.inventory:
				item.visible = False
	def talk(self):
		if self.friendly == True:
			print "The " + self.description + " wishes you a nice day."
		else:
			print "The " + self.description + " threatens your bodily integrity."		

class Item:
	def __init__(self, world, description, owner, location, visible = True):
		self.world = world
		self.description = description
		self.owner = None
		self.location = None
		self.move_to_room(location)
		self.visible = visible
	def move_to_character(self, new_owner):
		if self.owner != None:
			self.owner.inventory.remove(self)
		if self.location != None:
			self.location.inventory.remove(self)
			self.location = None
		self.owner = new_owner
		if self.owner != None:
			self.owner.inventory.append(self)
	def move_to_room(self, new_location):
		if self.owner != None:
			self.owner.inventory.remove(self)
			self.owner = None
		if self.location != None:
			self.location.inventory.remove(self)
		self.location = new_location
		self.location.inventory.append(self)
		if self.location != None:
			self.location.inventory.append(self)
		if self == world.player and flashlight in self.inventory:
			for character in self.location.inhabitants:
				character.visible = True
			for item in self.location.inventory:
				item.visible = True
		else:
			for character in self.location.inhabitants:
				character.visible = False
			for item in self.location.inventory:
				item.visible = False

world = World()

#Rooms
entrance = Room(world, "cold, bare entrance chamber", [], [])
grisly_chamber = Room(world, "grisly chamber", [], [])
long_cave = Room(world, "long, echoing cave", [], [])
small_alcove = Room(world, "tiny rock alcove", [], [])
glass_chamber = Room(world, "chamber with glassy walls", [], [])
chimney_room = Room(world, "very tall room like a chimney", [], [])

entrance.connections = {"north": grisly_chamber, "south": long_cave, "east": small_alcove}
grisly_chamber.connections = {"south": entrance, "north": glass_chamber, "east": chimney_room}
long_cave.connections = {"north": entrance}
small_alcove.connections = {"west": entrance, "north": chimney_room}
glass_chamber.connections = {"south": grisly_chamber}
chimney_room.connections = {"west": grisly_chamber, "south": small_alcove}

#Characters
wizened_witch = Character(world, "wizened old witch", None, grisly_chamber, [], True, True)
green_child = Character(world, "green-skinned child", None, long_cave, [], False, True)
bearded_dwarf = Character(world, "bearded dwarf", None, small_alcove, [], True, True)
disembodied_voice = Character(world, "disembodied voice", None, chimney_room, [], False, False)
scaly_beast = Character(world, "huge scaly beast", None, small_alcove, [], True, True)
talking_mule = Character(world, "mule who talks in human language", None, long_cave, [], True, True)
player = Character(world, "you", None, entrance, [], True, True)
world.player = player

#Items
flashlight = Item(world, "flashlight", None, grisly_chamber)
peas = Item(world, "bag of peas", None, grisly_chamber)
goblet = Item(world, "golden goblet", None, long_cave)
mallet = Item(world, "mallet of iron", None, small_alcove)
chips = Item(world, "bag of tortilla chips", None, chimney_room)
necklace = Item(world, "glass bead necklace", None, small_alcove)
tortoise = Item(world, "small green tortoise", None, long_cave)
sword = Item(world, "sword", None, entrance)

world.rooms = [entrance, grisly_chamber, long_cave, small_alcove, glass_chamber, chimney_room]
world.characters = [wizened_witch, green_child, bearded_dwarf, disembodied_voice, scaly_beast, talking_mule]
world.items = [peas, goblet, mallet, chips, necklace, tortoise, sword, flashlight]

#Shuffle the lists
random.shuffle(world.rooms)
random.shuffle(world.characters)
random.shuffle(world.items)

#Make room-character-item tuples and move characters and items into the rooms
for x in zip(world.rooms, world.characters, world.items):
	if x[1] != None:
		x[1].move_to_room(x[0])
	if x[2] != None:
		x[2].move_to_room(x[0])

world.player.move_to_room(entrance)

embodied_chars = [character for character in world.player.location.inhabitants if character != world.player and character.embodied == True]

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
	world.player.friendly = False

answer = ""
while not answer in ["1", "2"]:
    answer = raw_input(
"""What do you want to take with you into the cave?
	1. A sword
	2. A flashlight
> """)

inventory = []

if answer == "1":
	sword.move_to_character(world.player)
	print "You have a sword in your inventory!"
else:
	flashlight.move_to_character(world.player)
	print "You have a flashlight in your inventory!"

while True:

	raw_input("(Press Enter key)")

	for character in world.player.location.inhabitants:
		print character.description
	for item in world.player.location.inventory:
		print item.description

	question = "\nYou are in a " + world.player.location.description + "."
	for character in world.player.location.inhabitants:
		if character != world.player and character.visible:
			question = question + "\nThere is a " + character.description + " here."
	for item in (world.player.location.inventory):
		if item.visible:
			question = question + "\nOn the floor you see a " + item.description + "."
	if not flashlight in world.player.inventory:
		question = question + "\nIt's too dark to see anything else in here."
	question = question + "\nWhat do you want to do?"

	answer_dict = {}
	qcount = 1

	for character in world.player.location.inhabitants:
		if character != world.player and character.visible == True:
			question = question + "\n    >Talk to the " + character.description + " (" + str(qcount) + ")"
			answer_dict[qcount] = ("talk", character)
			qcount += 1
	for character in world.player.location.inhabitants:
		if character != world.player and character.visible == True:
			question = question + "\n    >Pick up the " + character.description + " (" + str(qcount) + ")"
			answer_dict[qcount] = ("pick up", character)
			qcount += 1
	for item in world.player.location.inventory:
		if item.visible == True:
			question = question + "\n    >Pick up the " + item.description + " (" + str(qcount) + ")"
			answer_dict[qcount] = ("pick up", item)
			qcount += 1
	if not flashlight in world.player.inventory:
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
	for direction in world.player.location.connections.keys():
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
			if world.player.friendly == True:
				if answer_dict[answer][1].friendly == True:
					print "You pick up the " + answer_dict[answer][1].description + "."
					answer_dict[answer][1].move_to_character(world.player)
				else:
					if len(player.inventory) != 0:
						thing = random.choice(world.player.inventory)
						thing.move_to_character(answer_dict[answer][1])
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
			answer_dict[answer][1].move_to_character(world.player)
		continue
	if answer_dict[answer][0] == "wave":
		print "You swing your sword wildly about."
		if len(embodied_chars) != 0:
			print "There is a shout very close to you.\nYou find an injured " + embodied_chars[0].description + " on the floor."
			embodied_chars[0].visible = True
			embodied_chars.remove(embodied_chars[0])
		else:
			print "After a while you feel quite silly and put it away again."
		continue
	if answer_dict[answer][0] == "yell":
		print "You hear the echo of your own voice."
		if len(embodied_chars) != 0:
			print "There are footsteps running away."
			direction = random.choice(world.player.location.connections.keys())
			embodied_chars[0].move_to_room(world.player.location.connections[direction])
		continue
	if answer_dict[answer][0] == "feel":
		if len(world.player.location.inventory) != 0:
			for item in world.player.location.inventory:
				print "On the floor you find a " + item.description + ". You pick it up."
				item.move_to_character(world.player)
		else:
			print "You find nothing of interest in the room."
		continue
	if answer_dict[answer][0] == "leave":
		print "You leave the cave and start the journey home.\n\nYour inventory is:\n"
		for n in world.player.inventory:
			print ">" + n.description
		print "\nWell done! You have made the clan of " + pants_colour.capitalize() + "-pants proud.\n"
		break
	if answer_dict[answer][0] == "drop":
		if world.player.inventory == []:
			print "You have nothing to drop!"
		else:
			dcount = 1
			drop_dict = {}
			drop_selection = "What do you want to drop?\n    >Nothing (" + str(dcount) + ")"
			drop_dict[dcount] = "nothing"
			dcount += 1
			for item in world.player.inventory:
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
				drop_dict[drop_answer].move_to_room(world.player.location)
				continue

	print "You go " + answer_dict[answer][1] + " to the next chamber."
	world.player.move_to_room(world.player.location.connections[answer_dict[answer][1]])
