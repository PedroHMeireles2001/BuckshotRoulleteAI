from constants import PREFIX
class action:
    def action(self, player, opponent, game):
        pass

    def get_name(self):
        pass


class ShootSelf(action):
    def action(self, player, opponent, game):
        is_live = game.shotgun.shoot(player,game)
        if not is_live:
            player.play_turn(game,opponent)
            return 5
        else:
            return -10

    def get_name(self):
        return "Shoot Self"


class ShootOpponent(action):
    def action(self, player, opponent, game):
        is_live = game.shotgun.shoot(opponent,game)
        if is_live:
            return 5
        else:
            return -5

    def get_name(self):
        return "Shoot Opponent"


class item(action):
    def action(self, player, opponent, game):
        if player.itens[self.__class__] > 0:
            self.use(player,opponent,game)
            player.itens[self.__class__] -= 1
            player.play_turn(game, opponent)
            return 1
        else:
            if not game.is_silent:
                print(PREFIX + " Você não tem esse item")
            return -5



    def use(self, player,opponent, game):
        pass


class Beer(item):
    def use(self,player, opponent, game):
        game.shotgun.pump(game)

    def get_name(self):
        return "Use Beer"


class Cigarret(item):
    def use(self, player, opponent, game):
        if player.life < player.MAX_LIFE:
            player.life += 1

    def get_name(self):
        return "Use Cigarrets"


class Cuffs(item):
    def use(self, player, opponent, game):
        opponent.is_cuffed = True

    def get_name(self):
        return "Use Cuffs"


class MagnifyingGlass(item):
    def use(self, player, opponent, game):
        if game.shotgun.shells[0]:
            if not game.is_silent:
                print(PREFIX + " Is a live shell")
        else:
            if not game.is_silent:
                print(PREFIX + " Is a dead shell")

    def get_name(self):
        return "Use Magnifying Glass"


class Saw(item):
    def use(self, player, opponent, game):
        game.shotgun.is_cut = True

    def get_name(self):
        return "Use Saw"
