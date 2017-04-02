from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'ultimatum'
    players_per_group = 2
    num_rounds = 1
    endowment = 10


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    offer = models.FloatField(min=0,
                              max=Constants.endowment,
                              widget=\
                              widgets.SliderInput(attrs={'step': '0.1'}))
    accept = models.BooleanField(choices=[(False,'Reject'),(True,'Accept')],
                                widget=widgets.RadioSelectHorizontal())

    def set_payoffs(self):
        proposer = self.get_player_by_role('Proposer')
        responder = self.get_player_by_role('Responder')
        proposer.payoff = (Constants.endowment - self.offer) * self.accept
        responder.payoff = self.offer * self.accept


class Player(BasePlayer):
    def role(self):
        if self.id_in_group == 1:
            return 'Proposer'
        if self.id_in_group == 2:
            return 'Responder'
