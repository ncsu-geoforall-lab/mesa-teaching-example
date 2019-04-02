from mesa import Model
from mesa.datacollection import DataCollector
from mesa.space import MultiGrid
from mesa.time import RandomActivation

from .agent import TreeCell, MovingAgent


class ForestDisease(Model):
    """
    Simple Forest Fire model.
    """
    def __init__(self, height=100, width=100, density=0.65, mortality=1, wind='N', distance='1'):
        """
        Create a new forest fire model.

        Args:
            height, width: The size of the grid to model
            density: What fraction of grid cells have a tree in them.
        """
        # Initialize model parameters
        self.height = height
        self.width = width
        self.density = density
        self.mortality = mortality
        self.wind = wind
        self.distance = distance

        # Set up model objects
        self.schedule = RandomActivation(self)
        self.grid = MultiGrid(height, width, torus=False)

        self.datacollector = DataCollector(
            {"Fine": lambda m: self.count_type(m, "Fine"),
             "Infected": lambda m: self.count_type(m, "Infected"),
             "Dead": lambda m: self.count_type(m, "Dead")})

        # Place a tree in each cell with Prob = density
        for (contents, x, y) in self.grid.coord_iter():
            if self.random.random() < self.density:
                # Create a tree
                new_tree = TreeCell((x, y), self)
                self.grid._place_agent((x, y), new_tree)
                self.schedule.add(new_tree)
                
        center = (int(width / 2), int(height / 2))
        movingAgent = MovingAgent(center, self)
        self.grid._place_agent(center, movingAgent)
        new_tree = TreeCell(center, self)
        self.grid._place_agent(center, new_tree)
        self.schedule.add(new_tree)
        self.schedule.add(movingAgent)

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        """
        Advance the model by one step.
        """
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)

        # Halt if no more fire
        if self.count_type(self, "Fine") == 0:
            self.running = False

    @staticmethod
    def count_type(model, tree_condition):
        """
        Helper method to count trees in a given condition in a given model.
        """
        count = 0
        for tree in model.schedule.agents:
            if tree.condition == tree_condition:
                count += 1
        return count
