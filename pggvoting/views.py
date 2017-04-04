from . import models
from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
import random
from .models import Constants

class ShuffleWaitPage(WaitPage):
    wait_for_all_groups = True

    def is_displayed(self):
        return self.round_number > 1

    def after_all_players_arrive(self):
        losers = []
        new_matrix = self.subsession.get_group_matrix()
        print('OLD MATRIX',new_matrix)
        for g in new_matrix:
            for i, p in enumerate(g):
                if p.participant.vars['smallest']:
                    print('PLAYER IS LOSER:::', p.id_in_subsession)
                    losers.append(g.pop(i))
        losers.reverse()
        print('LOSERS',losers)
        for i, g in enumerate(new_matrix):
            new_matrix[i].append(losers[i])
        print('NEW MATRIX', new_matrix)
        self.subsession.set_group_matrix(new_matrix)
        print('CHECK IF MATRIX IS UPDATED',self.subsession.get_group_matrix())


class Voting(Page):
    form_model = models.Player
    form_fields = ['vote']

    def is_displayed(self):
        return self.round_number > 1 \
            and not self.player.participant.vars['smallest']


class VotingWaitPage(WaitPage):
    def after_all_players_arrive(self):
        votes = self.group.count_votes()
        # if votes


class Contribute(Page):
    """Player: Choose how much to contribute"""

    form_model = models.Player
    form_fields = ['contribution']
    timeout_submission = {'contribution': 0}


class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        self.group.set_payoffs()
        self.group.setsmallest()

class Results(Page):
    ...


class FinalResults(Page):
    """Final earnings are shown"""
    def is_displayed(self):
        return self.subsession.round_number == Constants.num_rounds


page_sequence = [
    ShuffleWaitPage,
    Voting,
    VotingWaitPage,
    Contribute,
    ResultsWaitPage,
    # Results,
    # FinalResults,
]
