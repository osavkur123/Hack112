#################################################
# hackathon.py
#
# Your name: Carl Buford
# Your andrew id: cbuford
#################################################

import cmu_112_graphics
from cmu_112_graphics import *
from PIL import Image
from tkinter import *

import csv
import os
import locale
import multiprocessing
import threading
import queue
import tkinter as tk
from tkinter import ttk
from functools import partial
from typing import List, Dict

import math, copy, random

FILE_FOOD_DATA = "FoodData.csv"

# From https://www.cs.cmu.edu/~112/notes/notes-2d-lists.html#printing
# Helper function for print2dList.
# This finds the maximum length of the string
# representation of any item in the 2d list
def maxItemLength(a):
    maxLen = 0
    rows = len(a)
    for row in range(rows):
        for col in range(len(a[row])):
            maxLen = max(maxLen, len(str(a[row][col])))
    return maxLen

# Because Python prints 2d lists on one row,
# we might want to write our own function
# that prints 2d lists a bit nicer.
def print2dList(a):
    if (a == []):
        # So we don't crash accessing a[0]
        print([])
        return
    rows = len(a)
    fieldWidth = maxItemLength(a)
    print("[ ", end="")
    for row in range(rows):
        if (row > 0): print("\n  ", end="")
        print("[ ", end="")
        for col in range(len(a[row])):
            if (col > 0): print(", ", end="")
            # The next 2 lines print a[row][col] with the given fieldWidth
            formatSpec = "%" + str(fieldWidth) + "s"
            print(formatSpec % str(a[row][col]), end="")
        print(" ]", end="")
    print("]")

# From https://www.cs.cmu.edu/~112/notes/notes-recursion-part1.html#powerset
def powerset(a):
    # Base case: the only possible subset of an empty list is the empty list.
    if (len(a) == 0):
        return [ [] ]
    else:
        # Recursive Case: remove the first element, then find all subsets of the
        # remaining list. Then for each subset, use two versions of that subset:
        # one without the first element, and another one with it.

        partialSubsets = powerset(a[1:])
        allSubsets = [ ]
        for subset in partialSubsets:
            allSubsets.append(subset)
            allSubsets.append([a[0]] + subset)
        return allSubsets

