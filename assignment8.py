import random
import argparse
import time


class Player:
    def __init__(self, name, score=0):
        self.score = score
        self.name = name

    def getScore(self):
        return self.score

    def getName(self):
        return self.name

    def addScore(self, score):
        if score < 0:
            raise Exception('score arg < 0')
        self.score += score


class HumanPlayer(Player):
    def __init__(self, name, score=0):
        self.score = score
        self.name = name

    @staticmethod
    def getDecision(turnPts):
        """Returns True if player decided to roll"""
        ch = input('Enter "h" to HOLD or "r" to ROLL? ')
        while ch not in ['r', 'h']:
            ch = input('Enter "h" to HOLD or "r" to ROLL? ')
        return ch == 'r'

    def __str__(self):
        return "Human({}) : {:d} pts.".format(self.name, self.score)


class ComputerPlayer(Player):
    def __init__(self, name, score=0):
        self.score = score
        self.name = name

    def getDecision(self, turnPts):
        """Returns True if player decided to roll"""
        return turnPts < min(25, 100 - self.getScore())

    def __str__(self):
        return "Computer({}) : {:d} pts.".format(self.name, self.score)


class PlayerFactory:
    def getPlayer(self, name, ptype, score=0):
        if ptype == 'human':
            return HumanPlayer(name, score)
        elif ptype == 'computer':
            return ComputerPlayer(name, score)
        else:
            raise Exception("wrong player type '{:s}'".format(ptype))


class Dice:
    def __init__(self, seed=0):
        random.seed(a=seed)

    def roll(self):
        roll = random.randrange(1, 7)
        print ('dice rolling..', roll)
        return roll


class Game:
    def __init__(self, p1type, p2type):
        factory = PlayerFactory()
        self.die = Dice(0)
        self.players = [
            factory.getPlayer('1', p1type),
            factory.getPlayer('2', p2type)
        ]

    def start(self):
        turn = 0
        current = self.players[turn]
        Game.show_instructions()
        while not self.play(current):
            for p in self.players:
                print (p)
            turn = (turn + 1) % len(self.players)
            current = self.players[turn]
        for p in self.players:
            print (p)
        print ('\n{} won!!'.format(current.getName()))

    def play(self, player):
        """ Handles one whole turn """
        print ("\n{}'s turn:".format(player.getName()))
        pts, decision = 0, True
        roll = 0
        while decision:
            roll = self.die.roll()
            if roll == 1:
                pts = 0
                print ('zero points, rolled a one!')
                break
            else:
                pts += roll
                print ('pts:', pts)
                decision = player.getDecision(pts)
        player.addScore(pts)
        return player.getScore() > 99

    @staticmethod
    def show_instructions():
        print ("""
            Welcome to the game of Pig. To win, be the
            player with the most points at the end of the
            game. The game ends at the end of a round where
            at least one player has 100 or more points\n
            On each turn, you may roll the die as many times
            as you like to obtain more points. However, if
            you a 1, your turn is over, and you do not
            obtain any points that turn.
        """)


class TimedGameProxy(Game):
    maxTime = 10  # time out after 60 sec

    def __init__(self, p1type, p2type):
        factory = PlayerFactory()
        self.die = Dice(0)
        self.players = [
            factory.getPlayer('1', p1type),
            factory.getPlayer('2', p2type)
        ]

    def start(self):
        turn = 0
        current = self.players[turn]
        Game.show_instructions()
        startTime = time.time()
        while not self.play(current):
            for p in self.players:
                print (p)
            turn = (turn + 1) % len(self.players)
            current = self.players[turn]
            # no more turns if 1 minute has passed:
            if time.time() - startTime >= TimedGameProxy.maxTime:
                print ('\n-- Time Out! --\n')
                break
        for p in self.players:
            print (p)
        winner = self.players[0] if self.players[0].getScore(
        ) >= self.players[1].getScore() else self.players[1]
        print ('\n{} won!!'.format(winner.getName()))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('player1', help='player type: computer or human')
    parser.add_argument('player2', help='player type: computer or human')
    parser.add_argument('--timed', help='timed or not', action="store_true")
    args = parser.parse_args()
    if args.timed:
        TimedGameProxy(args.player1, args.player2).start()
    else:
        Game(args.player1, args.player2).start()


if __name__ == '__main__':
    main()
