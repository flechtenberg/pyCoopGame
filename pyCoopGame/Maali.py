import pyomo.environ as pyo
from pyomo.opt import SolverStatus, TerminationCondition
import pandas as pd


def calculate_weights(v, N, players):
    W = {}
    for c in players:
        W_c = 0
        for z in v.keys():
            if c in z:
                subset_without_c = frozenset(z - {c})
                if subset_without_c in v:
                    W_c += v[z] - v[subset_without_c]
                else:
                    print(f"Warning: subset {subset_without_c} not found in v.")
        W[c] = W_c / v[N]
    return W


def create_maali_model(players, v, W, N):
    model = pyo.ConcreteModel()

    # Variables
    model.x = pyo.Var(players, within=pyo.NonNegativeReals)
    model.lam = pyo.Var(within=pyo.NonNegativeReals)

    # Objective
    model.obj = pyo.Objective(expr=model.lam, sense=pyo.maximize)

    # Constraints
    model.constraints = pyo.ConstraintList()

    for c in players:
        if W[c] != 0:
            model.constraints.add((1 / W[c]) * model.x[c] >= model.lam)
        else:
            model.constraints.add(model.x[c] == 0)

    for c in players:
        model.constraints.add(model.x[c] >= v[frozenset({c})])

    model.constraints.add(sum(model.x[c] for c in players) == v[N])

    return model


def solve_maali_model(instance, GAMS=False):
    if GAMS:
        solver = pyo.SolverFactory('gams')
    else:
        solver = pyo.SolverFactory('glpk')
    results = solver.solve(instance, keepfiles=False, tee=False, report_timing=False)
    instance.solutions.load_from(results)
    return results, instance


def maali(game, GAMS=False):
    game['coalition'] = game['coalition'].apply(frozenset)
    v = {frozenset(coalition): value for coalition, value in zip(game['coalition'], game['value'])}

    players = list(set(player for coalition in game['coalition'] for player in coalition))
    N = frozenset(players)

    # Calculate weights
    W = calculate_weights(v, N, players)

    # Create and solve the model
    model = create_maali_model(players, v, W, N)
    results, solved_model = solve_maali_model(model, GAMS)

    # Return the results
    if (results.solver.status == SolverStatus.ok) and (
            results.solver.termination_condition == TerminationCondition.optimal):
        print("Maali's solution properly calculated.")
        return {j: pyo.value(solved_model.x[j]) for j in players}
    else:
        print("Solver failed to find an optimal solution.")
        return None


# Example game data
data = {
    'coalition': [[], [1], [2], [3], [1, 2], [1, 3], [2, 3], [1, 2, 3]],
    'value': [0, 36.91, 0.18, 2.48, 38.61, 39.46, 3.00, 41.53]
}
game = pd.DataFrame(data)

# Call the maalis function
allocations = maali(game, GAMS=r'C:\GAMS\37\gams.exe')
print(allocations)
