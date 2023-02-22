from PIL import Image, ImageGrab
import cv2
import numpy as np
from tesserocr import PyTessBaseAPI, PSM
import pyautogui
import time
import csv

csvDict = {}

with open("effects.csv", "r", newline="") as effectscsv:
    fileReader = csv.reader(effectscsv, delimiter=",")
    for i in fileReader:
        csvDict[i[0]] = int(i[1])

numeralsToNumbers = {
    "": 0,
    "I": 1,
    "II": 2,
    "III": 3,
    "IV": 4,
    "V": 5,
    "VI": 6,
    "VII": 7,
    "VIII": 8,
    "IX": 9,
    "X": 10
}

problemEffects = {
    1: "MP recovery rate with",
    2: "Enemy weakness physical",
    3: "Afflicted enemy: break",
    4: "Afflicted enemy: physical",
    5: "Afflicted enemy: magic",
    6: "During lightbringer: break",
    7: "Enemy weakness break",
    8: "Charge time reduction: Whi",
    9: "Ailment buildup when",
    10: "Damage Dealt: Swo",
    11: "Damage Dealt: Gre",
    12: "Damage Dealt: Lan",
    13: "Damage Dealt: Kat",
    14: "Damage Dealt: Dag",
    15: "Damage Dealt: Knu",
    16: "Buff Duration: Meikyo",
    17: "MP Cost: Meikyo",
    18: "Improved Effect: Meikyo",
    19: "Charge Time Reduction: lai",
    20: "Damage Dealt: lai",
    21: "MP Cost: lai",
    22: "Charge Time Reduction: Lance Hull"
}

problemEffectsFull = {
    1: "MP Recovery Rate with Normal Attacks",
    2: "Enemy Weakness Physical Break Damage Dealt",
    3: "Afflicted Enemy: Break Damage Dealt",
    4: "Afflicted Enemy: Physical Damage Dealt",
    5: "Afflicted Enemy: Magic Damage Dealt",
    6: "During Lightbringer: Break Damage Dealt",
    7: "Enemy Weakness Break Damage Dealt",
    8: "Charge Time Reduction: White Magic",
    9: "Ailment Buildup When Damaged: Runic",
    10: "Damage Dealt: Sword: Combo Ability",
    11: "Damage Dealt: Greatsword: Combo Ability",
    12: "Damage Dealt: Lance: Combo Ability",
    13: "Damage Dealt: Katana: Combo Ability",
    14: "Damage Dealt: Dagger: Combo Ability",
    15: "Damage Dealt: Knuckles: Combo Ability",
    16: "Buff Duration: Meikyo-Shisui",
    17: "MP Cost: Meikyo-Shisui",
    18: "Improved Effect: Meikyo-Shisui",
    19: "Charge Time Reduction: Iai-Giri",
    20: "Damage Dealt: Iai-Giri",
    21: "MP Cost: Iai-Giri",
    22: "Charge Time Reduction: Lance Hurl"
}


time.sleep(7) #make longer - 10s or so

latency = 0.05

affinityPoints = (471, 304, 528, 329)
effectsPoints = (642, 603, 948, 830)

textLeft = 85
textTop = [3]
textWidth = 514
textHeight = 69

for row in range(1,6):
    textTop.append(textTop[0] + (textTop[0] + textHeight)*(row))

#upper = Top + (Top + Height)*row (where row is 0-5)
#left = Left
#lower = Top + Height
#right = Left + Width

symbolLeft = 14
symbolTop = [2]
symbolWidth = 72
symbolHeight = 70

for row in range(1,6):
    symbolTop.append(symbolTop[0] + (symbolTop[0] + symbolHeight)*(row))

colourTop = [2]
colourHeight = 36

for row in range(1,6):
    colourTop.append(colourTop[0] + (colourHeight*row))

problemClips = []
problemIndex = 0


#items = ["item1.png","item2.png","item3.png","item4.png","item5.png","item6.png","item7.png","item8.png","item9.png","item10.png","item11.png","item12.png","item13.png","item14.png","item15.png","item16.png","item17.png"]
#items = ["item17.png"]
#items = ["test.png"]

def ds4Input(keyPress):
    pyautogui.keyDown(keyPress)
    time.sleep(0.1) #so that inputs last long enough to register
    pyautogui.keyUp(keyPress)

def PullGreyscaleImage(points):
    image = ImageGrab.grab(bbox = points) #image grab
    image = np.array(image)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.bitwise_not(image)
    image = cv2.resize(image ,None, fx=2, fy=2, interpolation = cv2.INTER_CUBIC)
    image = Image.fromarray(image)
    return image
    
