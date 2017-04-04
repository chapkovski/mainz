from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)



class Constants(BaseConstants):
    name_in_url = 'simplepgg'
    players_per_group = 3
    num_others_per_group = players_per_group - 1
    num_rounds = 2
    endowment = 100
    efficiency_factor = 2


class Subsession(BaseSubsession):
    def before_session_starts(self):
        if self.session.config['random']:
            self.group_randomly()



class Group(BaseGroup):
    total_contribution = models.IntegerField()
    average_contribution = models.FloatField()
    individual_share = models.CurrencyField()


    def set_payoffs(self):
        self.total_contribution = sum([p.contribution for p in self.get_players()])
        self.average_contribution = self.total_contribution/ Constants.players_per_group
        self.individual_share = self.total_contribution * Constants.efficiency_factor / Constants.players_per_group
        for p in self.get_players():
            p.payoff = Constants.endowment - p.contribution + self.individual_share


AGE_CHOICES =(
    (1, "<20"),
    (2, "21-30"),
    (3, "31-40"),
    (4, "41-50"),
    (5, "51-60"),
    (6, ">60"),
)


class Player(BasePlayer):
    contribution = models.IntegerField(
        min=0, max=Constants.endowment,
        doc="""The amount contributed by the player""",)
    gender = models.CharField(initial=None,
                        choices=['Male', 'Female'],
                        verbose_name='What is your gender?',
                        widget=widgets.RadioSelect())
    age = models.PositiveIntegerField(verbose_name='What is your age?',
                                        choices=AGE_CHOICES,
                                        initial=None,
                                        widget=widgets.RadioSelect)
