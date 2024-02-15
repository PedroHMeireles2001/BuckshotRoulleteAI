import actions
from Shotgun import Shotgun
import random
class Game:
    ITENS_PER_RELOAD = 4

    def __init__(self, player1, player2,is_silent=False):
        self.player1 = player1
        self.player2 = player2
        self.shotgun = Shotgun()
        self.is_silent = is_silent

    def start(self):
        self.shotgun.reload(self)
        while True:
            self.player1.play_turn(self,self.player2)
            if self.check_victory() is not None:
                return self.check_victory()
            self.player2.play_turn(self,self.player1)
            if self.check_victory() is not None:
                return self.check_victory()

    def check_victory(self):
        if self.player1.life <= 0 or self.player1.score <= -50:
            return (self.player2,self.player1)
        elif self.player2.life <=0 or self.player2.score <= -50:
            return (self.player1,self.player2)
        else:
            return None

    def shuffle_itens(self):
        self.shuffle_itens_forplayer(self.player1)
        self.shuffle_itens_forplayer(self.player2)
    def shuffle_itens_forplayer(self,player):
        ITENS = {0: actions.Beer, 1: actions.Cigarret, 2: actions.Cuffs, 3: actions.MagnifyingGlass, 4: actions.Saw}
        for i in range(self.ITENS_PER_RELOAD):
            item = random.randrange(0,4)
            player.itens[ITENS[item]] += 1