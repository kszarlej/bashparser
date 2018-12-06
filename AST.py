
class Node(object):

    def accept(self, visitor):
        result = visitor.visit(self)
        return result

    def iaccept(self, visitor):
        result = visitor.visit(self)

        if isinstance(result, list):
            if result:
                return result[0]
            else:
                return None
        else:
            return result


class Identifier(Node):
    def __init__(self, identifier):
        self.identifier = identifier


class Variable(Node):
    def __init__(self, identifier):
        self.identifier = identifier


class BinExpr(Node):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right


class Program(Node):
    def __init__(self, instructions):
        self.instructions = instructions


class Assignment(Node):
    def __init__(self, identifier, value):
        self.identifier = identifier
        self.value = value


class Instructions(Node):
    def __init__(self, instruction, instructions):
        self.instructions = []
        if instruction:
            self.instructions.append(instruction)
        if instructions:
            self.instructions.extend(instructions.instructions)


class Const(Node):
    def __init__(self, value):
        self.value = value


class Number(Const):
    pass


class String(Const):
    pass


class Boolean(Const):
    pass


class DoubleParenArithmetic(Node):
    def __init__(self, expression):
        self.expression = expression


class If(Node):
    def __init__(self, expression, instructions, elseinstructions):
        self.expression = expression
        self.instructions = instructions
        self.elseinstructions = elseinstructions


class Break(Node):
    pass


class Continue(Node):
    pass


class While(Node):
    def __init__(self, expression, instructions):
        self.expression = expression
        self.instructions = instructions


class Echo(Node):
    def __init__(self, expression):
        self.expression = expression


class CommandCall(Node):
    def __init__(self, command, switches, arguments):
        self.command = command
        self.arguments = arguments
        self.switches = switches


class CommandSwitch(Node):
    def __init__(self, switch):
        self.switch = switch


class ArgumentList(Node):
    def __init__(self, argument_list):
        self.argument_list = argument_list


class SwitchList(Node):
    def __init__(self, switch_list):
        self.switch_list = switch_list
