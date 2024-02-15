import random

import actions
import constants
from constants import PREFIX
import os
import time
import neat
import pickle

ACTIONS = {
        0: actions.ShootOpponent(),
        1: actions.ShootSelf(),
        2: actions.Beer(),
        3: actions.Cigarret(),
        4: actions.Cuffs(),
        5: actions.MagnifyingGlass(),
        6: actions.Saw(),
    }

class player:

    MAX_LIFE = 6

    def __init__(self, name):
        self.name = name
        self.score = 0
        self.is_cuffed = False
        self.life = self.MAX_LIFE
        self.itens = {actions.Beer: 0, actions.Cigarret:0, actions.Cuffs:0, actions.MagnifyingGlass:0, actions.Saw:0}

    def decide(self, opponent, shotgun):
        return 1

    def play_turn(self, game, opponent):
        if self.is_cuffed:
            if not game.is_silent:
                print(f"{PREFIX} Player {self.name} is cuffed!")
            self.is_cuffed = False
            return
        decidion = self.decide(opponent, game.shotgun)
        self.score += ACTIONS[decidion].action(self,opponent,game)
        self.pos_turn()

    def pos_turn(self):
        pass


class HumanPlayer(player):
    def decide(self, opponent, shotgun):
        time.sleep(3)
        os.system('cls' if os.name == 'nt' else 'clear')
        print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
        print(f"Player {self.name} turns!")
        print(f"Your life: {self.life}, Opponent life: {opponent.life}")
        print(f"Live shells: {shotgun.live_shells}, Dead shells: {shotgun.dead_shells}")
        print(f"Beer: {self.itens[actions.Beer]},Cigarrets: {self.itens[actions.Cigarret]},Cuffs: {self.itens[actions.Cuffs]},Glasses: {self.itens[actions.MagnifyingGlass]},Saw: {self.itens[actions.Saw]}")
        for i,act in ACTIONS.items():
            print(f"{i}) {act.get_name()}")
        print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
        return self.input_decidion(0,6)


    def input_decidion(self,min,max):
        while True:
            try:
                decidion = int(input("> "))
                if not (decidion < min or decidion > max):
                    return decidion
                else:
                    print("Opção inválida")
            except:
                print("Opção inválida")

class NeatPlayer(player):
    def __init__(self, genome, config):
        super().__init__(self.generate_random_name())
        self.genome = genome
        self.network = neat.nn.FeedForwardNetwork.create(genome,config)


    def decide(self, opponent, shotgun):
        inputs = [shotgun.live_shells, shotgun.dead_shells, self.life, opponent.life, self.itens[actions.Beer], self.itens[
            actions.Cigarret], self.itens[actions.Cuffs], self.itens[actions.MagnifyingGlass], self.itens[actions.Saw]]
        outputs = self.network.activate(inputs)
        return outputs.index(max(outputs))

    def pos_turn(self):
        self.genome.fitness = self.score
    def generate_random_name(self):
        vowels = 'aeiou'
        consonants = 'bcdfghjklmnpqrstvwxyz'
        name_length = random.randint(4, 8)  # Set a random length for the name (between 4 and 8 letters)
        name = ''

        for i in range(name_length):
            if i % 2 == 0:  # If it's an even position, add a consonant
                name += random.choice(consonants)
            else:  # If it's an odd position, add a vowel
                name += random.choice(vowels)

        return name.capitalize()  # Capitalize the name to start with an uppercase letter

class AiPlayer(NeatPlayer):
    def __init__(self):
        super().__init__(self.get_genome(),self.get_config())
    def get_genome(self):
        with open(constants.FILENAME_GENOME, 'rb') as f:
            return pickle.load(f)
    def get_config(self):
        return neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
                                    neat.DefaultStagnation, "neatconfig.txt")