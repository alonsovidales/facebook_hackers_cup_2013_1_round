#!/usr/bin/env python

import fileinput, itertools, multiprocessing, time

__author__ = "Alonso Vidales"
__email__ = "alonso.vidales@tras2.es"
__date__ = "2013-02-02"

class ScreenImage:
    __debug = False
    __screen = None
    __image = None
    __pixels = None

    def resolve(self):
        # Create the set of rectangles
        rectangles = []
        for pixel in self.__pixels:
            fromX = pixel[0] - self.__image['w'] + 1
            fromY = pixel[1] - self.__image['h'] + 1
            toX = pixel[0]
            toY = pixel[1]

            if fromX < 1:
                fromX = 1
            if fromY < 1:
                fromY = 1

            if toX > (self.__screen['w'] - self.__image['w'] + 1):
                toX = self.__screen['w'] - self.__image['w'] + 1
            if toY > (self.__screen['h'] - self.__image['h'] + 1):
                toY = self.__screen['h'] - self.__image['h'] + 1

            if self.__debug:
                print "Point: %s - From: %s:%s To: %s:%s" % (pixel, fromX, fromY, toX, toY)

            rectangles.append([fromX, fromY, toX, toY])

        validPositions = 0
        if (self.__screen['h'] - self.__image['h'] + 1) < (self.__screen['w'] - self.__image['w'] + 1):
            for row in xrange(1, (self.__screen['h'] - self.__image['h'] + 2)):
                unvalidByRow = set()
                for rectangle in rectangles:
                    if (
                        rectangle[1] <= row and
                        rectangle[3] >= row):
                        #print "Rectangle: %s - %s" % (rectangle, (self.__screen['w'] - self.__image['w'] + 1))
                        if rectangle[2] < (self.__screen['w'] - self.__image['w'] + 1):
                            checkTo = rectangle[2]
                        else:
                            checkTo = (self.__screen['w'] - self.__image['w'] + 1)

                        #print "From: %s To: %s" % (rectangle[0], checkTo + 2)
                        for col in xrange(rectangle[0], checkTo + 1):
                            unvalidByRow.add(col)

                if self.__debug:
                    print "Row: %s - %s" % (row, unvalidByRow)
                validPositions += (self.__screen['w'] - self.__image['w'] + 1) - len(unvalidByRow)
        else:
            for col in xrange(1, (self.__screen['w'] - self.__image['w'] + 2)):
                unvalidByCol = set()
                for rectangle in rectangles:
                    if (
                        rectangle[0] <= col and
                        rectangle[2] >= col):
                        if rectangle[3] < (self.__screen['h'] - self.__image['h'] + 1):
                            checkTo = rectangle[3]
                        else:
                            checkTo = (self.__screen['h'] - self.__image['h'] + 1)

                        for row in xrange(rectangle[1], checkTo + 1):
                            unvalidByCol.add(row)

                if self.__debug:
                    print "Col: %s - %s" % (col, unvalidByCol)
                validPositions += (self.__screen['h'] - self.__image['h'] + 1) - len(unvalidByCol)
            
        return validPositions

    def __init__(self, inLinePos, inW, inH, inP, inQ, inN, inX, inY, inA, inB, inC, inD):
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
            pixels.add("%s:%s" % (pixel['x'] + 1, pixel['y'] + 1))

        self.__pixels = []
        for pixel in pixels:
            pos = map(int, pixel.split(':'))
            self.__pixels.append(pos)


        if self.__debug:
            print "Screen: %s" % (self.__screen)
            print "Image: %s" % (self.__image)
            print "Pixels: %s" % (self.__pixels)

        print "Case #%s: %s" % (inLinePos, self.resolve())

if __name__ == "__main__":
    lines = [line.replace('\n', '') for line in fileinput.input()]
    cpus = multiprocessing.cpu_count()

    for linePos in xrange(1, int(lines[0]) + 1):
        info = map(int, lines[linePos].split())
        p = multiprocessing.Process(target = ScreenImage, args = (linePos, info[0], info[1], info[2], info[3], info[4], info[5], info[6], info[7], info[8], info[9], info[10]))
        p.start()

        while len(multiprocessing.active_children()) >= cpus:
            time.sleep(0.1)
