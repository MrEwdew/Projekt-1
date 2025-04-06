from mldog.app.context import DefaultDrillContext
from mldog.app.ui.ui import MLDOGUI
from mldog.app.plugins.drill_detect.drill_detect_app import DrillDetectApplication

if __name__ == "__main__":
    # construct a new application context instance
    context = DefaultDrillContext()

    # register additional application plugins
    # context.registerApplication(<your-application-class-here>, 'Your Application Name/Title Here')
    context.registerApplication(DrillDetectApplication, "Drill Detect")

    # run GUI for context
    ui = MLDOGUI(context)
    ui.run()
