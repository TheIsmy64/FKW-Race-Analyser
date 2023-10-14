from Modules.functions import *
from Modules.constants import *

class Time:
	# Parameters
	# sign			(string)	- The sign of the time, either "+" or "-"
	# frames		(int)		- The number of frames of the time
	# minutes		(int)		- The number of minutes of the time
	# seconds		(int)		- The number of seconds of the time
	# milliseconds	(int)		- The number of milliseconds of the time (might not correspond 100% to the time in frames)
	
	# Initialisers
	def __init__(self, frames):
		self.sign = "+" if frames >= 0 else "-"
		self.frames = abs(frames)
		self.minutes = int(frames / 3600)
		self.seconds = int(frames / 60) - self.minutes * 60
		self.milliseconds = int(frames * 50 / 3) - (self.minutes * 60 + self.seconds) * 1000
	
	def empty():
		return Time(0)
	
	def frame():
		return Time(1)
	
	def cap():
		return Time(359999)
	
	def from_string(string):
		time = Time.empty()
		try:
			if len(string) == 9:
				return time.set_precise("+", int(string[0:2]), int(string[3:5]), int(string[6:9]))
			if len(string) == 10:
				if string[0] == "+" or string[0] == "-":
					return time.set_precise(string[0], int(string[1:3]), int(string[4:6]), int(string[7:10]))
			else:
				raise Exception(f"\"{string}\" is not a valid Time string.")
		except:
			raise Exception(f"\"{string}\" is not a valid Time string.")
	
	# Representators
	def __repr__(self):
		stringMinutes = str(self.minutes)
		stringSeconds = str(self.seconds)
		stringMilliseconds = str(self.milliseconds)
		if self.minutes < 10:
			stringMinutes = "0" + stringMinutes
		if self.seconds < 10:
			stringSeconds = "0" + stringSeconds
		if self.milliseconds < 100:
			stringMilliseconds = "0" + stringMilliseconds
		if self.milliseconds < 10:
			stringMilliseconds = "0" + stringMilliseconds
		return f"{self.sign}{stringMinutes}:{stringSeconds}.{stringMilliseconds}"
	
	def repr_unsigned(self):
		return self.__repr__()[1:]
	
	def repr_short(self):
		return self.__repr__()[1:9]
	
	def repr_frames(self):
		return self.frames
	
	# Setters
	def increment_by_frames(self, frames):
		self.frames += frames
		self.minutes = int(self.frames / 3600)
		self.seconds = int(self.frames / 60) - self.minutes * 60
		self.milliseconds = int(self.frames * 50 / 3) - (self.minutes * 60 + self.seconds) * 1000
	
	def increment(self):
		self.increment_by_frames(1)
	
	def set_precise(self, sign, minutes, seconds, milliseconds):
		self.sign = sign
		if sign not in ("+", "-"):
			self.sign = "+"
		self.frames = ((minutes * 60) + seconds) * 60 + int(milliseconds * 50 / 3)
		self.minutes = minutes
		self.seconds = seconds
		self.milliseconds = milliseconds
	
	def set_from_milliseconds(self, milliseconds):
		self.sign = "+" if milliseconds >= 0 else "-"
		self.minutes = int(abs(milliseconds) / 60000)
		self.seconds = int(abs(milliseconds) / 1000) - self.minutes * 60
		self.milliseconds = abs(milliseconds) % 1000
	
	# Overloaded Operators
	def __add__(self, other):	# ( + )
		time = Time.empty()
		time.set_from_milliseconds(self.to_milliseconds() + other.to_milliseconds())
		return time
	
	def __sub__(self, other):	# ( - )
		time = Time.empty()
		time.set_from_milliseconds(self.to_milliseconds() - other.to_milliseconds())
		return time
	
	def __lt__(self, other):	# ( < )
		return self.to_milliseconds() < other.to_milliseconds()
	
	def __gt__(self, other):	# ( > )
		return self.to_milliseconds() > other.to_milliseconds()
	
	def __eq__(self, other):	# ( == )
		return self.to_milliseconds() == other.to_milliseconds()
	
	def __ne__(self, other):	# ( != )
		return self.to_milliseconds() != other.to_milliseconds()
	
	# Other Methods
	def to_milliseconds(self):
		sign = -1 if self.sign == "-" else 1
		return ((self.minutes * 60 + self.seconds) * 1000 + self.milliseconds) * sign
	
	def to_hours(self):
		sign = -1 if self.sign == "-" else 1
		return ((self.milliseconds / 1000 + self.seconds) / 60 + self.minutes) / 60 * sign

class Distance:
	# Parameters
		# distance		(float)		- The distance in kilometers
	
	# Initialisers
	def __init__(self, distance):
		self.distance = distance
	
	def empty():
		return Distance(0)
	
	def from_speed_and_time(s, t):
		return Distance(s.speed * t.to_hours())
	
	# Representators
	def __repr__(self):
		return f"{self.distance:.3f} km"
	
	def repr_mode(self, dispMode):
		if dispMode not in displayDistanceDict:
			raise Exception(f"{dispMode} is not a valid display mode of {self}. Valid display modes are:\n • Metric\n • Imperial\n • IS")
		return f"{self.distance * sfDistanceDict[dispMode]:.3f} {displayDistanceDict[dispMode]}"
	
	# Overloaded Operators
	def __add__(self, other):	# ( + )
		return Distance(self.distance + other.distance)
	
	def __sub__(self, other):	# ( - )
		return Distance(self.distance - other.distance)
	
	def __lt__(self, other):	# ( < )
		return self.distance < other.distance
	
	def __gt__(self, other):	# ( > )
		return self.distance > other.distance

class Speed:
	# Parameters
		# speed			(float)		- The speed in kilometers per hour
	
	# Initialisers
	def __init__(self, spd):
		self.speed = spd
	
	def empty():
		return Speed(0)
	
	def from_distance_and_time(d, t):
		return Speed(d.distance / t.to_hours())
	
	# Representators
	def __repr__(self):
		stringReverse = ""
		if self.speed < 0:
			stringReverse = " (R)"
		return f"{abs(self.speed):.2f} km/h{stringReverse}"
	
	def repr_mode(self, dispMode):
		if dispMode not in displayDistanceDict:
			raise Exception(f"{dispMode} is not a valid display mode of {self}. Valid display modes are:\n • Metric\n • Imperial\n • IS")
		stringReverse = ""
		if self.speed < 0:
			stringReverse = " (R)"
		return f"{abs(self.speed) * sfSpeedDict[dispMode]:.2f} {displaySpeedDict[dispMode]}{stringReverse}"
	
	# Overloaded Operators
	def __lt__(self, other):
		return self.speed < other.speed
	
	def __gt__(self, other):
		return self.speed > other.speed

class Lap:
	# Parameters
		# lp			(int)		- The pointer in memory where the lap data is stored
		# number		(int)		- The number of the lap
		# cumTime		(Time)		- The Time at which the lap was completed with respect to the beginning of the race
		# time			(Time)		- The Time in which the lap was completed
		# timeFromFirst	(Time)		- The Time difference between the player's lap and 1st place's lap (0 if the player is itself in 1st)
		# timeFromAhead (Time)		- The Time difference between the player's lap and the lap of the player directly ahead (indicates the difference from 2nd if the player is itself in 1st)
		# cumDistance	(Distance)	- The total distance driven from the start of the race to the completion of this lap
		# distance		(Distance)	- The distance driven during the lap
		# avgSpeed		(Speed)		- The average speed at which the lap was driven
	
	# Initialisers
	def __init__(self, lapPointer, lapNumber, cumTime, lapTime, from1st, fromAhead, lapDist, cumDist, avgSpeed):
		self.lp = lapPointer
		self.number = lapNumber
		self.cumTime = cumTime
		self.time = lapTime
		self.timeFromFirst = from1st
		self.timeFromAhead = fromAhead
		self.cumDistance = cumDist
		self.distance = lapDist
		self.avgSpeed = avgSpeed
	
	def empty(lapPointer):
		return Lap(lapPointer, 0, Time.empty(), Time.empty(), Time.empty(), Time.empty(), Distance.empty(), Distance.empty(), Speed.empty())
	
	# Representators
	def __repr__(self):
		stringNumber = str(self.number)
		stringSpeed = str(self.avgSpeed)
		if self.number < 10:
			stringNumber = " " + stringNumber
		if abs(self.avgSpeed.speed) < 100:
			stringSpeed = " " + stringSpeed
		if abs(self.avgSpeed.speed) < 10:
			stringSpeed = " " + stringSpeed
		return f"Lap {stringNumber}\t\t{self.time.repr_unsigned()}\t{self.timeFromFirst}\t{self.timeFromAhead}\t{self.distance}\t{stringSpeed}\n"
	
	def repr_mode(self, dispMode):
		stringNumber = str(self.number)
		stringSpeed = self.avgSpeed.repr_mode(dispMode)
		if self.number < 10:
			stringNumber = " " + stringNumber
		if abs(self.avgSpeed.speed) < 100:
			stringSpeed = " " + stringSpeed
		if abs(self.avgSpeed.speed) < 10:
			stringSpeed = " " + stringSpeed
		return f"Lap {stringNumber}\t\t{self.time.repr_unsigned()}\t{self.timeFromFirst}\t{self.timeFromAhead}\t{self.distance.repr_mode(dispMode)}\t{stringSpeed}\n"
	
	# Setters
	def update_cumulative_time(self):
		minutes = read_half(self.lp + 0x04)
		seconds = read_byte(self.lp + 0x06)
		milliseconds = read_half(self.lp + 0x08)
		self.cumTime.set_precise("+", minutes, seconds, milliseconds)

