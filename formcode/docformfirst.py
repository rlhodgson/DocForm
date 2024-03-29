"""DOC Form, takes user input through GUI and enters it into a database table
   Author: Rachel Hodgson
   Start Date: 30-05-2019
   Completion Date: 28-06-2019
"""

from tkinter import * 
from tkinter.ttk import *
import sqlite3
import os
#importing necessary modules to carry out the tkinter model and feed info back to the database

class DocForm(): #form class
    
    def __init__(self, window, tracks, conditions, difficulty, track_name, recorded_cond):
        '''initiator function'''
        self.conditions = conditions
        self.diff = difficulty
        self.track_name = track_name
        self.recorded_cond = recorded_cond
        
        
        self.title = Label(window, text="DOC Form", font=("Arial", 14))
        self.title.grid(row=0, column=1, padx=5, pady=5)
        #title of form
        
        
        self.trackname = Label(window, text='Track Name: ')
        self.trackname.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
        #label for track name selection
        
        
        self.combo = Combobox(window, values=tracks, width=12)
        self.combo.selection_clear()
        self.combo.grid(row=1, column=1, columnspan=2, padx=5, pady=5)
        self.combo.bind('<<ComboboxSelected>>', self.selectedtrack) 
        #combobox that suggests the tracks in the list at the beginning
        #when selected the 'selectedtrack' function will be undergone
        
        
        self.condition = Label(window, text='Select the conditions you want to report')
        self.condition.grid(row=2, column=0, columnspan=3, padx=5, pady=5)
        #label for selecting conditions
         
           
        self.mud = Button(window, text='Muddy Track', command=self.mud)
        self.mud.grid(row=3, column=0, padx=5, pady=5)
        
        self.flood = Button(window, text='Flooding', command=self.mud)
        self.flood.grid(row=3, column=1, padx=5, pady=5)
        
        self.gravel = Button(window, text='Loose Gravel', command=self.mud)
        self.gravel.grid(row=3, column=2, padx=5, pady=5)
        
        self.trees = Button(window, text='Fallen Trees', command=self.mud)
        self.trees.grid(row=4, column=0, padx=5, pady=5)
        
        self.slides = Button(window, text='Landslides', command=self.mud)
        self.slides.grid(row=4, column=1, padx=5, pady=5)
        
        self.ruts = Button(window, text='Rutted Track', command=self.mud)
        self.ruts.grid(row=4, column=2, padx=5, pady=5)        
        
        
        self.diffbut = Label(window, text="Please select a difficulty 1 - 10")
        self.diffbut.grid(row=5, column=0, columnspan=2, padx=5, pady=5)    
        #label for difficulty entry
          
           
        self.difficulty = Entry(window, width=14)
        self.difficulty.grid(row=5, column=2, padx=5, pady=5)
        self.difficulty.bind('<KeyRelease>', self.getdifficulty)
        #when the user finishes their entry the 'getdifficulty' function is called
        
        
        self.complete = Button(window, text='Finalize', command=self.finalize)
        self.complete.grid(row=6, column=1, padx=5, pady=5)
        #complete button that goes to the 'finalize' function when pressed
        
        
        self.final = Label(window, text='')
        self.final.grid(row=7, column=0, padx=5, pady=5)
        #label to say 'completed' when the process is finished
        
    def mud(self):
        '''does stuff'''
        pass
        
    def selectedtrack(self, event):
        '''retrieves the selected track from the track combo box'''
        track = self.combo.get()
        self.track_name = track
    
   
    def addcond(self, event):
        '''adds a condition to the recorded condition list'''
        condition = self.condcombo.get()
        self.recorded_cond.append(condition)
    
    
    def getdifficulty(self, event):
        '''retrieves the difficulty entered into the entry box'''
        try:
            diff = self.difficulty.get()
            self.diff = diff
            if int(self.diff) < 0 or int(self.diff) > 10:
                raise ValueError           
        except ValueError:
            print("Please select sufficient difficulty\n")  
            os._exit(0)
        #handles input error where the user inputs a difficulty out of the given range
    
        
    def finalize(self):
        '''last part of the program, enters the information into the database'''
        self.final['text'] = "Completed!"
        
        final_condition = ''
        for cond in self.recorded_cond:
            final_condition += cond
            
        max_length = 0
        for condition in self.conditions:
            if len(condition) > max_length:
                max_length = len(condition)
        
        

        if len(final_condition) > max_length:
            print("Please select only one condition\n")
            os._exit(0)
            
        #ensures the condition is a string that can be entered into the database field
        
        track_name = self.track_name
        difficulty = self.diff
        conditions = final_condition
       
        import datetime
        x = datetime.datetime.now()
        date = x.strftime("%x")    
        #sets the date the form is being filled out so this does not have to be entered
    
        newrecord = (track_name.capitalize(), difficulty, conditions.capitalize(), date)
        #tuple of all information
    
        with sqlite3.connect("db/tracks.db") as db: #opening correct database
            cursor = db.cursor()
            cursor.execute("INSERT INTO Tracks(TrackName,Difficulty,Conditions,Date) VALUES (?,?,?,?)",newrecord) #inserts the information into the correct columns of the database
            db.commit()        

        
def main():
    '''main function that calls the form class'''
    window = Tk() #creates a tkinter window
    listconditions = ['Muddy Track', 'Flooding', 'Loose Gravel', 'Fallen Trees', 'Landslides', 'Rutted Track']
    difficultylevel = None #to be initiated
    track_name = None #to be initiated
    tracks = ['Routeburn', 'Milford', 'Heaphy', 'Able Tasman', 'Avalanche Peak']
    recorded_cond = []
    form = DocForm(window, tracks, listconditions, difficultylevel, track_name, recorded_cond)
    window.mainloop()
    
main()
