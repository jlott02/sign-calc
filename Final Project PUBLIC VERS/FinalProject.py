"""
Author: Jules
Date written: 2/16/2024
Assignment: Final Project
This program is a GUI zodiac calculator. The user enters their date of birth, and then the program will return their western zodiac sign as well as their Chinese
zodiac sign.
REQUIRES BREEZYPYTHONGUI! Make sure breezypythongui.py is installed in the same directory as your Python executable before use.
"""
import tkinter as tk
from tkinter import PhotoImage
from breezypythongui import EasyFrame
from breezypythongui import MessageBox
import os

class InvalidDateException(Exception):
    # Raised when invalid date is given by user
    pass

"""Main code for the calculator"""

class ZodiacCalculator(EasyFrame):
    """Initial formatting of the GUI"""
    def __init__(self):
        EasyFrame.__init__(self, title = 'Zodiac Calculator')

        base_folder = os.path.dirname(__file__) # Variable for image access
        image_path = os.path.join(base_folder, 'constellation.gif') # Variable for image access
        self.starImage = PhotoImage(file=image_path) # Holds image for the main window
        imageLabel = self.addLabel(text = '', row = 0, column = 0, sticky = 'NSEW', columnspan = 2)
        imageLabel["image"] = self.starImage

        self.addLabel(text = "An image of a starry purple sky.", row = 1, column = 0, sticky = 'NSEW', columnspan = 2)
        self.addLabel(text = "Enter your birth date information to discover your zodiac signs:", row = 2, column = 0, sticky = "NSEW", columnspan = 2)
        self.addLabel(text = "Month:", row = 3, column = 0)
        self.addLabel(text = "Day:", row = 4, column = 0)
        self.addLabel(text = "Year:", row = 5, column = 0)
        self.userMonth = self.addIntegerField(value = "", row = 3, column = 1, width = 8) # Month field
        self.userDay = self.addIntegerField(value = "", row = 4, column = 1, width = 8) # Day field
        self.userYear = self.addIntegerField(value = "", row = 5, column = 1, width = 8) # Year fied
        self.addButton(text = 'Calculate', row = 6, column = 0, command = self.checkInput)
        self.addButton(text = "Exit", row = 6, column = 1, command = self.close)
    
    """Checks input for non-numerical and invalid data before calling the main logic functions"""

    def checkInput(self):
        """Ensures user input contains only integers"""
        try:
            self.userMonthCalc = self.userMonth.getNumber() # Holds user month
            self.userDayCalc = self.userDay.getNumber() # Holds user day
            self.userYearCalc = self.userYear.getNumber() # Holds user year 
        except ValueError:
            MessageBox(self, title = "Error!", message = "Make sure you have filled out all boxes and entered only numbers. Please try again.", width = 50, height = 10)
            return
        """Calls the date validation function to ensure a valid date was supplied"""
        try:
            self.validateDate(self.userDayCalc, self.userMonthCalc, self.userYearCalc)
        except InvalidDateException:
            return
        """Main zodiac calculation functions are called"""
        try:
            self.calculateChineseZodiac(self.userYearCalc)
            self.calculateWesternZodiac(self.userDayCalc, self.userMonthCalc)
        except:
            return
        """Placeholder result message boxes for debugging purposes. Results will be displayed in a new window in the final version."""
        MessageBox(self, title = "Error!", message = self.zodiacAnimal, width = 50, height = 10)
        MessageBox(self, title = "Error!", message = self.userSign, width = 50, height = 10)
        return
    
    """Validates the date. Takes user-supplied day, month, and year as parameters."""

    def validateDate(self, day, month, year):
        self.thirtyOneDays = (1, 3, 5, 7, 8, 10, 12) # Months with 31 days
        self.thirtyDays = (4, 6, 9, 11) # Months with 30 days

        if year <= 0: # Ensures year is not negative
            MessageBox(self, title = "Error!", message = "Year value cannot be negative or 0! Please try again.", width = 50, height = 10)
            raise InvalidDateException
        if (month < 1) or (month > 12): # Ensures month value is between 1 and 12
            MessageBox(self, title = "Error!", message = "Month value must be between 1 and 12! Please try again.", width = 50, height = 10)
            raise InvalidDateException
        if day < 1: # Ensures day value is not less than 1
            MessageBox(self, title = "Error!", message = "Day value cannot be less than 1! Please try again.", width = 50, height = 10)
            raise InvalidDateException        
        if (month in self.thirtyOneDays) and (day > 31): # If the month given is one with 31 days, allow values up to 31
            MessageBox(self, title = "Error!", message = "Day value cannot exceed 31 for specified month! Please try again.", width = 50, height = 10)
            raise InvalidDateException
        if (month in self.thirtyDays) and (day > 30): # If the month given has 30 days, allow values up to 30
            MessageBox(self, title = "Error!", message = "Day value cannot exceed 30 for specified month! Please try again.", width = 50, height = 10)
            raise InvalidDateException
        # Special checks for February. If year is not a leap year, allow a day value only up to 28. 29 if it is a leap year.
        if (month == 2) and (year % 4 != 0) and (day > 28):
            MessageBox(self, title = "Error!", message = "Day value cannot exceed 28 for specified month! Please try again.", width = 50, height = 10)
            raise InvalidDateException
        elif (month == 2) and (year % 4 == 0) and (day > 29):
            MessageBox(self, title = "Error!", message = "Day value cannot exceed 29 for specified month! Please try again.", width = 50, height = 10)
            raise InvalidDateException

    """Function to determine the user's Chinese zodiac sign. Takes year as a parameter. Returns user's animal."""

    def calculateChineseZodiac(self, year):
        self.animals = ("Monkey", "Rooster", "Dog", "Pig", "Rat", "Ox", "Tiger", "Rabbit", "Dragon", "Snake", "Horse", "Goat") # Holds Chinese zodiac signs
        self.zodiacAnimal = self.animals[year % 12]
        return self.zodiacAnimal
    
    """Function to determine user's western zodiac sign. Takes day and month as parameters. Returns the user's zodiac sign."""

    def calculateWesternZodiac(self, day, month):
        self.zodiacSigns = ("Capricorn", "Aquarius", "Pisces", "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius") # Holds western zodiac signs
        if (month == 12) and (day >= 22):
            self.userSign = self.zodiacSigns[0]
            return self.userSign
        elif (month == 12) and (day < 22):
            self.userSign = self.zodiacSigns[11]
            return self.userSign
        if (month == 11) and (day >= 22):
            self.userSign = self.zodiacSigns[11]
            return self.userSign
        elif (month == 11) and (day < 22):
            self.userSign = self.zodiacSigns[10]
            return self.userSign
        if (month == 10) and (day >= 23):
            self.userSign = self.zodiacSigns[10]
            return self.userSign
        elif (month == 10) and (day < 23):
            self.userSign = self.zodiacSigns[9]
            return self.userSign
        if (month == 9) and (day >= 23):
            self.userSign = self.zodiacSigns[9]
            return self.userSign
        elif (month == 9) and (day < 23):
            self.userSign = self.zodiacSigns[8]
            return self.userSign
        if (month == 8) and (day >= 23):
            self.userSign = self.zodiacSigns[8]
            return self.userSign
        elif (month == 8) and (day < 23):
            self.userSign = self.zodiacSigns[7]
            return self.userSign
        if (month == 7) and (day >= 23):
            self.userSign = self.zodiacSigns[7]
            return self.userSign
        elif (month == 7) and (day < 23):
            self.userSign = self.zodiacSigns[6]
            return self.userSign
        if (month == 6) and (day >= 21):
            self.userSign = self.zodiacSigns[6]
            return self.userSign
        elif (month == 6) and (day < 21):
            self.userSign = self.zodiacSigns[5]
            return self.userSign
        if (month == 5) and (day >= 21):
            self.userSign = self.zodiacSigns[5]
            return self.userSign
        elif (month == 5) and (day < 21):
            self.userSign = self.zodiacSigns[4]
            return self.userSign
        if (month == 4) and (day >= 20):
            self.userSign = self.zodiacSigns[4]
            return self.userSign
        elif (month == 4) and (day < 20):
            self.userSign = self.zodiacSigns[3]
            return self.userSign
        if (month == 3) and (day >= 21):
            self.userSign = self.zodiacSigns[3]
            return self.userSign
        elif (month == 3) and (day < 21):
            self.userSign = self.zodiacSigns[2]
            return self.userSign
        if (month == 2) and (day >= 19):
            self.userSign = self.zodiacSigns[2]
            return self.userSign
        elif (month == 2) and (day < 19):
            self.userSign = self.zodiacSigns[1]
            return self.userSign
        if (month == 1) and (day >= 20):
            self.userSign = self.zodiacSigns[1]
            return self.userSign
        elif (month == 1) and (day < 20):
            self.userSign = self.zodiacSigns[0]
            return self.userSign

    """Function for the exit button. Closes the program."""

    def close(self):
        ZodiacCalculator().destroy()
        quit()


def main():
    ZodiacCalculator().mainloop()
if __name__ == "__main__":
    main()
