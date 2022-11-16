import random
import time

import names
import re
from tkinter import *
from PIL import Image, ImageTk

from PIL import ImageTk

CARD_PATH = 'assets/cards/'

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
    pattern_letter = re.compile("^[VDRAvdrapP]$")
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
        """ supprime la première carte du deck et la retourne """
        return self.cards.pop(0)

    def __str__(self) -> str:
        return str(self.__cards)

    def __len__(self):
        return len(self.__cards)

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

    def file_name(self):
        """ retourne le nom de fichier correspondant à l'image de la carte """
        file_name = ''
        match self.__symbol:
            case '2':
                file_name += '2_of_'
            case '3':
                file_name += '3_of_'
            case '4':
                file_name += '4_of_'
            case '5':
                file_name += '5_of_'
            case '6':
                file_name += '6_of_'
            case '7':
                file_name += '7_of_'
            case '8':
                file_name += '8_of_'
            case '9':
                file_name += '9_of_'
            case '10':
                file_name += '10_of_'
            case 'V':
                file_name += 'jack_of_'
            case 'D':
                file_name += 'queen_of_'
            case 'R':
                file_name += 'king_of_'
            case 'A':
                file_name += 'ace_of_'
        match self.__color:
            case '♡':
                file_name += 'hearts.png'
            case '♤':
                file_name += 'spades.png'
            case '♧':
                file_name += 'clubs.png'
            case '♢':
                file_name += 'diamonds.png'
        return file_name

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

    @property
    def color(self):
        return self.__color

    def __repr__(self):
        return f"{self.__symbol} {self.__color}"


class Player:
    def __init__(self, player_name=None):
        self._name: str = player_name if player_name is not None else \
            names.get_first_name()
        self._hand: list = []
        self.role = None
        self.card_to_give = 0

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
        """ demande le nom au joueur humain et l'applique à Player.name """
        if not isinstance(self, AIPlayer):
            self._name = input("Quel est votre Prénom?")

    def add_to_hand(self, card: Card):
        """ ajoute une carte à la main du joueur """
        self._hand.append(card)
        self._hand.sort()

    def remove_from_hand(self, cards: list):
        """ supprime la liste de carte passé en paramètre de la main du joueur"""
        for c in cards:
            self._hand.remove(c)

    def empty_hand(self):
        """ vide la main du joueur"""
        self._hand = []

    @property
    def hand(self):
        return self._hand

    @property
    def name(self):
        return self._name

    def set_name(self, name):
        self._name = name

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
        """ demande au joueur la carte qu'il veut joueur, retourne le symbol """
        choice = None
        print('Your current deck is : ')
        print(self.hand)
        print("\n")
        while (choice is None or self.has_symbol(choice) < 1) and choice != "P":
            choice = input('Quelle carte voulez vous jouer  (passer : p)?')
            choice = value_exist(choice)

        return choice

    def ask_number_of_card_to_play(self, symbol):
        """ demande au joueur humain le nombre de fois qu'il veut joueur la carte en paramètre
         retourne la quantité qu'il veut joueur"""
        nb_card = None
        while nb_card is None or nb_card > self.has_symbol(symbol):
            try:
                nb_card = int(input("Combien de {} voulez vous jouer ?".format(symbol)))
            except:
                nb_card = None
        return nb_card

    def give_chosen_card(self, player, nb_cards):
        """
        for x in range(0, nb_cards):
            card_to_add = self.ask_card_to_give()
            player.add_to_hand(card_to_add)
            """


class AIPlayer(Player):

    def give_chosen_card(self, player, nb_card):
        """ l'ia donne ses (nb_cards) moins bonne cartes au joueur passé en paramètre  """
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


def ask_player_number():
    """ input console pour demander le nombre de joueur total de la partie """
    nb_player = None
    while nb_player is None or nb_player < 3 or nb_player > 8:
        try:
            nb_player = int(input('Combien de joueur pour cette partie ?'))
        except:
            nb_player = None
    return nb_player


