from pydicom import dcmread
import numpy as np 
from datetime import datetime
import sys

class Done(Exception): pass

greenBox = {'left top' : [], 'ritgh top': [], 'left bottom': [], 'right bottom': []}

slicesValues = []
noisySlices = []
colorValue = {}

###########################################################################################
def createCollorValueDic():
    print("strting createCollorValueDic()")
    q = 325
    try:
        for y in range(len(film[0][0])):
            for x in range(len(film[0])):
                if((film[0][x][y][0] == 255 and film[0][x][y][1] == 255 and film[0][x][y][2] == 0) or q != 325):
                    q = q - 1
                    if(film[0][x][y][0] == 0 and film[0][x][y][1] == 0 and film[0][x][y][2] == 0):
                        raise Done
                    colorValue[' '.join(str(a) for a in film[0][x][y].tolist())] = q
    except Done:
        pass

###########################################################################################

def findGreenBoxCoordinates():
    print("strting findGreenBoxCoordinates()")
    try:
        greenFound = 0
        for y in range(len(film[0])):
            for x in range(len(film[0][0])):
                if(greenFound == 0 and  ((140 <= film[0][y][x][0] <= 170) and ( 160 <= film[0][y][x][1] <= 190) and (50 <= film[0][y][x][2] <= 70))):
                    greenFound = 1
                if(greenFound == 1):
                    if(len(greenBox['left top']) == 0):
                        greenBox['left top'] = [x,y]
                    if(film[0][y][x+1][0] == 0 and film[0][y][x+1][1] == 0 and film[0][y][x+1][2] == 0):
                        greenBox['ritgh top'] = [x,y]
                        raise Done
    except Done: 
        pass
        
    try:
        for y in range(greenBox['left top'][1], len(film[0])):
            x = greenBox['left top'][0]
            if(film[0][y+1][x][0] == 0 and film[0][y+1][x][1] == 0 and film[0][y+1][x][2] == 0):
                        greenBox['left bottom'] = [x,y]
                        greenBox['right bottom'] = [greenBox['ritgh top'][0], y]
                        raise Done
    except Done:
        pass

###########################################################################################

def createSlicesValue():
    print("strting createSlicesValue()")
    for slice in film:
        slicesValues.append(0)
        for y in range(greenBox['left top'][0], greenBox['right bottom'][0]):
            for x in range(greenBox['left top'][1], greenBox['right bottom'][1]):
                colorKey = ' '.join(str(a) for a in slice[x][y])
                if(colorKey in colorValue.keys()):
                    slicesValues[len(slicesValues)-1] = slicesValues[len(slicesValues)-1] + colorValue[colorKey]

###########################################################################################

def testNoise(threshold = 1000000):
    print("strting testNoise()")
    for sliceValue in slicesValues:
        if(sliceValue < threshold):
            noisySlices.append(0)
        else:
            noisySlices.append(1)


###########################################################################################
def mergeNoisySplices():
    print("strting mergeNoisySplices()")
    howManyWrong = 0
    i = 0 

    lt = greenBox['left top'][1]
    rt = greenBox['right bottom'][1]
    lb = greenBox['left top'][0]
    rb = greenBox['right bottom'][0]

    while i < len(noisySlices):
        if(noisySlices[i] == 1):
            howManyWrong = howManyWrong+1
            if(noisySlices[i+1] == 0 or i+1 == len(noisySlices)):
                print(i, '/', len(noisySlices))
                i += 1
                before = np.array(ds.pixel_array[i-howManyWrong-1])
                after = np.array(ds.pixel_array[i])
                before = before.astype(int)
                after = after.astype(int)
                if(noisySlices[0] == 1 and i-howManyWrong == 0):
                    before = after 
                if(noisySlices[len(noisySlices)-1] == 1 and i == len(noisySlices)):
                    after = before 

                mergedSlice = np.sqrt((((before ** 2) + (after ** 2))/2))
                mergedSlice = mergedSlice.astype(int)
                
                for y in range(lt, rt):
                    for slice in range(i-howManyWrong, i):
                                ds.pixel_array[slice][y][lb:rb] = mergedSlice[y][lb:rb]

                howManyWrong = 0
        i += 1


###########################################################################################

def createNewDICM(outputFile = str(datetime.now().strftime("%Y-%m-%d %H-%M-%S")) +'.dcm'):
    print("strting createNewDICM()")
    ds.PixelData = ds.pixel_array.tobytes()
    ds.save_as(outputFile)
    print("Done")

###########################################################################################





if(__name__ == "__main__"):
    inputFile = sys.argv[1]
    ds = dcmread(inputFile)
    film = np.array(ds.pixel_array)
    createCollorValueDic()
    findGreenBoxCoordinates()
    createSlicesValue()
    testNoise()
    mergeNoisySplices()
    if(len(sys.argv) == 2):
        createNewDICM()
    else:
        outputFile = sys.argv[2]
        createNewDICM(outputFile)