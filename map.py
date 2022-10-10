
# used to split lists into chunks
def divide_chunks(l, n):
     
    # looping till length l
    for i in range(0, len(l), n):
        yield l[i:i + n]

#neccisary for geocoder to run, idk why
if __name__ == '__main__':

    # allows program to check if a coordinate is in the US
    import reverse_geocoder

    #allows for the program to check if a location is on land
    from global_land_mask import globe

    #used for display
    import pygame

    #just in case
    import random
    import math
    import time

    #initializing pygame
    WHITE = (255,255,255)
    pygame.init()

    #finds size of display and creates pygame window
    infoObject = pygame.display.Info()
    width = int(infoObject.current_w/2)
    height = int((infoObject.current_h - 60)/2)
    DISPLAY = pygame.display.set_mode((width, height), 0, 32)
    pygame.display.set_caption('Coaster Map')
    DISPLAY.fill(WHITE)

    #List of every pixel/coord on screen
    coordsList = []

    #populating list
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
    print(coordsList[10])
    #formating to input into reverse geocoder
    rgInput = []
    for i in coordsList:
        rgInput.append((i[2],i[3]))
    print(len(rgInput))
    print(rgInput[10])
    #adds extra variable to the coordinate tuple that defines its color based off of wether or not its in the US
    results = reverse_geocoder.search(rgInput)
    print(len(results))
    print(results[10])
    for i in range(len(results)):
        if(globe.is_land(coordsList[i][2],coordsList[i][3]) and results[i]['cc'] == "US"):
            coordsList[i][4] = 1
        print(str(int((i/len(results))*100)) + "% done")
    #creates display
    print(coordsList[10])
    for i in coordsList:
        if i[4] == 1:
            pygame.draw.rect(DISPLAY,(0,0,0),((-1 * i[0]) + (width),(-1 * i[1]) + (height),1,1))
            pygame.display.update()

    print('done')

    while(True):

        #allows user to quit if program is taking to long
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        pygame.display.update()
