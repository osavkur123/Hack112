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

class MealPlan:
    def __init__(self, favsList, FoodData):
        # favsList is a 2-d list with of the user's 3 favorite
        # breakfasts, lunches, dinners, and snacks (4 rows 3 cols)
        # FoodData is a csv file with all the info for possible foods
        self.favsList = favsList 
        self.FoodData = FoodData    #FILE_FOOD_DATA

class MealVariant:
    def __init__(self, csv_row):
        self.id = int(csv_row["ID"])
        self.location = csv_row["Location"]
        self.name = csv_row["Name"]
        self.price = float(csv_row["Price"])
        self.cal = int(csv_row["Calories"])
        self.fat = int(csv_row["Fat"])
        self.satFat = int(csv_row["SatFat"])
        self.sodium = int(csv_row["Sodium"])
        self.chol = int(csv_row["Cholesterol"])
        self.carbs = int(csv_row["Carbs"])
        self.fiber = int(csv_row["Fiber"])
        self.isBfBlock = bool(csv_row["Breakfast"]) # !!! Wrong to do bool()???
        self.isLBlock = bool(csv_row["Lunch"])
        self.isDBlock = bool(csv_row["Dinner"])
        self.isSnack = bool(csv_row["Snack"])

def testMealClasses():
    print('Testing class MealPlan()...', end='')
    assert(1 == 0)
    print('Passed!')

def testAll():
    testMealClasses()

def main():
    meal_variants = dict()
    with open(FILE_FOOD_DATA, "r") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            meal = MealVariant(row)
            meal_variants.setdefault(meal.id, meal)
    testAll()

if __name__ == '__main__':
    main()
