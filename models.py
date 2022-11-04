import random
import names

COLORS = ['♡', '♤', '♧', '♢']
VALUES = {
    '2': 15,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    '10': 10,
    'V': 11,
    'D': 12,
    'R': 13,
    'A': 14
}
ROLES = {
    0: 'Président',
    1: 'Vice-Président',
    2: 'Vice-Trouduc',
    3: 'Trouduc'
}


class Deck:
    """ Deck du jeu de société du Président. """

    def __init__(self):
        self.__cards: list = []
        """ Génération d'un deck de 52 cartes"""
        for (symbol, val) in VALUES.items():
            for color in COLORS:
                new_card = Card(symbol, color)
                self.__cards.append(new_card)

    def shuffle(self) -> None:
        """ Mélanger les cartes de mon deck. """
        random.shuffle(self.__cards)

    def pick_card(self):
        return self.cards.pop(0)

    def __str__(self) -> str:
        return str(self.__cards)

    @property
    def cards(self):
        return self.__cards


class Card:
    __symbol: str
    __value: int
    __color: str

    def __init__(self, symbol: str, color: str):
        """
            Card Constructor.
            attrs:
                symbol: One of the VALUES keys.
                color:  One of the  COLORS values.
        """

        self.__symbol = symbol
        self.__value = VALUES[symbol]
        self.__color = color

    def __lt__(self, other):
        return self.__value < other.value

    def __gt__(self, other):
        return self.__value > other.value

    def __eq__(self, other):
        return self.__value == other.value

    def __ne__(self, other):
        return self.__value != other.value

    def is_eq(self, symbol):
        return self.__value == VALUES[symbol]

    def is_ge(self, symbol):
        return self.__value >= VALUES[symbol]

    def is_le(self, symbol):
        return self.__value <= VALUES[symbol]

    def is_lt(self, symbol):
        return self.__value < VALUES[symbol]

    @property
    def value(self):
        return self.__value

    @property
    def symbol(self):
        return self.__symbol

    def __repr__(self):
        return f"{self.__symbol} {self.__color}"


class Player:
    def __init__(self, player_name=None):
        self._name: str = player_name if player_name is not None else \
            names.get_first_name()
        self._hand: list = []
        # roles: 0 : president, 1 vice president, 2 vice trouduc, 3 trouduc
        self.role = None

    def add_to_hand(self, card: Card):
        self._hand.append(card)
        self._hand.sort()

    def remove_from_hand(self, cards: list):
        for c in cards:
            self._hand.remove(c)

    def empty_hand(self):
        self._hand = []

    @property
    def hand(self):
        return self._hand

    @property
    def name(self):
        return self._name

    def play(self, symbol, nb_cards) -> list:
        """
        Remove from the hand of the player, all cards having a corresponding symbol.
        Args:
            symbol: The symbol to look for.

        Returns: The cards removed from the hand of the player. It will return an empty array if
        nothing is found.

        """
        # cards_played = [card for card in self._hand if card.symbol == symbol and len(cards_played) <= nb_cards]
        cards_played = []
        for card in self._hand:
            if card.symbol == symbol and len(cards_played) < nb_cards:
                cards_played.append(card)

        self.remove_from_hand(cards_played)
        return cards_played

    def __repr__(self):
        return f"{self.name}\t: {self.hand}"

    def has_symbol(self, card_symbol) -> int:
        nb_cards = 0
        for card in self._hand:
            if card.symbol == card_symbol:
                nb_cards += 1
        return nb_cards


class AIPlayer(Player):
    def play(self, choice, nb_cards: int) -> list:
        """
        Play a card correspondig to what has been played on the table.
        TODO: Implement an AI
        Args:
            choice: The minimum card value to play.
            nb_cards: The number of cards to play.

        Returns: An array of cards to play.

        """
        # if choice == 0:
        cards_played = []

        best_choice = None
        for index, card in enumerate(self.hand):
            if best_choice is None and card.is_ge(choice) and \
                    self.has_symbol(card.symbol) >= nb_cards:
                cards_played = self._hand[index:index + nb_cards]
                best_choice = card.symbol

        self.remove_from_hand(cards_played)
        return cards_played if best_choice is not None else []


