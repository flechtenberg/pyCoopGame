import pyomo.environ as pyo
from pyomo.opt import SolverStatus, TerminationCondition

def feasible_model():
    """
    Builds an abstract model of the utility exchange network.
    """
    model = pyo.AbstractModel()
    # ##########################
    # SETS
    # ##########################
    model.COAL = pyo.Set(doc='Set of coalitions')
    model.PLAYER = pyo.Set(doc='Set of players')
    model.PLAYER_SUB = pyo.Set(model.COAL, doc='Player subsets')
    # ##########################
    # VARIABLES
    # ##########################
    model.xj = pyo.Var(model.PLAYER, within=pyo.NonNegativeReals, doc='allocation to player i')
    model.nu = pyo.Var(within=pyo.Reals, doc='nu parameter for minmax core')
    model.eps = pyo.Var(within=pyo.Reals, doc='epsilon parameter for least core')
    # ##########################
    # PARAMETERS
    # ##########################
    model.value = pyo.Param(model.COAL, mutable=True, doc='value of each coalition')
    model.gc = pyo.Param(mutable=True, doc='value of grand coalition')
    # ##########################
    # CONSTRAINTS
    # ##########################
    model.INCREASE = pyo.Constraint(model.COAL, rule=increase_constraint_rule)
    model.EFFICIENCY = pyo.Constraint(rule=efficiency_constraint_rule)
    model.EPS_CONST = pyo.Constraint(rule=eps_constraint_rule)
    model.NU_CONST = pyo.Constraint(rule=nu_constraint_rule)
    # ##########################
    # OBJECTIVE FUNCTION
    # ##########################
    model.OBJ1 = pyo.Objective(sense=pyo.minimize, rule=obj1_rule)
    model.OBJ2 = pyo.Objective(sense=pyo.minimize, rule=obj2_rule)
    model.OBJ3 = pyo.Objective(sense=pyo.maximize, rule=obj3_rule)
    return model

def increase_constraint_rule(model, i):
    return sum(model.xj[j] for j in model.PLAYER_SUB[i]) >= model.nu * model.value[i] - model.eps

def efficiency_constraint_rule(model):
    return sum(model.xj[j] for j in model.PLAYER) == model.gc

def eps_constraint_rule(model):
    return model.eps == 0

def nu_constraint_rule(model):
    return model.nu == 1

def obj1_rule(model):
    return sum(model.xj[j] for j in model.PLAYER)

def obj2_rule(model):
    return model.eps

def obj3_rule(model):
    return model.nu

def instantiate_model(model_data):
    """
    Builds an instance of the optimization model with specific data and objective function.

    Parameters:
    model_data (dict): Dictionary with parameters that populate the model

    Returns:
    pyomo.ConcreteModel: The instantiated model instance
    """
    model = feasible_model()
    problem = model.create_instance(model_data, report_timing=False)
    return problem

def solve_model(instance, GAMS=False):
    """
    Solves the instance of the optimization model.

    Parameters:
    instance (pyomo.ConcreteModel): The model instance to solve
    GAMS (bool, optional): Indicates whether to use GAMS solver. Defaults to False.

    Returns:
    tuple: A tuple containing the solver results and the solved instance
    """
    solver = pyo.SolverFactory('glpk') if not GAMS else pyo.SolverFactory('gams')
    results = solver.solve(instance, keepfiles=False, tee=False, report_timing=False)
    instance.solutions.load_from(results)
    return results, instance

