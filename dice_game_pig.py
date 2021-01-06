import random


def input_num(prompt='Please enter a number: ', mini=0, maxi=100):
    """Read a positive number with the given prompt."""

    while True:
        try:
            num = int(input(prompt))
            if (num < mini or
                (maxi is not None and num > maxi)):
                    print('Number is not within range: {} to {}'.format(mini, maxi))
            else:
                break

        except ValueError:
            print('enter a number')
            continue
    return num


class RolledOneException(Exception):
    pass


class Die:
    """A die to play with."""

    def __init__(self):
        self.value = random.randint(1, 6)

    def roll(self):
        """Returns the rolled dice, or raises RolledOneException if 1."""

        self.value = random.randint(1, 6)
        if self.value == 1:
            raise RolledOneException

        return self.value


    def __str__(self):
        return "Rolled " + str(self.value) + "."


class Box:
    """Temporary score box holder class."""

    def __init__(self):
        self.value = 0


    def reset(self):
        self.value = 0


    def add_dice_value(self, dice_value):
        self.value += dice_value


class Player(object):
    """Base class for different player types."""

    def __init__(self, name=None):
        self.name = name
        self.score = 0


    def add_score(self, player_score):
        """Adds player_score to total score."""

        self.score += player_score


    def __str__(self):
        """Returns player name and current score."""

        return str(self.name) + ": " + str(self.score)


class ComputerPlayer(Player):
    cpu_names=['cpu1', 'cpu2', 'cpu3', 'cpu4']


    def __init__(self, num):
        """Assigns a cpu name from cpu_names, or Cpu#."""

        if num < len(self.cpu_names):
            name = self.cpu_names[num]
        else:
            name = 'Cpu{}'.format(num)

        super(ComputerPlayer, self).__init__(name)


    def keep_rolling(self, box):
        """Randomly decides if the CPU player will keep rolling."""

        while box.value < (10 + random.randint(1, 35)):
            print("  Computer will roll again.")
            return True
        print("  Computer will hold.")
        return False


class HumanPlayer(Player):
    def __init__(self, name):
        super(HumanPlayer, self).__init__(name)


    def keep_rolling(self, box):
        """Asks the human player, if they want to keep rolling."""

        human_decision = input_num("  1 - Roll again, 0 - Hold? ", 0, 1)
        if human_decision == 1:
            return True
        else:
            return False


class GameManager:
    def __init__(self, humans=1, computers=1):
        """Initialises the game, optionally asking for human player names."""

        self.players = []
        if humans == 1:
            self.players.append(HumanPlayer('Human'))
        else:
            for i in range(humans):
                player_name = input('Enter name of human player no. {}: '.format(i))
                self.players.append(HumanPlayer(player_name))

        for i in range(computers):
            self.players.append(ComputerPlayer(i))

        self.no_of_players = len(self.players)

        self.die = Die()
        self.box = Box()


    @staticmethod
    def welcome():
        """Prints a welcome message including rules."""

        print("*" * 70)
        print("Welcome to Pig Dice!" .center(70))
        print("*" * 70)
        print("The objective is to be the first to reach 100 points." .center(70))
        print("On each turn, the player will roll a die." .center(70))
        print("The die value will stored in a temporary score box." .center(70))
        print("(If the die value is 1, the player earns no points," .center(70))
        print("and the turn goes to the next player.)" .center(70))
        print("A human player has an option to either roll again," .center(70))
        print("or hold. If you hold, the score in the" .center(70))
        print("temporary box will be added to your total score." .center(70))
        print(" Good luck! " .center(70, "*"))
        print(" Remember " .center(70, "*"))
        print(" Fortune favors the brave... " .center(70, "*"))
        print(" but chance favors the smart! " .center(70, "*"))
        print()
        print("I will now decide who starts" .center(70, " "))
        print()


    def decide_first_player(self):
        """Randomly chooses a player to begin, and prints who is starting."""

        self.current_player = random.randint(1, self.no_of_players) % self.no_of_players

        print('{} starts'.format(self.players[self.current_player].name))


    def next_player(self):
        """Advanced self.current_player to next player."""
        self.current_player = (self.current_player + 1) % self.no_of_players



    def previous_player(self):
        """Changes self.current_player to previous player."""

        self.current_player = (self.current_player - 1) % self.no_of_players


    def get_all_scores(self):
        """Returns a join all players scores."""

        return ', '.join(str(player) for player in self.players)


    def play_game(self):
        """Plays an entire game."""

        self.welcome()
        self.decide_first_player()

        while all(player.score < 100 for player in self.players):
            print('\nCurrent score --> {}'.format(self.get_all_scores()))
            print('\n*** {} to play ***'.format(self.players[self.current_player].name))
            self.box.reset()

            while self.keep_rolling():
                pass

            self.players[self.current_player].add_score(self.box.value)
            self.next_player()

        ## The previous player has won...
        self.previous_player()
        print(' {} has won '.format(self.players[self.current_player].name).center(70, '*'))


    def keep_rolling(self):
        """Adds rolled dice to box. Returns if human/cpu wants to continue.

        If either player rolls a 1, the box value is reset, and turn ends.
        """
        try:
            dice_value = self.die.roll()
            self.box.add_dice_value(dice_value)
            print('Last roll: {}, new box value: {}'.format(dice_value, self.box.value))

            # Check if human (by asking) or computer(calculating) will keep rolling
            return self.players[self.current_player].keep_rolling(self.box)

        except RolledOneException:
            print('  Rolled one. Switching turns')
            self.box.reset()
            return False


def main():
    human_players = input_num('How many human players? ')
    computer_players = input_num('How many computer players? ')

    game_manager = GameManager(human_players, computer_players)
    game_manager.play_game()


if __name__ == '__main__':
    main()