def FindInventoryLength():
    #press R3 twice (sort by affinity from new)
    ds4Input("f")
    time.sleep(latency)
    ds4Input("f")
    time.sleep(latency)
    pages = 1
    increments = 0
    with PyTessBaseAPI(psm=PSM.SINGLE_WORD) as api:
        api.SetVariable("tessedit_char_whitelist","1234567890%")
        affinity = PullGreyscaleImage(affinityPoints)
        api.SetImage(affinity)
        affinityPrevious = int(api.GetUTF8Text().replace("%","")) #Set initial affinity for page scroll
        #Press down on D-Pad 2x
        ds4Input("4")
        time.sleep(latency)
        ds4Input("4")
        time.sleep(latency)
        #Press right on D-Pad
        ds4Input("3")
        time.sleep(latency)
        while True:
            affinity = PullGreyscaleImage(affinityPoints)
            api.SetImage(affinity)
            affinityCurrent = int(api.GetUTF8Text().replace("%",""))
            print(affinityCurrent, ">", affinityPrevious)
            if affinityCurrent > affinityPrevious:
                pages = pages - 2
                break
            else:
                affinityPrevious = affinityCurrent #Set current as previous and move onto next number
                pages += 1
                #press right on D-Pad
                ds4Input("3")
                time.sleep(latency)
        #Press down on D-Pad 2x
        time.sleep(latency)
        for page in range(pages):
            #Press right on D-Pad
            ds4Input("3")
            time.sleep(latency)
        affinity = PullGreyscaleImage(affinityPoints)
        api.SetImage(affinity)
        affinityPrevious = int(api.GetUTF8Text().replace("%","")) #Set initial affinity for incremental scroll
        time.sleep(latency)
        while True:
            affinity = PullGreyscaleImage(affinityPoints)
            api.SetImage(affinity)
            affinityCurrent = int(api.GetUTF8Text().replace("%",""))
            if affinityCurrent > affinityPrevious:
                itemTotal = increments + (pages * 19)
                print("Item total:", itemTotal)
                break
            else:
                affinityPrevious = affinityCurrent #Set current as previous and move onto next number
                increments += 1
                #press down on D-Pad
                ds4Input("4")
                time.sleep(latency)
        #Press R3 four times
        ds4Input("f")
        time.sleep(latency)
        ds4Input("f")
        time.sleep(latency)
        ds4Input("f")
        time.sleep(latency)
        ds4Input("f")
        time.sleep(latency)
        return itemTotal
        #affinity = np.array(affinity)
        #affinityCorrected = cv2.cvtColor(affinity, cv2.COLOR_RGB2BGR)
        #cv2.imshow("Chaos?", affinityCorrected)



