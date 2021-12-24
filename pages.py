from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
from otree.api import (models)
import csv 
from django.db import models
import os
import pathlib
import pandas as pandasForSortingCSV

print(pathlib.Path(__file__).parent.resolve())
with open (os.path.join(pathlib.Path(__file__).parent.resolve(), 'new_25_oct.csv')) as f:
    reader = csv.reader(f)
    templist = []
    idlist = []
    for row in reader: 
        idlist.append(row[0])
        templist.append(
            {
                'id' : row[0],
                'gender' : row[1],
                'race' : row[2],
                'fall_score' : row[3],
                'spring_score' : row[4],
                'pet': row[5],
                'parent1' : row[6],
                'parent2': row[7],
                'quality1': row[8],
                'quality2': row[9],
            }
        )

# with open (os.path.join(pathlib.Path(__file__).parent.resolve(), '25_oct_payoff.csv')) as f:
#     payoff_csv = csv.reader(f)
# os.path.join(pathlib.Path(__file__).parent.resolve(), '25_oct_payoff.csv')
# csvData = pandasForSortingCSV.read_csv(os.path.join(pathlib.Path(__file__).parent.resolve(), '25_oct_payoff.csv'))


male_white_counter = 1

class background(Page):
    "This page introduces the experiment"
    pass

class introClass(Page):
    "screen 2"
    pass


class classroom(Page):
    "This page introduces the assigned class to the subject with flashcards"
    "Rank the students with fill in the blanks as ranks"
    form_model = 'player'
    form_fields = ['ranks']
    # [x for x in childid]
    def vars_for_template(self):
        for id in idlist:
            self.player.ranks[id] = 0
        # print(','.join(idlist))
        return {
            'idlist': ','.join(idlist),
            'templist' : templist
        }
    
    def before_next_page(self):
        print(self.player.ranks)
    
score_fields = ['Asian Students', 'Girls', 'Dog Owners', 'Students with both parents working', 'White students', 'Extroverted students', 'Boys', 'Unruly students', 'Cat owners']

def helperPayoff_Avgs(scores):
    # What should this function do?
    # Subtract Actual score from Assigned score
    # Loop over scores
    # Get the score and subtract
    total = 0
    ActualAvg = {
        'Asian Students' : '57',
        'Girls' : '51.7',
        'Dog Owners' : '50.9',
        'Students with both parents working' : '49.1',
        'White students':'55',
        'Extroverted students' : '54.3',
        'Boys' : '51.6',
        'Unruly students' : '50.7',
        'Cat owners' : '53.8'
    }
    # Asian Students 57
    # Girls  51.7
    # Dog owners 50.9
    # Both parents working 49.1
    # white students 55
    # extroverted students 54.3
    # boys 51.6
    # unruly students 50.7
    # cat owners 53.8
    for key,value in scores.items():
        # print(f'{key} {value}')
        # print(ActualAvg[key])
        temp = 0 if value == '' else int(value)
        total += (float(ActualAvg[key]) - temp) ** 2
    constant = 3000
    return constant - total

class studentAverages(Page):
    "This page shows student averages accross the whole group, then asks to rate"
    form_model = 'player'
    form_fields = ['scores']
    def vars_for_template(self):
        for name in score_fields:
            self.player.scores[name] = 0
        return {
            'fields' : score_fields,
            'fieldlist' : ','.join(score_fields)
        }
    def before_next_page(self):
        print(self.player.scores)
        helperPayoff_Avgs(self.player.scores)

class trueAvgs(Page):
    "This page shows true values of flashcard ranks and then asks to fill"
    "in the blanks for average scores again"
    "This page shows student averages accross the whole group, then asks to rate"
    form_model = 'player'
    form_fields = ['new_scores']
    def vars_for_template(self):
        for name in score_fields:
            self.player.new_scores[name] = 0
        return {
            'fields' : score_fields,
            'fieldlist' : ','.join(score_fields),
            'templist' : templist,
        }
    def before_next_page(self):
        print(self.player.new_scores)
        # print(self.player.ranks_spring)
        # print(type(self.player.ranks_spring))
        helperPayoff_Avgs(self.player.new_scores)
    
# Gets a dictionary
def helperPayoff(ranks):
    # What should this function do?
    # Subtract Actual Rank from Assigned rank
    # Loop over ranks
    # Use child_name or ALPHABET to index into csv with ranks
    # Get the rank and subtract
    total = 0
    for key,value in ranks.items():
        # print(f'{key} {value}')
        with open (os.path.join(pathlib.Path(__file__).parent.resolve(), '25_oct_payoff.csv')) as f:
            csvData = csv.reader(f)
            for col in csvData:
                if key == col[0]:
                    # print(f'Child: {key}, Actual Rank: {col[3]}, Rank: {value}')
                    temp = 0 if value == '' else int(value)
                    total += (int(col[3]) - temp) ** 2
                    break
    constant = 3000
    return constant - total





class fallScores(Page):
    form_model = 'player'
    form_fields = ['ranks_spring']
    def vars_for_template(self):
        for id in idlist:
            self.player.ranks_spring[id] = 0
        return {
            'idlist': ','.join(idlist),
            'templist' : templist,
        }
    def before_next_page(self):
        print(self.player.ranks_spring)
        helperPayoff(self.player.ranks_spring)
        # print(type(self.player.ranks_spring))
        # participant.payoff = 
    


page_sequence = [
    background, 
    introClass,
    classroom, # will have flashcards 
    studentAverages, # will have avg values and fill in the blanks
    fallScores,
    trueAvgs, # will show Flashcards with values and then fill blanks again
]
