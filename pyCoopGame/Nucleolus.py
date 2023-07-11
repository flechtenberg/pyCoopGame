import pyomo.environ as pyo
from pyomo.opt import SolverStatus, TerminationCondition

def create_model():
    """ This function builds an abstract model on top of the ecoinvent database """
    model = pyo.AbstractModel()
    # SETS
    model.COAL = pyo.Set(doc='Set of coalitions')
    model.INDEX = pyo.Set(doc='Set of indices')
    model.FINAL_INDEX = pyo.Set(within=model.INDEX)
    model.PLAYER = pyo.Set(doc='Set of players')
    model.PLAYER_SUB = pyo.Set(model.COAL, doc='Player subsets')
    # VARIABLES
    model.dik = pyo.Var(model.COAL, model.INDEX - model.FINAL_INDEX, within=pyo.NonNegativeReals, doc='dik')
    model.tk = pyo.Var(model.INDEX - model.FINAL_INDEX, within=pyo.Reals)
    model.phi = pyo.Var(model.COAL, within=pyo.Reals)
    model.xj = pyo.Var(model.PLAYER, within=pyo.NonNegativeReals)
    # PARAMETERS
    model.indexk = pyo.Param(model.INDEX, mutable=True, within=pyo.Reals)
    model.lambdak = pyo.Param(model.INDEX, mutable=True, within=pyo.Reals, doc='lambda')
    model.value = pyo.Param(model.COAL, mutable=True, within=pyo.Reals)
    model.gc = pyo.Param(mutable=True, within=pyo.Reals)
    # CONSTRAINTS
    model.ORDER = pyo.Constraint(model.COAL, model.INDEX - model.FINAL_INDEX,
                                 rule=lambda model, i, k: model.dik[i, k] >= model.phi[i] - model.tk[k])
    model.EXCESS = pyo.Constraint(model.COAL, rule=lambda model, i: model.phi[i] == model.value[i] - sum(model.xj[j] for j in model.PLAYER_SUB[i]))
    model.EFFICIENCY = pyo.Constraint(rule=lambda model: sum(model.xj[j] for j in model.PLAYER) == model.gc)
    # OBJECTIVE
    model.OBJ = pyo.Objective(sense=pyo.minimize,
                              rule=lambda model: sum((model.lambdak[k] - model.lambdak[k + 1]) * (model.indexk[k] * model.tk[k] + sum(model.dik[i, k] for i in model.COAL)) for k in model.INDEX - model.FINAL_INDEX))
    return model

def instantiate(model_data):
    """ This function builds an instance of the optimization model with specific data and objective function

    Parameters:
    model_data: Dictionary with parameters that populate the model
    """
    model = create_model()
    problem = model.create_instance(model_data, report_timing=False)
    return problem

def solve_model(instance, GAMS=False):
    """ This function solves the instance of the optimization model

    Parameters:
    GAMS: Indicates whether to use GAMS solver
    """
    # Solver set-up
    if GAMS is False:
        solver = pyo.SolverFactory('glpk')
    else:
        solver = pyo.SolverFactory('gams')
    results = solver.solve(instance, keepfiles=False, tee=False, report_timing=False) #, io_options=io_options)
    instance.solutions.load_from(results)
    return results, instance

def nucleolus(game, delta=0.5, GAMS=False, tk=False):
    COAL = [str(coal) for coal in game['coalition']]
    INDEX = game.index.tolist()
    FINAL_INDEX = [len(COAL) - 1]
    PLAYER = list(set([element for sublist in game['coalition'] for element in sublist]))
    PLAYER_SUB = {str(coal): coal for coal in game['coalition']}

    indexk = {k: k for k in INDEX}
    lambdak = {k: delta ** (k - 1) for k in INDEX}
    lambdak[FINAL_INDEX[0]] = 0
    value = {str(game['coalition'][ind]): game['value'][ind] for ind in game.index}
    gc = {None: max(game['value'])}

    model_data = {
        None: {
            'COAL': COAL,
            'INDEX': INDEX,
            'FINAL_INDEX': FINAL_INDEX,
            'PLAYER': PLAYER,
            'PLAYER_SUB': PLAYER_SUB,
            'indexk': indexk,
            'lambdak': lambdak,
            'value': value,
            'gc': gc,
        }
    }

    instance = instantiate(model_data)

    results, instance_solved = solve_model(instance, GAMS)
    if tk:
        tks = [instance_solved.tk[j].value for j in [ind for ind in INDEX if ind not in FINAL_INDEX]]
        xjs = {j: instance_solved.xj[j].value for j in PLAYER}
        print(tks)
        print(xjs)
        return tks

    if (results.solver.status == SolverStatus.ok) and (results.solver.termination_condition == TerminationCondition.optimal):
        print('Nucleolus properly calculated\n')
    else:
        print('Solver failed while calculating Nucleolus!\n')
    return {j: instance_solved.xj[j].value for j in PLAYER}

def compare_tks(tk1, tk2):
    if tk1 == tk2:
        print('equal')
        return 0
    print('not equal')
    for t1, t2 in zip(tk1, tk2):
        if t1 > t2:
            return -1
        if t2 > t1:
            return 1
    return 0

def nucl_screen(game, deltas, GAMS=False):
    tks = {}
    ranking = {}
    for delta in deltas:
        print(delta)
        tks[delta] = nucleolus(game, delta=delta, GAMS=GAMS, tk=True)
        ranking[delta] = 0
    for delta1 in deltas:
        for delta2 in deltas:
            incr = compare_tks(tks[delta1], tks[delta2])
            ranking[delta1] -= incr
            ranking[delta2] += incr
    print(ranking)
