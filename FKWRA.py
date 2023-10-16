from Modules.classes import *
from Modules.constants import *
from Modules.functions import *

def main():
	# Clear the terminal
	clear_screen()
	hide_cursor()
	# Get the arguments
	refreshRate, dispMode, waitForRefreshRate = handle_arguments()
	# Forever...
	while True:
		try:
			# Preliminary setup
			hook_and_check_for_MKW()
			clear_screen()
			# Wait for a race to start
			race = Race.wait_for_race()
			# Initialise players
			race.add_players()
			realPlayer = race.players[race.get_real_player_id()]
			# Start the execution time from 1
			framesCaught = 0
			clear_screen()
			# While in the race...
			while race.is_ongoing() and race.rip != NULL:
				# If a frame has passed, update the data
				race.update_timer()
				if race.time.delta() != 0:
					framesCaught += 1
					race.update(framesCaught)
				# Print the data of the real player on screen according to the refresh rate
				if race.time.currState % refreshRate == 0 or not waitForRefreshRate:
					race.print_race_header(framesCaught)
					realPlayer.print_all_except_laps(dispMode)
					realPlayer.print_latest_laps(dispMode)
					go_to_top()
				handle_savestates(race.time.currState, framesCaught)
			# The race has just finished, print the final screen and update the data periodically
			isEndOfRace = True
			isLapScreen = False
			while isEndOfRace:
				clear_screen()
				race.update(framesCaught)
				if isLapScreen:
					race.print_race_header(framesCaught)
					realPlayer.print_all_except_laps(dispMode)
					isLapScreen = False
				else:
					realPlayer.print_all_laps(dispMode)
					isLapScreen = True
				for i in range(5):
					wait()
				if not realPlayer.has_finished():
					isEndOfRace = False
		except Exception as e:
			handle_panic(e)

if __name__ == '__main__':
	main()