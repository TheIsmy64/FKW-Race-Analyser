import argparse
import dolphin_memory_engine as dp
import os
import platform
import time
import cursor

from Modules.constants import *

# Dolphin Memory Engine Functions
def read_byte(pointer):
	return dp.read_byte(pointer)

def read_half(pointer): 
	return dp.read_byte(pointer) * 256 + dp.read_byte(pointer + 1)

def read_word(pointer):
	return dp.read_word(pointer)

def read_float(pointer):
	return dp.read_float(pointer)

def read_gameID():
	return chr(dp.read_byte(DMO)) + chr(dp.read_byte(DMO + 0x01)) + chr(dp.read_byte(DMO + 0x02))

def read_region():
	return chr(dp.read_byte(DMO + 0x03))

# Mario Kart Wii checking functions. It checks if the game that's playing is Mario Kart Wii.
def check_gameID():
	try:
		if read_gameID() != "RMC":
			print("This may not be an instance of Mario Kart Wii.         \n • If it is: wait a few moments.\n • If it isn't: please, close the game and start Mario Kart Wii.")
			go_to_top()
			return False
		return True
	except:
		dp.un_hook()
		return False

def hook_and_check_for_MKW():
	isMKW = False
	while not isMKW:
		# Hook to the game when it gets detected
		while not dp.is_hooked():
			print(end = "Waiting for an instance of Mario Kart Wii on Dolphin...\r")
			dp.hook()
		# Check if the game is an instance of Mario Kart Wii
		isMKW = check_gameID()

# Bit Manipulation Functions
def get_bit(word, bit):
	return (word & pow(2, bit)) != 0

# Maths Functions
def sum_2d_array(array):
	return sum(map(sum, array))

# Terminal Functions
def clear_screen():
	if platform.system() == "Windows":
		os.system("cls")
	else:
		os.system("clear")

def go_to_top():
	print(LINE_UP * 100, end = LINE_UP)

def hide_cursor():
	cursor.hide()

def wait():
	time.sleep(1)

# Handling Functions
def handle_arguments():
	parser = argparse.ArgumentParser()
	parser.add_argument("-r", "--refreshrate", type = int, default = 60, choices = range(0, 10000), metavar="[0 - 10000]",
						help = "Determines the refresh rate of the displayed data measured in in-game frames. The default is 60 (1 second). If it's set to 0, the data will be displayed in real time.")
	parser.add_argument("-d", "--displaymode", choices = ["Metric", "Imperial", "IS"], default = "Metric",
						help = "Determines the display mode of lengths and distances in either kilometers, miles or meters. The default is \"Metric\".")
	args = parser.parse_args()
	waitForRefreshRate = True
	if args.refreshrate == 0:
		args.refreshrate = 1
		waitForRefreshRate = False
	return args.refreshrate, args.displaymode, waitForRefreshRate

def handle_panic(exception):
	clear_screen()
	print(exception, f"{LEFT}.\n")
	for i in range(9):
		print(end = f"Trying to unhook and hook again in {9 - i}.\r")
		wait()
	dp.un_hook()
	clear_screen()

def handle_savestates(raceTime, executionTime):
	if raceTime - executionTime < 0:
		clear_screen()
		print("A savestate has been used!")
		exit()