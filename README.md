# Travelling Salesperson Problem

## Solved by Genetic Algorithm, Simmulated Annealing, and Ant Colony Optimization.

## Collaborators:

1. Yufei Tao
2. Jason Bockover
3. Ashley Maddix
4. Camilo Schaser-Hughes

### To run:

1. Install NumPy
2. Install matplotlib.pyplot
3. Install PySimpleGUI
4. Run the program with `python main.py`

### Nota Bene:

Some adjustments may need to be made to varialbes within program code. Adjustable variables will be on top of each subsequent files code. Files with adjustable vars:

- `ga.py`
- `aGoAtACO.py`
- `simAnTSP.py`

### Datasets:

The datasets used for this project were from: https://people.sc.fsu.edu/~jburkardt/datasets/tsp/tsp.html  
As best as we can figure, the datasets are:

1. A simple 5 map with small distances.
2. The map of French cities.
3. Dantzig42, a reduction of 48 contiguous city / states + D.C.
4. The 48 contiguous U.S. capitals.

### Notes on current implementation:

Upon starting, you will have 4 options for running the program. All 3 implementations should be set up with variables for the 48 puzzle, for other puzzles you may have to adjust variables at top of code in order to get more optimal results. After selecting map / puzzle option will be able to choose 1 of 3 of algorithms to approximate an optimal solution. At the end of each a graph will be printed visualizing the results.

For the ACO, the end tao (representation of pheromone) will write itself to the file name finalTao.txt. Because we were having troubles escaping the local minima for the ACO, if no change is detected in any of the ants tours over so many iterations, a homogeny message will display and the iterations will stop.

We did have a couple alternate versions of algorithms going as well. Those can be run with `python newGA.py` and `python antColony.py` and are GA and ACO algorithms, respectively.
