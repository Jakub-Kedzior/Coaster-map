#takes hexadecimal input, returns rgb output
from turtle import xcor


def hex_to_rgb(value):
    value = value.lstrip('#')
    lv = len(value)
    return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

#neccisary for geocoder to run, idk why
if __name__ == '__main__':

    #for math stuff
    import math

    # allows program to check if a coordinate is in the US
    import reverse_geocoder

    #allows for the program to check if a location is on land
    from global_land_mask import globe

    #used for display
    import pygame

    #takes park data and turns it into a 2d array
    import csv
    datafile = open('Locations.csv', 'r')
    datareader = csv.reader(datafile, delimiter=',')
    data = []
    for row in datareader:
        data.append(row)  

    #initializing pygame
    WHITE = (255,255,255)
    pygame.init()

    #finds size of computer display and creates pygame window that is 1/4 the size
    infoObject = pygame.display.Info()
    width = int(infoObject.current_w/2)
    height = int((infoObject.current_h - 60)/2)
    DISPLAY = pygame.display.set_mode((width, height), 0, 32)
    pygame.display.set_caption('Coaster Map')
    DISPLAY.fill(WHITE)

    #List of every pixel/coord on screen
    coordsList = []

    #populating list with every pixel on the display
    for i in range(width):
        for j in range(height):

            #allows user to quit if program is taking to long
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            #translating pixels to coordinates
            lat = (j * (25/(float(height)))) + 25
            long = -1 * ((i * (59/float(width))) + 66)
            coordsList.append([i,j,lat,long,0])

    #formating to input into reverse geocoder by getting rid of everything except for coordinates
    rgInput = []
    for i in coordsList:
        rgInput.append((i[2],i[3]))

    #adds extra variable to the coordList that defines if it is part of the continental US
    results = reverse_geocoder.search(rgInput)
    for i in range(len(results)):
        if(globe.is_land(coordsList[i][2],coordsList[i][3]) and results[i]['cc'] == "US"):
            coordsList[i][4] = 1

    #creates display by iterating through the pixels of the screen and coloring by comparison to the csv
    for i in coordsList:
        if i[4] == 1:
            #iterating through parks to see which one is closest
            color = "#000000"
            closest = 9999999
            for j in data:
                #calculates the distance between the park and pixel, usingthe numhber of coasters as a weight
                distance = (1/float(j[1])) * math.dist((float(j[2]),float(j[3])),(i[2],i[3]))
                if distance < closest:
                    color = j[4]
                    closest = distance
            pygame.draw.rect(DISPLAY,hex_to_rgb(color),((-1 * i[0]) + (width),(-1 * i[1]) + (height),1,1))
            pygame.display.update()

    print('done')

    while(True):
        
        #allows user to quit if program is taking to long
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        (x,y) = pygame.mouse.get_pos()
        x = -x + width
        y = -y + height
        y = (y * (25/(float(height)))) + 25
        x = -1 * ((x * (59/float(width))) + 66)
        name = "none"
        closest = 9999999
        for j in data:
                #calculates the distance between the park and pixel, usingthe numhber of coasters as a weight
                distance = (1/float(j[1])) * math.dist((float(j[2]),float(j[3])),(y,x))
                if distance < closest:
                    name = str(j[0])
                    closest = distance
        
        print(name)
        name = name + ' ' * (60 - len(name))
        text = pygame.font.Font('freesansbold.ttf', 20).render(name, True, (0,0,0), (255,255,255))
 
        textRect = text.get_rect()
        textRect.left = 0
        textRect.bottom = height
        DISPLAY.blit(text, textRect)
        pygame.display.update()
    
