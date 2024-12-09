import adsk.core
import adsk.fusion
import traceback

def run(context):
    ui = None
    try:
        # Access the Fusion 360 application and user interface
        app = adsk.core.Application.get()
        ui = app.userInterface
        design = adsk.fusion.Design.cast(app.activeProduct)

        # Ensure an active design is open
        if not design:
            ui.messageBox('No active Fusion design', 'Error')
            return

        rootComp = design.rootComponent

        # Create a new component to hold all copied bodies
        newOcc = rootComp.occurrences.addNewComponent(adsk.core.Matrix3D.create())
        newComp = newOcc.component
        newComp.name = 'Consolidated_Bodies'

        # Iterate over all occurrences in the design
        for occ in rootComp.allOccurrences:
            # Skip the newly created component's occurrence
            if occ.component == newComp:
                continue

            # Check if this occurrence is visible
            if not occ.isLightBulbOn:
                continue

            # Iterate over all bodies in the occurrence's component
            for body in occ.component.bRepBodies:
                # Check if the body is visible
                if body.isLightBulbOn:
                    # Copy the visible body to the new component
                    body.copyToComponent(newOcc)

        ui.messageBox('All visible bodies have been copied to the new component "Consolidated_Bodies".')

    except:
        if ui:
            ui.messageBox('Failed:\n{}'.format(traceback.format_exc()))
