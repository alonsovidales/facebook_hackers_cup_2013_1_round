#!/usr/bin/env python

import fileinput, re, itertools

__author__ = "Alonso Vidales"
__email__ = "alonso.vidales@tras2.es"
__date__ = "2013-02-02"

class ScreenImage:
    __debug = True
    __screen = None
    __image = None
    __pixels = None

    def resolve(self):
        
        return ""


    def __init__(self, inW, inH, inP, inQ, inN, inX, inY, inA, inB, inC, inD):
        self.__screen = {
            'w': inW,
            'h': inH
        }

        self.__image = {
            'w': inP,
            'h': inQ
        }

        auxPixels = [{
            'x': inX,
            'y': inY
        }]

        for pixel in xrange(1, inN):
            auxPixels.append({
                'x':  (auxPixels[pixel - 1]['x'] * inA + auxPixels[pixel - 1]['y'] * inB + 1) % inW,
                'y': (auxPixels[pixel - 1]['x'] * inC + auxPixels[pixel - 1]['y'] * inD + 1) % inH
            })

        # Remove the duplicated pixels
        pixels = set()
        for pixel in auxPixels:
            pixels.add("%s:%s" % (pixel['x'], pixel['y']))

        self.__pixels = []
        for pixel in pixels:
            pos = map(int, pixel.split(':'))
            self.__pixels.append(pos)

        if self.__debug:
            print "Screen: %s" % (self.__screen)
            print "Image: %s" % (self.__image)
            print "Pixels: %s" % (self.__pixels)

if __name__ == "__main__":
    lines = [line.replace('\n', '') for line in fileinput.input()]

    for linePos in xrange(1, int(lines[0]) + 1):
        info = map(int, lines[linePos].split())
        print "Case #%s: %s" % (linePos, ScreenImage(info[0], info[1], info[2], info[3], info[4], info[5], info[6], info[7], info[8], info[9], info[10]).resolve())
