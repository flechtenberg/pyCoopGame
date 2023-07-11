import random
from itertools import combinations
import pandas as pd

def create_game(n=1, seed=None):
    '''
    Function that creates a (random) n-player TU game
    :param n: number of players in the game
    :param seed: seed for random number generation (optional)
    :return: A fully specified game in the form of a DataFrame
    '''
    # Set random seed if provided
    if seed is not None:
        random.seed(seed)

    players = range(n)
    # Generate all coalitions for the n-player game

    coalitions = [comb for i in range(n+1) for comb in combinations(players, i)]

    # Generate benefits for all coalitions
    values = {(): 0.0}
    game = {'coalition': [], 'value': []}
    for k, coal in enumerate(coalitions, start=0):
        incr = random.random()
        pre = max(values[tuple([x for x in coal if x != player])] for player in coal) if len(coal) > 0 else 0
        if len(coal) <= 1:
            values[coal] = 0
            game['coalition'].append(list(coal))
            game['value'].append(0)
        else:
            values[coal] = pre + incr
            game['coalition'].append(list(coal))
            game['value'].append(pre + incr)

    game_df = pd.DataFrame(game)
    print(f'The {n}-player game has been created')
    print('###############\n')
    return game_df
