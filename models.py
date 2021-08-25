from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)

from jsonfield import JSONField

author = 'Tanmay Mittal'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'mathClass'
    players_per_group = None
    num_rounds = 1
    bg_template = 'mathClass/bg.html'


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    ranks = JSONField(default=dict)
    scores = JSONField(default=dict)
    new_scores = JSONField(default=dict)