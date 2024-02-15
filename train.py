import neat

import constants
from Game import Game
from players import NeatPlayer
import threading
import pickle

GENERATION = 0

def play_game(player1, player2):
    game = Game(player1, player2, is_silent=True)
    winner, loser = game.start()
    print(
        f"Game finished. Winner: {winner.name} with {winner.genome.fitness}, Loser: {loser.name} with {loser.genome.fitness}")


def main_ai(genomes, config):
    global GENERATION
    GENERATION += 1

    pairs = []
    players = []
    for _, genome in genomes:
        genome.fitness = 0
        player = NeatPlayer(genome, config)
        players.append(player)

    print(f"Generation: {GENERATION}")

    for i in range(0, len(players), 2):
        if i + 1 < len(players):
            pair = (players[i], players[i + 1])
        else:
            players.remove(players[i])
        pairs.append(pair)

    print(f"Running games, {len(pairs)} pares")
    threads = []

    for pair1, pair2 in pairs:
        thread = threading.Thread(target=play_game, args=(pair1, pair2))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()


def run_ai():
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet,
                                neat.DefaultStagnation, "neatconfig.txt")
    population = neat.Population(config)
    winner = population.run(main_ai,2000)
    population.add_reporter(neat.StdOutReporter(True))
    population.add_reporter(neat.StatisticsReporter())

    with open(constants.FILENAME_GENOME, 'wb') as f:
        pickle.dump(winner, f)


if __name__ == "__main__":
    run_ai()