def create_model_data(game):
    """
    Creates model data from the game.

    Parameters:
    game (pd.DataFrame): DataFrame containing the game data

    Returns:
    dict: Dictionary containing the model data
    """
    game['coalition'] = [tuple(x) for x in game['coalition']]
    game = game.set_index('coalition')
    PLAYER = list(set([element for sublist in [i for i in game.index] for element in sublist]))
    COAL = [str(coal) for coal in game.index if str(coal) and str(coal) not in ['()'] and len(coal) < len(PLAYER)]
    GRAND_COAL = [coal for coal in game.index if str(coal) and str(coal) not in ['()'] and len(coal) == len(PLAYER)]
    PLAYER_SUB = {str(coal): list(eval(coal)) for coal in COAL}
    value = {str(coal): max(game['value'][eval(coal)], 0) for coal in COAL}
    gc = {None: max(float(game['value'][GRAND_COAL].iloc[0]),0)}
    print(gc)
    model_data = {None: {
        'COAL': COAL,
        'PLAYER': PLAYER,
        'PLAYER_SUB': PLAYER_SUB,
        'value': value,
        'gc': gc,
    }}
    return model_data

def core_exists(game, GAMS=False):
    """
    Checks if the set of core allocations is not empty.

    Parameters:
    game (pd.DataFrame): DataFrame containing the game data
    GAMS (bool, optional): Indicates whether to use GAMS solver. Defaults to False.

    Returns:
    bool: True if the core exists, False otherwise
    """
    model_data = create_model_data(game)
    instance = instantiate_model(model_data)
    instance.OBJ1.activate()
    instance.OBJ2.deactivate()
    instance.OBJ3.deactivate()
    results, instance_solved = solve_model(instance, GAMS)
    if results.solver.status == SolverStatus.ok and results.solver.termination_condition == TerminationCondition.optimal:
        print('The set of core allocations is NOT EMPTY\n')
        return True
    else:
        print('WARNING: The set of core allocations is EMPTY (!!!)\n')
        return False

def is_in_core(game, x, eps=0.000000001):
    """
    Checks if a given allocation is in the core.

    Parameters:
    game (pd.DataFrame): DataFrame containing the game data
    x (dict): The allocation dictionary
    eps (float, optional): Tolerance for comparing values. Defaults to 0.000000001.

    Returns:
    bool: True if the allocation is in the core, False otherwise
    """
    ratio = sum(x[p] for p in x) / max(game['value'])
    if ratio < 1 - eps or ratio > 1 + eps:
        return False
    for ind in game.index:
        if sum(x[p] for p in game['coalition'][ind]) < game['value'][ind] * (1 - eps):
            return False
    return True

def least_core(game, GAMS=False):
    """
    Calculates the least core of the game.

    Parameters:
    game (pd.DataFrame): DataFrame containing the game data
    GAMS (bool, optional): Indicates whether to use GAMS solver. Defaults to False.

    Returns:
    dict: Dictionary containing the allocations in the least core
    """
    model_data = create_model_data(game)
    instance = instantiate_model(model_data)
    instance.OBJ1.deactivate()
    instance.OBJ2.activate()
    instance.OBJ3.deactivate()
    instance.EPS_CONST.deactivate()
    results, instance_solved = solve_model(instance, GAMS)
    eps = instance_solved.OBJ2()
    if eps <= 0:
        print('The core is not empty and epsilon is ' + str(eps) + '\n')
    else:
        print('The core is empty and epsilon is ' + str(eps) + '\n')
    return {j: instance_solved.xj[j].value for j in instance.PLAYER}

def minmax_core(game, GAMS=False):
    """
    Calculates the minmax core of the game.

    Parameters:
    game (pd.DataFrame): DataFrame containing the game data
    GAMS (bool, optional): Indicates whether to use GAMS solver. Defaults to False.

    Returns:
    dict: Dictionary containing the allocations in the minmax core
    """
    model_data = create_model_data(game)
    instance = instantiate_model(model_data)
    instance.OBJ1.deactivate()
    instance.OBJ2.deactivate()
    instance.OBJ3.activate()
    instance.NU_CONST.deactivate()
    results, instance_solved = solve_model(instance, GAMS)
    nu = instance_solved.OBJ3()
    if nu >= 1:
        print('The core is not empty and nu is ' + str(nu) + '\n')
    else:
        print('The core is empty and nu is ' + str(nu) + '\n')
    return {j: instance_solved.xj[j].value for j in instance.PLAYER}
