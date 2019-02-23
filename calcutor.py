#!/usr/bin/python3
import sys, os
import itertools as IT

OPERATIONS = {
    '+': lambda a, b: a+int(b),
    '-': lambda a, b: a-int(b),
    'x': lambda a, b: a*int(b),
    '*': lambda a, b: a*int(b),
    '/': lambda a, b: a/int(b),
    '<': lambda a, b: int(a/10) 
}

def apply_operations(init, ops):
    # print('\t', init, ops)
    for op, value in ((OPERATIONS[o[0]], o[1:]) for o in ops):
        init = op(init, value)
    return init


def main():

    executable_name, moves, goal, init, *buttons = sys.argv

    moves = int(moves)
    goal = int(goal)
    init = int(init)

    # print('input:\n\tmoves: {}, goal: {}, init: {}, buttons: {}'.format(moves, goal, init, buttons))


    valid_combinations = []

    for ops in IT.chain.from_iterable(IT.permutations(i) for i in IT.combinations_with_replacement(buttons, moves)):
        if apply_operations(init, ops) == goal:
            valid_combinations.append(ops)

    print(*set(valid_combinations), sep='\n')




if __name__ == '__main__':
    main()
