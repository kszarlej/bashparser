from visit import when, on
import AST
import logging
from Memory import Memory
from subprocess import Popen, PIPE

class BreakCommand(Exception):
    """ Raised when break called in loop """


class ContinueCommand(Exception):
    """ Raised when continue is called in loop """


class Sys(object):

    def syscmd(self, command, timeout=10):
        proc = Popen(command, stdout=PIPE, stderr=PIPE, stdin=PIPE)
        stdout, stderr = proc.communicate()
        print(stdout.decode('utf-8'))


class Interpreter(object):

    def __init__(self):
        self.memory = Memory.memory
        self.state = 'normal'
        self.sys = Sys()

    def evaluate(self, left, op, right):
        return eval("{0} {1} {2}".format(left, op, right))

    @on('node')
    def visit(self, node):
        pass

    @when(AST.CommandCall)
    def visit(self, node):
        command = node.command.iaccept(self)

        if node.switches is not None:
            switches = node.switches.accept(self)
        else:
            switches = None

        if node.arguments is not None:
            arguments = node.arguments.accept(self)
        else:
            arguments = None

        args = [command.identifier]
        if switches:
            args = args + switches
        if arguments:
            args = args + arguments

        return self.sys.syscmd(args)

    @when(AST.SwitchList)
    def visit(self, node):
        switches = []
        for s in node.switch_list:
            switches.append("-{0}".format(s.iaccept(self)))

        return switches

    @when(AST.CommandSwitch)
    def visit(self, node):
        return node.switch.identifier

    @when(AST.ArgumentList)
    def visit(self, node):
        arguments = []
        for arg in node.argument_list:
            arguments.append("{0}".format(arg.iaccept(self)))

        return arguments

    @when(AST.Instructions)
    def visit(self, node):
        for instr in node.instructions:
            instr.iaccept(self)

    @when(AST.BinExpr)
    def visit(self, node):
        left = node.left.iaccept(self)
        right = node.right.iaccept(self)

        return self.evaluate(left, node.op, right)

    @when(AST.DoubleParenArithmetic)
    def visit(self, node):
        self.state = 'double_paren_arithemtic'
        return node.expression.iaccept(self)
        self.state == 'normal'

    @when(AST.Const)
    def visit(self, node):
        return node.value

    @when(AST.Identifier)
    def visit(self, node):
        if self.state == 'double_paren_arithemtic':
            return self.memory[node.identifier]
        else:
            return node.identifier

    @when(AST.Variable)
    def visit(self, node):
        v = node.identifier.split("$")[1]
        return self.memory[v]

    @when(AST.Program)
    def visit(self, node):
        node.instructions.iaccept(self)

    @when(AST.Echo)
    def visit(self, node):
        print(node.expression.iaccept(self))

    @when(AST.Assignment)
    def visit(self, node):
        val = node.value.iaccept(self)
        if val is not None:
            self.memory[node.identifier.identifier] = val

    @when(AST.If)
    def visit(self, node):
        if node.expression.iaccept(self):
            node.instructions.iaccept(self)
        else:
            if node.elseinstructions is not None:
                node.elseinstructions.iaccept(self)

    @when(AST.Break)
    def visit(self, node):
        raise BreakCommand("Break occured in loop")

    @when(AST.Continue)
    def visit(self, node):
        raise ContinueCommand("Continue occured in loop")

    @when(AST.While)
    def visit(self, node):
        try:
            while node.expression.iaccept(self):
                try:
                    node.instructions.iaccept(self)
                except ContinueCommand:
                    pass
        except BreakCommand:
            pass
