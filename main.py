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
    while wanna_continue:

        print('Your current deck is : ')
        print(g.main_player.hand, )
        print_ln()
        choice = '0'

        while g.main_player.has_symbol(choice) == 0:
            choice = input('What value do you wish to play ? ')

        plays = g.main_player.play(choice)
        print(f"You play {plays}")

        nb_cards = len(plays)
        for ai in g.ai_players:
            plays = ai.play(choice, nb_cards)
            print(f"{ai.name} plays \t {plays}")

            # Update latest card played
            if len(plays) > 0:
                choice = plays[0].symbol

        wanna_continue = input('Do you want to continue playing (y/N)? ')
        wanna_continue = (wanna_continue == 'Y' or wanna_continue == 'y')


if __name__ == '__main__':
    print_ln()
    print(
        """        *********************************************
        *** President : The cards game (TM) v.0.1 ***
        ********************************************* """)
    g = PresidentGame()
    #g.distribute_cards()
    game_loop(g)
    print('Thank you for playing. I hope you enjoyed !')
