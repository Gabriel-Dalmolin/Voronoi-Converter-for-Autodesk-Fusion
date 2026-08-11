import adsk.core

class InputChangedHandler(adsk.core.InputChangedEventHandler):
    def __init__(self, bodyInput: adsk.core.SelectionCommandInput, profileInput: adsk.core.SelectionCommandInput):
        super().__init__()

        self.tab = "3D"
        self.bodyInput = bodyInput
        self.profileInput = profileInput

    def notify(self, eventArgs: adsk.core.InputChangedEventArgs) -> None:
        changed = eventArgs.input

        if changed.id.strip() == "APITabBar":
            if self.tab == "3D":
                self.tab = "2D"
            elif self.tab == "2D":
                self.tab = "3D"

        if self.tab == "3D":
            self.tab = "3D"
            self.bodyInput.setSelectionLimits(1, 1)
            self.profileInput.setSelectionLimits(0, 1)
            self.profileInput.clearSelection()
        elif self.tab == "2D":
            self.tab = "2D"
            self.bodyInput.setSelectionLimits(0, 1)
            self.profileInput.setSelectionLimits(1, 1)
            self.bodyInput.clearSelection()