from game.utils import game
from game.player import *

if __name__ == "__main__":
    import sys
    MIN_VER = (3, 8)
    if sys.version_info[:2] < MIN_VER:
        sys.exit("This game requires Python {}.{}.".format(*MIN_VER))
    else:
        game.run()