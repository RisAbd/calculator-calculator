# Calculator The Game Solver

https://play.google.com/store/apps/details?id=com.sm.calculateme

# Usage

```bash

# as script arguments
./calculator_calculator.py -- MOVES_COUNT GOAL INITIAL_VALUE ACTIONS...

./calculator_calculator.py -- 4 64 128 x4 /4 sum '5=>16'

# if some arguments are missing script will wait for them in input

# as input 
echo '4 64 128 x4 /4 sum 5>16' | ./calculator_calculator.py --first

# some actions descriptions can be understood in bash as piping (e.g. <<, =>, * actions)
# don't forget to quote them or just use stdin 


```

## Supported Actions

I just reached 101 level, and added all seen actions till this level.
Actions seen so far:
* binary operations:
    * "+"
    * "-"
    * "/"
    * "*" 
* append operation, e.g. 1, 15 (means append 15 to end of current value)
* sum digits operation (sum)
* reverse (rev)
* transform (15=>51, 1>2)
* delete (<<)
* negotiation (+/-).

other actions (if any left) will be added as soon as i reach them. Or you can contribute (:
