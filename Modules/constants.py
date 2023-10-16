# Textual Constants
positionTexts = ("1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th", "9th", "10th", "11th", "12th")
imperialTexts = ("i", "imp", "imperial", "us", "usa", "american", "inches", "feet", "miles")
ISTexts = ("is", "standard", "meters")
vehicleTexts = ("Standard Kart S", "Standard Kart M", "Standard Kart L", "Booster Seat", "Classic Dragster", "Offroader", "Mini Beast", "Wild Wing", "Flame Flyer", "Cheep Charger", "Super Blooper", "Piranha Prowler", "Tiny Titan", "Daytripper", "Jetsetter", "Blue Falcon", "Sprinter", "Honeycoupe", "Standard Bike S", "Standard Bike M", "Standard Bike L", "Bullet Bike", "Mach Bike", "Flame Runner", "Bit Bike", "Sugarscoot", "Wario Bike", "Quacker", "Zip Zip", "Shooting Star", "Magikruiser", "Sneakster", "Spear", "Jet Bubble", "Dolphin Dasher", "Phantom")
characterTexts = ("Mario", "Baby Peach", "Waluigi", "Bowser", "Baby Daisy", "Dry Bones", "Baby Mario", "Luigi", "Toad", "Donkey Kong", "Yoshi", "Wario", "Baby Luigi", "Toadette", "Koopa Troopa", "Daisy", "Peach", "Birdo", "Diddy Kong", "King Boo", "Bowser Jr.", "Dry Bowser", "Funky Kong", "Rosalina", "Small Mii Outfit A (Male)", "Small Mii Outfit A (Female)", "Small Mii Outfit B (Male)", "Small Mii Outfit B (Female)", "Small Mii Outfit C (Male)", "Small Mii Outfit C (Female)", "Medium Mii Outfit A (Male)", "Medium Mii Outfit A (Female)", "Medium Mii Outfit B (Male)", "Medium Mii Outfit B (Female)", "Medium Mii Outfit C (Male)", "Medium Mii Outfit C (Female)", "Large Mii Outfit A (Male)", "Large Mii Outfit A (Female)", "Large Mii Outfit B (Male)", "Large Mii Outfit B (Female)", "Large Mii Outfit C (Male)", "Large Mii Outfit C (Female)", "Medium Mii", "Small Mii", "Large Mii", "Peach Biker Outfit", "Daisy Biker Outfit", "Rosalina Biker Outfit")

itemDict = {0x00: "Green Shell",
			0x01: "Red Shell",
			0x02: "Banana",
			0x03: "Fake Item Box",
			0x04: "Mushroom",
			0x06: "Bob-omb",
			0x07: "Blue Shell",
			0x08: "Lightning",
			0x09: "Star",
			0x0A: "Golden Mushroom",
			0x0B: "Mega Mushroom",
			0x0C: "Feather",
			0x0D: "POW Block",
			0x0E: "Thunder Cloud",
			0x0F: "Bullet Bill",
			0x14: "No Item"}

displayDistanceDict = {"Metric":	"km",
						"Imperial":	"miles",
						"IS":		"meters"}

displaySpeedDict = {"Metric":		"km/h",
					 "Imperial":	"mph",
					 "IS":			"m/s"}

# Other Constants
sfDistanceDict = {"Metric":		1,
				  "Imperial":	0.6213711922,
				  "IS":			1000}

sfSpeedDict = {"Metric":	1,
			   "Imperial":	0.6213711922,
			   "IS":		10 / 36}

CLOCK_OFFSET = 239
FKW_LAPS = 50
LAPS_SHOW_AMOUNT = 3
NULL = 0

# Terminal Constants
LINE_UP = "\033[1A"
LINE_CLEAR = "\x1b[2K"
LEFT = "\033[1D"
BLACK = "\033[30m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"
RESET = "\033[0;0m"
BOLD = "\033[1m"
REVERSE = "\033[2m"
BLACK_BACKGROUND = "\033[40m"
RED_BACKGROUND = "\033[41m"
GREEN_BACKGROUND = "\033[42m"
YELLOW_BACKGROUND = "\033[43m"
BLUE_BACKGROUND = "\033[44m"
MAGENTA_BACKGROUND = "\033[45m"
CYAN_BACKGROUND = "\033[46m"
WHITE_BACKGROUND = "\033[47m"

# Item Identifiers
GREEN_SHELL			= 0x00
RED_SHELL			= 0x01
BANANA				= 0x02
FAKE_ITEM_BOX		= 0x03
MUSHROOM			= 0x04
TRIPLE_MUSHROOM		= 0x05
BOB_OMB				= 0x06
BLUE_SHELL			= 0x07
LIGHTNING			= 0x08
STAR				= 0x09
GOLDEN_MUSHROOM		= 0x0A
MEGA_MUSHROOM		= 0x0B
FEATHER				= 0x0C
POW_BLOCK			= 0x0D
THUNDER_CLOUD		= 0x0E
BULLET_BILL			= 0x0F
TRIPLE_GREEN_SHELL	= 0x10
TRIPLE_RED_SHELL	= 0x11
TRIPLE_BANANA		= 0x12
NO_ITEM				= 0x14

# Static Instances of RaceInfo (SIRI)
raceInfoDict = {"P": 0x809BD730,
				"E": 0x809B8F70,
				"J": 0x809BC790,
				"K": 0x809ABD70}

# Static Instances of PlayerHolder (SIPH)
playerHolderDict = {"P": 0x809C18F8,
					"E": 0x809BD110,
					"J": 0x809C0958,
					"K": 0x809AFF38}

# Static Instances of ItemHolder (SIIH)
itemHolderDict = {"P": 0x809C3618,
				  "E": 0x809BEE20,
				  "J": 0x809C2678,
				  "K": 0x809B1C58}

# Dolphin Memory Offset
DMO = 0x80000000