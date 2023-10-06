import dolphin_memory_engine as dp
import os
import time
import sys
import platform
import tkinter

# Texts Lists
posTexts = ["1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th", "9th", "10th", "11th", "12th"]
itemTexts = ["Green Shell", "Red Shell", "Banana\t", "Fake Item Box", "Mushroom", "/", "Bob-omb\t", "Blue Shell", "Lightning", "Star\t", "Golden Mushroom", "Mega Mushroom", "Feather\t", "POW Block", "Thunder Cloud", "Bullet Bill", "/", "/", "/", "/", "None"]
imperialTexts = ["i", "imp", "imperial", "america", "american", "us", "usa", "inches", "feet", "miles", "mph"]

def read_half(p): 
    return dp.read_byte(p) * 256 + dp.read_byte(p + 1)

def precision(n, d):
    return ("{:." + str(d) + "f}").format(n)

def int_to_time(time):
    string = ""
    mins = int(time / 60000)
    secs = int((time - mins * 60000) / 1000)
    mils = time % 1000
    if mins < 10:
        string += "0"
    string += str(mins) + ":"
    if secs < 10:
        string += "0"
    string += str(secs) + "."
    if mils < 100:
        string += "0"
    if mils < 10:
        string += "0"
    string += str(mils)
    return string

def time_to_int(time):
    return (int(time[0:2]) * 60 + int(time[3:5])) * 1000 + int(time[6:9])

def time_diff(time1, time2):
    int_time1 = time_to_int(time1)
    int_time2 = time_to_int(time2)
    diff = int_time1 - int_time2
    if int_time1 < int_time2:
        return "-" + int_to_time(-diff)
    return int_to_time(diff)

def print_pos_tracker(posTimes, execTime, playerCount):
    print("Pos\tTime\t\tPercentage")
    for i in range(playerCount):
        posTime = frames_to_short_time(posTimes[i])
        posPerc = float_to_percentage(posTimes[i] / execTime)
        print(posTexts[i] + "\t" + posTime + "\t" + posPerc)
    print("")

def print_lap_data(lapData, distanceText, speedText):
    i = 0
    print("Lap\tTime\t\tDistance\tAverage Speed")
    for lap in lapData:
        i += 1
        if lap[4] > 0.001:
            print(str(i) + "\t" + lap[2] + "\t" + precision(lap[4], 3) + " " + distanceText + "\t" + precision(lap[6], 2) + " " + speedText)
    print("")

def print_item_counts(itemCounts):
    print("Item\t\t\tSingle\tDouble\tTriple\tTotal")
    for i in range(16):
        singles = itemCounts[i][0]
        doubles = itemCounts[i][1]
        triples = itemCounts[i][2]
        if i != 0x05 and i != 0x0E:
            print(itemTexts[i] + "\t\t" + str(singles) + "\t" + str(doubles) + "\t" + str(triples) + "\t" + str(singles + 2 * doubles + 3 * triples))
        if i == 0x0E:
            print(itemTexts[i] + "\t\t" + str(singles) + "\t\t\t" + str(singles))
    print("")

def get_bit(w, b):
    return (w & pow(2, b)) != 0

def frames_to_short_time(time):
    return int_to_time(int(time * 1000 / 60))[0:8]

def float_to_percentage(n):
    n = n * 100
    string = "{:.2f}".format(n) + "%"
    while len(string) < 7:
        string = "0" + string
    return string

def clear_screen():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

def handle_arguments(args):

    # Check for option: Refresh Rate
    rrID = "-rr"
    rr = 60
    if rrID in args:
        try:
            rr = int(args[args.index(rrID) + 1])
            if rr < 0:
                rr = 60
        except:
            rr = 60
            
    # Check for option: Measurement Mode
    mmID = "-mm"
    mm = "metric"
    sf = 1
    if mmID in args:
        mm = str(args[args.index("-mm") + 1]).lower()
        if mm in imperialTexts:
            sf = 0.6213711922
            mm = "imperial"
    
    return [rr, mm, sf]

