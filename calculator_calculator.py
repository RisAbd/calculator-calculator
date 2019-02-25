#!/usr/bin/python3
import sys, os
import itertools as IT


import typing as T


class Game:

    def __init__(self, moves_count, goal, initial_value, actions, *, name=None):
        self.name = name
        self.moves_count = self.moves = moves_count
        self.goal = goal
        self.initial_value = self.initial = initial_value
        self.actions = self.buttons = actions

    def __str__(self):
        return (self.name+' ' if self.name else '') + '{} -> {}: {{{}}} * {}'.format(
            self.initial_value,
            self.goal,
            ', '.join(map(str, self.actions)),
            self.moves_count,
            )




class Action:

    def __call__(self, context):
        raise NotImplementedError()


class Func(Action):

    def __init__(self, func: T.Callable, name=None):
        self.name = name or func.__name__
        self.action_func = func

    def __call__(self, *args, **kwargs):
        return self.action_func(*args, **kwargs)

    def __str__(self):
        return self.name


class ActionParser:
    def parse(self, raw: str) -> T.Optional[T.Callable]:
        raise NotImplementedError()


# Actions

class BinaryOperation(Action):
    def __init__(self, operation: str, value: int, func: T.Callable[[int, int], int]):
        self.op = operation
        self.value = value
        self.func = func
    def __call__(self, ctx):
        ctx.current = self.func(ctx.current, self.value)
    def __str__(self):
        return '{}{}'.format(self.op, self.value)


class BinaryOperationParser(ActionParser):

    binary_operations = {
        '+': lambda a, b: a+b,
        '-': lambda a, b: a-b,
        '/': lambda a, b: a/b,
        '*': lambda a, b: a*b,
        'x': lambda a, b: a*b,
        '^': lambda a, b: a**b,
    }

    def parse(self, raw):
        if len(raw) < 2:
            return
        op = raw[0]
        v = raw[1:]
        if op in self.binary_operations and (v.isdigit() or v[1:].isdigit()):
            return BinaryOperation(op, int(v), self.binary_operations[op])


class Reverse(Action):
    def __call__(self, ctx):
        c = int(ctx.current)
        ctx.current = int(('-' if c < 0 else '') + str(abs(c))[::-1])


class ReverseActionParser(ActionParser):
    def parse(self, raw):
        if raw.lower() in 'rvs rvrs reverse rev r rv revs'.split():
            return Func(Reverse(), name='reverse')


class Append(Action):
    def __init__(self, value: T.Union[int, str]):
        self.value = str(value)
    def __call__(self, ctx):
        ctx.current = int(str(int(ctx.current))+self.value)
    def __str__(self):
        return self.value


class AppendParser(ActionParser):
    def parse(self, raw):
        if raw.isdigit():
            return Append(raw)


class Delete(Action):
    def __call__(self, ctx):
        c = ctx.current
        r = str(int(c))[:-1]
        if c == 0 or r in ('', '-'):
            v = 0
        else:
            v = int(r)
        ctx.current = v


class DeleteActionParser(ActionParser):
    def parse(self, raw):
        if raw in ('<', '<<'):
            return Func(Delete(), '<<')


class Swap(Action):
    def __init__(self, a, b):
        self.a, self.b = a, b
    def __call__(self, ctx):
        ctx.current = int(str(int(ctx.current)).replace(self.a, self.b))
    def __str__(self):
        return '{}=>{}'.format(self.a, self.b)


class SwapActionParser(ActionParser):
    def parse(self, raw):
        for sw in ('=>', '>'):
            if sw in raw:
                return Swap(*raw.split(sw))


class Negotiate(Action, ActionParser):
    def parse(self, raw):
        if raw in ('+/-', '+-', ):
            return self
    def __call__(self, ctx):
        ctx.current = -ctx.current
    def __str__(self):
        return '+/-'


class SumDigits(Action, ActionParser):
    def parse(self, raw):
        if raw.lower() in ('sum', 's'):
            return self
    def __call__(self, ctx):
        ctx.current = sum(map(int, (ch for ch in str(ctx.current) if ch.isdigit())))
    def __str__(self):
        return 'sum'



class Solution:         # type: T.List[Action]
    
    class Context:
        def __init__(self, i):
            self.initial = i
            self.current = i

        def __str__(self):
            return str(self.current)

    def __init__(self, initial, goal, actions):
        self.initial = initial
        self.goal = goal
        self.actions = actions

    def solve(self, *, verbose=False) -> bool:
        ctx = self.Context(self.initial)
        for a in self.actions:
            try:
                a(ctx)
                if ctx.current - int(ctx.current) != 0:
                    return False
            except ValueError:
                raise
                return False
        if verbose:
            print(ctx.current)
        return ctx.current == self.goal

    def __bool__(self):
        return self.solve()

    def __str__(self):
        return ', '.join(map(str, self.actions))

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        if not isinstance(other, Solution):
            return NotImplemented
        return hash(self) == hash(other)


def parsers():
    return [
        BinaryOperationParser(),
        DeleteActionParser(),
        AppendParser(),
        SwapActionParser(),
        Negotiate(),
        ReverseActionParser(),
        SumDigits(),
    ]


def parse_actions(raw_actions, parsers):
    actions = []
    for ra in raw_actions:
        for p in parsers:
            action = p.parse(ra)
            if action:
                actions.append(action)
                break
        else:
            assert False, 'unknown action: '+ra
    return actions


class Context:
    def __init__(self, i):
        self.initial = i
        self.current = i

    def __str__(self):
        return str(self.current)


def solve(game, *, live=False, any=False) -> T.Set[Solution]:

    # actions = parse_actions(game.actions, parsers())

    solutions = set()
    for actions_variant in IT.chain.from_iterable(map(IT.permutations, IT.combinations_with_replacement(game.actions, game.moves_count))):
        s = Solution(initial=game.initial_value, goal=game.goal, actions=actions_variant)
        # print(s)
        if s:
            if live and s not in solutions:
                print(s)
            solutions.add(s)
            if any and solutions:
                break

    return solutions


def main():

    import optparse

    parser = optparse.OptionParser(usage='%prog [options] -- MOVES GOAL INTIAL ACTIONS...')

    parser.add_option('--live', '-f', dest='live', default=False, action='store_true', help='print any solution immideately when found')
    parser.add_option('--short', '--first', dest='short', default=False, action='store_true', help='finish at first found solution')

    opts, args = parser.parse_args()


    while len(args) < 4:
        args = args + input().split()

    moves, goal, init, *actions = args
    moves, goal, init = map(int, [moves, goal, init])

    g = Game(moves, goal, init, parse_actions(actions, parsers()))
    print(g)

    print(*solve(g, live=opts.live, any=opts.short), sep='\n')


if __name__ == '__main__':
    main()