class MealPlan(object):
    def __init__(self, favsList, mealList, mealVariants):
        # favsList is a 2-d list of the mealVariant classes; user's 3 favorite
        # breakfasts, lunches, dinners, and snacks (4 rows 3 cols)
        # mealVariants is a dict mapping all the info for possible foods 
        # mealList is the master 2-d of all the meals 
        # (row 0 is breakfasts, 1 is lunches, 2 is dinners, 3 is snacks)
        self.favsList = favsList 
        self.mealList = mealList 
        self.mealVariants = mealVariants    # Dict
        # Daily Amounts
        self.cal = 0
        self.findAvgCal()
        fat = (13/400)*self.cal
        satFat = (1/100)*self.cal
        sodium = (6/5)*self.cal
        chol = (3/20)*self.cal
        carbs = (3/20)*self.cal
        fiber = (1/80)*self.cal
        self.dailyAmounts = [self.cal, fat, satFat, sodium, chol, carbs, fiber]
        self.blocks = 207
        self.dineX = 825
        self.days = 112
        self.nutritiousCombos = [ ]
        self.mealComboPricesBlocks = [ ]
        self.mealComboPricesNoBlocks = [ ]
    
    def findAvgCal(self):
        for mealType in self.favsList:
            mealAvg = sum([meal.cal for meal in mealType])/len(mealType)
            self.cal += mealAvg

    def generateNutrientPlan(self):
        for bfast in self.favsList[0]:
            for lunch in self.favsList[1]:
                for dinner in self.favsList[2]:
                    # for snack in self.favsList[3]:
                    snacks = self.favsList[3]
                    combos = powerset([bfast, lunch, dinner] + snacks)
                    for i in range(len(combos)):
                        isNutritious = True
                        badNutrients = 0
                        cal = 0
                        fat = 0
                        satFat = 0
                        sodium = 0
                        chol = 0
                        carbs = 0
                        fiber = 0
                        for j in range(len(combos[i])):
                            cal += combos[i][j].cal
                            fat += combos[i][j].fat
                            satFat += combos[i][j].satFat
                            sodium += combos[i][j].sodium
                            chol += combos[i][j].chol
                            carbs += combos[i][j].carbs
                            fiber += combos[i][j].fiber
                        todaysAmounts = [cal, fat, satFat, sodium, chol, carbs, fiber]
                        for j in range(len(self.dailyAmounts)):
                            error = abs(self.dailyAmounts[j]-todaysAmounts[j])/self.dailyAmounts[j]
                            if (error > .1):
                                badNutrients += 1
                                if (badNutrients > 1):
                                    isNutritious = False
                        if (isNutritious and combos[i] not in self.nutritiousCombos):
                            self.nutritiousCombos.append(combos[i])

    def generateMealPrices(self):
        for nutritiousCombo in self.nutritiousCombos:
            priceSnacks = 0
            priceAll = 0
            blocks = 0
            for meal in nutritiousCombo:
                if (meal.isBfBlock or meal.isLBlock or meal.isDBlock):
                    blocks += 1
                    priceAll += meal.price
                else:
                    priceAll += meal.price
                    priceSnacks += meal.price
            self.mealComboPricesBlocks.append((nutritiousCombo, blocks, priceSnacks))
            self.mealComboPricesNoBlocks.append((nutritiousCombo, priceAll))
        
    def generateMealSchedule(self):
        if self.days <= 1:
            maxOut(self.blocks, self.dineX)
            return [combo]
        else:
            averageBlocks = roundHalfUp(self.blocks/self.days)
            averageDineX = self.dineX/self.days
            maxOut(averageBlocks, averageDineX)
            self.blocks -= blocksUsedToday
            self.dineX -= dineXUsedToday
            self.days -= 1
            return [comboUsedToday] + self.generateMealPrices()
    
    def maxOut(self, blocks, dineX):
        if blocks == 0:
            for combo in self.mealComboPricesNoBlocks:
                pass
        else:
            for combo in self.mealComboPricesBlocks:
                pass

                

class MealVariant(object):
    def __init__(self, csv_row):
        self.id = int(csv_row["ID"])
        self.location = csv_row["Location"]
        self.name = csv_row["Name"]
        self.price = float(csv_row["Price"])
        self.cal = int(csv_row["Calories"])
        self.fat = int(csv_row["Fat"])
        self.satFat = float(csv_row["SatFat"])
        self.sodium = int(csv_row["Sodium"])
        self.chol = int(csv_row["Cholesterol"])
        self.carbs = int(csv_row["Carbs"])
        self.fiber = int(csv_row["Fiber"])
        self.isBfBlock = True if csv_row["Breakfast"] == "TRUE" else False
        self.isLBlock = True if csv_row["Lunch"] == "TRUE" else False
        self.isDBlock = True if csv_row["Dinner"] == "TRUE" else False
        self.isSnack = True if csv_row["Snack"] == "TRUE" else False

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return (isinstance(other, MealVariant) and self.id == other.id)

    def __repr__(self):
        return self.name

def getMealSchedule(favsList=[ ]):
    mealList = [ [ ], 
                 [ ],
                 [ ],
                 [ ] ]
    mealVariants = dict()
    with open(FILE_FOOD_DATA, "r") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            meal = MealVariant(row)
            if meal.isBfBlock:
                mealList[0].append(meal)
            elif meal.isLBlock:
                mealList[1].append(meal)
            elif meal.isDBlock:
                mealList[2].append(meal)
            else:
                mealList[3].append(meal)
            mealVariants.setdefault(meal.id, meal)
    if favsList != [ ]:
        MealPlan1 = MealPlan(favsList, mealList, mealVariants)
        MealPlan1.generateNutrientPlan()
        MealPlan1.generateMealPrices()
        return MealPlan1
    return mealVariants

def testMealClasses():
    print('Testing class MealPlan()...', end='')
    assert(1 == 0)
    print('Passed!')

def testAll():
    testMealClasses()

def main():
    getMealSchedule()
    testAll()

if __name__ == '__main__':
    main()
