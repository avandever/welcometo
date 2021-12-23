from flask import Flask, request
from random import Random
from string import ascii_lowercase
import time
from typing import Dict
from urllib.parse import urlencode

app = Flask(__name__)


def url_with_override(url: str, query: Dict[str, str], **overrides):
    """Helper function to produce a url with one or more params updated"""
    new_query = query.copy()
    new_query.update(overrides)
    return f"{url}?{urlencode(new_query)}"


@app.route("/", methods=["GET"])
@app.route("/<int:seed>", methods=["GET"])
def game(seed=None):
    """
    Return a page representing a game state. We rebuild the state every page
    load, with the seed ensuring that things turn out the same across loads.
    If no seed is provided, we set it to the current unix timestamp.
    """
    # seed provides continuity for shuffling
    if seed is None:
        seed = int(time.time())
    # We use this rather than request.url because that may not have seed in it yet
    game_url = f"/{seed}"
    # turn tracks advancement through the game
    query = dict(request.args)
    query.setdefault("turn", 1)
    turn = int(query["turn"])
    plan_statuses = [query.get(key, "open") for key in ["n1", "n2", "n3"]]
    next_page = url_with_override(game_url, query, turn=turn + 1)
    # Set advanced=off in url parameters to exclude advanced plans
    advanced = request.args.get("advanced")
    objs_a = list(range(6 if advanced == "off" else 11))
    objs_b = list(range(6 if advanced == "off" else 11))
    objs_c = list(range(6))
    r = Random(seed)
    # If this happened after deck shuffling we could end up swapping out plans
    r.shuffle(objs_a)
    r.shuffle(objs_b)
    r.shuffle(objs_c)
    objectives = [objs_a[0], objs_b[0], objs_c[0]]
    # This is simple enough
    deck = get_deck()
    r.shuffle(deck)
    pile_size = len(deck) // 3
    piles = [deck[pile_size * x:pile_size * (x + 1)] for x in range(3)]
    # TODO: Implement first goal completed reshuffle
    # This logic simulates flipping the 27th card from each pile over when
    # reshuffling
    for x in range((turn - 1) // 26):
        for pile in piles:
            last_card = pile.pop()
            r.shuffle(pile)
            pile.insert(0, last_card)
    # Here we actually identify the active cards from each pile
    # 26 % 26 = 0, but actually we want to treat turn 26 like turn 26, yet turn 27 like turn 1.
    mod_turn = (turn - 1) % 26 + 1
    if mod_turn == 0:
        mod_turn = 26
    symbol_cards = [p[mod_turn - 1] for p in piles]
    number_cards = [p[mod_turn] for p in piles]
    obj_tags = []
    # We identify the plans here, but don't place them in the html yet because
    # they will be displayed in a single column, not row
    # TODO: Parameterize image height and width
    for (i, choice) in enumerate(objectives):
        status = plan_statuses[i]
        opposite_status = "open" if status == "done" else "done"
        flip_link = url_with_override(game_url, query, **{f"n{i + 1}": opposite_status})
        back = "_back" if status == "done" else ""
        img = f"/static/card_images/n{i + 1}_{ascii_lowercase[choice]}{back}.png"
        tag = f"<a href={flip_link}><img src=\"{img}\" alt=\"An Objective\" height=272 width=208></a>"
        obj_tags.append(tag)
    # TODO: Use templates to build page
    # Building the table as we go is pretty ugly
    value = "<table><tr>"
    # Numbers go on top
    for card in number_cards:
        number_img = f"/static/card_images/{card.number_face}"
        tag = f"<img src=\"{number_img}\" alt=\"{card.number} flips to {card.symbol}\" height=272 width=208>"
        value += f"<td>{tag}</td>"
    # Insert objective n1 at the end of the row
    value += f"<td>{obj_tags[0]}</td>"
    # Start a new row
    value += "</tr><tr>"
    # Symbols go in row 2
    for card in symbol_cards:
        symbol_img = f"/static/card_images/{card.symbol_face}"
        tag = f"<img src=\"{symbol_img}\" alt=\"{card.symbol}\" height=272 width=208>"
        value += f"<td>{tag}</td>"
    # Insert objective n2 at the end of the row
    value += f"<td>{obj_tags[1]}</td>"
    # Third row consists of link to the next page, and third objective - still
    # in column 4
    value += f"</tr><tr><td><a href={next_page}>Next Turn</a></td><td></td><td></td>"
    value += f"<td>{obj_tags[2]}</td>"
    # Wrap up the table
    value += "</tr></table>"
    return value


class Card:
    """Representation of a card"""
    __slots__ = ["number", "symbol"]
    def __init__(self, number: str, symbol: str):
        self.number = number
        self.symbol = symbol

    @property
    def number_face(self):
        """Construct file name for image of card's number side, like 11_pool.png"""
        return f"{self.number}_{self.symbol}.png"

    @property
    def symbol_face(self):
        """Construct file name for image of card's symol side, like pool.png"""
        return f"{self.symbol}.jpg"


    def __str__(self):
        return f"{self.number}/{self.symbol}"


# The deck as designed in the original game
deck = [
    Card(number="one", symbol="investment"),
    Card(number="two", symbol="investment"),
    Card(number="four", symbol="investment"),
    Card(number="five", symbol="investment"),
    Card(number="five", symbol="investment"),
    Card(number="six", symbol="investment"),
    Card(number="seven", symbol="investment"),
    Card(number="seven", symbol="investment"),
    Card(number="eight", symbol="investment"),
    Card(number="eight", symbol="investment"),
    Card(number="nine", symbol="investment"),
    Card(number="nine", symbol="investment"),
    Card(number="ten", symbol="investment"),
    Card(number="eleven", symbol="investment"),
    Card(number="eleven", symbol="investment"),
    Card(number="twelve", symbol="investment"),
    Card(number="fourteen", symbol="investment"),
    Card(number="fifteen", symbol="investment"),
    Card(number="three", symbol="pool"),
    Card(number="four", symbol="pool"),
    Card(number="six", symbol="pool"),
    Card(number="seven", symbol="pool"),
    Card(number="eight", symbol="pool"),
    Card(number="nine", symbol="pool"),
    Card(number="ten", symbol="pool"),
    Card(number="twelve", symbol="pool"),
    Card(number="thirteen", symbol="pool"),
    Card(number="one", symbol="park"),
    Card(number="two", symbol="park"),
    Card(number="four", symbol="park"),
    Card(number="five", symbol="park"),
    Card(number="five", symbol="park"),
    Card(number="six", symbol="park"),
    Card(number="seven", symbol="park"),
    Card(number="seven", symbol="park"),
    Card(number="eight", symbol="park"),
    Card(number="eight", symbol="park"),
    Card(number="nine", symbol="park"),
    Card(number="nine", symbol="park"),
    Card(number="ten", symbol="park"),
    Card(number="eleven", symbol="park"),
    Card(number="eleven", symbol="park"),
    Card(number="twelve", symbol="park"),
    Card(number="fourteen", symbol="park"),
    Card(number="fifteen", symbol="park"),
    Card(number="three", symbol="construction"),
    Card(number="four", symbol="construction"),
    Card(number="six", symbol="construction"),
    Card(number="seven", symbol="construction"),
    Card(number="eight", symbol="construction"),
    Card(number="nine", symbol="construction"),
    Card(number="ten", symbol="construction"),
    Card(number="twelve", symbol="construction"),
    Card(number="thirteen", symbol="construction"),
    Card(number="three", symbol="bis"),
    Card(number="four", symbol="bis"),
    Card(number="six", symbol="bis"),
    Card(number="seven", symbol="bis"),
    Card(number="eight", symbol="bis"),
    Card(number="nine", symbol="bis"),
    Card(number="ten", symbol="bis"),
    Card(number="twelve", symbol="bis"),
    Card(number="thirteen", symbol="bis"),
    Card(number="one", symbol="fence"),
    Card(number="two", symbol="fence"),
    Card(number="three", symbol="fence"),
    Card(number="five", symbol="fence"),
    Card(number="five", symbol="fence"),
    Card(number="six", symbol="fence"),
    Card(number="six", symbol="fence"),
    Card(number="seven", symbol="fence"),
    Card(number="eight", symbol="fence"),
    Card(number="eight", symbol="fence"),
    Card(number="nine", symbol="fence"),
    Card(number="ten", symbol="fence"),
    Card(number="ten", symbol="fence"),
    Card(number="eleven", symbol="fence"),
    Card(number="eleven", symbol="fence"),
    Card(number="thirteen", symbol="fence"),
    Card(number="fourteen", symbol="fence"),
    Card(number="fifteen", symbol="fence"),
]

def get_deck():
    """Get the deck. This is mostly silly."""
    return deck.copy()
