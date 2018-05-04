# Cellular Automaton for Education
Simple cellular automaton implementation. Designed for use in an educational setting.

## Example Execution
<p align="center">
  <img src="https://i.imgur.com/K5dk8nC.gif"></img>
</p>

## Command line arguments and controls
Controls and command line arguments can be viewed by running cellular_automaton.py with the argument -h or --help.

## Program Structure
The program is split into two files: cellular_automaton.py, and rules.py. The former houses most of the program logic, command line parameter handling, graphics, and the “main” method. The latter simply gives the former the rules by which to advance the grid. Each function in rules.py receives a grid and returns the next grid. A new function, or “rule” can be added to rules.py, and can be passed in via the “rule” command line parameter without any changes to cellular_automaton.py. This is useful in an educational setting. A student can design their own cellular automata by writing a single simple function, and still get the benefits of a more sophisticated program. Three example rules are defined: “seeds”, “life”, and “life_without_death.”

## Companion Paper
This program was created for CSCI 474 Artificial Intelligence at Drury University. A paper was submitted with the program, and is also in this repository. It is a recommended read for anyone looking to run the program.

## Dependencies and How to Install Them
The only dependency is <a href = "https://bitbucket.org/pyglet/pyglet/wiki/Download"> pyglet. </a> Instructions for installation can be found on pyglet's website. Developed with pyglet v1.3.2.
