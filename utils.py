
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

