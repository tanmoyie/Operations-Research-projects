import pyomo.environ as pyo
from pyomo.opt import SolverFactory
import numpy as np


class TravelingSalesmanProblem:
    def __init__(self, num_cities=10):
        self.num_cities = num_cities
        self.distance_matrix = self.generate_distance_matrix()
        self.model = self.create_model()

    def generate_distance_matrix(self):
        np.random.seed(20)
        distance_matrix = np.random.randint(10, 100, size=(self.num_cities, self.num_cities))
        np.fill_diagonal(distance_matrix, 0) # since we created random distances, diagonals also contain values,
        # which is supposed to be zero.
        return distance_matrix

    def create_model(self):
        model = pyo.ConcreteModel()
        model.N = pyo.RangeSet(self.num_cities)  # pyo.Set(initialize=range(1, self.num_cities+1)) #
        model.distance = pyo.Param(model.N, model.N, initialize=lambda model, i, j: self.distance_matrix[i - 1, j - 1])
        model.x = pyo.Var(model.N, model.N, within=pyo.Binary)
        model.u = pyo.Var(model.N, within=pyo.NonNegativeReals)

        def obj_rule(model):
            return sum(model.distance[i, j] * model.x[i, j] for i in model.N for j in model.N)

            # (pyo.summation(model.distance, model.x))

        model.obj = pyo.Objective(rule=obj_rule, sense=pyo.minimize)

        def constraint1(model, i):
            return sum(model.x[i, j] for j in model.N if i != j) == 1

        model.con1 = pyo.Constraint(model.N, rule=constraint1)

        def constraint2(model, j):
            return sum(model.x[i, j] for i in model.N if j != i) == 1

        model.con2 = pyo.Constraint(model.N, rule=constraint2)

        def sub_tour_elimination_rule(model, i, j):
            if i != j and i != 1 and j != 1:
                return model.u[i] - model.u[j] + self.num_cities * model.x[i, j] <= self.num_cities - 1
            else:
                return pyo.Constraint.Skip

        model.sub_tour_elim = pyo.Constraint(model.N, model.N, rule=sub_tour_elimination_rule)

        return model

    def solve(self):
        solver = SolverFactory('glpk')
        result = solver.solve(self.model, tee=False)
        # result = solver.solve(self.model).write()

        # self.model.pprint()
        print('result.Solver.status', f'{result.Solver.status=}')  #, {self.model.cost_function()}

        route = []
        # for i in range(1, self.num_cities + 1):
        #    for j in range(1, self.num_cities + 1):
                # if pyo.value(self.model.x[i, j]) == 1.0:
                #     route.append((i, j))

        l = list(self.model.x.keys())
        for i in l:
            if self.model.x[i]() == 1.0:
                # print(i, '--', self.model.x[i]())
                route.append(i)
        return route

    def print_route(self, route):
        print("Optimal Route:")
        for arc in route:
            print(f"City {arc[0]} -> City {arc[1]}")


