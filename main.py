from Game import Game
from players import HumanPlayer, AiPlayer

PVP = False
def main():
    print("=-=-=-=-=-=-=-=-=-=-=-=-=")
    print("Welcome to buckshot roullete")
    print(f"Gamemode: PvP" if PVP else "Gamemode:  PvE")
    print("=-=-=-=-=-=-=-=-=-=-=-=-=")
    player1 = HumanPlayer(input("Enter player1 name: "))
    player2 = HumanPlayer(input("Enter player2 name: ")) if PVP else AiPlayer()
    game = Game(player1, player2)
    game.start()





if __name__ == "__main__":
    main()
