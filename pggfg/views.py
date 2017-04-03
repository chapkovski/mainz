from . import models
from ._builtin import Page, WaitPage
from otree.api import Currency as c, currency_range
# from otree.api import models as m
from .models import Constants
from otree.api import widgets
import random


class Introduction(Page):
    """Description of the game: How to play and returns expected"""
    def is_displayed(self):
        return self.subsession.round_number == 1


class Contribute(Page):
    """Player: Choose how much to contribute"""

    form_model = models.Player
    form_fields = ['contribution']
    timeout_submission = {'contribution':
                          random.randint(0, Constants.endowment)}


class ContributionWaitPage(WaitPage):
    """Waiting till all players make their decisions about the contribution"""
    body_text = "Waiting for other participants to contribute."


class Punishment(Page):
    """here the decision to punish the peers is taken"""
    form_model = models.Player

    def is_displayed(self):
        return self.subsession.punishment

    def punishment_fields(self):
        others = self.player.get_others_in_group()
        fields_to_show = ['punishP{}'.format(p.id_in_group) for p in others]
        return fields_to_show

    def get_form_fields(self):
        fields_to_show = self.punishment_fields()
        return fields_to_show

    """Participants take decision whether to detect the smallest contributor"""
    def before_next_page(self):
        form_data = self.form.data
        for f in self.punishment_fields():
            newrec = models.Punishment(sender=self.player.id_in_group,
                                       receiver=f.strip('punishP'),
                                       group=self.group,
                                       punishment_sum=form_data[f],)
            newrec.save()

class PunishmentWaitPage(WaitPage):
    """Waiting for the group to finish the punishment stage before
    showing them results"""
    def is_displayed(self):
        return self.subsession.punishment



class ResultsWaitPage(WaitPage):

    def after_all_players_arrive(self):
        self.group.set_payoffs()



class Results(Page):
    """Players payoff: How much each has earned in this round"""
    def is_displayed(self):
        return self.subsession.round_number < Constants.num_rounds

    def vars_for_template(self):
        return {
                'total_earnings': Constants.efficiency_factor*self.group.total_contribution,
                }


class FinalWaitPage(WaitPage):
    wait_for_all_groups = True

    def is_displayed(self):
        return self.subsession.round_number == Constants.num_rounds


class FinalResults(Page):
    """Final earnings are shown"""
    def is_displayed(self):
        return self.subsession.round_number == Constants.num_rounds

    def vars_for_template(self):
        return {
        'total_earnings': self.group.total_contribution*Constants.efficiency_factor, }


page_sequence = [
    # Introduction,
    Contribute,
    ContributionWaitPage,
    Punishment,
    PunishmentWaitPage,
    ResultsWaitPage,
    Results,
    FinalWaitPage,
    FinalResults,
]
