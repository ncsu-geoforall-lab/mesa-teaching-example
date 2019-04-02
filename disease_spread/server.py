from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter

from .model import ForestDisease

COLORS = {"Fine": "#00AA00",
          "Infected": "#880000",
          "Dead": "#000000",
          "Spreading": "#FFF900"}


def forest_disease_portrayal(tree):
    if tree is None:
        return
    portrayal = {"Shape": "rect", "w": 1, "h": 1, "Filled": "true", "Layer": 0}
    (x, y) = tree.get_pos()
    portrayal["x"] = x
    portrayal["y"] = y
    portrayal["Color"] = COLORS[tree.condition]
    return portrayal


canvas_element = CanvasGrid(forest_disease_portrayal, 100, 100, 500, 500)
tree_chart = ChartModule([{"Label": label, "Color": color} for (label, color) in COLORS.items()])

model_params = {
    "height": 100,
    "width": 100,
    "density": UserSettableParameter("slider", "Tree density", 0.65, 0.01, 1.0, 0.01),
    "mortality": UserSettableParameter("slider", "Dead after n years", 1, 1, 10, 1),
    "wind": UserSettableParameter('choice', 'Prevailing wind direction', value='N',
                                  choices=['N', 'S', 'E', 'W']),
    "distance": UserSettableParameter("slider", "Distance", 1, 1, 5, 1)

}
server = ModularServer(ForestDisease, [canvas_element, tree_chart], "Forest Disease", model_params)
