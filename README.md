# FKW-Race-Analyser
A program that collects data from FKW races in real time.

## Requirements
* Python 3.10 or newer.
* The *dolphin-memory-engine* python library that can be found [here](https://github.com/henriquegemignani/py-dolphin-memory-engine), or it can be installed by typing `pip install dolphin-memory-engine` in a terminal.

### Python Modules Used
* argparse
* cursor
* dolphin-memory-engine
* os
* platform
* time

## Use
* Launch the script with `python FKWRA.py`. You can launch it with the argument `-h` for help with the other options.
* Open any game region of Formula Kart Wii on any Dolphin Emulator instance.
* When a race starts, the program will automatically find the data it needs!