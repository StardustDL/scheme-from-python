from sfpy.tokens import LEFT
from .evaluators import Evaluator
from .programs import Program
from .functions import Function, function
from .values import Symbol


def define(evaluator: Evaluator):
    @function(count=2, lazy=True)
    def context(*args: Program):
        name, value = args
        assert len(name) == 1, "The symbol name must be a single string."

        symbol = Symbol(name[0])
        assert symbol.valid(), "The symbol name is not valid."

        evaluator.symbol(symbol, evaluator.evaluate(value))

        return symbol

    return context


def branch(evaluator: Evaluator):
    @function(count=3, lazy=True)
    def context(*args: Program):
        predicate, exprTrue, exprFalse = args
        return evaluator.evaluate(exprTrue if evaluator.evaluate(predicate) else exprFalse)

    return context


def lambdafunc(evaluator: Evaluator):
    @function(count=2, lazy=True)
    def context(*args: Program):
        parameters, body = args
        assert len(parameters) > 0 and parameters.valid(
        ) and parameters[0] == LEFT, f"Parameter list {parameters} is invalid."

        parameters = parameters[1:-1].split()
        assert all(
            len(p) == 1 for p in parameters), f"Parameter list {parameters} is invalid."
        assert len(set(p[0] for p in parameters)) == len(
            parameters), "Parameter names contain conflicts."

        parameters = [Symbol(p[0]) for p in parameters]
        assert all(s.valid()
                   for s in parameters), f"Parameter list {parameters} is invalid."

        @function(count=len(parameters), repr=f"( lambda ( {' '.join(p.raw for p in parameters)} ) {' '.join(body)} )")
        def raw(*args):
            sub = evaluator.sub()
            for parameter, argument in zip(parameters, args):
                sub.symbol(parameter, argument)
            return sub.evaluate(body)

        return raw

    return context