class PresidentGame:
    def __init__(self, nb_players: int = 3):
        self.__generate_players(nb_players)
        self.distribute_cards()
        self.round = Round()
        self.current_role_available = 1
        self.is_ended = False
        self.list_role = None
        self.generate_list_role()
        self.is_first_game = True
        self.message = None

    def next_player(self):
        """
        print(self.players)
        while not self.round.is_ended() and not self.last_one_player():
            # si le joueur à encore des cartes en main
            if len(self.players[self.round.current_player].hand) > 0:
                # vérification du type de joueur : humain ou IA

                if not isinstance(self.players[self.round.current_player], AIPlayer):
                    # c'est l'humain qui joue
                    self.human_play()
                else:
                    # C'est à L'IA de jouer
                    self.ia_play()

                # si le joueur ou l'iA vient de finir sa main, un role lui est attribué
                if len(self.players[self.round.current_player].hand) < 1:
                    self.set_role(self.round.current_player)
"""
        self.round.set_current_player((self.round.current_player + 1) % len(self.players))
        if len(self.round.last_play()) > 0:
            self.test_rules()

    def ia_play(self):
        """ fait jouer l'ia en fonction de ce qu'il y a dans self.round.last_play(),
        si l'ia joue en premier, il joue comme s'il y avait un 3 sur la table"""
        plays = []
        current_player = self.players[self.round.current_player]

        if len(current_player.hand) > 0:
            if self.round.is_started:
                plays = self.players[self.round.current_player].play(self.round.last_play()[0].symbol,
                                                                     len(self.round.last_play()))
            else:
                plays = self.players[self.round.current_player].play('3', 1)
            # si le nombre de carte joué est supèrieur à 0 le dernier joueur ayant joué est le joueur actuel
            if len(plays) > 0:
                self.round.update(self.round.current_player, plays)
            if len(current_player.hand) == 0:
                self.set_role(self.round.current_player)

        print(f"{self.players[self.round.current_player].name} plays \t {plays}")

    def human_play(self):
        """
        fonction pour la version terminal
        demande au joueur de sélectionner une carte ou passer, vérification que le joueur peut jouer la sélection
        """
        current_player = self.players[self.round.current_player]
        # print('Your current deck is : ')
        # print(self.main_player.hand)
        # print("\n")
        # si il y à déjà des cartes en jeux
        # le joueur est contraint de jouer un certain nombre de cartes
        # et une valeur minimum
        if self.round.is_started:
            choice = None
            choice_nb_cards = 0
            # tant que la valeur jouée n'est pas supérieur à la valeur de la table
            # et que la valeur en question n'est pas en nombre supérieur ou égale dans le jeu du joueur
            # par rapport au nombre de cartes sur la table, on demande une valeur
            while choice == '' or choice is None or \
                    not (self.round.last_play()[0].is_le(choice) and len(self.round.last_play()) <=
                         self.players[
                             self.round.current_player].has_symbol(choice)):
                choice = current_player.ask_card_to_play()
                if choice == 'P':
                    break
                choice_nb_cards = len(self.round.last_play())
            # il n'y a pas de carte en jeu, pas de contrainte de valeur ou de nombre de cartes
        else:
            choice = '0'
            choice_nb_cards = 0
            while self.main_player.has_symbol(choice) == 0:
                choice = current_player.ask_card_to_play()
            # si le joueur à plusieur fois la même carte, on lui demande le nombre de cartes
            # qu'il veut poser
            if current_player.has_symbol(choice) != 1:
                # tant que le nombre demandé est supérieur au nombres de cartes possédé,
                # on refait la demande
                while choice_nb_cards == '' or self.main_player.has_symbol(
                        choice) < choice_nb_cards or choice_nb_cards < 1:
                    choice_nb_cards = current_player.ask_number_of_card_to_play(choice)
            # le joueur à la carte en un seul exemplaire, on ne demande pas le nombre de
            # cartes qu'il veut poser
            else:
                choice_nb_cards = 1

        plays = self.main_player.play(choice, choice_nb_cards)
        if len(plays) > 0:
            self.round.update(self.round.current_player, plays)
        print(f"You play {plays}")

    def set_first_player(self):
        """ configure self.round.current_player en fonction de qui est le président ou qui a la dame de coeur """
        if not self.is_first_game:
            for player in self.players:
                if player.role == 1:
                    self.round.set_current_player(self.players.index(player))
                    self.message = "le président est {}, à lui/elle de commencer !!!".format(player.name)
                    print("le président est {}, à lui/elle de commencer !!!".format(player.name))
        else:
            for player in self.players:
                for card in player.hand:
                    if card.symbol == "D" and card.color == '♡':
                        self.round.set_current_player(self.players.index(player))
                        self.message = "{} a la dame de coeur, à lui/elle de commencer !!".format(player.name)
                        print("{} a la dame de coeur, à lui/elle de commencer !!".format(player.name))

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
            if len(self.players) > 4:
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
        # si moins de 5 joueurs : trois rôles : président, trouduc, neutre
        if nb_player < 5:
            for x in range(2, nb_player + 1):
                if x == nb_player:
                    self.list_role[x] = "Trouduc"
                else:
                    self.list_role[x] = None

        # si 5 joueurs ou plus : cinq rôles : président + vice, trouduc + vice, neutre
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

        if self.list_role[self.players[id_player].role] == "Président":
            self.players[id_player].card_to_give = 2

        if self.list_role[self.players[id_player].role] == "Vice-Président":
            self.players[id_player].card_to_give = 1

        self.is_first_game = False

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
            presentation = "Dites bonjour à {}, ce joueur possède {} cartes".format(player.name, len(player.hand))
            return presentation

    # def __generate_round(self):
    #   return self.__round

    def last_one_player(self):
        """ return vrai s'il reste qu'un seul joueur """
        players_left = 0
        for player in self.__players:
            if len(player.hand) > 0:
                players_left += 1
        return players_left <= 1

    def test_rules(self):
        """ test les différentes règles du jeu """
        # si quelqu'un joue un ou plusieurs 2, le tour est fini et il prend la main
        if self.round.last_play()[0].symbol == "2":
            self.round.set_current_player(self.round.last_player)
            self.message = ("{} a joué un 2 et remporte la main !!".format(
                self.players[self.round.last_player].name))
            self.round.set_current_player(self.round.last_player)
            print("{} a joué un 2 et remporte la main !!".format(
                self.players[self.round.last_player].name))
            self.round.set_current_player(self.round.last_player)
            return

        # si 4 carte de symbole identique son posé sur le dessus du paquet, le joueur ayant posé la dernière carte remporte la main
        i = 0
        nb_card_same_symbol = 0
        symbol = self.round.last_play()[0].symbol
        while i < 4 and self.round.nb_cards_on_table() > 3:
            for sets in self.round.cards_on_table:
                for card in sets:
                    if card.symbol == symbol:
                        nb_card_same_symbol += 1
                    i += 1
        if nb_card_same_symbol == 4:
            self.message = ("les quatres même cartes ont été joué d'affilé, {} remporte la main !!!".format(
                self.players[self.round.last_player].name))
            self.round.set_current_player(self.round.last_player)

            print("les quatres même cartes ont été joué d'affilé, {} remporte la main !!!".format(
                self.players[self.round.last_player].name))
            self.round.set_current_player(self.round.last_player)
            return

        # si une carte de même symbole est joué, le joueur suivant passe sont tour
        if self.round.last_play()[0].symbol == self.round.cards_on_table[len(self.round.cards_on_table) - 2][
            0].symbol and len(self.round.cards_on_table) > 1:
            print("{} passe son tour :-(".format(self.players[self.round.current_player].name))
            self.round.set_current_player((self.round.current_player + 1) % len(self.players))

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
        self.__cards_on_table = []
        self.__current_player = 0
        self.__last_player = 1

    def nb_cards_on_table(self):
        """ retourne le nombre de cartes en jeu """
        nb_cards = 0
        for sets in self.__cards_on_table:
            for card in sets:
                nb_cards += 1
        return nb_cards

    def next_round(self):
        """ enlève les cartes de la table, reset le flag "is_started" à False et paramètre "last_player à une valeur qui ne peut pas être égale au "current_player" """
        self.__last_player = -1
        self.__is_started = False
        self.__cards_on_table = []

    def last_play(self):
        """ retourne la/les dernière cartes joué """
        if len(self.__cards_on_table) == 0:
            return []
        return self.cards_on_table[len(self.__cards_on_table) - 1]

    def update(self, last_player, plays):
        """ met à jour le last_player et les cartes sur la tables avec les paramètres envoyés, passe le flag is_started du round à True """
        self.__last_player = last_player
        self.__cards_on_table.append(plays)
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


