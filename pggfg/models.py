from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random
from otree.db.models import Model, ForeignKey

from django import forms


# from otree.db.serializedfields import JSONField

doc = """
public good game with some variations depending on session configs:
- punishment stage (for session 4)
- collective sanctions (for session 7)
"""


class Constants(BaseConstants):
    name_in_url = 'pggfg'
    players_per_group = 3
    num_others_per_group = players_per_group - 1
    num_rounds = 2

    instructions_template = 'pggfg/Instructions.html'

    endowment = 100
    efficiency_factor = 2
    punishment_factor = 3
    punishment_limit = int(endowment/punishment_factor)


class Subsession(BaseSubsession):
    punishment = models.BooleanField()

    def before_session_starts(self):
        if 'punishment' in self.session.config:
            self.punishment = self.session.config['punishment']
        else:
            self.punishment = False




class Group(BaseGroup):
    # myjson = JSONField(null=True, doc="""json for saving punishment matrix.

    total_contribution = models.IntegerField()
    average_contribution = models.FloatField()
    individual_share = models.CurrencyField()


    def set_payoffs(self):
        self.total_contribution = sum([p.contribution for p in self.get_players()])
        self.average_contribution = self.total_contribution/ Constants.players_per_group
        self.individual_share = self.total_contribution * Constants.efficiency_factor / Constants.players_per_group
        for p in self.get_players():
            pun_sent = Punishment.objects.filter(group=self,
                                                 sender=p.id_in_group).\
                                                 values_list('punishment_sum',
                                                             flat=True)
            p.punishment_sent = sum(pun_sent)
            pun_recv = Punishment.objects.filter(group=self,
                                                 receiver=p.id_in_group).\
                                                 values_list('punishment_sum',
                                                             flat=True)
            p.punishment_received = sum(pun_recv) * Constants.punishment_factor
            p.payoff = Constants.endowment - p.contribution + \
                self.individual_share - p.punishment_sent -\
                p.punishment_received



class Player(BasePlayer):
    punishment_sent = models.IntegerField()
    punishment_received = models.IntegerField()
    contribution = models.IntegerField(
        min=0, max=Constants.endowment,
        doc="""The amount contributed by the player""",)


for i in range(Constants.players_per_group):
    Player.add_to_class("punishP{}".format(i+1),
                        models.IntegerField(
            verbose_name="Participant {}".format(i+1),
            min=0,
            max=Constants.endowment,
        ))


class Punishment(Model):
    sender = models.IntegerField()
    receiver = models.IntegerField()
    punishment_sum = models.IntegerField()
    group = ForeignKey(Group)