class PresidentGame:
    def __init__(self, nb_players: int = 3):
        self.__generate_players(nb_players)
        self.round = Round()
        self.current_role_available = 0
        self.is_ended = True

    def players_active(self):
        nb_players_active = 0
        for player in self.players:
            if len(player.hand) > 0:
                nb_players_active += 1
        return nb_players_active

    def set_role(self, id_player):
        # s'il y a moins de 4 joueurs, pas de vice president ou vice trouduc
        if len(self.__players) < 4:
            # attribution des roles 0: president  3: trouduc
            if self.current_role_available == 0:
                self.players[id_player].role = 0
                self.current_role_available = 3
            elif self.current_role_available == 3 and self.players_active() == 1:
                self.players[id_player].role = 3
                # l'attribution du role trouduc met fin à la partie
                self.is_ended = True
                self.current_role_available = 0

        # s'il y a 4 joueurs ou plus, on inclus les vis
        if len(self.__players) >= 4:
            # attribution des roles 0: president  1: Vice president  2: vice trouduc  3: trouduc
            if self.current_role_available == 0:
                self.players[id_player].role = 0
                self.current_role_available = 1
            elif self.current_role_available == 1:
                self.players[id_player].role = 1
                self.current_role_available = 2
            elif self.current_role_available == 2 and self.players_active() == 1:
                self.players[id_player].role = 2
                self.current_role_available = 3
            elif self.current_role_available == 3 and self.players_active() == 1:
                self.players[id_player].role = 3
                self.is_ended = True
                self.current_role_available = 0

        if self.players[id_player] is None:
            print('**********************************************\n{} n\'a plus de carte et n\'a pas de rôle :-( '
                  '\n**********************************************' .format(self.__players[id_player].name))
        else:
            print('**********************************************\n{} est {} '
                  '!!!\n**********************************************' .format(self.__players[id_player].name,
                                                                                ROLES[self.__players[id_player].role]))

    def new_game(self):
        self.current_role_available = 0
        self.distribute_cards()

    def __generate_players(self, nb_players: int):
        self.__players = [Player()]
        for _ in range(nb_players - 1):
            self.__players.append(AIPlayer())

    def __generate_cards(self):
        self.__deck = Deck()
        self.__deck.shuffle()

    def distribute_cards(self):
        for player in self.__players:
            player.empty_hand()
        self.__generate_cards()
        giving_card_to_player = 0
        nb_players = len(self.__players)
        while len(self.__deck.cards) > 45:
            card = self.__deck.pick_card()
            self.__players[giving_card_to_player].add_to_hand(card)
            giving_card_to_player = (giving_card_to_player + 1) % nb_players
        self.introduction_player()

    def introduction_player(self):
        for player in self.players:
            print("Dites bonjour à {}, ce joueur possède {} cartes".format(player.name, len(player.hand)))

    # def __generate_round(self):
    #   return self.__round

    def last_one_player(self):
        players_left = 0
        for player in self.__players:
            if len(player.hand) > 0:
                players_left += 1
        return players_left <= 1

    @property
    def players(self):
        return self.__players

    @property
    def ai_players(self):
        return self.__players[1:]

    @property
    def main_player(self):
        """ Main player is player 0 """
        return self.__players[0]


# @property
# def round(self):
#   return self.__round


class Round:

    def __init__(self):
        self.__is_started = False
        self.__cards_on_table = None
        self.__current_player = 0
        self.__last_player = 1

    def next_round(self):
        self.__last_player = -1
        self.__is_started = False
        self.__cards_on_table = None

    def update(self, last_player, plays):
        self.__last_player = last_player
        self.__cards_on_table = plays
        self.__is_started = True

    def is_ended(self):
        return self.__last_player == self.__current_player

    def set_cards_on_table(self, cards):
        self.__cards_on_table = cards

    def set_current_player(self, value):
        self.__current_player = value

    def set_last_player(self, value):
        self.__last_player = value

    def start(self):
        self.__is_started = True

    def stop(self):
        self.__is_started = False

    @property
    def current_player(self):
        return self.__current_player

    @property
    def last_player(self):
        return self.__last_player

    @property
    def cards_on_table(self):
        return self.__cards_on_table

    @property
    def is_started(self):
        return self.__is_started
