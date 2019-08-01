from cx_Freeze import setup, Executable

# On appelle la fonction setup
setup(
    name = "path following algorithm",
    version = "0.1",
    description = "Make the robot Cozmo follow a trajectory given in an excel file",
    executables = [Executable("run.py")],
)