class LapTracker:
	# Parameters
		# laps			(Lap[1-50])	- The data from the 50 laps
	
	# Initialisers
	def __init__(self):
		self.laps = []
	
	# Setters
	def setup_lap(self, number, totalDistance):
		if number == 1:
			self.laps[number - 1] = Lap()
	
	# Representators
	def __repr__(self):
		string = "Lap\t\tTime\t\tFrom 1st\tFrom Ahead\tDistance\tAverage Speed\n"
		for lap in self.laps:
			if lap.time != Time.empty():
				string += str(lap)
		return string
	
	def repr_mode(self, dispMode):
		string = "Lap\t\tTime\t\tFrom 1st\tFrom Ahead\tDistance\tAverage Speed\n"
		for lap in self.laps:
			string += lap.repr_mode(dispMode)
		return string
	
	def print_latest(self, amount, dispMode):
		string = "Lap\t\tTime\t\tFrom 1st\tFrom Ahead\tDistance\tAverage Speed\n"
		latestLapNumber = self.get_latest_lap_number()
		for lap in self.laps:
			if lap.number in range(max(1, latestLapNumber - amount), latestLapNumber):
				string += lap.repr_mode(dispMode)
		return string
	
	# Other Methods
	def get_latest_lap_number(self):
		for lap in self.laps:
			if lap.time == Time.empty():
				return lap.number
	
	def get_fastest_lap(self):
		fastestLap = self.laps[0]
		if len(self.laps) > 1:
			for lap in self.laps[1:]:
				if lap.time > fastestLap.time:
					fastestLap = lap
		return fastestLap
	
	def get_slowest_lap(self):
		slowestLap = self.laps[0]
		if len(self.laps) > 1:
			for lap in self.laps[1:]:
				if lap.time < slowestLap.time:
					slowestLap = lap
		return slowestLap
	
	def get_longest_lap(self):
		longestLap = self.laps[0]
		if len(self.laps) > 1:
			for lap in self.laps[1:]:
				if lap.distance > longestLap.distance:
					longestLap = lap
		return longestLap
	
	def get_shortest_lap(self):
		shortestLap = self.laps[0]
		if len(self.laps) > 1:
			for lap in self.laps[1:]:
				if lap.distance < shortestLap.distance:
					shortestLap = lap
		return shortestLap
	
	def get_best_lap_by_average_speed(self):
		bestLapAvgSpeed = self.laps[0]
		if len(self.laps) > 1:
			for lap in self.laps[1:]:
				if lap.avgSpeed > bestLapAvgSpeed.avgSpeed:
					bestLapAvgSpeed = lap
		return bestLapAvgSpeed
	
	def get_worst_lap_by_average_speed(self):
		worstLapAvgSpeed = self.laps[0]
		if len(self.laps) > 1:
			for lap in self.laps[1:]:
				if lap.avgSpeed < worstLapAvgSpeed.avgSpeed:
					worstLapAvgSpeed = lap
		return worstLapAvgSpeed

class Item:
	# Parameters
		# id			(int)		- The item's identifying number
		# amount		(int)		- The amount of items it represents
	
	# Initialisers
	def __init__(self, id, amount):
		if amount > 1 and id == THUNDER_CLOUD:
			raise Exception("Thunder Clouds should not have an item amount greater than 1.")
		self.id = id
		self.amount = amount
	
	def empty():
		return Item(NO_ITEM, 0)
	
	# Representators
	def __repr__(self):
		return f"{self.amount}× {itemDict[self.id]}"
	
	# Overloaded Operators
	def __eq__(self, other):
		return self.id == other.id and self.amount == other.amount
	
	def __ne__(self, other):
		return self.id != other.id or self.amount != other.amount
	
	# Other Methods
	def is_valid(self):
		return self.id != TRIPLE_MUSHROOM and self.id >= 0 and self.id <= 15 and self.amount >= 1 and self.amount <= 3

class ItemCounter:
	# Parameters
		# id			(int)		- The item's identifying number
		# singles		(int)		- The amount of single items counted
		# doubles		(int)		- The amount of double items counted
		# triples		(int)		- The amount of triple items counted
		# total			(int)		- The total amount of items counted
	
	# Initialisers
	def __init__(self, id, singles, doubles, triples):
		self.id = id
		self.singles = singles
		self.doubles = doubles
		self.triples = triples
		self.total = singles + doubles * 2 + triples * 3
	
	def empty():
		return ItemCounter(NO_ITEM, 0, 0, 0)
	
	def from_item(item):
		self = ItemCounter.empty()
		self.id = item.id
		self.singles = 1 if item.amount == 1 else 0
		self.doubles = 1 if item.amount == 2 else 0
		self.triples = 1 if item.amount == 3 else 0
		self.total = self.singles + self.doubles * 2 + self.triples * 3
		return self
	
	# Representators
	def __repr__(self):
		if self.id == THUNDER_CLOUD:
			return f"{itemDict[self.id]}\t\t{self.singles}\t\t\t{self.total}"
		extraTab = ""
		if self.id in [BANANA, BOB_OMB, STAR, FEATHER]:
			extraTab = "\t"
		return f"{itemDict[self.id]}{extraTab}\t\t{self.singles}\t{self.doubles}\t{self.triples}\t{self.total}"
	
	# Setters
	def set_item(self, id):
		self.id = id
	
	def increment_singles(self):
		self.singles += 1
		self.total += 1
	
	def increment_doubles(self):
		if self.id == THUNDER_CLOUD:
			raise Exception("Thunder Clouds should not have an item amount greater than 1.")
		self.doubles += 1
		self.total += 2
	
	def increment_triples(self):
		if self.id == THUNDER_CLOUD:
			raise Exception("Thunder Clouds should not have an item amount greater than 1.")
		self.triples += 1
		self.total += 3
	
	def increment_by_amount(self, amount):
		if amount < 1 or amount > 3:
			raise Exception(f"{amount} is not a possible amount for items.")
		match amount:
			case 1:
				self.increment_singles()
			case 2:
				self.increment_doubles()
			case 3:
				self.increment_triples()
	
	# Getters
	def get_box_amount(self):
		return self.singles + self.doubles + self.triples
			
class ItemTracker:
	# Parameters
		# counters		(ItemCounter[15])	- The counters for all items
	
	# Initialisers
	def __init__(self):
		self.counters = []
		for id in itemDict.keys():
			if id != NO_ITEM:
				counter = ItemCounter.empty()
				counter.set_item(id)
				self.counters.append(counter)
	
	# Representators
	def __repr__(self):
		string = "Item\t\t\tSingles\tDoubles\tTriples\tTotal\n"
		for counter in self.counters:
			string += f"{counter}\n"
		return string
	
	# Setters
	def increment_by_item(self, item):
		if item.is_valid():
			self.counters[self.get_index_from_item_id(item.id)].increment_by_amount(item.amount)
	
	# Getters
	def get_index_from_item_id(self, id):
		i = 0
		while self.counters[i].id != id:
			i += 1
		return i
	
	def get_box_amount(self):
		amount = 0
		for counter in self.counters:
			amount += counter.get_box_amount()
		return amount

class PositionTracker:
	# Parameters
		# players		(int)				- The amount of players in the race
		# posTimes		(Time[1-12])		- The cumulative time the player has been in that position
	
	# Initialisers
	def __init__(self, players):
		if players < 1 or players > 12:
			raise Exception("A race has to hold at least 1 player and can't hold more than 12 players!")
		self.players = players
		self.posTimes = []
		for i in range(players):
			self.posTimes.append(Time.empty())
	
	# Representators
	def __repr__(self):
		if self.players == 1:
			return ""
		string = "Position\tTime\n"
		for player in range(self.players):
			string += f"{positionTexts[player]}\t\t{self.posTimes[player].repr_short()}\n"
		return string
	
	# Setters
	def increment(self, position):
		self.posTimes[position - 1].increment()

class TwoStates:
	# Parameters
		# currState		(*any*)			- The current state of the class
		# prevState		(*any*)			- The previous state of the class
	
	# Initialisers
	def __init__(self, current, previous):
		self.currState = current
		self.prevState = previous
	
	def empty():
		return TwoStates(0, 0)
	
	# Representators
	def __repr__(self):
		return f"Previous State:\t{self.prevState}\nCurrent State:\t{self.currState}"
	
	def repr_current(self):
		return f"{self.currState}"
	
	# Setters
	def set_current(self, current):
		self.currState = current
	
	def set_previous(self, previous):
		self.prevState = previous
	
	def shift_and_set(self, new):
		self.prevState = self.currState
		self.currState = new
	
	# Other Methods
	def delta(self):
		return self.currState - self.prevState