class Window(Tk):

    def __init__(self):
        super().__init__()
        self.title('Jeu du président')
        self.configure(bg='black')
        self.geometry('1600x900')
        self.resizable(height=False, width=False)
        self.bg_menu = PhotoImage(file="assets/president_game.png")
        self.bg_play = PhotoImage(file="assets/poker_table.png")

        self.bg_home = Label(self, image=self.bg_menu)
        self.bg_home.place(x=0, y=0)
        self.bg_home.place()

        #### home_page
        self.home = Frame(self, bg="black")

        self.btn_play = Button(self.home, text="Jouer",
                               command=lambda: [self.hide_home_page(), self.display_play_page()])
        self.btn_play.pack()
        self.btn_parameters = Button(self.home, text="Paramètres",
                                     command=lambda: [self.hide_home_page(), self.display_parameters_page()])
        self.btn_parameters.pack()

        #### parameters_page
        self.parameters = Frame(self, bg="black")

        # resolutions
        self.res_label = Label(self.parameters, text="Quelle résolution souhaitez-vous ?")
        self.res_label.pack()

        self.btn_res_1600x900 = Button(self.parameters, text="1600x900",
                                       command=lambda: self.set_resolution('1600x900'))
        self.btn_res_1600x900.pack()
        self.btn_res_1440x900 = Button(self.parameters, text="1440x900",
                                       command=lambda: self.set_resolution('1440x900'))
        self.btn_res_1440x900.pack()
        self.btn_res_1536x864 = Button(self.parameters, text="1536x864",
                                       command=lambda: self.set_resolution('1536x864'))
        self.btn_res_1536x864.pack()
        self.btn_res_1366x768 = Button(self.parameters, text="1366x768",
                                       command=lambda: self.set_resolution('1366x768'))
        self.btn_res_1366x768.pack()

        # paramètres du jeu

        # self.name_label = Label(self.parameters, text="Quel prénom souhaitez-vous utiliser pour vos parties ?")
        # self.name_label.pack()

        # self.input_name = Entry(self.parameters)
        # self.input_name.pack()

        # self.btn_validate_parameters = Button(self.parameters, text="Valider", command=lambda: self.set_parameters())
        # self.btn_validate_parameters.pack(side=TOP, padx=50, pady=10)

        self.back_btn = Button(self.parameters, text=u'\u21a9',
                               command=lambda: [self.display_home_page(), self.hide_parameters_page()])
        self.back_btn.pack(anchor="w", side="bottom", padx=10, pady=10)

        #### play_page

        # game parameter

        self.bg_game = Label(self, image=self.bg_play)

        self.play = Frame(self, bg="black")

        self.label_player_name = Label(self.play, text="Votre prénom :")
        self.label_player_name.pack(pady=5)

        self.input_player_name = Entry(self.play)
        self.input_player_name.pack(pady=5)

        self.player_label = Label(self.play, text="Combien de joueur souhaitez-vous dans vos parties ?(defaut = 3)")
        self.player_label.pack(pady=5)

        self.input_nb_player = Entry(self.play)
        self.input_nb_player.pack(pady=5)

        self.btn_validate_players = Button(self.play, text="Valider", command=lambda: self.launch_game())
        self.btn_validate_players.pack(side=TOP, padx=50, pady=10)

        self.back_btn = Button(self.play, text=u'\u21a9',
                               command=lambda: [self.display_home_page(), self.hide_play_page()])
        self.back_btn.pack(anchor="w", side="bottom", padx=10, pady=10)

        # play desk

        self.play_desk = Frame(self, bg="black")

        self.bg_game_desk = Label(self.play_desk, image=self.bg_play)
        self.bg_game_desk.place(x=0, y=0)

        self.label_player_deck = Label(self.play_desk)
        self.label_player_deck.pack(pady=5)

        self.player_hand = Frame(self.play_desk)
        self.player_hand.pack(pady=5)

        self.label_temporary = Label(self.play_desk)
        self.label_temporary.pack(pady=5)

        self.info_message = Label(self.play_desk, text="message d'information")
        self.info_message.pack(pady=5)

        self.input_card_played = Entry(self.play_desk)
        self.input_card_played.pack(pady=5)

        self.label_nb_carte = Label(self.play_desk, text="nombre de cartes")
        self.label_nb_carte.pack(pady=5)

        self.input_nb_card_played = Entry(self.play_desk)
        self.input_nb_card_played.pack(pady=5, )

        self.button_card_played = Button(self.play_desk, text="Jouer", command=lambda: self.validate_card())
        self.button_card_played['state'] = 'disabled'
        self.button_card_played.pack(pady=20)

        self.button_give_card = Button(self.play_desk, text="Donner une carte", command=lambda: self.give_card())

        self.card_on_table = Frame(self.play_desk)
        self.card_on_table.pack(pady=20)

        self.ai_players_frame = Frame(self.play_desk, bg='black')
        self.ai_players_frame.pack()

        # player frame / end game screen

        self.end_game_frame = Frame(self)

        self.frame_roles = Frame(self)
        self.frame_roles.pack(pady=5)

        self.btn_replay = Button(self.end_game_frame, text="Rejouer !!", command=lambda: self.launch_game())
        self.btn_replay.pack(pady=5)

        self.ai_players = []

        self.input_res = None
        self.messagebox = None

        self.president_game = None

        self.display_home_page()

    def display_home_page(self):
        """ affiche la page d'accueil"""
        self.home.pack()

    def display_play_page(self):
        """ affiche la page des paramètres d'avant jeu"""
        self.bg_game.place(x=0, y=0)
        self.play.pack()

    def launch_game(self, duration=4500):
        """ lance une nouvelle partie
        paramètre une nouvelle partie avec le nombre de joueur demandé, le nom du joueur indiqué, sinon aléatoire
        """
        if self.president_game is None:

            try:
                nb_player = int(self.input_nb_player.get())
                self.president_game = PresidentGame(nb_player)
            except:
                self.president_game = PresidentGame()
            name = self.input_player_name.get()
            if name != '':
                self.president_game.main_player.set_name(name)
            self.generate_ai_player()
        else:
            self.play_desk.pack()
            self.btn_replay.pack_forget()
            self.president_game.new_game()
            self.update_ai_players()

        print(self.president_game.players)

        self.information = "Bonjour {name} la partie est configuré pour {number} joueur(s) {name_information}".format(
            name="joueur" if self.input_player_name.get() == "" else self.input_player_name.get(),
            number=self.input_nb_player.get(),
            name_information="Vous souhaitez changer de pseudo ? Allez dans les paramètres" if self.input_player_name.get() == "" else "")
        self.info_label = Label(self, text=self.information)
        self.info_label.pack()
        self.info_label.after(duration, self.info_label.destroy)

        self.play.pack_forget()
        self.update_player_hand()
        # self.play_desk.pack(side=BOTTOM, pady=50)
        self.play_desk.pack(side='top', fill='both', expand='true')

        self.president_game.set_first_player()
        print("set_first_player")

        print("first game : {}".format(self.president_game.is_first_game))
        if self.president_game.main_player.role is not None:
            print('mewsage role')
            match self.president_game.list_role[self.president_game.main_player.role]:
                case "Président":
                    self.info_message.configure(text="Vous êtes Président, donnez deux cartes : ")
                case "Vice-Président":
                    self.info_message.configure(text="Vous êtes Vice-Président, donnez une cartes : ")
                case "Vice-Trouduc":
                    self.info_message.configure(text="Vous êtes Vice-Trouduc, vous avez donné votre meilleurs carte : ")
                case "Trouduc":
                    self.info_message.configure(text="Vous êtes Trouduc, vous avez donné vos deux meilleurs cartes : ")

            role = self.president_game.list_role[self.president_game.main_player.role]

            if role == "Président" or role == "Vice-Président":

                self.button_give_card.pack(pady=5)

                self.button_card_played.pack_forget()
                self.input_nb_card_played.pack_forget()
                self.label_nb_carte.pack_forget()
                self.input_nb_card_played.pack_forget()
                self.card_on_table.pack_forget()
                self.ai_players_frame.pack_forget()

        else:

            while self.president_game.round.current_player != 0 and self.president_game.players_active() > 1:
                self.president_game.ia_play()
                self.president_game.next_player()
                if self.president_game.round.is_ended():
                    self.president_game.round.next_round()
                    self.temporary_message()
                self.update_ai_players()
                self.update_card_on_table()

            self.info_message.configure(text='Quelle carte voulez vous jouer (passer: p)?')
            self.button_card_played['state'] = 'normal'

    def generate_ai_player(self):
        """ génère l'affichage des joueurs et leur nombre de cartes """
        for player in self.president_game.players:
            label = Label(self.ai_players_frame, text='{} : {} cartes'.format(player.name, len(player.hand)))
            label.pack()
            self.ai_players.append(label)

        self.label_player_deck.configure(text="voici votre jeu {} :".format(self.president_game.main_player.name))

    def give_card(self):
        """ demande au joueur de donné des cartes s'il a à les choisir """
        value = value_exist(self.input_card_played.get())
        role = self.president_game.list_role[self.president_game.main_player.role]

        if value is not None and value != 'P' and self.president_game.main_player.has_symbol(value) > 0:
            card = self.president_game.main_player.play(value, 1)[0]
            match role:
                case "Président":
                    for player in self.president_game.players:
                        if self.president_game.list_role[player.role] == "Trouduc":
                            player.add_to_hand(card)
                case "Vice-Président":
                    for player in self.president_game.players:
                        if self.president_game.list_role[player.role] == "Vice-Trouduc":
                            player.add_to_hand(card)

            self.president_game.main_player.card_to_give -= 1
            if self.president_game.main_player.card_to_give == 0:
                self.button_give_card.pack_forget()

                self.label_nb_carte.pack(pady=5)
                self.input_nb_card_played.pack(pady=5)
                self.input_nb_card_played.pack(pady=5)
                self.button_card_played.pack(pady=5)
                self.card_on_table.pack(pady=5)
                self.ai_players_frame.pack(pady=5)

                self.info_message.configure(text="Quelle carte voulez vous jouer (passer : P)?")

                self.president_game.card_exchange()

                self.president_game.set_first_player()
                if self.president_game.round.current_player != 0:
                    while self.president_game.round.current_player != 0 and self.president_game.players_active() > 1:
                        self.president_game.ia_play()
                        self.president_game.next_player()
                        if self.president_game.round.is_ended():
                            self.president_game.round.next_round()
                            self.temporary_message()
                        self.update_ai_players()
                        self.update_card_on_table()

            self.update_player_hand()
            self.update_card_on_table()


    def validate_card(self):
        """ bouton principale de jeu
         récupère le symbol et la nombre de carte que le joueur demande puis vérifie s'il peut les jouer
         """
        main_player = self.president_game.main_player
        # récupération des valeurs
        value = self.input_card_played.get()
        choice = value_exist(value)
        try:
            nb_card = int(self.input_nb_card_played.get())
        except:
            nb_card = None

        plays = []
        if choice is not None:

            # si le round a deja commencé, vérification que le joueur peut jouer les cartes demandés
            if len(self.president_game.round.last_play()) > 0:
                print('round already started !')
                if choice == 'P':
                    print('vous passez votre tour')

                elif self.president_game.round.last_play()[0].is_le(choice) and len(
                        self.president_game.round.last_play()) <= self.president_game.players[
                    self.president_game.round.current_player].has_symbol(choice):
                    plays = main_player.play(choice, len(self.president_game.round.last_play()))

            # le joueur joue ce qu'il veut
            else:
                print('first player to play !')
                if nb_card is not None and main_player.has_symbol(choice) >= nb_card:
                    plays = main_player.play(choice, nb_card)

            if len(plays) > 0:
                self.president_game.round.update(self.president_game.round.current_player, plays)
            print(f"You play {plays}")

            if len(plays) > 0 or choice == 'P':
                self.president_game.next_player()

            self.input_card_played.delete(0, 'end')
            self.input_nb_card_played.delete(0, 'end')
            self.update_player_hand()

            if len(self.president_game.main_player.hand) == 0:
                self.president_game.set_role(0)
                self.end_game()
                return

            if self.president_game.round.is_ended():
                self.president_game.round.next_round()
                self.temporary_message()

            if self.president_game.round.is_ended():
                for widget in self.card_on_table.winfo_children():
                    widget.destroy()
            if not self.president_game.round.is_ended():
                while self.president_game.round.current_player != 0 and self.president_game.players_active() > 1:
                    self.president_game.ia_play()
                    self.president_game.next_player()
                    if self.president_game.round.is_ended():
                        self.president_game.round.next_round()
                        self.temporary_message()
                    self.update_ai_players()

            self.update_card_on_table()
            self.update_role()

            if self.president_game.players_active() == 1:
                self.end_game()

    def end_game(self):
        """ lorsque le jouer n'a plus de carte, les ia finissent la parties seul"""
        while self.president_game.players_active() > 1:
            self.president_game.ia_play()
            self.president_game.next_player()
            if self.president_game.round.is_ended():
                self.temporary_message()

        self.president_game.round.next_round()

        self.update_ai_players()
        self.update_card_on_table()
        self.update_role()

        self.play_desk.pack_forget()
        self.end_game_frame.pack()
        self.btn_replay.pack()

    def update_role(self):
        """ met à jour l'affichage du rôle des jouers """
        for child in self.frame_roles.winfo_children():
            child.destroy()
        for player in self.president_game.players:
            if player.role is not None:
                if self.president_game.list_role[player.role] is not None:
                    label = Label(self.frame_roles,
                                  text="{} : {}".format(player.name, self.president_game.list_role[player.role]))
                    label.pack(pady=5)

    def update_player_hand(self):
        """ met à jour l'affichage de la main du jouer """
        for child in self.player_hand.winfo_children():
            child.destroy()
        for card in self.president_game.main_player.hand:
            path = CARD_PATH + card.file_name()

            image1 = Image.open(path)
            image1 = image1.resize((70, 125))

            test = ImageTk.PhotoImage(image1)

            label1 = Label(self.player_hand, image=test)
            label1.configure(width=70, height=125)
            label1.image = test

            label1.pack(side=RIGHT)

    def temporary_message(self):
        """ met à jour le message de jeu """
        self.label_temporary.configure(text=self.president_game.message)
        # self.label_temporary.pack(pady=5)
        # self.label_temporary.after(5000, self.info_label.pack_forget())

    def update_ai_players(self):
        """ met à jour l'affichage des joueurs et leur nombre de carte """
        for player in self.president_game.players:
            id = self.president_game.players.index(player)
            text = "{}: {} cartes".format((player.name), len(player.hand))
            self.ai_players[id].configure(text=text)

    def update_card_on_table(self):
        """ met à jour l'affichage des dernière cartes joués"""
        for child in self.card_on_table.winfo_children():
            child.destroy()
        for card in self.president_game.round.last_play():
            path = CARD_PATH + card.file_name()

            image1 = Image.open(path)
            image1 = image1.resize((70, 125))

            test = ImageTk.PhotoImage(image1)

            label1 = Label(self.card_on_table, image=test)
            label1.configure(width=70, height=125)
            label1.image = test

            label1.pack(side=RIGHT)

    def display_parameters_page(self):
        """ affiche la page des paramètres """
        self.parameters.pack()

    def hide_home_page(self):
        """ cache la page d'accueil """
        self.home.pack_forget()

    def hide_play_page(self):
        """ cache la page de jeu"""
        self.bg_game.place_forget()
        self.play.pack_forget()

    def hide_parameters_page(self):
        """cache la page des paramètres"""
        self.parameters.pack_forget()

    def set_resolution(self, res):
        """ change la résolution de la fenêtre principale """
        self.geometry(res)

    def set_parameters(self):
        """ paramètre le nom du joueur humain  """
        self.president_game.main_player.name = self.input_name.get()
