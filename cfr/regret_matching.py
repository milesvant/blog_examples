import numpy as np


class RPS:
    def __init__(self):
        self.name = "Rock-Paper-Scissors"
        self.n_actions = [3, 3]
        self.R = 0
        self.P = 1
        self.S = 2

    def play(self, identity_hero, action_hero, action_villan):
        if action_hero == action_villan:
            return 0
        if action_hero == self.R:
            return 1 if action_villan == self.S else -1
        if action_hero == self.S:
            return 1 if action_villan == self.P else -1
        if action_hero == self.P:
            return 1 if action_villan == self.R else -1

    def strategy_string(self, strategy):
        return f"Rock: { strategy[self.R] }, Paper: { strategy[self.P] }, Scissors: { strategy[self.S] }"



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
            return np.uniform(regrets.size)
        else:
            return regrets / total_pos_regret


    def solve(self, iterations):
        print(f"Running solve for { self.game.name } with { iterations } iterations")
        strategy1 = np.random.random(self.game.n_actions[0])
        strategy1 /= strategy1.sum()
        strategy2 = np.random.random(self.game.n_actions[1])
        strategy2 /= strategy2.sum()

        cum_strategy1, cum_strategy2 = strategy1, strategy2

        for _ in range(iterations):
            strategy1 = self.get_strategy(self.calculate_regrets(0, strategy1, strategy2))
            strategy2 = self.get_strategy(self.calculate_regrets(1, strategy2, strategy1))

            cum_strategy1 += strategy1
            cum_strategy2 += strategy2

        nash1, nash2 = cum_strategy1 / iterations, cum_strategy2 / iterations
        print(f"After { iterations } iterations,  player 1 plays [{ self.game.strategy_string(nash1) }] and player 2 plays [{ self.game.strategy_string(nash2) }]")
        return nash1, nash2


if __name__ == "__main__":
    rm = RegretMatching(RPS())
    strategy1, strategy2 = rm.solve(1000)
