import dolphin_memory_engine as dp
import os
import time
import sys

# Texts Lists
posTexts = ["1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th", "9th", "10th", "11th", "12th"]
itemTexts = ["Green Shell", "Red Shell", "Banana\t", "Fake Item Box", "Mushroom", "/", "Bob-omb\t", "Blue Shell", "Lightning", "Star\t", "Golden Mushroom", "Mega Mushroom", "Feather\t", "POW Block", "Thunder Cloud", "Bullet Bill", "/", "/", "/", "/", "None"]

def read_half(p):
    top = dp.read_byte(p)
    bottom = dp.read_byte(p + 1)
    return top * 256 + bottom

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
    mins = int(time[0:2])
    secs = int(time[3:5])
    mils = int(time[6:9])
    return (mins * 60 + secs) * 1000 + mils

def time_diff(time1, time2):
    int_time1 = time_to_int(time1)
    int_time2 = time_to_int(time2)
    diff = int_time1 - int_time2
    if int_time1 < int_time2:
        return "-" + int_to_time(-diff)
    return int_to_time(diff)

def print_pos_tracker(posTimes, execTime):
    print("Pos\tTime\t\tPercentage")
    for i in range(12):
        posTime = frames_to_short_time(posTimes[i])
        posPerc = float_to_percentage(posTimes[i] / execTime)
        print(posTexts[i] + "\t" + posTime + "\t" + posPerc)
    print("")

def print_lap_data(lapData):
    i = 0
    print("Lap\tTime\t\tDistance\tAvg Speed")
    for lap in lapData:
        i += 1
        if lap[0] != 0:
            print(str(i) + "\t" + lap[2] + "\t" + precision(lap[4], 3) + "km\t\t" + precision(lap[6], 2) + "km/h")

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
            
    print("Total Successful Boxes:\t" + str(sum(map(sum, itemCounts))) + "\n")

def get_bit(w, b):
    return (w & pow(2, b)) != 0

def frames_to_short_time(time):
    return int_to_time(int(time * 1000 / 60))[0:8]

def float_to_percentage(n):
    n = n * 100
    string = "{:.2f}".format(n) + "%"
    if n < 100:
        string = "0" + string
    if n < 10:
        string = "0" + string
    return string

