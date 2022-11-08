import random
import names
import re
from tkinter import *

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
        self.__generate_players(ask_player_number())
        self.round = Round()
        self.current_role_available = 1
        self.is_ended = False
        self.list_role = None
        self.generate_list_role()
        self.is_first_game = True

    def next_player(self):
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

            self.round.set_current_player((self.round.current_player + 1) % len(self.players))
            self.test_rules()

    def ia_play(self):
        if self.round.is_started:
            plays = self.players[self.round.current_player].play(self.round.last_play()[0].symbol,
                                                                 len(self.round.last_play()))
        else:
            plays = self.players[self.round.current_player].play('3', 1)
        # si le nombre de carte joué est supèrieur à 0 le dernier joueur ayant joué est le joueur actuel
        if len(plays) > 0:
            self.round.update(self.round.current_player, plays)
        print(f"{self.players[self.round.current_player].name} plays \t {plays}")

    def human_play(self):
        current_player = self.players[self.round.current_player]
        #print('Your current deck is : ')
        #print(self.main_player.hand)
        #print("\n")
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
        if not self.is_first_game:
            for player in self.players:
                if player.role == 1:
                    self.round.set_current_player(self.players.index(player))
                    print("le président est {}, à lui/elle de commencer !!!".format(player.name))
        else:
            for player in self.players:
                for card in player.hand:
                    if card.symbol == "D" and card.color == '♡':
                        self.round.set_current_player(self.players.index(player))
                        print("{} a la dame de coeur, à lui/elle de commencer !!".format(player.name))

        self.is_first_game = False

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
        # si quelqu'un joue un ou plusieurs 2, le tour est fini et il prend la main
        if self.round.last_play()[0].symbol == "2":
            self.round.set_current_player(self.round.last_player)
            print("le 2 remporte la main !!")
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
            print("les quatres même cartes ont été joué d'affilé, {} remporte la main !!!".format(
                self.players[self.round.last_player].name))
            self.round.set_current_player(self.round.last_player)
            return

        # si une carte de même symbole est joué, le joueur suivant passe sont tour
        if self.round.last_play()[0].symbol == self.round.cards_on_table[len(self.round.cards_on_table) - 2][0].symbol and len(self.round.cards_on_table) > 1:
            print("{} passe son tour :-("  .format(self.players[self.round.current_player].name))
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
        self.geometry('1920x1080')
        self.resizable(height=False, width=False)
        self.bg_menu = PhotoImage(file="assets/president_game.png")
        self.bg_play = PhotoImage(file="assets/poker_table.png")
        self.home_page()
        self.input_res = None
        self.messagebox = None
        self.mainloop()

    def home_page(self):
        self.bg_home = Label(self, image=self.bg_menu)
        self.bg_home.place(x=0, y=0)

        self.home = Frame(self, bg="black")
        self.home.pack()

        self.btn_play = Button(self.home, text="Jouer", command=lambda: [self.play_page(), self.hide_home_page()])
        self.btn_play.pack()

        self.btn_parameters = Button(self.home, text="Paramètres",
                                     command=lambda: [self.parameters_page(), self.hide_home_page()])
        self.btn_parameters.pack()

    def play_page(self):
        self.bg_game = Label(self, image=self.bg_play)
        self.bg_game.place(x=0, y=0)

        self.play = Frame(self, bg="black")
        self.play.pack()

    def parameters_page(self):
        self.bg_home = Label(self, image=self.bg_menu)
        self.bg_home.place(x=0, y=0)

        self.parameters = Frame(self, bg="black")
        self.parameters.pack()

        self.ask_geometry()
        self.ask_player()
        self.ask_name()

        self.back_btn = Button(self.parameters, text=u'\u21a9', command=lambda: [self.home_page(), self.hide_parameters_page()])
        self.back_btn.pack(anchor="w", side="bottom", padx=10, pady=10)

    def hide_home_page(self):
        self.home.destroy()

    def hide_parameters_page(self):
        self.parameters.destroy()

    def ask_geometry(self):
        self.parameters = Frame(self, bg="black")
        self.parameters.pack()

        self.res_label = Label(self.parameters, text="Quelle résolution souhaitez-vous ?")
        self.res_label.pack()

        self.btn_res_1600x900 = Button(self.parameters, text="1600x900", command=lambda: self.set_resolution('1600x900'))
        self.btn_res_1600x900.pack()

        self.btn_res_1280x720 = Button(self.parameters, text="1280x720", command=lambda: self.set_resolution('1280x720'))
        self.btn_res_1280x720.pack()

        self.btn_res_1440x900 = Button(self.parameters, text="1440x900", command=lambda: self.set_resolution('1440x900'))
        self.btn_res_1440x900.pack()

        self.btn_res_1536x864 = Button(self.parameters, text="1536x864", command=lambda: self.set_resolution('1536x864'))
        self.btn_res_1536x864.pack()

        self.btn_res_1366x768 = Button(self.parameters, text="1366x768", command=lambda: self.set_resolution('1366x768'))
        self.btn_res_1366x768.pack()

        self.btn_res_1920x1080 = Button(self.parameters, text="1920x1080", command=lambda: self.set_resolution('1920x1080'))
        self.btn_res_1920x1080.pack()

    def set_resolution(self, res):
        self.geometry(res)

    def ask_player(self):
        self.parameters = Frame(self, bg="black")
        self.parameters.pack()

        self.player_label = Label(self.parameters, text="Combien de joueur souhaitez-vous dans vos parties ?")
        self.player_label.pack()

        self.input_player = Entry(self.parameters)
        self.input_player.pack()

        self.btn_player = Button(self.parameters, text="Valider", command=self.set_player)
        self.btn_player.pack(side=TOP, padx=50, pady=10)

    def ask_name(self):
        self.name_label = Label(self.parameters, text="Quel prénom souhaitez-vous utiliser pour vos parties ?")
        self.name_label.pack()

        self.input_name = Entry(self.parameters)
        self.input_name.pack()

        self.btn_name = Button(self.parameters, text="Valider", command=self.set_name)
        self.btn_name.pack(side=TOP, padx=50, pady=10)

    def set_player(self):
        print(self.input_player.get())

    def set_name(self):
        print(self.input_name.get())