class Player:
	# Parameters
		# Pointers
			# pp			(int)					- The Player pointer in the game's memory
			# ripp			(int)					- The RaceInfoPlayer pointer in the game's memory
			# ihpp			(int)					- The ItemHolderPlayer pointer in the game's memory
			# pparams		(int)					- The PlayerParams pointer in the game's memory
			# psub10		(int)					- The PlayerSub10 pointer in the game's memory
			# psub1C		(int)					- The PlayerSub1C pointer in the game's memory
		# Simple Data
			# bitFields		(int[5])				- The bitfields stored in PlayerSub1C
			# pid			(int)					- The player's id in the game's memory
			# ptype			(int)					- The player's type:	0: CPU - 1: Player (offline) - 2: Player (online) - 3: Opponent (online)
			# vehicleID		(int)					- The vehicle's id
			# characterID	(int)					- The character's id
			# raceComp		(float)					- The race completion achieved by the player
			# speed			(Speed)					- The current speed of the player
			# distance		(Distance)				- The total distance driven by the player
			# avgSpeed		(Speed)					- The average speed at which the player drove
		# States
			# lapState		(TwoStates of int)		- The maximum lap that the player has reached
			# posState		(TwoStates of int)		- The player's position state
			# trickState	(TwoStates of boolean)	- The player's trick state
			# oobState		(TwoStates of boolean)	- The player's out of bounds state
			# mtState		(TwoStates of int)		- The player's miniturbo state
			# mtBoostState	(TwoStates of int)		- The player's miniturbo boost state
			# megaState		(TwoStates of boolean)	- The player's mega mushroom state 
			# starState		(TwoStates of boolean)	- The player's star state
			# bulletState	(TwoStates of boolean)	- The player's bullet bill state
			# tcState		(TwoStates of boolean)	- The player's thundercloud state
			# shockedState	(TwoStates of boolean)	- The player's shocked state
			# squishedState	(TwoStates of boolean)	- The player's squished state
			# airState		(TwoStates of boolean)	- The player's air state
			# itemState		(TwoStates of Item)		- The player's item state
			# rouletteState	(TwoStates of Item)		- The player's roulette state (only for real players)
		# Timers
			# megaTime		(Time)					- The player's cumulative mega mushroom time
			# starTime		(Time)					- The player's cumulative star time
			# bulletTime	(Time)					- The player's cumulative bullet bill time
			# tcTime		(Time)					- The player's cumulative thundercloud time
			# shockedTime	(Time)					- The player's cumulative shocked time
			# squishedTime	(Time)					- The player's cumulative squished time
			# airTime		(Time)					- The player's cumulative air time
		# Counters
			# tricksCount	(int)					- How many tricks the player performed
			# mtCount		(int)					- How many miniturbos the player performed
			# respawnCount	(int)					- How many times the player respawned
			# boxCount		(int)					- How many item box roulettes the player has successfully rolled
		# Complex Data
			# lapTracker	(LapTracker)			- The player's lap data
			# itemTracker	(ItemTracker)			- The player's item data
			# posTracker	(PositionTracker)		- The player's position data
	
	# Initialisers
	def __init__(self, pPointer, ripPointer, ihpPointer):
		# Get pointers
		self.pp = pPointer
		self.ripp = ripPointer
		self.ihpp = ihpPointer
		self.pparams = read_word(self.pp + 0x1C)
		playerSub = read_word(self.pp + 0x34)
		self.psub10 = read_word(playerSub + 0x10)
		self.psub1C = read_word(playerSub + 0x1C)
		# Get bitfields
		self.bitFields = []
		for i in range(5):
			self.bitFields.append(read_word(self.psub1C + (i + 1) * 0x04))
		# Get simple data
		self.pid = read_byte(self.ripp + 0x08)
		self.ptype = -1
		for i in range(4):
			if get_bit(self.bitFields[4], i) == 1:
				self.ptype = i
		if self.ptype == -1:
			raise Exception(f"Player {self.pid} has no type!")
		self.vehicleID = read_word(self.pparams + 0x04)
		self.characterID = read_word(self.pparams + 0x08)
		self.raceComp = read_float(self.ripp + 0x10)
		self.speed = Speed.empty()
		self.distance = Distance.empty()
		self.avgSpeed = Speed.empty()
		# Setup states
		self.lapState = TwoStates(min(max(int(self.raceComp), 1), FKW_LAPS + 1), min(max(int(self.raceComp), 1), FKW_LAPS + 1))
		self.posState = TwoStates.empty()
		self.trickState = TwoStates.empty()
		self.oobState = TwoStates.empty()
		self.mtState = TwoStates.empty()
		self.mtBoostState = TwoStates.empty()
		self.megaState = TwoStates.empty()
		self.starState = TwoStates.empty()
		self.bulletState = TwoStates.empty()
		self.tcState = TwoStates.empty()
		self.shockedState = TwoStates.empty()
		self.squishedState = TwoStates.empty()
		self.airState = TwoStates.empty()
		self.itemState = TwoStates(Item.empty(), Item.empty())
		self.rouletteState = TwoStates(Item.empty(), Item.empty())
		# Setup timers
		self.megaTime = Time.empty()
		self.starTime = Time.empty()
		self.bulletTime = Time.empty()
		self.tcTime = Time.empty()
		self.shockedTime = Time.empty()
		self.squishedTime = Time.empty()
		self.airTime = Time.empty()
		# Setup counters
		self.tricksCount = 0
		self.mtCount = 0
		self.respawnCount = 0
		self.boxCount = 0
		# Setup complex data
		self.lapTracker = LapTracker()
		lapFinishTimes = read_word(self.ripp + 0x3C)
		for i in range(FKW_LAPS - 1):
			lapFinishTime = lapFinishTimes + i * 0x0C
			self.lapTracker.laps.append(Lap(lapFinishTime, i + 1, Time.empty(), Time.empty(), Time.empty(), Time.empty(), Distance.empty(), Distance.empty(), Speed.empty()))
		self.lapTracker.laps.append(Lap(read_word(self.ripp + 0x40), FKW_LAPS, Time.empty(), Time.empty(), Time.empty(), Time.empty(), Distance.empty(), Distance.empty(), Speed.empty()))
		self.itemTracker = ItemTracker()
		self.posTracker = PositionTracker(1)
		
	# Setters
	def make_position_tracker(self, playerCount):
		self.posTracker = PositionTracker(playerCount)
	
	def update_data(self, framesCaught):
		# Update bitfields
		for i in range(5):
			self.bitFields[i] = read_word(self.psub1C + (i + 1) * 0x04)
		# Update simple data
		self.raceComp = read_float(self.ripp + 0x10)
		self.speed = Speed(read_float(self.psub10 + 0x20))
		self.distance += Distance.from_speed_and_time(self.speed, Time.frame())
		self.avgSpeed = Speed.from_distance_and_time(self.distance, Time(framesCaught))
	
	def update_states(self):
		# Update states
		self.lapState.shift_and_set(min(max(int(self.raceComp), 1), 50))
		self.posState.shift_and_set(read_byte(self.ripp + 0x20))
		self.trickState.shift_and_set(get_bit(self.bitFields[1], 6) or get_bit(self.bitFields[1], 15))
		self.oobState.shift_and_set(get_bit(self.bitFields[0], 4))
		self.mtState.shift_and_set(int(read_half(self.psub10 + 0xFC) / 2))
		self.mtBoostState.shift_and_set(read_half(self.psub10 + 0x0102))
		self.megaState.shift_and_set(get_bit(self.bitFields[2], 15))
		self.starState.shift_and_set(get_bit(self.bitFields[1], 31))
		self.bulletState.shift_and_set(get_bit(self.bitFields[2], 27))
		self.tcState.shift_and_set(get_bit(self.bitFields[2], 29))
		self.shockedState.shift_and_set(get_bit(self.bitFields[2], 7))
		self.squishedState.shift_and_set(get_bit(self.bitFields[2], 16))
		self.airState.shift_and_set(read_word(self.psub1C + 0x1C))
		self.itemState.shift_and_set(Item(read_word(self.ihpp + 0x8C), read_word(self.ihpp + 0x90)))
		self.rouletteState.shift_and_set(Item(read_word(self.ihpp + 0x70), 1))
	
	def update_timers(self):
		# Update timers
		if self.megaState.currState == 1:
			self.megaTime.increment()
		if self.starState.currState == 1:
			self.starTime.increment()
		if self.bulletState.currState == 1:
			self.bulletTime.increment()
		if self.tcState.currState == 1:
			self.tcTime.increment()
		if self.shockedState.currState == 1:
			self.shockedTime.increment()
		if self.squishedState.currState == 1:
			self.squishedTime.increment()
		if self.airState.currState != 0:
			self.airTime.increment()
	
	def update_counters(self):
		# Update counters
		if self.trickState.delta() == 1:
			self.tricksCount += 1
		if self.mtState.delta() == -1 and self.mtBoostState.delta() != 0:
			self.mtCount += 1
		if self.oobState.delta() == -1:
			self.respawnCount += 1
		self.boxCount = self.itemTracker.get_box_amount()
	
	def update_item_tracker(self):
		# Update item tracker
		if self.itemState.prevState.id == NO_ITEM and self.itemState.currState.id != NO_ITEM:
			self.itemTracker.increment_by_item(self.itemState.currState)
		if self.rouletteState.prevState.id == THUNDER_CLOUD and self.rouletteState.currState.id == NO_ITEM and self.tcState.currState == 1:
			self.itemTracker.increment_by_item(Item(THUNDER_CLOUD, 1))
	
	def update_position_tracker(self):
		self.posTracker.increment(self.posState.currState)
	
	def update_lap_tracker(self):
		a = 0
	
	def update(self, raceTime):
		self.update_data(raceTime)
		self.update_item_tracker()
		self.update_position_tracker()
		self.update_lap_tracker()
		self.update_states()
		self.update_timers()
		self.update_counters()
	
	# Getters
	def has_finished(self):
		return get_bit(read_word(self.ripp + 0x38), 1)
	
	# Representators
	def print_data(self, dispMode):
		print(f"Position:\t{positionTexts[self.posState.currState - 1]} \t\tCombo:\t\t{characterTexts[self.characterID]} on the {vehicleTexts[self.vehicleID]}")
		print(f"Lap:\t\t{self.lapState.currState} / {FKW_LAPS} ({self.raceComp:.2f})\tSpeed:\t\t{self.speed.repr_mode(dispMode)} ({self.avgSpeed.repr_mode(dispMode)})          ")
		print(f"Distance:\t{self.distance.repr_mode(dispMode)}\tItem:\t\t{self.itemState.currState}          ")
		print(f"Boxes:\t\t{self.boxCount}\t\tTricks:\t\t{self.tricksCount}")
		print(f"Miniturbos:\t{self.mtCount}\t\tRespawns:\t{self.respawnCount}")
		print()
	
	def print_timers(self):
		print(f"Mega Time:\t{self.megaTime.repr_short()}\tStar Time:\t{self.starTime.repr_short()}")
		print(f"Bullet Time:\t{self.bulletTime.repr_short()}\tTC Time:\t{self.tcTime.repr_short()}")
		print(f"Shocked Time:\t{self.shockedTime.repr_short()}\tSquished Time:\t{self.squishedTime.repr_short()}")
		print(f"Air Time:\t{self.airTime.repr_short()}")
		print()
	
	def print_trackers(self, dispMode):
		print(self.posTracker)
		print(self.itemTracker)
		print(self.lapTracker.print_latest(3, dispMode))
	
	def print_trackers_finished(self, dispMode):
		print(self.posTracker)
		print(self.itemTracker)
		print(self.lapTracker)
	
	def print_all(self, dispMode):
		self.print_data(dispMode)
		self.print_timers()
		if self.has_finished():
			self.print_trackers_finished(dispMode)
		else:
			self.print_trackers(dispMode)
	
	# Other Methods
	def has_finished_lap(self):
		return self.lapState.delta() == 1

