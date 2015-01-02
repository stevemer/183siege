
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

