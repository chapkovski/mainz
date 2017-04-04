from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)



class Constants(BaseConstants):
    name_in_url = 'pggvoting'
    players_per_group = 3
    num_others_per_group = players_per_group - 1
    num_rounds = 2
    endowment = 100
    efficiency_factor = 2


class Subsession(BaseSubsession):
    def before_session_starts(self):
        for p in self.get_players():
            p.participant.vars['smallest'] = False


class Group(BaseGroup):
    total_contribution = models.IntegerField()
    average_contribution = models.FloatField()
    individual_share = models.CurrencyField()

    def setsmallest(self):
        mincontrib = min([p.contribution for p in self.get_players()])
        smallest = [p for p in self.get_players()
                    if p.contribution == mincontrib][0]
        smallest.participant.vars['smallest'] = True
        allothers = [p for p in self.get_players() if p != smallest]
        for o in allothers:
            o.participant.vars['smallest'] = False

    def count_votes(self):
        return sum([p.vote for p in self.get_players()]
                   if not p.participant.vars['smallest'])

    def set_payoffs(self):
        activeplayers = [p for p in self.get_players() if not p.missinground]
        num_active_players = len(activeplayers)
        self.total_contribution = sum([p.contribution for p in activeplayers])
        self.average_contribution = self.total_contribution/ num_active_players
        self.individual_share = self.total_contribution * Constants.efficiency_factor / num_active_players
        for p in activeplayers:
            p.payoff = Constants.endowment - p.contribution + self.individual_share


class Player(BasePlayer):
    contribution = models.IntegerField(
        min=0, max=Constants.endowment,
        doc="""The amount contributed by the player""",)
    vote = models.BooleanField(initial=False)
    missinground = models.BooleanField(initial=False)
