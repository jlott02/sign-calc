"""
Author: Jules Lotkowski
Date written: 2/16/2024
Assignment: Final Project
This program is a GUI zodiac calculator. The user enters their date of birth, and then the program will return their western zodiac sign as well as their Chinese
zodiac sign.
REQUIRES BREEZYPYTHONGUI! Make sure breezypythongui.py is installed in the same directory as your Python executable before use.
"""
import tkinter as tk
from tkinter import Grid
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
        EasyFrame.__init__(self, title = 'Zodiac Calculator', background = "#d7c4de")
        """Image handling"""
        base_folder = os.path.dirname(__file__) # Variable for image access
        image_path = os.path.join(base_folder, 'constellation.gif') # Variable for image access
        self.starImage = PhotoImage(file=image_path) # Holds image for the main window
        imageLabel = self.addLabel(text = '', row = 0, column = 0, sticky = 'NSEW', columnspan = 2, background = "#d7c4de") # Label for image
        imageLabel["image"] = self.starImage
        """Adding labels, integer fields, and buttons"""
        self.addLabel(text = "An image of a starry purple sky.", row = 1, column = 0, sticky = 'NSEW', columnspan = 2, background = "#d7c4de")
        self.addLabel(text = "Enter your birth date information to discover your zodiac signs:", row = 2, column = 0, sticky = "NSEW", columnspan = 2, background = "#d7c4de")
        self.addLabel(text = "Month:", row = 3, column = 0, background = "#d7c4de", sticky = "E", font = ('Arial', 9, 'bold'))
        self.addLabel(text = "Day:", row = 4, column = 0, background = "#d7c4de", sticky = "E", font = ('Arial', 9, 'bold'))
        self.addLabel(text = "Year:", row = 5, column = 0, background = "#d7c4de", sticky = "E", font = ('Arial', 9, 'bold'))
        self.userMonth = self.addIntegerField(value = "", row = 3, column = 1, width = 8, sticky = "W") # Month field
        self.userDay = self.addIntegerField(value = "", row = 4, column = 1, width = 8, sticky = "W") # Day field
        self.userYear = self.addIntegerField(value = "", row = 5, column = 1, width = 8, sticky = "W") # Year fied
        self.calculateButton = self.addButton(text = 'Calculate', row = 6, column = 0, command = self.checkInput) # Calculate button
        self.calculateButton["background"] = '#f2efb9'
        self.mainExitButton = self.addButton(text = "Exit", row = 6, column = 1, command = self.close) # Exit button
        self.mainExitButton["background"] = '#f2efb9'
    
    """Checks input for non-numerical and invalid data before calling the main logic functions"""

    def checkInput(self):
        """Ensures user input contains only integers"""
        try:
            self.userMonthCalc = self.userMonth.getNumber() # Holds user month
            self.userDayCalc = self.userDay.getNumber() # Holds user day
            self.userYearCalc = self.userYear.getNumber() # Holds user year
        except ValueError: # If any box is empty or does not contain a number, display error message
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
        """Disable the calculate button until the back button is clicked on the result window"""
        self.calculateButton["state"] = "disabled"
        try: # Open results window
            self.resultsWindow(self.zodiacAnimal, self.userSign)
        except:
            return
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
        self.zodiacAnimal = self.animals[year % 12] # Determines and stores the user's Chinese zodiac sign
        return self.zodiacAnimal
    
    """Function to determine user's western zodiac sign. Takes day and month as parameters. Returns the user's zodiac sign."""

    def calculateWesternZodiac(self, day, month):
        self.zodiacSigns = ("Capricorn", "Aquarius", "Pisces", "Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo", "Libra", "Scorpio", "Sagittarius") # Holds western zodiac signs
        """Logic to determine user's western zodiac sign and store the result as a variable"""
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
    
    """Function for back button on results window. Closes results window and enables the calculate button"""
    def back(self):
        self.calculateButton["state"] = "normal"
        self.top.destroy()

    """Displays the results window, taking animal and sign as parameters"""
    def resultsWindow(self, animal, sign):
        """Variables for zodiac images, image descriptions, and short descriptions for zodiac meanings"""
        self.animalImage = ''
        self.zodiacImage = ''
        self.animalImageDescriptionText = ''
        self.zodiacImageDescriptionText = ''
        self.animalDescriptionText = ''
        self.zodiacDescriptionText = ''

        """Labels for results, create back and exit button"""
        self.top = tk.Toplevel()
        self.top.title("Results")
        self.top.configure(background = "#d7c4de")
        self.animalLabel = tk.Label(self.top, text = "You are year of the:", background = "#d7c4de", font = ('Arial', 9, 'bold')) # Labels Chinese zodiac result
        self.animalResult = tk.Label(self.top, text = animal, background = "#d7c4de") # Displays Chinese zodiac result
        self.zodiacLabel = tk.Label(self.top, text = "Your zodiac sign is:", background = "#d7c4de", font = ('Arial', 9, 'bold')) # Labels western zodiac result
        self.zodiacResult = tk.Label(self.top, text = sign, background = "#d7c4de") # Displays western zodiac result
        self.backButton = tk.Button(self.top, text = "Back", command = self.back, background= '#f2efb9') # Back button
        self.exitButton = tk.Button(self.top, text = "Exit", command = self.close, background= '#f2efb9') # Close button

        self.resultLogic() # Calls function for displaying result images and descriptions

        """Labels for image and result descriptions. Text is determined by the resultLogic function"""
        self.animalImageDescription = tk.Label(self.top, text = self.animalImageDescriptionText, background = "#d7c4de")
        self.zodiacImageDescription = tk.Label(self.top, text = self.zodiacImageDescriptionText, background = "#d7c4de")
        self.animalDescription = tk.Label(self.top, text = self.animalDescriptionText, background = "#d7c4de")
        self.zodiacDescription = tk.Label(self.top, text = self.zodiacDescriptionText, background = "#d7c4de")

        """Image handling"""
        animalBaseFolder = os.path.dirname(__file__) # Variable for image access
        animalImagePath = os.path.join(animalBaseFolder, self.animalImage) # Variable for image access
        self.animalImageDisplay = PhotoImage(file=animalImagePath) # Holds image for the main window
        animalImageLabel = tk.Label(self.top, text = "", background = "#d7c4de")
        animalImageLabel["image"] = self.animalImageDisplay
        zodiacBaseFolder = os.path.dirname(__file__) # Variable for image access
        zodiacImagePath = os.path.join(zodiacBaseFolder, self.zodiacImage) # Variable for image access
        self.zodiacImageDisplay = PhotoImage(file=zodiacImagePath) # Holds image for the main window
        zodiacImageLabel = tk.Label(self.top, text = "", background = "#d7c4de")
        zodiacImageLabel["image"] = self.zodiacImageDisplay

        """Formatting"""
        zodiacImageLabel.grid(row = 0, column = 1, padx = 5, pady = 5)
        animalImageLabel.grid(row = 0, column = 0, padx = 5, pady = 5)
        self.animalImageDescription.grid(row = 1, column = 0, padx = 5)
        self.zodiacImageDescription.grid(row = 1, column = 1, padx = 5)
        self.animalLabel.grid(row = 2, column = 0, padx = 5, pady = 5, sticky = "E")
        self.animalResult.grid(row = 2, column = 1, padx = 5, pady = 5, sticky = "W")
        self.animalDescription.grid(row = 3, columnspan = 2)
        self.zodiacLabel.grid(row = 4, column = 0, padx = 5, pady = 5, sticky = "E")
        self.zodiacResult.grid(row = 4, column = 1, padx = 5, pady = 5, sticky = "W")
        self.zodiacDescription.grid(row = 5, columnspan = 2)
        self.backButton.grid(row = 6, column = 0, padx = 5, pady = 5)
        self.exitButton.grid(row = 6, column = 1, padx = 5, pady = 5)

    """Sets images, image descriptions, and result descriptions depending on animal and sign"""
    def resultLogic(self):
        """Determines Chinese zodiac image and descriptions"""
        if self.zodiacAnimal == "Monkey":
            self.animalImage = 'monkey.png'
            self.animalImageDescriptionText = "An image of a monkey."
            self.animalDescriptionText = "You are creative, quick-witted, and clever!"
        if self.zodiacAnimal == "Rooster":
            self.animalImage = 'rooster.png'
            self.animalImageDescriptionText = "An image of a rooster."
            self.animalDescriptionText = "You are confident and assertive!"
        if self.zodiacAnimal == "Dog":
            self.animalImage = 'dog.png'
            self.animalImageDescriptionText = "An image of a dog."
            self.animalDescriptionText = "You are a reliable and loyal friend!"
        if self.zodiacAnimal == "Pig":
            self.animalImage = 'pig.png'
            self.animalImageDescriptionText = "An image of a pig."
            self.animalDescriptionText = "You are laid-back and honest!"
        if self.zodiacAnimal == "Rat":
            self.animalImage = 'rat.png'
            self.animalImageDescriptionText = "An image of a rat."
            self.animalDescriptionText = "You are highly social and witty!"
        if self.zodiacAnimal == "Ox":
            self.animalImage = 'ox.png'
            self.animalImageDescriptionText = "An image of an ox."
            self.animalDescriptionText = "You are hard-working and value practicality!"
        if self.zodiacAnimal == "Tiger":
            self.animalImage = 'tiger.png'
            self.animalImageDescriptionText = "An image of a tiger."
            self.animalDescriptionText = "You are a confident and courageous leader!"
        if self.zodiacAnimal == "Rabbit":
            self.animalImage = 'rabbit.png'
            self.animalImageDescriptionText = "An image of a rabbit."
            self.animalDescriptionText = "You are peaceful and have an eye for detail!"
        if self.zodiacAnimal == "Dragon":
            self.animalImage = 'dragon.png'
            self.animalImageDescriptionText = "An image of a dragon."
            self.animalDescriptionText = "You radiate intelligence and power!"
        if self.zodiacAnimal == "Snake":
            self.animalImage = 'snake.png'
            self.animalImageDescriptionText = "An image of a snake."
            self.animalDescriptionText = "You are humorous and persuasive!"
        if self.zodiacAnimal == "Horse":
            self.animalImage = 'horse.png'
            self.animalImageDescriptionText = "An image of a horse."
            self.animalDescriptionText = "You are energetic and positive!"
        if self.zodiacAnimal == "Goat":
            self.animalImage = 'goat.png'
            self.animalImageDescriptionText = "An image of a goat."
            self.animalDescriptionText = "You are gentle and compassionate!"

        """Determines western zodiac image and descriptions"""
        if self.userSign == "Capricorn":
            self.zodiacImage = 'capricorn.png'
            self.zodiacImageDescriptionText = "The Capricorn symbol."
            self.zodiacDescriptionText = "You are determined and hard-working!"
        if self.userSign == "Aquarius":
            self.zodiacImage = 'aquarius.png'
            self.zodiacImageDescriptionText = "The Aquarius symbol."
            self.zodiacDescriptionText = "You are analytical and love problem-solving!"
        if self.userSign == "Pisces":
            self.zodiacImage = 'pisces.png'
            self.zodiacImageDescriptionText = "The Pisces symbol."
            self.zodiacDescriptionText = "You have a strong sense of empathy and romance!"
        if self.userSign == "Aries":
            self.zodiacImage = 'aries.png'
            self.zodiacImageDescriptionText = "The Aries symbol."
            self.zodiacDescriptionText = "You are strongly motivated and competitve!"
        if self.userSign == "Taurus":
            self.zodiacImage = 'taurus.png'
            self.zodiacImageDescriptionText = "The Taurus symbol."
            self.zodiacDescriptionText = "You are a stubborn yet diligent hard-worker!"
        if self.userSign == "Gemini":
            self.zodiacImage = 'gemini.png'
            self.zodiacImageDescriptionText = "The Gemini symbol."
            self.zodiacDescriptionText = "You are unpredictable and clever!"
        if self.userSign == "Cancer":
            self.zodiacImage = 'cancer.png'
            self.zodiacImageDescriptionText = "The Cancer symbol."
            self.zodiacDescriptionText = "You are nurturing and empathetic!"
        if self.userSign == "Leo":
            self.zodiacImage = 'leo.png'
            self.zodiacImageDescriptionText = "The Leo symbol."
            self.zodiacDescriptionText = "You are a born leader and love being the center of attention!"
        if self.userSign == "Virgo":
            self.zodiacImage = 'virgo.png'
            self.zodiacImageDescriptionText = "The Virgo symbol."
            self.zodiacDescriptionText = "You are logical and a perfectionist!"
        if self.userSign == "Libra":
            self.zodiacImage = 'libra.png'
            self.zodiacImageDescriptionText = "The Libra symbol."
            self.zodiacDescriptionText = "You are sociable and seek harmony in your life!"
        if self.userSign == "Scorpio":
            self.zodiacImage = 'scorpio.png'
            self.zodiacImageDescriptionText = "The Scorpio symbol."
            self.zodiacDescriptionText = "You are independent and intense!"
        if self.userSign == "Sagittarius":
            self.zodiacImage = 'sagittarius.png'
            self.zodiacImageDescriptionText = "The Sagittarius symbol."
            self.zodiacDescriptionText = "You are charming and bold!"





def main():
    ZodiacCalculator().mainloop()
if __name__ == "__main__":
    main()
