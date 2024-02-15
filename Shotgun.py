import random
from constants import PREFIX
import time
import os
class Shotgun:
    MAX_SHELLS = 8
    MIN_SHELLS = 2
    shells = []

    def __init__(self):
        self.live_shells = 0
        self.dead_shells = 0
        self.is_cut = False

    def pump(self,game):
        is_live = self.shells[0]
        if is_live:
            self.live_shells -= 1
            if not game.is_silent:
                print(PREFIX + " is a live shell!")
        else:
            self.dead_shells -= 1
            if not game.is_silent:
                print(PREFIX + " is a dead shell!")

        self.shells.pop(0)
        if (len(self.shells)) <= 0:
            self.reload(game)

    def reload(self,game):
        sheels_qnt = random.randrange(self.MIN_SHELLS, self.MAX_SHELLS)
        for i in range(sheels_qnt):
            is_live = bool(random.getrandbits(1))
            if is_live:
                self.live_shells += 1
            else:
                self.dead_shells += 1

            self.shells.append(is_live)

        if not game.is_silent:
            print("=-=-=-=-=-=-=-=-=-=-=-=-=")
            print("Shotgun (re)loaded")
            print(f"Live shells: {self.live_shells}")
            print(f"Dead shells: {self.dead_shells}")
            print("=-=-=-=-=-=-=-=-=-=-=-=-=")
            time.sleep(3)
            os.system('cls' if os.name == 'nt' else 'clear')


        game.shuffle_itens()

    def shoot(self, player,game):
        is_live = self.shells[0]
        if is_live:
            player.life -= 2 if self.is_cut else 1

        self.is_cut = False
        self.pump(game)

        return is_live
