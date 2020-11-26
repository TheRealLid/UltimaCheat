import time


#  Offset stored as an int. Used in
OFFSET = {"STR": int(0x0E), "INT": int(0x10), "DEX": int(0x0F), "MAGIC": int(0x11), "HP": int(0x12),
          "HM": int(0x14), "EXP": int(0x16), "GOLD": int(0x204), "KEY": int(0x206), "GEMS": int(0x207),
          "SKULLKEY": int(0x20B), "BLACKBADGE": int(0x218), "MAGICCARPET": int(0x20A), "MAGICAXE": int(0x240)}

#  The max amount of an item/stat you can have within the game
MAXVAL = {"STR": int(99), "INT": int(99), "DEX": int(99), "MAGIC": int(99), "HP": int(999), "HM": int(999),
          "EXP": int(9999), "GOLD": int(9999), "KEY": int(100), "GEMS": int(100), "SKULLKEY": int(100),
          "BLACKBADGE": int(1), "MAGICCARPET": int(99), "MAGICAXE": int(100)}

OPTIONS = ["STR", "INT", "DEX", "MAGIC", "HP", "HM", "EXP", "GOLD", "KEY", "SKULLKEY", "GEMS", "BLACKBADGE",
           "MAGICCARPET", "MAGICAXE"]

CHARACTERS = ["Player Charcter", "Shamino", "Iolo", "Mariah", "Geoffrey", "Jaana", "Julia", "Dupre", "Katrina", "Sentri", "Gwenno",
              "Johne", "Johne", "Gorn", "Maxewell", "Toshi", "Saduj"]


#  opens the save.gam file, converts the content, and puts it into data
def read_save(filePath):
    with open(filePath, "rb") as save:
        data = list(bytearray(save.read()))
        save.close()
        return data


#  writes the changes back into the save.gam file
def write_save(data, filePath):
    with open(filePath, "wb") as save:
        save.write(bytearray(data))
        save.close()


#  Makes all stats max and gives max amount of all items within program
def pown3d_mode(data):
    i = 0
    while i < len(OPTIONS):
        if i < 7:
            j = 0
            for j in range(16):
                change_data(data, OPTIONS[i], str(MAXVAL[OPTIONS[i]]), j)
                time.sleep(0.01)
        else:
            change_data(data, OPTIONS[i], str(MAXVAL[OPTIONS[i]]), 0)
        i += 1
        time.sleep(0.01)


#  changes the hex values within save.gam
def change_data(data, statName, newVal, character):
    #  gets the index for the desired attribute from offset dictionary
    stateName = statName.upper()
    index = OFFSET[statName]
    if character > 0:
        index = index + (int(0x20) * character)
    #  validates user input is within acceptable parameters
    while int(newVal) > MAXVAL[statName] or int(newVal) < 0:
        newVal = input("\n Must enter a value within the range of (0-" + str(MAXVAL[statName]) + ")")
    #  checks if the attribute is 2 bytes
    if MAXVAL[statName] > 255:
        needsPadBit = False
        #  converts the new value into hex
        hNewStatVal = hex(int(newVal))
        temp = hNewStatVal
        #  checks if there is an odd amount of digits
        #  With odd digits we need to pad the hex value
        if len(hNewStatVal) % 2 != 0:
            needsPadBit = True
        # reorders the hex value because ULTIMA_5 uses little endian
        hNewStatVal = hNewStatVal[len(hNewStatVal) - 2] + hNewStatVal[len(hNewStatVal) - 1]
        if needsPadBit:
            hNewStatVal += "0"
            hNewStatVal += temp[2]
        else:
            hNewStatVal += temp[2] + temp[3]
        print("changing " + statName + " from " + str(int(hNewStatVal[2:] + hNewStatVal[:2], 16)) + " to " + newVal)
        if stateName in OPTIONS[4:7]:
            print("for character: " + CHARACTERS[character])
        #  updates the values in the data array
        data[index] = int(hNewStatVal[0] + hNewStatVal[1], 16)
        data[index + 1] = int(hNewStatVal[2] + hNewStatVal[3], 16)
    else:
        print("changing " + statName + " from " + str(data[index]) + " to " + newVal)
        if stateName in OPTIONS[0:4]:
            print("for character: " + CHARACTERS[character])
        #  updates the values in the data array
        data[index] = int(newVal)


#  lets the use select a specific stat or item
def edit_game(data):
    user_input = input("What would you like to change?\nStr\nInt\nDex\nHP\nHM\nEXP\nMagic\nGOLD\nKey"
                       "\nGems\nSkullKey\nBlackBadge\nMagicCarpets\nMagicAxes\n ")
    user_input = user_input.upper()
    character = 0
    if user_input in OPTIONS[:7]:
        character = input("Which character are we modifying the stats of\n0)Player "
                          "Character\n1)Shamino\n2)Iolo\n3)Mariah\n4)Geoffrey\n5)Jaana\n6)Julia\n7)Dupre\n8)Katrina"
                          "\n9)Sentri\n10)Gwenno\n11)Johne\n12)Gorn\n13)Maxewell\n14)Toshi\n15)Saduj")
    newVal = input(" What would you like to change " + user_input + " to (0-" + str(MAXVAL[user_input]) + ")")
    change_data(data, user_input, newVal, int(character))


if __name__ == '__main__':
    #filePath = "C:/DOSGames/Ultima_5/SAVED.GAM"
    filePath = input("Please enter the file path of our Ultima_5 save file you wish to modify, "
                     "EX C:/DOSGames/Ultima_5/SAVED.GAM\n")
    saveFile = read_save(filePath)
    user_input = -1
    while user_input != 0:
        user_input = int(input("Enter 1 to make edits,Enter 2 to use pown3d mode(gives max everything). Enter 0 to "
                               "save changes\n"))
        if user_input == 1:
            edit_game(saveFile)
        if user_input == 2:
            pown3d_mode(saveFile)
    write_save(saveFile, filePath)
    # STILL NEED TO ADD OTHER CHARACTER STATS CHANGE
    # This should be easy by adding their offset to the offset of the original character
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