# Display Mode
def main():

    # Initialisation of variables
    gameID = ""
    NOITEM = 20
    oldClock = 0
    execTime = 0
    previousRaceComp = 0
    distance = 0
    starTime = 0
    shockedTime = 0
    megaTime = 0
    squishTime = 0
    bulletTime = 0
    tcTime = 0
    airTime = 0
    tricksCount = 0
    previousItem = NOITEM
    previousItemCount = 0
    currentItem = NOITEM
    currentItemCount = 0
    roulettePreviousItem = NOITEM
    inTrick = 0
    inZipperTrick = 0
    wasInTrick = 0
    wasInZipperTrick = 0
    mtState = 0
    mtBoost = 0
    mtPreviousState = 0
    mtCount = 0
    smtCount = 0
    posTimes = [0] * 12
    itemCounts = [[0 for x in range(3)] for y in range(16)]
    lapData = [[0, 0, "00:00.000", "00:00.000", 0, 0, 0] for y in range(50)]
    localClock = 0
    printingFlags = [False, False, False, False, False]
    
    args = handle_arguments(sys.argv)
    refreshRate = args[0]
    noLimit = refreshRate == 0
    measurementMode = args[1]
    scalingFactor = args[2]
    
    # Try Forever...
    while True:
        try:
            while not dp.is_hooked():
                if not printingFlags[0]:
                    clear_screen()
                    print("Start the game before proceeding!")
                    printingFlags[0] = True
                dp.hook()
            printingFlags[0] = False
            
            while gameID != "RMC":
                if not printingFlags[1]:
                    clear_screen()
                    print("This may not be an instance of Mario Kart Wii!\n • If it is: wait a couple of seconds.\n • If it isn't: change game and retry!")
                    printingFlags[1] = True
                gameID = chr(dp.read_byte(0x80000000)) + chr(dp.read_byte(0x80000001)) + chr(dp.read_byte(0x80000002))
            printingFlags[1] = False
            
            region = chr(dp.read_byte(0x80000003))
            staticInstanceInfo = 0
            staticInstancePlayer = 0
            staticInstanceItem = 0

            if region == "P":
                staticInstanceInfo = 0x809bd730
                staticInstancePlayer = 0x809c18f8
                staticInstanceItem = 0x809c3618
            if region == "E":
                staticInstanceInfo = 0x809b8f70
                staticInstancePlayer = 0x809bd110
                staticInstanceItem = 0x809bee20
            if region == "J":
                staticInstanceInfo = 0x809bc790
                staticInstancePlayer = 0x809c0958
                staticInstanceItem = 0x809c2678
            if region == "K":
                staticInstanceInfo = 0x809abd70
                staticInstancePlayer = 0x809aff38
                staticInstanceItem = 0x809b1c58
            
            RaceInfo = dp.read_word(staticInstanceInfo)
            PlayerHolder = dp.read_word(staticInstancePlayer)
            ItemHolder = dp.read_word(staticInstanceItem)
            
            if RaceInfo != 0 and PlayerHolder != 0 and ItemHolder != 0:
                
                # Some Race related pointers
                RaceInfoPlayers     = dp.read_word(RaceInfo + 0x0C)
                RaceInfoPlayer      = dp.read_word(RaceInfoPlayers)
                
                # Some Player related pointers
                pid                 = dp.read_byte(RaceInfoPlayer + 0x08)
                Players             = dp.read_word(PlayerHolder + 0x20)
                Player              = dp.read_word(Players + pid * 0x04)
                PlayerSub           = dp.read_word(Player + 0x10)
                PlayerParams        = dp.read_word(Player + 0x14)
                PlayerSub10         = dp.read_word(PlayerSub + 0x10)
                PlayerSub1C         = dp.read_word(PlayerSub + 0x1C)
                
                # Some Item related pointers
                ItemHolderPlayer    = dp.read_word(ItemHolder + 0x14)
                PlayerRoulette      = ItemHolderPlayer + 0x54
                PlayerInventory     = ItemHolderPlayer + 0x88
                
                # Data from RaceInfo
                stage               = dp.read_word(RaceInfo + 0x28)
                
                # Data from RaceInfoPlayer
                raceComp            = dp.read_float(RaceInfoPlayer + 0x10)
                pos                 = dp.read_byte(RaceInfoPlayer + 0x20)
                currentLap          = read_half(RaceInfoPlayer + 0x24)
                clock               = dp.read_word(RaceInfoPlayer + 0x2C) - 412 # Offset for proper maths
                framesFirst         = dp.read_word(RaceInfoPlayer + 0x30)
                stateFlags          = dp.read_word(RaceInfoPlayer + 0x38)
                lapFinishTimes      = dp.read_word(RaceInfoPlayer + 0x3C)
                raceFinishTime      = dp.read_word(RaceInfoPlayer + 0x40)
                
                # Data from PlayerHolder
                playerCount         = dp.read_byte(PlayerHolder + 0x24)
                
                # Data from PlayerSub10
                speed               = dp.read_float(PlayerSub10 + 0x20) * scalingFactor
                
                # Data from PlayerSub1C
                bitfield0           = dp.read_word(PlayerSub1C + 0x04)
                bitfield1           = dp.read_word(PlayerSub1C + 0x08)
                bitfield2           = dp.read_word(PlayerSub1C + 0x0C)
                
                # Data from PlayerInventory
                currentItem         = dp.read_word(PlayerInventory + 0x04)
                currentItemCount    = dp.read_word(PlayerInventory + 0x08)
                rouletteNextItem    = dp.read_word(PlayerRoulette + 0x1C)
                
                isRace = stage == 2
                if isRace and oldClock != clock and clock != 0:
                    
                    # We're in a race and the program is running: we increment the execution time by 1
                    execTime += 1
                    
                    # Item states and timers
                    inStar      = get_bit(bitfield1, 31)
                    isShocked   = get_bit(bitfield2, 7)
                    inMega      = get_bit(bitfield2, 15)
                    isSquished  = get_bit(bitfield2, 16)
                    inBullet    = get_bit(bitfield2, 27)
                    hasTC       = get_bit(bitfield2, 29)
                    inAir       = dp.read_word(PlayerSub1C + 0x1C) != 0
                    
                    starTime += inStar
                    shockedTime += isShocked
                    megaTime += inMega
                    squishTime += isSquished
                    bulletTime += inBullet
                    tcTime += hasTC
                    airTime += inAir
                    
                    # Speed and distance
                    distance += abs(speed) / 216000
                    avgSpeed = distance * 216000 / execTime
                    speedText = "km/h"
                    distanceText = "km"
                    if measurementMode == "imperial":
                        speedText = "mph"
                        distanceText = "miles"
                    if speed < 0:
                        speedText += " (R)"
                    
                    # Position Timers
                    posTimes[pos - 1] += 1
                    
                    # Miniturbos
                    mtState = read_half(PlayerSub10 + 0xFC)
                    mtBoost = read_half(PlayerSub10 + 0x0102)
                    if (mtState == 0 or mtState == 1) and mtBoost != 0:
                        if mtPreviousState == 2:
                            mtCount += 1
                        if mtPreviousState == 3:
                            smtCount += 1
                    
                    # Tricks
                    inTrick = get_bit(bitfield1, 6)
                    inZipperTrick = get_bit(bitfield1, 15)
                    if not wasInTrick and inTrick:
                        tricksCount += 1
                    if not wasInZipperTrick and inZipperTrick:
                        tricksCount += 1
                    
                    # Items
                    if previousItem == NOITEM and currentItem != NOITEM:
                        itemCounts[currentItem][currentItemCount - 1] += 1
                    if roulettePreviousItem == 0x0E and rouletteNextItem == NOITEM and hasTC:
                        itemCounts[roulettePreviousItem][0] += 1
                    
                    # End of Lap
                    lcLap = int(raceComp) - 1   # Latest Completed Lap
                    if int(previousRaceComp) != int(raceComp) and lcLap >= 1:
                        
                        mins = read_half(lapFinishTimes + (lcLap - 1) * 0x0C + 0x04)
                        secs = dp.read_byte(lapFinishTimes + (lcLap - 1) * 0x0C + 0x06)
                        mils = read_half(lapFinishTimes + (lcLap - 1) * 0x0C + 0x08)
                        cumTime = int_to_time((mins * 60 + secs) * 1000 + mils)
                        
                        if lcLap == 1:
                            lapData[lcLap - 1] = [
                                                                clock,                      # Lap Clock
                                                                clock,                      # Cumulative Clock
                                                                cumTime,                    # Lap Time
                                                                cumTime,                    # Cumulative Time
                                                                distance,                   # Lap Distance
                                                                distance,                   # Cumulative Distance
                                                                distance * 216000 / clock   # Average Speed
                                                              ]
                        else:
                            lapData[lcLap - 1] = [
                                                                clock - lapData[lcLap - 2][1],                                                # Lap Clock
                                                                clock,                                                                        # Cumulative Clock
                                                                time_diff(cumTime, lapData[lcLap - 2][3]),                                    # Lap Time
                                                                cumTime,                                                                      # Cumulative Time
                                                                distance - lapData[lcLap - 2][5],                                             # Lap Distance
                                                                distance,                                                                     # Cumulative Distance
                                                                (distance - lapData[lcLap - 2][5]) * 216000 / (clock - lapData[lcLap - 2][1]) # Average Speed
                                                              ]
                    
                    # Display
                    if execTime % refreshRate == 0 or noLimit:
                        clear_screen()
                        
                        # Reset the printing flag of other messages
                        printingFlags = [False, False, False, False, False]
                        
                        # Print Program Data
                        print("Execution Time:\t\t" + str(execTime) + "\t\tRace Clock:\t\t" + str(clock))
                        print("Frames Lost:\t\t" + str(clock - execTime) + "\t\tData accuracy:\t\t" + float_to_percentage(execTime / clock))
                        
                        # Print General Data
                        print("Current Lap:\t\t" + str(currentLap) + " / 50\t\tRace Completion:\t" + precision(raceComp, 3))
                        print("Speed:\t\t\t" + precision(abs(speed), 2) + " " + speedText + "\tAverage Speed:\t\t" + precision(avgSpeed, 2) + " " + speedText)
                        print("Total distance:\t\t" + precision(distance, 3) + " " + distanceText)
                        print("Position:\t\t" + posTexts[pos - 1])
                        print("Current Item:\t\t" + str(currentItemCount) + "× " + itemTexts[currentItem])
                        print("Tricks:\t\t\t" + str(tricksCount))
                        print("Miniturbos:\t\t" + str(mtCount + smtCount) + " (" + str(mtCount) + " + " + str(smtCount) + ")")
                        print("Item Boxes:\t\t" + str(sum(map(sum, itemCounts))))
                        print("")
                        
                        # Print Timers
                        print("Star Time:\t\t" + frames_to_short_time(starTime) + "\tMega Time:\t\t" + frames_to_short_time(megaTime))
                        print("Shocked Time:\t\t" + frames_to_short_time(shockedTime) + "\tSquished Time:\t\t" + frames_to_short_time(squishTime))
                        print("Bullet Time:\t\t" + frames_to_short_time(bulletTime) + "\tThundercloud Time:\t" + frames_to_short_time(tcTime))
                        print("Air Time:\t\t" + frames_to_short_time(airTime))
                        print("")
                        
                        # Print Position Tracker
                        print_pos_tracker(posTimes, execTime, playerCount)
                        
                        # Print Item Counts
                        print_item_counts(itemCounts)
                        
                        # Print Lap Data
                        print_lap_data(lapData, distanceText, speedText)
                        
                        print("\n\n\n\n\n\n\n\n\n\n\n\n\n")
                    
                    mtPreviousState = mtState
                    previousRaceComp = raceComp
                    wasInTrick = inTrick
                    wasInZipperTrick = inZipperTrick
                    roulettePreviousItem = rouletteNextItem
                    previousItem = currentItem
                    oldClock = clock
                    
                # Get Finish Time
                minsFinish = read_half(raceFinishTime + 0x04)
                secsFinish = dp.read_byte(raceFinishTime + 0x06)
                milsFinish = read_half(raceFinishTime + 0x08)
                cumFinish = (minsFinish * 60 + secsFinish) * 1000 + milsFinish
                
                # Needs logic fixing and lap 50 data
                if cumFinish != 0:
                    time.sleep(1)
                    clear_screen()
                    
                    print("Execution Time:\t\t" + str(execTime) + "\t\tRace Clock:\t\t" + str(clock) + "\t\tFrames Lost:\t" + str(clock - execTime))
                    print("Current Lap:\t\t" + str(currentLap) + "/50\t\tRace Completion:\t" + precision(raceComp, 3))
                    print("Speed:\t\t\t" + precision(abs(speed), 2) + " " + speedText + "\tAverage Speed:\t\t" + precision(avgSpeed, 2) + " " + speedText)
                    print("Total distance:\t\t" + precision(distance, 3) + " " + distanceText)
                    print("Position:\t\t" + posTexts[pos - 1])
                    print("Star Time:\t\t" + str(starTime) + "\t\tMega Time:\t\t" + str(megaTime))
                    print("Shocked Time:\t\t" + str(shockedTime) + "\t\tSquished Time:\t\t" + str(squishTime))
                    print("Bullet Time:\t\t" + str(bulletTime) + "\t\tThundercloud Time:\t" + str(tcTime))
                    print("Current Item:\t\t" + str(currentItemCount) + "× " + itemTexts[currentItem])
                    print("Tricks Count:\t\t" + str(tricksCount))
                    
                    print("")
                    
                    print_pos_tracker(posTimes, execTime, playerCount)
                    print_item_counts(itemCounts)
                    print_lap_data(lapData, distanceText, speedText)
                    
                    print("\n\n\n\n\n\n\n\n\n\n\n\n\n")
             
            else:
                if not printingFlags[2]:
                    clear_screen()
                    print("Waiting for a race to start!")
                    printingFlags[2] = True
                
                oldClock = 0
                execTime = 0
                previousRaceComp = 0
                distance = 0
                starTime = 0
                shockedTime = 0
                megaTime = 0
                squishTime = 0
                bulletTime = 0
                tcTime = 0
                airTime = 0
                tricksCount = 0
                previousItem = NOITEM
                previousItemCount = 0
                currentItem = NOITEM
                currentItemCount = 0
                roulettePreviousItem = NOITEM
                inTrick = 0
                wasInTrick = 0
                inZipperTrick = 0
                wasInZipperTrick = 0
                mtState = 0
                mtBoost = 0
                mtPreviousState = 0
                mtCount = 0
                smtCount = 0
                posTimes = [0] * 12
                itemCounts = [[0 for x in range(3)] for y in range(16)]
                lapData = [[0, 0, "00:00.000", "00:00.000", 0, 0, 0] for y in range(50)]
                localClock += 1
                printingFlags = [False, False, True, False, False]
        
        except Exception as e:
                clear_screen()
                print("An error has occurred!")
                print(e)
                input()

if __name__ == '__main__':
    main()