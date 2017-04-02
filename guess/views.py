from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants
import random


class Decision(Page):
    form_model = models.Player
    form_fields = ['guess']
    def is_displayed(self):
        print("WE ARE IN INDISPALYED")
        return True

    def vars_for_template(self):
        toguess = random.randint(Constants.minguess, Constants.maxguess)
        self.player.toguess = toguess

    def before_next_page(self):
        self.player.set_payoff()


class Results(Page):
    def vars_for_template(self):
        diff = abs(self.player.guess - self.player.toguess)
        return {'diff':diff}


page_sequence = [
    Decision,
    Results
]