class Race:
	# Parameters
		# Pointers
			# rip			(int)					- The RaceInfo pointer in the game's data
			# php			(int)					- The PlayerHolder pointer in the game's data
			# ihp			(int)					- The ItemHolder pointer in the game's data
		# Other Data
			# time			(TwoStates of int)		- The current time of the race
			# stage			(int)					- The race's stage
			# playerCount	(int)					- The amount of players in the race
			# players		(Player[1-12])			- The players' data of the race
	
	# Initialisers
	def __init__(self, raceInfoPointer, playerHolderPointer, itemHolderPointer):
		self.rip = raceInfoPointer
		self.php = playerHolderPointer
		self.ihp = itemHolderPointer
		self.time = TwoStates(0, 0)
		self.stage = read_word(self.rip + 0x28)
		self.playerCount = read_byte(self.php + 0x24)
		self.players = []
	
	def wait_for_race():
		raceInfo = NULL
		playerHolder = NULL
		itemHolder = NULL
		raceState = -1
		secondPass = False
		while raceInfo == NULL or raceState < 2:
			if not secondPass:
				clear_screen()
				print("Waiting for a self to start...")
				secondPass = True
			raceInfo = read_word(raceInfoDict[read_region()])
			raceState = read_word(raceInfo + 0x28)
		playerHolder = read_word(playerHolderDict[read_region()])
		itemHolder = read_word(itemHolderDict[read_region()])
		clear_screen()
		return Race(raceInfo, playerHolder, itemHolder)
	
	# Representators
	def print_race_header(self, framesCaught):
		print(f"Frames Caught:\t{framesCaught}\t\tFrames Lost:\t{self.time.currState - framesCaught}")
		print(f"Race Time:\t{Time(self.time.currState).repr_short()}\tAccuracy:\t{framesCaught / self.time.currState:.2%}  ")
	# Setters
	def update_pointers(self):
		self.rip = read_word(raceInfoDict[read_region()])
		self.php = read_word(playerHolderDict[read_region()])
		self.ihp = read_word(itemHolderDict[read_region()])
	
	def update_timer(self):
		self.time.shift_and_set(read_word(self.rip + 0x20) - CLOCK_OFFSET)
	
	def update_stage(self):
		self.stage = read_word(self.rip + 0x28)
	
	def update_player_count(self):
		self.playerCount = read_byte(self.php + 0x24)
	
	def update_laps(self):
		for lapPlayer in self.players:
			# If the player has completed a lap, proceed, otherwise go to the next player
			if lapPlayer.has_finished_lap():
				lapIndex = int(lapPlayer.raceComp) - 2
				lapCompleted = lapPlayer.lapTracker.laps[lapIndex]
				lapCompleted.update_cumulative_time()
				lapCompleted.cumDistance = lapPlayer.distance
				# If this is lap 1, the time and distance of the lap are the same as the cumulative time and distance
				if lapIndex == 0:
					lapCompleted.time = lapCompleted.cumTime
					lapCompleted.distance = lapCompleted.cumDistance
				# Otherwise, the time and distance of the lap are the difference of the cumulative times and distances with the previous lap
				else:
					lapPrevious = lapPlayer.lapTracker.laps[lapIndex - 1]
					lapCompleted.time = lapCompleted.cumTime - lapPrevious.cumTime
					lapCompleted.distance = lapCompleted.cumDistance - lapPrevious.cumDistance
				# Don't forget to calculate the average speed
				lapCompleted.avgSpeed = Speed.from_distance_and_time(lapCompleted.distance, lapCompleted.time)
				# If the player is in first place, proceed to the next player, otherwise go on
				if lapPlayer.posState.currState != 1:
					# Find the player in first place and the player ahead. This can be done simultaneously
					firstTime = Time.cap()
					aheadTime = Time.empty()
					lapFirst = Lap.empty(0)
					# Search through all the players that are not the player who completed the lap
					for otherPlayer in self.players:
						if otherPlayer.pid != lapPlayer.pid:
							lapOther = otherPlayer.lapTracker.laps[lapIndex]
							# If we find a better time, record it and the lap of the player who achieved it
							if lapOther.cumTime < firstTime and lapOther.cumTime != Time.empty():
								firstTime = lapOther.cumTime
								lapFirst = otherPlayer.lapTracker.laps[lapIndex]
							# If we find a worse time, record it
							if lapOther.cumTime > aheadTime:
								aheadTime = lapOther.cumTime
					# Calculate the time differences from first place and from the player ahead
					lapCompleted.timeFromFirst = lapCompleted.cumTime - firstTime
					lapCompleted.timeFromAhead = lapCompleted.cumTime - aheadTime
					# Lastly, if the player who completed the lap is in second, update the time difference of the player who finished this lap in first
					if lapPlayer.posState.currState == 2:
						lapFirst.timeFromAhead = lapFirst.cumTime - lapCompleted.cumTime
	
	def update(self, framesCaught):
		self.update_pointers()
		self.update_timer()
		self.update_stage()
		self.update_laps()
		self.update_player_count()
		for player in self.players:
			player.update(framesCaught)
	
	def add_players(self):
		raceInfoPlayers = read_word(self.rip + 0x0C)
		playerPointers = read_word(self.php + 0x20)
		for i in range(self.playerCount):
			raceInfoPlayer = read_word(raceInfoPlayers + i * 0x04)
			playerPointer = read_word(playerPointers + i * 0x04)
			itemHolderPlayer = read_word(self.ihp + i * 0x04 + 0x14)
			self.players.append(Player(playerPointer, raceInfoPlayer, itemHolderPlayer))
			self.players[i].make_position_tracker(self.playerCount)
	
	# Getters
	def get_player_by_id(self, id):
		for i in range (self.playerCount):
			if id == self.players[i].pid:
				return self.players[i]
		raise Exception(f"No player with id {id} was found.")
	
	def get_real_player_id(self):
		for player in self.players:
			if player.ptype == 1 or player.ptype == 2:
				return player.pid
	
	# Other Methods
	def is_ongoing(self):
		return self.stage == 2