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

# Helper function for print2dList.
# This finds the maximum length of the string
# representation of any item in the 2d list
def maxItemLength(a):
    maxLen = 0
    rows = len(a)
    cols = len(a[0])
    for row in range(rows):
        for col in range(cols):
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
    cols = len(a[0])
    fieldWidth = maxItemLength(a)
    print("[ ", end="")
    for row in range(rows):
        if (row > 0): print("\n  ", end="")
        print("[ ", end="")
        for col in range(cols):
            if (col > 0): print(", ", end="")
            # The next 2 lines print a[row][col] with the given fieldWidth
            formatSpec = "%" + str(fieldWidth) + "s"
            print(formatSpec % str(a[row][col]), end="")
        print(" ]", end="")
    print("]")

class MealPlan(object):
    def __init__(self, favsList, mealList, mealVariants):
        # favsList is a 2-d list of the mealVariant classes; user's 3 favorite
        # breakfasts, lunches, dinners, and snacks (4 rows 3 cols)
        # mealVariants is a dict mapping all the info for possible foods 
        # mealList is the master 2-d of all the meals 
        # (row 0 is breakfasts, 1 is lunches, 2 is dinners, 3 is snacks)
        self.favsList = favsList 
        self.mealVariants = mealVariants    # Dict
        for bfast in self.favsList[0]:
            for lunch in self.favsList[1]:
                for dinner in self.favsList[2]:
                    for snack in self.favsList[3]:
                        price = bfast.price+lunch.price+dinner.price+snack.price
                        cal = bfast.cal+lunch.cal+dinner.cal+snack.cal
                        fat = bfast.fat+lunch.fat+dinner.fat+snack.fat
                        satFat = bfast.satFat+lunch.satFat+dinner.satFat+snack.satFat
                        sodium = bfast.sodium+lunch.sodium+dinner.sodium+snack.sodium
                        chol = bfast.chol+lunch.chol+dinner.chol+snack.chol
                        carbs = bfast.carbs+lunch.carbs+dinner.carbs+snack.carbs
                        fiber = bfast.fiber+lunch.fiber+dinner.fiber+snack.fiber
                        print('wow')

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
        self.isBfBlock = bool(csv_row["Breakfast"]) # !!! Wrong to do bool()???
        self.isLBlock = bool(csv_row["Lunch"])
        self.isDBlock = bool(csv_row["Dinner"])
        self.isSnack = bool(csv_row["Snack"])

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return (isinstance(other, MealVariant) and self.id == other.id)

    def __repr__(self):
        return self.name

def testMealClasses():
    print('Testing class MealPlan()...', end='')
    assert(1 == 0)
    print('Passed!')

def testAll():
    testMealClasses()

def main():
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
    testAll()

if __name__ == '__main__':
    main()
