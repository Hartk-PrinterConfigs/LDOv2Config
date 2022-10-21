from codecs import charmap_decode
import PIL
import os
from PIL import Image
import json
from operator import truediv
from matplotlib.cbook import index_of
import sacn
import time
import math
import sys

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

from numpy import asarray
from array import *
width = 16
height = 16
imgs = []

file = sys.argv[1].split("|")[0]
count = int(sys.argv[1].split("|")[1])

#location = __location__+"\\block"
location = __location__+"/"+file
sleepTime = 0.09
loopCount = math.floor(count/sleepTime)

fileCount = 0
for path in os.listdir(location):
    if os.path.isfile(os.path.join(location, path)):
        fileCount += 1


for i in range(fileCount):
    im = Image.open(os.path.join(location,str(i+1)+'.png'))
   #im = Image.open(os.path.join(__location__, sys.argv[1]))
    imgs.append(im)
    


dmxGif = []
for im in imgs:
    channelsPerUniverse = 510
    numOfPixels = width*height
    numOfChannels = numOfPixels * 3
    numOfUniverses = math.ceil(numOfChannels / channelsPerUniverse)
    index = 0
    lIndex = 1
    T = []
    STR = ""

    pixel_values = list(im.getdata())
    pv = []
    if im.format == "BMP" or im.format == None:
        if imgs.index(im) == 0:
            pal = im.palette.colors
        colors = []
        for color in pal:
            colors.append(color)

        if imgs.index(im) > 0:
         for pixel in pixel_values:
            checkVal = (pixel[0],pixel[1],pixel[2])
            if checkVal in colors:
                    pv.append(colors.index(checkVal))
         pixel_values = pv

    universeDmxData = []
    
    if im.format == None:
        data = []
        for i in range(16):
            pvl = pixel_values[i::16]
            data.append(pvl)
    else:
        data = asarray(im)

    data = data[::-1]
    for  x in data:
        if (lIndex % 2) == 0:
            x = x[::-1]

        for k in x:

            if im.format == "BMP" or im.format == None:
                if len(T) < channelsPerUniverse:
                    print(imgs.index(im))
                    color = colors[k]
                    T.append(color[0])
                    T.append(color[1])
                    T.append(color[2])
                else:
                    universeDmxData.append(T)
                    T = []
                    color = colors[k]
                    T.append(color[0])
                    T.append(color[1])
                    T.append(color[2])
            else:
                if len(T) >= channelsPerUniverse:
                    universeDmxData.append(T)
                    T = []
                T.append(int(k[0]))
                T.append(int(k[1]))
                T.append(int(k[2]))
        lIndex += 1
    if len(T) > 0:
        universeDmxData.append(T)
        T = []

        dmxGif.append(universeDmxData)
        S = []
sender = sacn.sACNsender(bind_address='0.0.0.0')
sender.start()
dli = len(dmxGif)
for i in range(loopCount):
    index = i % dli
    dmxData = dmxGif[index]
    for universe in dmxData:
        ui = dmxData.index(universe) + 1
        sender.activate_output(ui)
        sender[ui].destination = "192.168.1.22"
        sender[ui].multicast = False # keep in mind that multicast on windows is a bit 
        dmt = ((universe))
        sender[ui].dmx_data = dmt
    sender.manual_flush = True # turning off the automatic sending of packets
    time.sleep(0.09)
    sender.flush()

sender.manual_flush = False # keep manual flush off as long as possible, because if it is on, the automatic
sender.stop()
sys.exit