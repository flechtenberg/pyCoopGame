import math

def validate(game):
    """
    Validates the style of the passed dataframe for a cooperative game.

    Parameters:
    game (pd.DataFrame): DataFrame containing the game data

    Returns:
    None
    """
    # Check format of dataframe
    if list(game.columns) == ['coalition', 'value']:
        print('The passed dataframe has the correct columns\n')

    # Check if indices are correct type
    if game.index.dtype == 'int64':
        print('The indices have the correct type (int)\n')

    # Check if coalitions are correct type
    if all(isinstance(coal, list) for coal in game['coalition']):
        print('The coalitions have the correct type (list)\n')

    # Check if values are correct type
    if all(isinstance(value, float) for value in game['value']):
        print('The values have the correct type (float)\n')

    # Number of players according to the number of coalitions
    num_coalitions = len(game)
    num_players = math.log2(num_coalitions)

    # Number of individual players passed in the dataframe
    unique_players = set([element for sublist in game['coalition'] for element in sublist])
    num_individual_players = len(unique_players)

    if num_players == num_individual_players:
        print(f'The number of coalitions ({num_coalitions}) correctly matches the number of individual players in the game ({num_individual_players})\n')

    # Check empty coalition and grand coalition
    empty_coalition = game['coalition'].apply(lambda x: len(x) == 0)
    grand_coalition = game['coalition'].apply(lambda x: len(x) == num_players)

    if (empty_coalition & (game['value'] == 0)).any():
        print('The value of the empty coalition is 0\n')

    if (grand_coalition & (game['value'] == game['value'].max())).any():
        print('The value of the grand coalition is the maximum\n')
