from dungeon_generator import getEntrance
from getch import getch
import time

def printBattlefield(img, img2, width, height):
    final_image = []
    image = img.split("\n")
    image2 = img2.split("\n")
    if len(image) > height:
        return ["BAD IMAGE SPLIT"] * height
    if len(image2) > height:
        return ["BAD IMAGE2 SPLIT"] * height
    if len(image) < height:
        for i in range(height - len(image)): image.insert(0, "|")
    if len(image2) < height:
        for i in range(height - len(image2)): image2.append("|")
    for i in range(height):
        final_image.append(image[i] + " " * (width + 1 - len(image[i]) - len(image2[i])) + image2[i]) 

    for line in final_image:
        print line


def printMessageBox(message):
    print "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"
    msg = message.split("\n")
    for i in range(min(8, len(msg))):
        print "| {:80s}                                                                                |".format(msg[i])
    if len(msg) < 8:
        for i in range(8 - len(msg)):
            print "| {:80s}                                                                                |".format("")
    print "- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"

def printHelpScreen():
    for i in range(45):
        print
    print "HELP SCREEN:"
    print "Movement: WASD"
    print "Battle:"
    print "\tx - Attack"
    print "\tc - Raise Shield"
    print "\ti - Use Potion"
    print "\tv - Begin Switching Weapons"
    print "\t\t< - Select Left Hand (while switching weapons)"
    print "\t\t>  - Select Right Hand (while switching weapons)"
    print "\t\t\t Finally, press any number key to select a weapons slot to use."
    print; print; print
    print "That's not a valid command! ('h' for help) ",

def entranceAnimation():
    outside = getEntrance()
    for line in outside:
        print ''.join(line)
    print "Press [ENTER] to begin your adventure..."
    getch()
    player_x = 30
    player_y = 79
    old = outside[player_x][player_y]
    outside[player_x][player_y] = 'X'
    for line in outside:
        print ''.join(line)
    time.sleep(.5)
    while (player_x > 14):
        outside[player_x][player_y] = old
        player_x -= 1
        old = outside[player_x][player_y]
        outside[player_x][player_y] = 'X'
        for line in outside:
            print ''.join(line)
        time.sleep(.25)
    time.sleep(1)
    for i in range(22):
        print
    print " " * 70 + "Begin"
    for i in range(22):
        print
    time.sleep(2)
