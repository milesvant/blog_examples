import numpy as np


class Game:
    def play(self, identity_hero, action_hero, action_villan):
        return self.payoffs[action_hero][action_villan]


class RPS(Game):
    def __init__(self):
        self.name = "Rock-Paper-Scissors"
        self.payoffs = [[0, -1, 1], [1, 0, -1], [-1, 1, 0]]
        self.n_actions = (3, 3)


    def strategy_string(self, strategy):
        return f"Rock: { strategy[0] }, Paper: { strategy[1] }, Scissors: { strategy[2] }"


class PrisonersDilemma(Game):
    def __init__(self):
        self.name = "Prisoner's Dilemma"
        self.payoffs = [[-5, 0], [-10, -2]]
        self.n_actions = (2, 2)


    def strategy_string(self, strategy):
        return f"Defect: { strategy[0] }, Cooperate: {strategy[1] }"



class RegretMatching:
    def __init__(self, game):
        self.game = game


    def calculate_regrets(self, identity_hero, strategy_hero, strategy_villan):
        action_utilities = np.zeros(self.game.n_actions[identity_hero])
        for action_hero in range(self.game.n_actions[identity_hero]):
            for action_villan in range(self.game.n_actions[1 - identity_hero]):
                action_utilities[action_hero] += strategy_villan[action_villan] * self.game.play(identity_hero, action_hero, action_villan)
        hero_utility = np.dot(strategy_hero, action_utilities)
        regret = action_utilities - hero_utility
        return regret


    def get_strategy(self, regrets):
        regrets[regrets < 0] = 0
        total_pos_regret = regrets.sum()
        if total_pos_regret == 0:
            strategy = np.random.uniform(size=regrets.size)
            return strategy / strategy.sum()
        else:
            return regrets / total_pos_regret


    def solve(self, iterations):
        print(f"Running solve for { self.game.name } with { iterations } iterations")
        strategy1 = np.random.random(self.game.n_actions[0])
        strategy1 /= strategy1.sum()
        strategy2 = np.random.random(self.game.n_actions[1])
        strategy2 /= strategy2.sum()

        cum_regrets1, cum_regrets2 = np.zeros(strategy1.size), np.zeros(strategy2.size)
        cum_strategy1, cum_strategy2 = strategy1, strategy2

        for _ in range(iterations):
            cum_regrets1 += self.calculate_regrets(0, strategy1, strategy2)
            cum_regrets2 += self.calculate_regrets(1, strategy2, strategy1)
            strategy1 = self.get_strategy(cum_regrets1)
            strategy2 = self.get_strategy(cum_regrets2)
            cum_strategy1 += strategy1
            cum_strategy2 += strategy2

        nash1, nash2 = cum_strategy1 / (iterations + 1), cum_strategy2 / (iterations + 1)
        print(f"After { iterations } iterations,  player 1 plays [{ self.game.strategy_string(nash1) }] and player 2 plays [{ self.game.strategy_string(nash2) }]")
        return nash1, nash2


if __name__ == "__main__":
    print("__________________________________________________________________________________________________")
    rps_rm = RegretMatching(RPS())
    rps_rm.solve(1000)
    print("__________________________________________________________________________________________________")
    pd_rm = RegretMatching(PrisonersDilemma())
    pd_rm.solve(1000)
    print("__________________________________________________________________________________________________")
