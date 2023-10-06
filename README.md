# FKW-Race-Analyser
A program that collects data from FKW races in real time.

## System Requirements
* Python 3.8 or newer.
* The *dolphin-memory-engine* python library that can be found [here](https://github.com/henriquegemignani/py-dolphin-memory-engine), or it can be installed by typing `pip install dolphin-memory-engine` in a terminal.

## Use
* Launch the script with `python FKWRA.py` with the possibility of adding the following arguments:
  * `-rr refreshRate` sets the refresh rate of the display in in-game frames.
    * To use real time refresh rate, set this option to `0`.
	* The default value is `60`, or 1 second.
  * `-mm measurementMode` sets the measurement mode of the distances and speeds on the display.
    * To use the imperial measurement mode, set this option to `imperial` or `miles`.
	* If this option isn't set, the default metric measurement mode is used.
* Open any game region of Formula Kart Wii on any Dolphin Emulator instance.
* When a race starts, the program will automatically find the data it needs!

WARNING: the lower the refresh time is, the more inaccurate the program becomes, risking losing many frames of gameplay and gathering a lot of data. For users with low-end PCs, it's recommended to not go under `60`.
