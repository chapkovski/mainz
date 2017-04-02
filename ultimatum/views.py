from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class Intro(Page):
    pass


class Offer(Page):
    form_model = models.Group
    form_fields = ['offer']
    
    def is_displayed(self):
        return self.player.role() == 'Proposer'

    def vars_for_template(self):
        ...


class OfferWaitPage(WaitPage):
    title_text = "You are Responder"
    body_text = "Please wait while the Proposer decides how many tokens he \
    or she will offer to you..."


class Accept(Page):
    form_model = models.Group
    form_fields = ['accept']

    def is_displayed(self):
        return self.player.role() == 'Responder'

    def vars_for_template(self):
        return {'offer_text': "The Proposer offers you {} points. Would you like \
         to accept or reject this offer?".format(self.group.offer)}


class ResultsWaitPage(WaitPage):
    title_text = "You are Proposer"
    body_text = "Please wait while the Responder decides about accepting \
    or rejecting your offer..."

    def after_all_players_arrive(self):
        self.group.set_payoffs()


class Results(Page):
    def vars_for_template(self):
        return {'accept': 'Accept' if self.group.accept else 'Reject'}


page_sequence = [
    Intro,
    Offer,
    OfferWaitPage,
    Accept,
    ResultsWaitPage,
    Results
]
