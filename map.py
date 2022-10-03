
# used to split lists into chunks
def divide_chunks(l, n):
     
    # looping till length l
    for i in range(0, len(l), n):
        yield l[i:i + n]

#neccisary for geocoder to run, idk why
if __name__ == '__main__':
    # allows program to check if a coordinate is in the US
    import reverse_geocoder

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
    DISPLAY = pygame.display.set_mode((infoObject.current_w, infoObject.current_h - 60), 0, 32)
    pygame.display.set_caption('Coaster Map')
    DISPLAY.fill(WHITE)

    #List of every pixel/coord on screen
    coordsList = []

    #populating list
    for i in range(infoObject.current_w):
        for j in range(infoObject.current_h - 60):

            #allows user to quit if program is taking to long
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()

            #translating pixels to coordinates
            long = (j * (25/(infoObject.current_h - 60))) + 25
            lat = (i * (59/infoObject.current_w)) + 66

            coordsList.append([i,j,lat,long,0])

    #formating to input into reverse geocoder
    rgInput = []
    rgChunk = []
    counter = 1800
    print(coordsList[20000])
    time.sleep(100)
    for i in coordsList:
        if counter <= 0:
            rgInput.append(rgChunk)
            rgChunk = []
            counter = 1800
        counter -=1
        rgChunk.append((i[2],i[3]))


    #adds extra variable to the coordinate tuple that defines its color based off of wether or not its in the US
    results =[]
    counter = 0
    for i in rgInput:
        #allows user to quit if program is taking to long
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        resultChunk = reverse_geocoder.search(i)
        results = results + resultChunk

        counter +=1
        print(str((int((counter/len(rgInput)) * 100)))+ "% done")


    for i in range(len(results)):
        if(results[i]['cc'] == "US"):
            coordsList[i][4] = 1
        else:
            coordsList[i][4] = 0

    #creates display
    counter = 0
    for i in coordsList:
        if i[4] == 1:
            pygame.draw.rect(DISPLAY,(0,0,0),(i[1],i[2],1,1))
            pygame.display.update()
            print(i)
            counter += 1
            print(counter)

    print('done')

    while(True):

        #allows user to quit if program is taking to long
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        pygame.display.update()