# Display Mode
def main():

    # Initialisation of variables
    gameID = ""
    NOITEM = 20
    oldClock = 0
    execTime = 0
    previousRaceComp = 0
    distance = 0
    reversing = False
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
    try:
        timeLimit = int(sys.argv[1])
        if timeLimit < 0
            timeLimit = 60
    except:
        timeLimit = 60
    noLimit = timeLimit == 0
    
    # Forever...
    while 1:
        
        if isinstance(timeLimit, int):
            if timeLimit < 0:
                noLimit = True
        else:
            noLimit = True
        
        while not dp.is_hooked():
            if localClock % 10 == 0:
                os.system("cls")
                print("Start the game before proceeding!")
            dp.hook()
            localClock += 1
        
        while gameID != "RMC":
            if localClock % 100000 == 0:
                os.system("cls")
                print("This is not an instance of Mario Kart Wii! Change game and retry!")
            gameID = chr(dp.read_byte(0x80000000)) + chr(dp.read_byte(0x80000001)) + chr(dp.read_byte(0x80000002))
            localClock += 1
        
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
            
            RaceInfoPlayers     = dp.read_word(RaceInfo + 0x0C)
            RaceInfoPlayer      = dp.read_word(RaceInfoPlayers)
            ItemHolderPlayer    = dp.read_word(ItemHolder + 0x14)
            PlayerRoulette      = ItemHolderPlayer + 0x54
            PlayerInventory     = ItemHolderPlayer + 0x88
            
            # Data from RaceInfo
            stage               = dp.read_word(RaceInfo + 0x28)
            
            # Data from RaceInfoPlayer
            pid                 = dp.read_byte(RaceInfoPlayer + 0x08)
            raceComp            = dp.read_float(RaceInfoPlayer + 0x10)
            pos                 = dp.read_byte(RaceInfoPlayer + 0x20)
            currentLap          = read_half(RaceInfoPlayer + 0x24)
            clock               = dp.read_word(RaceInfoPlayer + 0x2C) - 412 # Offset for proper maths
            framesFirst         = dp.read_word(RaceInfoPlayer + 0x30)
            stateFlags          = dp.read_word(RaceInfoPlayer + 0x38)
            lapFinishTimes      = dp.read_word(RaceInfoPlayer + 0x3C)
            raceFinishTime      = dp.read_word(RaceInfoPlayer + 0x40)
            
            Players             = dp.read_word(PlayerHolder + 0x20)
            Player              = dp.read_word(Players + pid * 0x04)
            PlayerSub           = dp.read_word(Player + 0x10)
            PlayerParams        = dp.read_word(Player + 0x14)
            PlayerSub10         = dp.read_word(PlayerSub + 0x10)
            PlayerSub1C         = dp.read_word(PlayerSub + 0x1C)
            
            
            # Data from PlayerSub10
            speed               = dp.read_float(PlayerSub10 + 0x20)
            
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
                if speed < 0:
                    reversing = True
                    speedText = "km/h (R)"
                else:
                    reversing = False
                
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
                latestCompletedLap = int(raceComp) - 1
                if int(previousRaceComp) != int(raceComp) and latestCompletedLap >= 1:
                    
                    mins = read_half(lapFinishTimes + (latestCompletedLap - 1) * 0x0C + 0x04)
                    secs = dp.read_byte(lapFinishTimes + (latestCompletedLap - 1) * 0x0C + 0x06)
                    mils = read_half(lapFinishTimes + (latestCompletedLap - 1) * 0x0C + 0x08)
                    cumTime = int_to_time((mins * 60 + secs) * 1000 + mils)
                    
                    if latestCompletedLap == 1:
                        lapData[latestCompletedLap - 1] = [
                                                            clock,                                                  # Lap Clock
                                                            clock,                                                  # Cumulative Clock
                                                            cumTime,                                                # Lap Time
                                                            cumTime,                                                # Cumulative Time
                                                            distance,                                               # Lap Distance
                                                            distance,                                               # Cumulative Distance
                                                            distance * 216000 / clock                               # Average Speed
                                                          ]
                    else:
                        lapData[latestCompletedLap - 1] = [
                                                            clock - lapData[latestCompletedLap - 2][1],                                                             # Lap Clock
                                                            clock,                                                                                                  # Cumulative Clock
                                                            time_diff(cumTime, lapData[latestCompletedLap - 2][3]),                                                 # Lap Time
                                                            cumTime,                                                                                                # Cumulative Time
                                                            distance - lapData[latestCompletedLap - 2][5],                                                          # Lap Distance
                                                            distance,                                                                                               # Cumulative Distance
                                                            (distance - lapData[latestCompletedLap - 2][5]) * 216000 / (clock - lapData[latestCompletedLap - 2][1]) # Average Speed
                                                          ]
                
                # Display
                if execTime % timeLimit == 0 or noLimit:
                    os.system("cls")
                    
                    print("Execution Time:\t\t" + str(execTime) + "\t\tRace Clock:\t\t" + str(clock) + "\t\tFrames Lost:\t" + str(clock - execTime))
                    print("Current Lap:\t\t" + str(currentLap) + "/50\t\tRace Completion:\t" + precision(raceComp, 3))
                    print("Speed:\t\t\t" + precision(abs(speed), 2) + speedText + "\tAverage Speed:\t\t" + precision(avgSpeed, 2) + "km/h")
                    print("Total distance:\t\t" + precision(distance, 3) + "km")
                    print("Position:\t\t" + posTexts[pos - 1])
                    print("Star Time:\t\t" + frames_to_short_time(starTime) + "\tMega Time:\t\t" + frames_to_short_time(megaTime))
                    print("Shocked Time:\t\t" + frames_to_short_time(shockedTime) + "\tSquished Time:\t\t" + frames_to_short_time(squishTime))
                    print("Bullet Time:\t\t" + frames_to_short_time(bulletTime) + "\tThundercloud Time:\t" + frames_to_short_time(tcTime))
                    print("Air Time:\t\t" + frames_to_short_time(airTime))
                    print("Current Item:\t\t" + str(currentItemCount) + "× " + itemTexts[currentItem])
                    print("Tricks Count:\t\t" + str(tricksCount) + "\t\tMiniturbo Count:\t" + str(mtCount + smtCount) + " (" + str(mtCount) + " + " + str(smtCount) + ")")
                    
                    print("")
                    
                    print_pos_tracker(posTimes, execTime)
                    print_item_counts(itemCounts)
                    print_lap_data(lapData)
                    
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
            
            if cumFinish != 0:
                time.sleep(1)
                os.system("cls")
                
                print("Execution Time:\t\t" + str(execTime) + "\t\tRace Clock:\t\t" + str(clock) + "\t\tFrames Lost:\t" + str(clock - execTime))
                print("Current Lap:\t\t" + str(currentLap) + "/50\t\tRace Completion:\t" + precision(raceComp, 3))
                print("Speed:\t\t\t" + precision(abs(speed), 2) + speedText + "\tAverage Speed:\t\t" + precision(avgSpeed, 2) + "km/h")
                print("Total distance:\t\t" + precision(distance, 3) + "km")
                print("Position:\t\t" + posTexts[pos - 1])
                print("Star Time:\t\t" + str(starTime) + "\t\tMega Time:\t\t" + str(megaTime))
                print("Shocked Time:\t\t" + str(shockedTime) + "\t\tSquished Time:\t\t" + str(squishTime))
                print("Bullet Time:\t\t" + str(bulletTime) + "\t\tThundercloud Time:\t" + str(tcTime))
                print("Current Item:\t\t" + str(currentItemCount) + "× " + itemTexts[currentItem])
                print("Tricks Count:\t\t" + str(tricksCount))
                
                print("")
                
                print_pos_tracker(posTimes, execTime)
                print_item_counts(itemCounts)
                print_lap_data(lapData)
                
                print("\n\n\n\n\n\n\n\n\n\n\n\n\n")
         
        else:
            if localClock % 100000 == 0:
                os.system("cls")
                print("Waiting for a race to start!")
            oldClock = 0
            execTime = 0
            previousRaceComp = 0
            distance = 0
            reversing = False
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
            
if __name__ == '__main__':
    main()