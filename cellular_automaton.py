# Cellular Automaton
# Carter Sifferman, 2018
# For CSCI 474 Artificial Intelligence: Dr. Branton, Drury University

import pyglet
from pyglet.gl import *
import sys
import getopt
import rules

FRAME_TIME = 1 / 15
ON_COLOR = (0.2, 0.9, 0.2)
OFF_COLOR = (0.2, 0.2, 0.2)
SCALE = 4
SIM_SIZE = 256


# noinspection PyUnusedLocal
class Environment:

    def __init__(self, sim_size, scale, rule, example=False):
        self.center = int(sim_size/2)
        self.sim_size = sim_size
        self.scale = scale
        self.rule = rule
        self.example = example
        self.running = False
        self.iteration = 0

        # Create empty grid
        self.grid = [[0 for i in range(sim_size)] for j in range(sim_size)]

        # Define the edges to be trimmed each iteration
        self.edges = list()
        for n in range(sim_size):
            self.edges.append((1, n))
            self.edges.append((sim_size - 1, n))

    def simulate(self, delta_time):
        next_grid = [[0 for i in range(self.sim_size)] for j in range(self.sim_size)]
        self.grid = self.rule(self.grid, next_grid)
        self.iteration += 1

        # Trim the edges
        for x, y in self.edges:
            self.grid[x][y] = 0
            self.grid[y][x] = 0

    def render(self):
        # Convert grid to flat list
        batch = pyglet.graphics.Batch()
        for i in range(len(self.grid)):
            for j in range(len(self.grid)):
                if self.grid[i][j] == 1:
                    batch.add(1, pyglet.gl.GL_POINTS, None, ('v2i', (i, j)))
        glPointSize(float(self.scale-1))
        glColor3f(*ON_COLOR)
        batch.draw()

    def set_cell(self, x, y, value): self.grid[x][y] = value

    def clear(self):
        self.grid = [[0 for i in range(self.sim_size)] for j in range(self.sim_size)]
        self.iteration = 0


def handle_arguments(full_cmd_arguments):
    sim_size = SIM_SIZE
    scale = SCALE
    frame_time = FRAME_TIME
    rule = rules.seeds

    argument_list = full_cmd_arguments[1:]
    unix_options = "s:z:hf:r:"
    gnu_options = ["scale=", "size=", "help", "frametime=", "rule="]

    try:
        arguments, values = getopt.getopt(argument_list, unix_options, gnu_options)
    except getopt.error as err:
        print(str(err))
        sys.exit(2)

    for currentArgument, currentValue in arguments:
        print(currentArgument, currentValue)
        if currentArgument in ("-s", "--scale"):
            try:
                scale = int(currentValue)
            except ValueError:
                print("ERROR: Scale must be INT, using default scale (4) instead")
        if currentArgument in ("-z", "--size"):
            try:
                sim_size = int(currentValue)
            except ValueError:
                print("ERROR: Size must be INT, using default size (256) instead")
        if currentArgument in ("-h", "--help"):
            print("")
            print("Controls:")
            print("Press SPACE to play/pause simulation.")
            print("Press R to clear grid and reset iteration counter.")
            print("Press RIGHT arrow to advance forward one iteration")
            print("Click anywhere on window to add new cell, right click to delete.")
            print("Can only draw when simulation is paused.")
            print("")
            print("Supported arguments:")
            print("-h --help       |  Show help")
            print("-s --scale=     |  Set size of each cell in pixels (INT)")
            print("-z --size=      |  Set size of window in number of cells (INT)")
            print("-f --frametime= |  Set length of time between each frame in seconds (FLOAT)")
            print("-r --rule=      |  Set the simulation rule. Must be an exact function name in rules.py")
            sys.exit(0)
        if currentArgument in ("-f", "--frametime"):
            try:
                frame_time = float(currentValue)
            except ValueError:
                print("ERROR: Frametime must be FLOAT, using default frametime (1/15) instead")
        if currentArgument in ("-r", "--rule"):
            try:
                # NOTE: eval is generally not safe to use, but it's ok here because it's all being run locally
                rule = eval("rules." + currentValue)
            except ValueError:
                print("ERROR: Rule not found, using default rule (seeds) instead")

    return sim_size, scale, frame_time, rule


# -----------------------------------------------------Main Program-----------------------------------------------------
def main():
    sim_size, scale, frame_time, rule = handle_arguments(sys.argv)          # Handle command-line arguments
    env = Environment(sim_size=sim_size, scale=scale, rule=rule)            # Initialize environment
    # Initialize window
    window = pyglet.window.Window(env.sim_size * env.scale, env.sim_size * env.scale,
                                  caption="Paused | SPACE to play/pause, click to add cells, R to reset | Iteration: 0")
    pyglet.gl.glClearColor(*OFF_COLOR, 1)                                   # Set background color
    glScalef(env.scale, env.scale, env.scale)                               # Change render scale

    # Draw to window
    @window.event
    def on_draw():
        window.clear()  # remove this for fun
        env.render()
        if env.running:
            window.set_caption("Running | SPACE to play/pause, click to add cells, R to reset | Iteration: "
                               + str(env.iteration))
        else:
            window.set_caption("Paused | SPACE to play/pause, click to add cells, R to reset | Iteration: "
                               + str(env.iteration))

    # Handle mouse presses
    # noinspection PyUnresolvedReferences,PyUnusedLocal
    @window.event
    def on_mouse_press(x, y, button, modifiers):
        if button == pyglet.window.mouse.LEFT:
            env.set_cell(int(round(x/scale)), int(round(y/scale)), 1)
        if button == pyglet.window.mouse.RIGHT:
            env.set_cell(int(round(x/scale)), int(round(y/scale)), 0)

    # Handle mouse drags
    # noinspection PyUnresolvedReferences,PyUnusedLocal
    @window.event
    def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
        if pyglet.window.mouse.LEFT == buttons:
            env.set_cell(int(round(x/scale)), int(round(y/scale)), 1)
        if pyglet.window.mouse.RIGHT == buttons:
            env.set_cell(int(round(x/scale)), int(round(y/scale)), 0)

    # Handle key presses
    # noinspection PyUnusedLocal
    @window.event
    def on_key_press(symbol, modifiers):
        if symbol == pyglet.window.key.SPACE and not env.running:
            pyglet.clock.schedule_interval(env.simulate, frame_time)
            env.running = True
        elif symbol == pyglet.window.key.SPACE and env.running:
            pyglet.clock.unschedule(env.simulate)
            env.running = False
        elif symbol == pyglet.window.key.R:
            env.clear()
            pyglet.clock.unschedule(env.simulate)
            env.running = False
        elif symbol == pyglet.window.key.RIGHT and not env.running:
            env.simulate(None)

    pyglet.app.run()


if __name__ == '__main__':
    main()
