def tauvalue(game):
    # Extract the set of players
    players = set([element for sublist in [i for i in game['coalition']] for element in sublist])

    # Change the data type of coalitions from list to tuple to be hashable
    game['coalition'] = [tuple(x) for x in game['coalition']]
    game = game.set_index('coalition')

    # Find the grand coalition
    gc_list = [coal for coal in game.index if len(coal) == len(players)][0]
    gc = game['value'][tuple(gc_list)]

    # Determine the marginal profits
    Mi = {}
    for player in players:
        Mi[player] = gc - game['value'][tuple([p for p in gc_list if p is not player])]

    # Determine the minimum claim
    mi = {}
    for player in players:
        mi[player] = max([game['value'][coal]-sum(Mi[p] for p in coal if p is not player) for coal in game.index])

    # Determine alpha
    alpha = (gc-sum(Mi[p] for p in players))/(sum(mi[p] for p in players)-sum(Mi[p] for p in players))

    # Determine tau
    tau={p: alpha*mi[p]+(1-alpha)*Mi[p] for p in players}
    print('Tau Value properly calculated\n')

    return(tau)