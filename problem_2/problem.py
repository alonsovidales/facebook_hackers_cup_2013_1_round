#!/usr/bin/env python

import fileinput, re, itertools

__author__ = "Alonso Vidales"
__email__ = "alonso.vidales@tras2.es"
__date__ = "2013-02-02"

class Secutiry:
    __debug = False
    __validChars = set(['a', 'b', 'c', 'd', 'e', 'f', '?'])

    def __splitByLength(self, string, size):
        w = []
        n = len(string)
        for i in range(0, n, size):
            w.append([string[i:i + size], list(string[i:i + size])])

        return w

    def __checkMatches(self, inStr1, inStr2):
        possibleStr = ''

        for charPos in xrange(0, len(inStr1)):
            if inStr1[charPos] not in self.__validChars or inStr2[charPos] not in self.__validChars:
                return False

            if inStr1[charPos] == inStr2[charPos]:
                if inStr1[charPos] == '?':
                    possibleStr += 'a'
                else:
                    possibleStr += inStr1[charPos]
            elif inStr1[charPos] == '?':
                possibleStr += inStr2[charPos]
            elif inStr2[charPos] == '?':
                possibleStr += inStr1[charPos]
            else:
                return False

        return possibleStr

    def __searchPossibleString(self, inK1Sections, inK2SectionCounter, inPossibles, inCurrentStr = '', inPos = 0):
        if len(inK1Sections) == 0:
            return inCurrentStr

        if self.__debug:
            print "inK1Sections: %s" % (inK1Sections)
            print "inK2SectionCounter: %s" % (inK2SectionCounter)
            print "CurrentStr: %s" % (inCurrentStr)

        for k2Section, possible in inPossibles["%s_%s" % (inK1Sections[0][0], inPos)]:
            #print "Checking if %s" % (k2Section)
            if inK2SectionCounter[k2Section] > 0:
                auxK2SectionCounter = inK2SectionCounter.copy()
                auxK2SectionCounter[k2Section] -= 1
                auxK1Sections = inK1Sections[1:]

                #print auxK2SectionCounter
                #print inCurrentStr + possible

                possbleStr = self.__searchPossibleString(auxK1Sections, auxK2SectionCounter, inPossibles, inCurrentStr + possible, inPos + 1)
                if possbleStr <> False:
                    return possbleStr

        return False

    def resolve(self):
        # Divide the string in sections

        self.__k1 = self.__k1.replace('?', '?')
        self.__k2 = self.__k2.replace('?', '?')

        k1Sections = self.__splitByLength(self.__k1, len(self.__k1) / self.__sections)
        k2Sections = self.__splitByLength(self.__k2, len(self.__k2) / self.__sections)

        k2SectionCounter = {}
        for k2Section in k2Sections:
            if k2Section[0] in k2SectionCounter:
                k2SectionCounter[k2Section[0]] += 1
            else:
                k2SectionCounter[k2Section[0]] = 1

        if self.__debug:
            print "K1 Sections: %s" % (k1Sections)
            print "K2 Sections: %s" % (k2Sections)

        possibles = {}
        pos = 0
        #usageBySet = {}
        for section1 in k1Sections:
            possible = False
            compatibles = 0
            for section2 in k2Sections:
                possibleString = self.__checkMatches(section1[1], section2[1])
                if possibleString <> False:
                    compatibles += 1
                    possible = True
                    if "%s_%s" % (section1[0], pos) in possibles:
                        possibles["%s_%s" % (section1[0], pos)][section2[0]] = possibleString
                    else:
                        possibles["%s_%s" % (section1[0], pos)] = {section2[0]: possibleString}

            if possible == False:
                return "IMPOSSIBLE"
            
            #possibles["%s_%s" % (section1[0], pos)] = sorted(possibles["%s_%s" % (section1[0], pos)].items())
            possibles["%s_%s" % (section1[0], pos)] = sorted(possibles["%s_%s" % (section1[0], pos)].items(), key = lambda values: values[1])
            possibles["%s_%s" % (section1[0], pos)] = sorted(possibles["%s_%s" % (section1[0], pos)], key = lambda values: [x == y for (x, y) in zip(section1[0], values[0])].count(True), reverse = True)

            joinedK2Parts = ':'.join([key for key, value in possibles["%s_%s" % (section1[0], pos)]])

            """if joinedK2Parts in usageBySet:
                usageBySet[joinedK2Parts]['times'] += 1
                if usageBySet[joinedK2Parts]['times'] > usageBySet[joinedK2Parts]['len']:
                    return "IMPOSSIBLE"
            else:
                #print compatibles
                usageBySet[joinedK2Parts] = {
                    'times': 1,
                    'len': compatibles
                }"""

            pos += 1

        #print possibles

        #print [[possibleKey, len(possibleValues)] for possibleKey, possibleValues in possibles.items()]

        if self.__debug:
            print possibles

        possible = self.__searchPossibleString(k1Sections, k2SectionCounter, possibles)

        #print possible

        if possible == False:
            return "IMPOSSIBLE"

        return possible

    def __init__(self, inSections, k1, k2):
        self.__possibleStrings = []
        self.__sections = inSections
        self.__k1 = k1
        self.__k2 = k2

        if self.__debug:
            print "Sections: %s - Key1: %s - Key2: %s" % (self.__sections, self.__k1, self.__k2)
        

if __name__ == "__main__":
    lines = [line.replace('\n', '') for line in fileinput.input()]

    for test in xrange(0, int(lines[0])):
        print "Case #%s: %s" % (test + 1, Secutiry(int(lines[(test * 3) + 1]), lines[(test * 3) + 2], lines[(test * 3) + 3]).resolve())
