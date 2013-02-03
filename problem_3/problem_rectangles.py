#!/usr/bin/env python

import fileinput, itertools

__author__ = "Alonso Vidales"
__email__ = "alonso.vidales@tras2.es"
__date__ = "2013-02-02"

class ScreenImage:
    __debug = False
    __screen = None
    __image = None
    __pixels = None

    def __pointInRectangle(self, inX, inY, inRectangle):
        return inX >= inRectangle[0] and inX <= inRectangle[2] and inY >= inRectangle[1] and inY <= inRectangle[3]


    def __getRectIntersection(self, inRect1, inRect2):
        if (self.__pointInRectangle(inRect1[0], inRect1[1], inRect2) or
            self.__pointInRectangle(inRect1[2], inRect1[3], inRect2) or
            self.__pointInRectangle(inRect1[0], inRect1[3], inRect2) or
            self.__pointInRectangle(inRect1[2], inRect1[1], inRect2) or

            self.__pointInRectangle(inRect2[0], inRect2[1], inRect1) or
            self.__pointInRectangle(inRect2[2], inRect2[3], inRect1) or
            self.__pointInRectangle(inRect2[0], inRect2[3], inRect1) or
            self.__pointInRectangle(inRect2[2], inRect2[1], inRect1)):

            xEdges = sorted([inRect1[0], inRect1[2], inRect2[0], inRect2[2]])
            yEdges = sorted([inRect1[1], inRect1[3], inRect2[1], inRect2[3]])

            return (xEdges[2] - xEdges[1] + 1) * (yEdges[2] - yEdges[1] + 1)

        return 0

    def __getTotalArea(self, inRects):
        #print self.__pointInRectangle(3, 4, [0, 0, 6, 6])
        #print self.__getRectIntersection([3, 3, 6, 6], [4, 4, 7, 7])
        #print self.__getRectIntersection([3, 3, 6, 6], [6, 4, 7, 7])
        #exit()

        totalArea = 0

        for rect in inRects:
            totalArea += (rect[2] - rect[0] + 1) * (rect[3] - rect[1] + 1)

        print totalArea

        for rects in itertools.combinations(inRects, 2):
            print "%s - %s" % (rects, self.__getRectIntersection(rects[0], rects[1]))
            totalArea -= self.__getRectIntersection(rects[0], rects[1])
            print totalArea

        return totalArea

    def resolve(self):
        print self.__getTotalArea([[1, 1, 3, 3], [2, 2, 4, 4], [3, 0, 5, 2]])
        exit()

        possiblePositions = (self.__screen['h'] - self.__image['h'] + 1) * (self.__screen['w'] - self.__image['w'] + 1)
        setUnvalidPoints = set()

        # Create the set of rectangles
        rectangles = []
        for pixel in self.__pixels:
            fromX = pixel[0] - self.__image['w'] + 1
            fromY = pixel[1] - self.__image['h'] + 1
            toX = pixel[0]
            toY = pixel[1]

            if fromX < 0:
                fromX = 0
            if fromY < 0:
                fromY = 0
            if toX > (self.__screen['w'] - self.__image['w']):
                toX = self.__screen['w'] - self.__image['w']
            if toY > (self.__screen['h'] - self.__image['h']):
                toY = self.__screen['h'] - self.__image['h']

            if self.__debug:
                print "Point: %s - From: %s:%s To: %s:%s" % (pixel, fromX, fromY, toX, toY)

            rectangles.append([fromX, fromY, toX, toY])

        print self.__getTotalArea(rectangles)
        return possiblePositions - self.__getTotalArea(rectangles)

    def __init__(self, inW, inH, inP, inQ, inN, inX, inY, inA, inB, inC, inD):
        numbers = set([inW, inH, inP, inQ, inX, inY])

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
            numbers.add(pixel['x'])
            numbers.add(pixel['y'])
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
