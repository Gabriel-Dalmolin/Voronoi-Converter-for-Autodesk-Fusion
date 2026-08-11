import adsk.core
import adsk.fusion

from .ExecuteHandler import ExecuteHandler
from .DestroyHandler import DestroyHandler
from .InputChangedHandler import InputChangedHandler

class CommandHandler(adsk.core.CommandCreatedEventHandler):
    def __init__(self, handlers, root, baseFeature: adsk.fusion.BaseFeature):
        super().__init__()

        self.handlers = handlers
        self.root = root
        self.baseFeature = baseFeature

    def notify(self, args: adsk.core.CommandCreatedEventArgs) -> None:
        command = args.command

        inputs = command.commandInputs

        tab_3D = inputs.addTabCommandInput(
            "3D",
            "3D"
        )
        children_3D = tab_3D.children

        tab_2D = inputs.addTabCommandInput(
            "2D",
            "2D"
        )
        children_2D = tab_2D.children

        bodyInput = children_3D.addSelectionInput(
            "body",
            "Body",
            "Select the body you want to convert"
        )
        bodyInput.addSelectionFilter("Bodies")
        bodyInput.setSelectionLimits(1, 1)


        children_3D.addValueInput(
            "radius",
            "Radius of connections",
            "mm",
            adsk.core.ValueInput.createByString("1 mm")
        )

        profileInput = children_2D.addSelectionInput(
            "profile",
            "Profile",
            "Select the profile you want to convert"
        )
        profileInput.addSelectionFilter("Profiles")
        profileInput.setSelectionLimits(0, 1)


        children_2D.addValueInput(
            "thickness",
            "Thickness of connections",
            "mm",
            adsk.core.ValueInput.createByString("1 mm")
        )

        inputs.addIntegerSpinnerCommandInput(
            "size",
            "Cell size as percentage of bounding box size",
            0,
            95,
            1,
            40
        )

        inputs.addBoolValueInput(
            "lloyd",
            "Lloyd's relaxation",
            True,
            "",
            True
        )

        input_changed_handler = InputChangedHandler(bodyInput, profileInput)
        command.inputChanged.add(input_changed_handler)
        self.handlers.append(input_changed_handler)

        executeHandler = ExecuteHandler(self.root, input_changed_handler)
        command.execute.add(executeHandler)
        self.handlers.append(executeHandler)

        destroyHandler = DestroyHandler(self.baseFeature)
        command.destroy.add(destroyHandler)
        self.handlers.append(destroyHandler)