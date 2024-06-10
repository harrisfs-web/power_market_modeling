import gurobipy as gp
from gurobipy import GRB

# scenarios
#ω1: Low demand, high capacity - probability 0.2
#ω2: Medium demand, medium capacity - probability 0.5
#ω3: High demand, low capacity - probability 0.3

# data
regions = ['Region1', 'Region2']
technologies = ['Tech1', 'Tech2']
scenarios = ['Low', 'Medium', 'High']

c = {'Tech1': 60, 'Tech2': 30}  # Cost per MW for each technology
d = {'Low': {'Region1': 70, 'Region2': 90}, 'Medium': {'Region1': 100, 'Region2': 100}, 'High': {'Region1': 120, 'Region2': 160}}  # Demand in each scenario
e = {'Low': {'Region1': {'Tech1': 70, 'Tech2': 90}, 'Region2': {'Tech1': 80, 'Tech2': 100}},
     'Medium': {'Region1': {'Tech1': 70, 'Tech2': 40}, 'Region2': {'Tech1': 80, 'Tech2': 80}},
     'High': {'Region1': {'Tech1': 90, 'Tech2': 50}, 'Region2': {'Tech1': 80, 'Tech2': 60}}}  # Capacity in each scenario
p = {'Low': 0.2, 'Medium': 0.5, 'High': 0.3}  # Probability of each scenario
kappa = 20  # Cost per MW of energy traded
beta = 0.95  # Risk-aversion parameter for CVaR

# model
m = gp.Model("StochasticCVaREnergyPlanning")

# decision variables
x = m.addVars(regions, technologies, scenarios, name="x", vtype=GRB.CONTINUOUS, lb=0)
y = m.addVars(regions, regions, scenarios, name="y", vtype=GRB.CONTINUOUS, lb=0)
eta = m.addVar(name="eta", vtype=GRB.CONTINUOUS)
z = m.addVars(scenarios, name="z", vtype=GRB.CONTINUOUS, lb=0)

# objective function
m.setObjective(gp.quicksum(p[s] * (gp.quicksum(c[t] * x[r, t, s] for r in regions for t in technologies) +
                                    kappa * gp.quicksum(y[r1, r2, s] for r1 in regions for r2 in regions if r1 != r2)) for s in scenarios) +
               (1 / (1 - beta)) * (eta + gp.quicksum(p[s] * z[s] for s in scenarios)), GRB.MINIMIZE)

# constraints
for r in regions:
    for s in scenarios:
        m.addConstr(gp.quicksum(x[r, t, s] for t in technologies) +
                    gp.quicksum(y[r1, r, s] for r1 in regions if r1 != r) -
                    gp.quicksum(y[r, r2, s] for r2 in regions if r2 != r) >= d[s][r], name=f"demand_{r}_{s}")

for r in regions:
    for t in technologies:
        for s in scenarios:
            m.addConstr(x[r, t, s] <= e[s][r][t], name=f"capacity_{r}_{t}_{s}")

# CVaR
for s in scenarios:
    scenario_cost = gp.quicksum(c[t] * x[r, t, s] for r in regions for t in technologies) + \
                    kappa * gp.quicksum(y[r1, r2, s] for r1 in regions for r2 in regions if r1 != r2)
    m.addConstr(z[s] >= scenario_cost - eta, name=f"cvar_{s}")

# optimize
m.optimize()

# results
if m.status == GRB.OPTIMAL:
    for s in scenarios:
        print(f"\nScenario: {s}")
        for r in regions:
            for t in technologies:
                print(f"Energy produced in {r} by {t}: {x[r, t, s].X} MW")
        for r1 in regions:
            for r2 in regions:
                if r1 != r2:
                    print(f"Energy traded from {r1} to {r2}: {y[r1, r2, s].X} MW")
    print(f"\nTotal expected cost: {m.objVal} EUR")
else:
    print("No optimal solution found.")
