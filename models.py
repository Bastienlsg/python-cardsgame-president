import random
import names
import re

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


def value_exist(value):
    """ retourne la valeur uppercase s'il elle éxiste sinon None """
    print("test regex")
    pattern_letter = re.compile("^[VDRAvdra]$")
    pattern_number = re.compile("^[0-9]$")

    if pattern_letter.match(value) or pattern_number.match(value) or value == '10':
        return value.upper()
    else:
        return None


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
        self.role = None
        self.ask_name()

    def give_best_card(self, player, nb_card):
        """ le joueur donne sa meilleur carte au joueur passé en paramètre """
        for x in range(0, nb_card):
            card_to_add = self.hand[len(self.hand) - 1]
            card_to_remove = [card_to_add]
            self.remove_from_hand(card_to_remove)
            player.add_to_hand(card_to_add)
            player.hand.sort()
            print("{} donne ça meilleure carte à {}".format(self.name, player.name))

    def ask_name(self):
        if not isinstance(self, AIPlayer):
            self._name = input("Quel est votre Prénom?")

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
        """ retourne le nombre de carte correspondant au symbole, de le main du joueur """
        nb_cards = 0
        for card in self._hand:
            if card.symbol == card_symbol:
                nb_cards += 1
        return nb_cards


class HumanPlayer(Player):

    def ask_card_to_give(self):
        """ demande au joueur de donner une/des carte(s) de son jeu et retourne la/les carte(s) """
        print('Your current deck is : ')
        print(self.hand)
        print("\n")

        choice = None
        while choice is None or self.has_symbol(choice) < 1:
            choice = input('Quelle carte voulez vous donner ?')
            choice = value_exist(choice)

        return self.play(choice, 1)[0]

    def ask_card_to_play(self):
        choice = None
        print('Your current deck is : ')
        print(self.hand)
        print("\n")
        while choice is None:
            match state:
                # demande au joueur de jouer
                case 1:
                    choice = input('What value do you wish to play ? pass(p)')
                # demande au joueur de donner une carte
                case 2:
                    choice = input('Quelle carte voulez vous donner ?')

            choice = value_exist(choice)
        return choice

    def give_chosen_card(self, player, nb_cards):
        for x in range(0, nb_cards):
            card_to_add = self.ask_card_to_give()
            player.add_to_hand(card_to_add)