def ReadImageLoop():
    global problemIndex
    with PyTessBaseAPI(psm=PSM.SINGLE_LINE) as api2:
        kernel = np.ones((8,8),np.uint8)
        for item in range(inventoryLength):
            keep = False
            #print("Item",item)
            effects = PullGreyscaleImage(effectsPoints)
            colours = np.array(ImageGrab.grab(bbox = (667,604,669,790))) #image grab
            colours = cv2.blur(colours,(3,3))
            symbols = effects.crop(box = (symbolLeft, symbolTop[0], symbolLeft+symbolWidth, symbolTop[5]+symbolHeight))
            symbols = np.array(symbols)
            symbols = cv2.medianBlur(symbols,3)
            #structure = cv2.threshold(symbols,20,255,cv2.THRESH_BINARY_INV)[1]
            #structure = cv2.dilate(structure, kernel, iterations=2)
            symbols = cv2.threshold(symbols,50,255,cv2.THRESH_BINARY)[1]
            symbols = cv2.medianBlur(symbols,3)
            effects = np.array(effects)
            effects = cv2.medianBlur(effects,3)
            effects = Image.fromarray(effects)
            for row in range(6):
                numeral = []
                scanned = False
                vFound = False
                symbolColour = colours[colourTop[row],:][:,0].sum()/2
                topLine = np.array(symbols[symbolTop[row] + 22,:])
                middleLine = np.array(symbols[symbolTop[row] + 32,:])
                bottomLine = np.array(symbols[symbolTop[row] + 42,:])
                #structureLine = np.array(structure[symbolTop[row] + 32,:])
                i = 0
                #print(str(symbolColour))
                if symbolColour < 20:
                    numeral = ""
                else:
                    while(i < symbolWidth):
                        if topLine[i] == 0 and scanned == False:
                            scanned = True
                            if middleLine[i-2:i+3].sum() < 1275 and bottomLine[i-2:i+3].sum() < 1275:
                                numeral.append("I")
                            elif vFound == False and bottomLine[i-2:i+3].sum() == 1275:
                                numeral.append("V")
                                vFound = True
                            elif vFound == False:
                                numeral.append("X")
                                vFound = True
                                break
                        if topLine[i] == 255 and scanned == True:
                            scanned = False
                        i += 1
                numeral = "".join(numeral)
                if numeral == "":
                    clipping = effects.crop(box = (textLeft - symbolWidth, textTop[row], textLeft + textWidth, textTop[row]+ textHeight))
                else:
                    clipping = effects.crop(box = (textLeft, textTop[row], textLeft + textWidth, textTop[row] + textHeight))
                #clipping2 = symbols.crop(box = (0, 72*row, 69, (72*row)+72))
                #clipping = screenshot.crop(box = (effectsLeft, effectsTop[row], effectsLeft + effectsWidth, effectsTop[row] + effectsHeight))
                api2.SetImage(clipping)
                text = api2.GetUTF8Text().strip()
                text = text.replace(";",":").replace(".","")
                numeral = numeralsToNumbers[numeral]
                try:
                    if numeral < csvDict[text]:
                        pass
                    else:
                        keep = True
                        #print("keep", text, numeral)
                except:
                    try:
                        if text[0:7] == "Enables":
                            print(text, "ignored")
                            pass
                        else:
                            replaced = False
                            for line in range(len(problemEffects)):
                                if text[0:len(problemEffects[line+1])].lower() == problemEffects[line+1].lower():
                                    text = problemEffectsFull[line+1]
                                    replaced = True
                                    if numeral < csvDict[text]:
                                        #print("Entry -", text, "- corrected")
                                        break
                                    else:
                                        keep = True
                                        #print("Entry -", text, "- corrected")
                                        break
                            #if replaced == False:
                                #print("End of for loop reached -", text, "- not replaced")
                    except:
                        print(text, "- error during problemEffects dict check")
                    else:
                        confidence = api2.AllWordConfidences()
                        if len(confidence) == 0:
                            #clipping = np.array(clipping)
                            #cv2.putText(clipping, "Nothing detected" + "   (row " + str(row+1) + ")", (6,64), cv2.FONT_HERSHEY_PLAIN, 1.5, 0, 1)
                            #problemClips.append(clipping)
                            #problemIndex += 1
                            print("Nothing detected")
                        #elif (sum(confidence)/len(confidence)) < 80:
                            #print(text, "- bad confidence of ", sum(confidence)/len(confidence))
                        elif text not in csvDict and len(text) > 4 and text[0:7] != "Enables":
                            print(text, "- still not found after dictionary check (kept) - row", row+1, "with confidence: ", sum(confidence)/len(confidence))
                            if problemIndex < 100:
                                clipping = np.array(clipping)
                                cv2.putText(clipping, text + "  (row " + str(row+1) + ", conf " + str(sum(confidence)/len(confidence)) + ", index " + str(problemIndex) + ")", (6,64), cv2.FONT_HERSHEY_PLAIN, 1, 0, 1)
                                problemClips.append(clipping)
                                problemIndex += 1
                            keep = True
                #api2.Recognize()
                #text = api2.AllWords()
                #confid = api2.AllWordConfidences()
                #print(text)
                #print(" ".join(text))
                #print(confid)
            if keep == False:
                ds4Input("E")
                #time.sleep(latency)
            ds4Input("4")
            keep = False
            time.sleep(latency)
        for img in range (0,problemIndex):
            cv2.imshow("Chaos?", problemClips[img])
            cv2.waitKey(0)
        #screenshot = np.array(screenshot)
        #screenshotCorrected = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
        #cv2.imshow("Chaos?", screenshotCorrected)
        #symbolsCorrected = cv2.cvtColor(symbols, cv2.COLOR_RGB2BGR)
        #cv2.imshow("Chaos?", symbolsCorrected)
        #clipping = np.array(clipping)
        #clippingCorrected = cv2.cvtColor(clipping, cv2.COLOR_RGB2BGR)
        #cv2.imshow("Chaos?", clippingCorrected)

inventoryLength = FindInventoryLength()

#ReadImageLoop()

