import math

def dif_gain(name, n, game):
    """
    Calculates the difference between the gains of coalitions with n players including the player 'name'
    and those of coalitions with n-1 players not containing the player 'name'.

    Parameters:
    name (str): Name of the player
    n (int): Number of players in the coalitions
    game (pd.DataFrame): DataFrame containing the game data

    Returns:
    float: Difference in gains
    """
    sum_in = 0  # Sum of the gains of n-player coalitions including the player 'name'
    sum_ex = 0  # Sum of the gains of n-1 player coalitions not containing the player 'name'

    for ind in game.index:
        coalition = game['coalition'][ind]
        value = game['value'][ind]

        if len(coalition) == n - 1 and name not in coalition:
            sum_ex += value
        elif len(coalition) == n and name in coalition:
            sum_in += value

    return sum_in - sum_ex

def Shapley(game):
    """
    Calculates the Shapley value for each player in a cooperative game.

    Parameters:
    game (pd.DataFrame): DataFrame containing the game data

    Returns:
    dict: Dictionary containing the Shapley value for each player
    """
    players = set([element for sublist in game['coalition'] for element in sublist])
    Shapley = {player: 0 for player in players}

    n = len(players)
    for player in players:
        for j in range(1, n + 1):
            coef = math.factorial(n - j) * math.factorial(j - 1) / math.factorial(n)
            Shapley[player] += coef * dif_gain(player, j, game)

    print('Shapley value properly calculated\n')
    return Shapley
