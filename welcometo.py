from flask import Flask, request
from random import Random
from string import ascii_lowercase
import time

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "welcometo blah"


@app.route("/user/")
@app.route("/user/<username>")
def show_user_profile(username=None):
    return f"User {escape(username)}"


@app.route("/game/", methods=["GET"])
@app.route("/game/<int:seed>", methods=["GET"])
def game(seed=None):
    if seed is None:
        seed = int(time.time())
    turn = int(request.args.get("turn", 1))
    next_page = f"/game/{seed}?turn={turn + 1}"
    advanced = request.args.get("advanced")
    objs_a = list(range(6 if advanced == "off" else 11))
    objs_b = list(range(6 if advanced == "off" else 11))
    objs_c = list(range(6))
    r = Random(seed)
    r.shuffle(objs_a)
    r.shuffle(objs_b)
    r.shuffle(objs_c)
    objectives = [objs_a[0], objs_b[0], objs_c[0]]
    deck = get_deck()
    r.shuffle(deck)
    for x in range(turn // 26):
        extension = deck[(x - 1) * 27 * 3:(27 * x - 1) * 3]
        r.shuffle(extension)
        deck.extend(extension)
    piles = [[], [], []]
    for (i, card) in enumerate(deck):
        piles[i % 3].append(card)
    symbol_cards = [p[turn - 1] for p in piles]
    number_cards = [p[turn] for p in piles]
    value = "<table><tr>"
    obj_tags = []
    for (i, choice) in enumerate(objectives):
        img = f"/static/card_images/n{i + 1}_{ascii_lowercase[choice]}.png"
        tag = f"<img src=\"{img}\" alt=\"An Objective\" height=272 width=208>"
        obj_tags.append(tag)
    value += "</tr><tr>"
    for card in number_cards:
        number_img = f"/static/card_images/{card.number_face}"
        tag = f"<img src=\"{number_img}\" alt=\"{card.number} flips to {card.symbol}\" height=272 width=208>"
        value += f"<td>{tag}</td>"
    value += f"<td>{obj_tags[0]}</td>"
    value += "</tr><tr>"
    for card in symbol_cards:
        symbol_img = f"/static/card_images/{card.symbol_face}"
        tag = f"<img src=\"{symbol_img}\" alt=\"{card.symbol}\" height=272 width=208>"
        value += f"<td>{tag}</td>"
    value += f"<td>{obj_tags[1]}</td>"
    value += f"</tr><tr><td><a href={next_page}>Next Turn</a></td><td></td><td></td>"
    value += f"<td>{obj_tags[2]}</td>"
    value += "</tr></table>"
    return value


class Card:
    __slots__ = ["number", "symbol"]
    def __init__(self, number: str, symbol: str):
        self.number = number
        self.symbol = symbol

    @property
    def number_face(self):
        return f"{self.number}_{self.symbol}.png"

    @property
    def symbol_face(self):
        return f"{self.symbol}.jpg"


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
    return deck.copy()
