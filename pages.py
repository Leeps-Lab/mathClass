from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
from otree.api import (models)
import csv 
from django.db import models
import os
import pathlib

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

page_sequence = [
    background, 
    introClass,
    classroom, # will have flashcards 
    studentAverages, # will have avg values and fill in the blanks
    fallScores,
    trueAvgs, # will show Flashcards with values and then fill blanks again
]
