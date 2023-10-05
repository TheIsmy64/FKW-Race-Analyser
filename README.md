# FKW-Race-Analyser
A program that collects data from FKW races in real time.

## System Requirements
* Python 3.8 or newer.
* The *dolphin-memory-engine* python library that can be found [here](https://github.com/henriquegemignani/py-dolphin-memory-engine), or it can be installed by typing `pip install dolphin-memory-engine` in a terminal.

## Use
* Launch the script with `python FKWRA.py n` where n is the refresh time in in-game frames (for example, `120` would equal to 2 seconds).
 * If the argument isn't a positive integer, the refresh rate is automatically assigned the value of `60`.
 * If the argument is exactly `0`, the program will run in real time.
* Open any game region of Formula Kart Wii on any Dolphin Emulator instance.
* When a race starts, the program will automatically find the data it needs!

Warning: the lower the refresh time is, the more inaccurate the program becomes, risking losing many frames of gameplay and gathering a lot of data. For users with low-end PCs, it's recommended to not go under `60`.
