from itertools import product
from numpy import array, dot

class Lattice():
    def __init__(self, latticeVectors, latticeBasis):
        """latticeVectors: cartesian coords.; latticeBasis: lattice coords."""
        self.points = list()
        self.latticeVectors = array(latticeVectors)
        self.latticeBasis = array(latticeBasis)
        self.dimension = len(latticeVectors)
        self.translations = 0
        self.latticePoints = list()
        self.hoppings = list()

    def generatePoints(self, translations):
        """translations: dimension-tuple in lattice coords"""
        lbs = self.latticeBasis

        while len(translations) < 3:
            translations.append(1)
        translations = [range(i) for i in translations]
        self.translations = translations

        for i, j, k in product(translations[0], translations[1], translations[2]):
            latticePoint = [i, j, k]
            while len(latticePoint) > self.dimension:
                del latticePoint[-1]
            latticePoint = array(latticePoint)
            self.latticePoints.append(latticePoint)
            for basisPoint in lbs:
                self.points.append(latticePoint + basisPoint)

    def getPointsCartesian(self):
        """returns an d-dimensional array of floats"""
        pointsCartesian = list()

        for point in self.points:
            pointsCartesian.append(dot(point, self.latticeVectors))
        return array(pointsCartesian)

    def generateHoppings(self, hopping):
        knownHoppingEnergies =  list()
        lb = self.latticeBasis

        for a in range(len(self.latticePoints)):
            latticePoint = self.latticePoints[a]
            for b in range(a, len(self.latticePoints)):
                latticePoint2 = self.latticePoints[b]
                for r, h_r in hopping.items():
                    r = array(r)
                    h_r = array(h_r)
                    if all(latticePoint2 - latticePoint == r):
                        for i in range(len(h_r)):
                            for j in range(i+1, len(h_r), 1):
                                translation = array([latticePoint+lb[i,:], latticePoint+r+lb[j,:]])
                                if h_r[i, j] in knownHoppingEnergies:
                                    self.hoppings[index(knownHoppingEnergies, h_r[i, j])].append(translation)
                                else:
                                    knownHoppingEnergies.append(h_r[i, j])
                                    self.hoppings.append(list())
                                    self.hoppings[-1].append(translation)

    def generateHoppings2(self, hopping):
        knownHoppingEnergies =  list()
        lb = self.latticeBasis

        for a in range(len(self.latticePoints)):
            latticePoint = self.latticePoints[a]
            for b in range(a, len(self.latticePoints)):
                latticePoint2 = self.latticePoints[b]
                for r, h_r in hopping.items():
                    r = array(r)
                    h_r = array(h_r)
                    if all(latticePoint2 - latticePoint == r):
                        for i, j in product(range(len(h_r)), range(len(h_r))):
                            translation = array([latticePoint+lb[i,:], latticePoint+r+lb[j,:]])
                            if h_r[i, j] in knownHoppingEnergies and h_r[i, j] != 0:
                                self.hoppings[index(knownHoppingEnergies, h_r[i, j])].append(translation)
                            elif h_r[i, j] != 0:
                                knownHoppingEnergies.append(h_r[i, j])
                                self.hoppings.append(list())
                                self.hoppings[-1].append(translation)
        
        for i, linegroup in enumerate(self.hoppings):
            self.hoppings[i] = dropDoubleLines(linegroup)

    def getHoppingsCartesian(self):
        hoppingsCartesian = list()

        for group in self.hoppings:
            hoppingsCartesian.append(list())
            for line in group:
                newLine = list()
                for point in line:
                    newLine.append(dot(point, self.latticeVectors))
                hoppingsCartesian[-1].append(array(newLine))
        return hoppingsCartesian


def index(list0, val):
    i = 0
    if len(list0) > 0:
        searchVal = True
    else:
        res = None
        searchVal = False
    while searchVal and i < len(list0):
        if list0[i] == val:
            res = i
            searchVal = False
        else:
            i += 1
    if i == len(list0):
        res = None
    return res

def dropDoubleLines(lines):
    n_lines = len(lines)
    toBeDropped = list()
    for i in range(n_lines-1, -1, -1):
        for j in range(i-1, -1, -1):
            if linesEqual(lines[i], lines[j]):
                del lines[i]
                break
    return lines

def linesEqual(line1, line2):
    line1 = array(line1)
    line2 = array(line2)
    if (line1 == line2).all():
        return True
    elif (line1[0,:] == line2[1,:]).all() and (line1[1,:] == line2[0,:]).all():
        return True
    else:
        return False
