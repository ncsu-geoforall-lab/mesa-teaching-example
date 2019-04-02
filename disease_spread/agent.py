from mesa import Agent
from random import choice


class TreeCell(Agent):
    """
    A tree cell.

    Attributes:
        x, y: Grid coordinates
        condition: Can be "Fine", "Infected", or "Dead"
        unique_id: (x,y) tuple.

    unique_id isn't strictly necessary here, but it's good
    practice to give one to each agent anyway.
    """
    def __init__(self, pos, model):
        """
        Create a new tree.
        Args:
            pos: The tree's coordinates on the grid.
            model: standard model reference for agent.
        """
        super().__init__(pos, model)
        self.pos = pos
        self.condition = "Fine"
        self.count_inf_steps = 0

    def is_direction(self, pos1, pos2, direction):
        if direction == 'N' and (pos2[1] - pos1[1] > 0):
            return True
        if direction == 'S' and (pos2[1] - pos1[1] < 0):
            return True
        if direction == 'E' and (pos2[0] - pos1[0] > 0):
            return True
        if direction == 'W' and (pos2[0] - pos1[0] < 0):
            return True
        return False

    def step(self):
        """
        If the tree is on fire, spread it to fine trees nearby.
        """
        if self.condition == "Infected":
            self.count_inf_steps += 1
            for neighbor in self.model.grid.iter_neighbors(self.pos, moore=True,
                                                           include_center=False,
                                                           radius=self.model.distance):
                direction = choice(self.model.wind * 2 + 'NSEW')
                if self.is_direction(self.pos, neighbor.pos, direction):
                    if neighbor.condition == "Fine":
                        neighbor.condition = "Infected"
            if self.count_inf_steps > self.model.mortality:
                self.condition = "Dead"

    def get_pos(self):
        return self.pos


class MovingAgent(Agent):
    def __init__(self, pos, model, moore=False):
        super().__init__(pos, model)
        self.pos = pos
        self.moore = moore
        self.condition = "Spreading"

    def move(self):
        # Get neighborhood within vision
        neighbors = [i for i in self.model.grid.get_neighborhood(self.pos, self.moore, False)]
        neighbors.append(self.pos)

        self.random.shuffle(neighbors)
        self.model.grid.move_agent(self, neighbors[0])

    def step(self):
        self.move()
        this_cell = self.model.grid.get_cell_list_contents([self.pos])
        for agent in this_cell:
            if type(agent) is TreeCell:
                agent.condition = "Infected"

    def get_pos(self):
        return self.pos
