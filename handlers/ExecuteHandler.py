from jax import P

import adsk.core 
import adsk.fusion

from .InputChangedHandler import InputChangedHandler
from ..scripts.Spatial import body_to_voronoi
from ..scripts.Profile import profile_to_voronoi

class ExecuteHandler(adsk.core.CommandEventHandler):
    def __init__(self, root, input_changed_handler: InputChangedHandler):
        super().__init__()

        self.root = root
        self.input_changed_handler = input_changed_handler


    def notify(self, args: adsk.core.CommandEventArgs) -> None:
        command = args.command
        inputs = command.commandInputs

        tab = self.input_changed_handler.tab

        size = float(adsk.core.IntegerSpinnerCommandInput.cast(inputs.itemById("size")).value)
        lloyd = bool(adsk.core.BoolValueCommandInput.cast(inputs.itemById("lloyd")).value)

        if tab == "3D":
            selection = adsk.core.SelectionCommandInput.cast(inputs.itemById("body")).selection(0)
            body = adsk.fusion.BRepBody.cast(selection.entity)

            radius = float(adsk.core.ValueCommandInput.cast(inputs.itemById("radius")).value)

            body_to_voronoi(self.root, body, radius, size, lloyd)
        elif tab == "2D":
            selection = adsk.core.SelectionCommandInput.cast(inputs.itemById("profile")).selection(0)
            profile = adsk.fusion.Profile.cast(selection.entity)

            thickness = float(adsk.core.ValueCommandInput.cast(inputs.itemById("thickness")).value)

            profile_to_voronoi(profile, thickness)