from models import Window
from models import PresidentGame


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
    # boucle à chaque nouvelle partie
    while wanna_continue:
        g.new_game()
        g.card_exchange()
        g.set_first_player()
        # boucle à chaque début fois que les cartes sont ramassés et que le nouveau tour démarre
        while not g.last_one_player():
            g.round.next_round()
            # boucle à chaque fois qu'un joueur joue
            g.next_player()
            if not g.is_ended:
                print(
                    '************************************************\nTour remporté par {} ! à lui/elle de '
                    'commencer.\n************************************************\n'.format(
                        g.players[g.round.current_player].name))

        wanna_continue = input('Partie Suivante (y/N)? ')
        wanna_continue = (wanna_continue == 'Y' or wanna_continue == 'y')


if __name__ == '__main__':
    win = Window()
    win.mainloop()
    print(
        """        *********************************************
        *** President : The cards game (TM) v.0.1 ***
        ********************************************* """)
    g = PresidentGame()

    game_loop(g)
    print('Thank you for playing. I hope you enjoyed !')
