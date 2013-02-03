#!/usr/bin/env python

import fileinput, math

__author__ = "Alonso Vidales"
__email__ = "alonso.vidales@tras2.es"
__date__ = "2013-02-02"

class CardsGame:
    __debug = False


    def __binomialCoef(self, inN, inK):
        """
        Faster implementation of the binomial coeficient algorithm

        @param int <inN>: The number of elemenst
        @param int <inK>: Set of elements on N

        @return float: the result of the binomial coeffient
        """
        if 0 <= inK <= inN:
            ntok = 1

            for t in xrange(min(inK, inN - inK)):
                ntok = ntok * (inN - t) // (t + 1)

            return ntok
        
        return 0

    def resolve(self):
        totalValues = 0

        self.__cards = sorted(self.__cards, reverse = True)
        for cardPos in xrange(0, len(self.__cards)):
            m = len(self.__cards) - cardPos - 1
            n = self.__k - 1

            totalValues += ((self.__cards[cardPos] * self.__binomialCoef(m, n)))

            if m == n:
                break

        return totalValues % 1000000007


    def __init__(self, inK, inCards):
        self.__k = inK
        self.__cards = inCards

        if self.__debug:
            print "K: %s Cards: %s" % (self.__k, self.__cards)


if __name__ == "__main__":
    lines = [line.replace('\n', '') for line in fileinput.input()]

    for problem in xrange(0, int(lines[0])):
        problemInfo = lines[(problem * 2) + 1].split()
        print "Case #%s: %s" % (problem + 1, CardsGame(int(problemInfo[1]),map(int, lines[(problem * 2) + 2].split())).resolve())
