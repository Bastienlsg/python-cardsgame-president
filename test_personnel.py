import unittest
import models


class TestPlayers(unittest.TestCase):
    '''def test_player_printer(self):
        g = models.PresidentGame()
        capturedOutput = io.StringIO()  # Create StringIO object
        prevStdout = sys.stdout
        sys.stdout = capturedOutput  # and redirect stdout.
        g.introduction_player()
        sys.stdout = prevStdout  # Reset redirect.
        output_string = str(capturedOutput.getvalue())
        number = re.findall(r'\d+', output_string)
        self.assertFalse(len(number) == 0)'''

    def test_value_exist(self):
        test_array = ["*", "x", "/", "14", "-2"]
        test_array2 = ["7", "9", "0", "a", "R", "p"]
        for e in test_array:
            method = models.value_exist(e)
            self.assertTrue(method == None)
        for e in test_array2:
            method = models.value_exist(e)
            self.assertFalse(method == None)

    def test_deck_gen(self):
        deck = models.Deck()
        self.assertIsInstance(deck, models.Deck)
        self.assertTrue(len(deck) == 52)
        return deck

    def test_pick_card(self):
        deck = models.Deck()
        deck.pick_card()
        self.assertTrue(len(deck) == 51)

    def test_player_gen(self):
        player = models.Player()
        self.assertIsInstance(player, models.Player)

    def test_give_best_card(self):
        g = models.PresidentGame()
        player1 = g.players[0]
        player2 = g.players[1]
        player1_hand_start = len(player1.hand)
        player2_hand_start = len(player2.hand)
        player1.give_best_card(player2, 4)
        self.assertTrue(player1_hand_start-4 == len(player1.hand) and player2_hand_start+4 == len(player2.hand))

    def test_ask_name(self):
        player = models.Player()
        self.assertTrue(len(player._name) != 0)


if __name__ == '__main__':
    unittest.main()
