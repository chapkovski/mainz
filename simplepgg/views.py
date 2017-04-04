from . import models
from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range

from .models import Constants


class Demographics(Page):
    form_model = models.Player
    form_fields = ['age',
                   'gender']

    def is_displayed(self):
        return self.subsession.round_number == 1

    def before_next_page(self):
        self.player.participant.vars['gender'] = self.player.gender


class Contribute(Page):
    """Player: Choose how much to contribute"""

    form_model = models.Player
    form_fields = ['contribution']
    timeout_submission = {'contribution': 0}


class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        self.group.set_payoffs()


class Results(Page):
    ...


class FinalResults(Page):
    """Final earnings are shown"""
    def is_displayed(self):
        return self.subsession.round_number == Constants.num_rounds


page_sequence = [
    Demographics,
    # Introduction,
    Contribute,
    ResultsWaitPage,
    Results,
    FinalResults,
]
