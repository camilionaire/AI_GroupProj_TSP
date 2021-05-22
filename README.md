# Travelling Salesperson Problem

## solved by 3 different methods.

## Collaborators:

1. Yufei Tao
2. Jason Bockover
3. Ashley Maddix
4. Camilo Schaser-Hughes

### To run:
1. must have NumPy installed in environment
2. run with `python ./main.py <dataSet.txt>`
3. if no data set is supplied will run `five19.txt`

### Nota Bene:
The datasets have the number of 'cities' present followed by (if supplied) the optimal solution. \

### Notes on current implementation:
Will run SA function 200,000 times.  Right now there is a lot of output, basically every time it makes a non-improveing jump, it prints out what the current heuristic is, what the heuristic it is jumping to, the iteration, and the probability of it making that jump based on the temperature function.  It then prints out the solution it came up with along with it's final heuristic.