class AIPlayer(Player):

    def give_chosen_card(self, player, nb_card):
        for x in range(0, nb_card):
            card_to_add = self.hand[0]
            card_to_remove = [card_to_add]
            self.remove_from_hand(card_to_remove)
            player.add_to_hand(card_to_add)
            player.hand.sort()
            print("{} donne une carte de son choix à {}".format(self.name, player.name))

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
        self.__generate_players(self.ask_player_number())
        self.round = Round()
        self.current_role_available = 1
        self.is_ended = False
        self.list_role = None
        self.generate_list_role()
        self.is_first_game = True

    def ask_player_number(self):
        """ input console pour demander le nombre de joueur total de la partie """
        return int(input('Combien de joueur pour cette partie ?'))

    def card_exchange(self):
        """ procède à l'échange de cartes entres les présidents et les trouducs """
        # si ce n'est pas la première partie alors il y a des rôles et donc des échanges
        if not self.is_first_game:
            # le président et le trouduc échange leur cartes
            for player in self.players:
                if player.role == 1:
                    president = player
                elif player.role == len(self.players):
                    trouduc = player
            president.give_chosen_card(trouduc, 2)
            trouduc.give_best_card(president, 2)
            # s'il y a plus de 4 joueurs, les vices font également leur echange
            if len(self.players) > 3:
                for player in self.players:
                    if player.role == 2:
                        vice_president = player
                    elif player.role == len(self.players) - 1:
                        vice_trouduc = player
                vice_president.give_chosen_card(vice_trouduc, 1)
                vice_trouduc.give_best_card(vice_president, 1)


    def generate_list_role(self):
        """ génere la liste des rôles disponible en fonction du nombre de joueur """
        self.list_role = {1: 'Président'}
        nb_player = len(self.players)
        # si moins de 4 joueurs : trois rôles : président, trouduc, neutre
        if nb_player < 4:
            for x in range(2, nb_player + 1):
                if x == nb_player:
                    self.list_role[x] = "Trouduc"
                else:
                    self.list_role[x] = None

        # si 4 joueurs ou plus : cinq rôles : président + vice, trouduc + vice, neutre
        else:
            self.list_role[2] = 'Vice-Président'
            for x in range(3, nb_player + 1):
                if x == nb_player:
                    self.list_role[x] = "Trouduc"
                elif x == (nb_player - 1):
                    self.list_role[x] = "Vice-Trouduc"
                else:
                    self.list_role[x] = None

    def players_active(self):
        """ retourne le nombre de joueurs actif (encore avec des cartes en main) """
        nb_players_active = 0
        for player in self.players:
            if len(player.hand) > 0:
                nb_players_active += 1
        return nb_players_active

    def set_role(self, id_player):
        """ définit le rôle du joueur envoyé en paramètre en fonction des rôles encore disponible dans list_role du PresidentGame """
        self.players[id_player].role = self.current_role_available
        self.current_role_available += 1

        if self.list_role[self.players[id_player].role] is None:
            print('******** {} n\'a plus de carte et n\'a pas de rôle :-( '.format(self.__players[id_player].name))
        else:
            print('******** {} est {} '.format(self.__players[id_player].name,
                                               self.list_role[
                                                   self.players[id_player].role]))

            # s'il n'y à plus qu'un rôle à attribuer, c'est le trouduc et la partie est terminé
            if self.current_role_available == len(self.players):
                for player in self.players:
                    if len(player.hand) > 0:
                        self.is_ended = True
                        player.role = self.current_role_available
                        print(
                            '******** {} est le trouduc !!! '.format(player.name))

    def new_game(self):
        """ Réinitialise les rôles disponibles, ditribut les cartes, définis is_ended de PresidentGame à False """
        self.current_role_available = 1
        self.distribute_cards()
        self.is_ended = False

    def __generate_players(self, nb_players: int):
        """ Génère un joueur humain et un nombre de joueur IA passé en paramètre """
        self.__players = [HumanPlayer()]
        for _ in range(nb_players - 1):
            self.__players.append(AIPlayer())

    def __generate_cards(self):
        """ Génère un Deck et mélange les cartes """
        self.__deck = Deck()
        self.__deck.shuffle()

    def distribute_cards(self):
        """ Vide les mains des joueurs et distribue les cartes """
        for player in self.__players:
            player.empty_hand()
        self.__generate_cards()
        giving_card_to_player = 0
        nb_players = len(self.__players)
        while len(self.__deck.cards) > 0:
            card = self.__deck.pick_card()
            self.__players[giving_card_to_player].add_to_hand(card)
            giving_card_to_player = (giving_card_to_player + 1) % nb_players
        self.introduction_player()

    def introduction_player(self):
        """ présente les joueurs avec leur nom et leur nombre de cartes """
        for player in self.players:
            print("Dites bonjour à {}, ce joueur possède {} cartes".format(player.name, len(player.hand)))

    # def __generate_round(self):
    #   return self.__round

    def last_one_player(self):
        """ return vrai s'il reste qu'un seul joueur """
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
        """ enlève les cartes de la table, reset le flag "is_started" à False et paramètre "last_player à une valeur qui ne peut pas être égale au "current_player" """
        self.__last_player = -1
        self.__is_started = False
        self.__cards_on_table = None

    def update(self, last_player, plays):
        """ met à jour le last_player et les cartes sur la tables avec les paramètres envoyés, passe le flag is_started du round à True """
        self.__last_player = last_player
        self.__cards_on_table = plays
        self.__is_started = True

    def is_ended(self):
        """ Compare le last_player et le current_player, si c'est le même, retourne True """
        return self.__last_player == self.__current_player

    def set_cards_on_table(self, cards):
        self.__cards_on_table = cards

    def set_current_player(self, value):
        self.__current_player = value

    def set_last_player(self, value):
        self.__last_player = value

    def start(self):
        """ paramètre le flag is_started du round à True """
        self.__is_started = True

    def stop(self):
        """ paramètre le flag is_started du round à False """
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
