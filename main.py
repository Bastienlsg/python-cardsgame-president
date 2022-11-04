from models import PresidentGame, Player
from models import PresidentGame, AIPlayer
import random


def print_ln():
    print('\n')


def game_loop(g: PresidentGame):
    """
    The main game loop.
    Loops in circle until the user wants to quit the application.
    Args:
        g: The President Game instance.
    """
    wanna_continue = True
    while wanna_continue:
        g.new_game()

        while not g.last_one_player():
            print(g.players)

            g.round.next_round()

            while not g.round.is_ended() and not g.last_one_player():
                # si le joueur à encore des cartes en main
                if len(g.players[g.round.current_player].hand) > 0:
                    # vérification du type de joueur : humain ou IA et
                    # que le joueur à encore des cartes
                    if not isinstance(g.players[g.round.current_player], AIPlayer):
                        print('Your current deck is : ')
                        print(g.main_player.hand)
                        print_ln()
                        # si il y à déjà des cartes en jeux
                        # le joueur est contraint de jouer un certain nombre de cartes
                        # et une valeur minimum
                        if g.round.is_started:
                            choice = None
                            choice_nb_cards = 0
                            # tant que la valeur jouée n'est pas supérieur à la valeur de la table
                            # et que la valeur en question n'est pas en nombre supérieur ou égale dans le jeu du joueur
                            # par rapport au nombre de cartes sur la table, on demande une valeur
                            while choice == '' or choice is None or \
                                    not (g.round.cards_on_table[0].is_le(choice) and len(g.round.cards_on_table) <=
                                         g.players[
                                             g.round.current_player].has_symbol(choice)):
                                choice = input('What value do you wish to play ? pass(p)')
                                if choice == 'p':
                                    break
                                choice_nb_cards = len(g.round.cards_on_table)
                        # il n'y a pas de carte en jeu, pas de contrainte de valeur ou de nombre de cartes
                        else:
                            choice = '0'
                            choice_nb_cards = 0
                            while g.main_player.has_symbol(choice) == 0:
                                choice = input('What value do you wish to play ?')
                            # si le joueur à plusieur fois la même carte, on lui demande le nombre de cartes
                            # qu'il veut poser
                            if g.main_player.has_symbol(choice) != 1:
                                # tant que le nombre demander est supérieur au nombres de cartes possédé,
                                # on refait la demande
                                while choice_nb_cards == '' or g.main_player.has_symbol(
                                        choice) < choice_nb_cards or choice_nb_cards < 1:
                                    choice_nb_cards = input(f'How many {choice} do you want to play ?')
                                    if choice_nb_cards != '':
                                        choice_nb_cards = int(choice_nb_cards)
                            # le joueur à la carte en un seul exemplaire, on ne demande pas le nombre de
                            # cartes qu'il veut poser
                            else:
                                choice_nb_cards = 1

                        plays = g.main_player.play(choice, choice_nb_cards)
                        if len(plays) > 0:
                            g.round.update(g.round.current_player, plays)
                        print(f"You play {plays}")

                        nb_cards = len(plays)
                    # C'est à L'IA de jouer
                    else:
                        # print('symbol : {}  /  nb cartes : {}' .format(g.round.cards_on_table[0].symbol, nb_cards))
                        if g.round.is_started:
                            plays = g.players[g.round.current_player].play(g.round.cards_on_table[0].symbol,
                                                                           len(g.round.cards_on_table))
                        else:
                            plays = g.players[g.round.current_player].play('3', 1)
                        # si le nombre de carte joué est supèrieur à 0 le dernier joueur ayant joué est le joueur actuel
                        if len(plays) > 0:
                            g.round.update(g.round.current_player, plays)
                        print(f"{g.players[g.round.current_player].name} plays \t {plays}")

                    # si le joueur ou l'iA vient de finir sa main, un role lui est attribué
                    if len(g.players[g.round.current_player].hand) < 1:
                        g.set_role(g.round.current_player)

                g.round.set_current_player((g.round.current_player + 1) % len(g.players))

            print(
                '************************************************\nTour remporté par {} ! à lui/elle de '
                'commencer.\n************************************************\n'.format(
                    g.players[g.round.current_player].name))
        for player in g.players:
            print('{}   role: {}'.format(player.name, player.role))
        wanna_continue = input('Partie Suivante (y/N)? ')
        wanna_continue = (wanna_continue == 'Y' or wanna_continue == 'y')


if __name__ == '__main__':
    print_ln()
    print(
        """        *********************************************
        *** President : The cards game (TM) v.0.1 ***
        ********************************************* """)
    g = PresidentGame()
    # g.distribute_cards()
    game_loop(g)
    print('Thank you for playing. I hope you enjoyed !')
