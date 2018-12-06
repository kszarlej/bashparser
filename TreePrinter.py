import AST
import logging


def addToClass(cls):

    def decorator(func):
        setattr(cls, func.__name__, func)
        return func
    return decorator


class TreePrinter:

    @classmethod
    def printIndented(cls, string, level):
        print("| " * level + str(string))

    @addToClass(AST.Node)
    def printTree(self, indent):
        raise Exception("printTree not defined in class " + self.__class__.__name__)

    @addToClass(AST.Program)
    def printTree(self, indent):
        self.instructions.printTree(indent)

    @addToClass(AST.Identifier)
    def printTree(self, indent):
        TreePrinter.printIndented(self.identifier, indent)

    @addToClass(AST.Variable)
    def printTree(self, indent):
        TreePrinter.printIndented(self.identifier, indent)

    @addToClass(AST.BinExpr)
    def printTree(self, indent):
        TreePrinter.printIndented(self.op, indent)
        self.left.printTree(indent+1)
        self.right.printTree(indent+1)

    @addToClass(AST.Instructions)
    def printTree(self, indent):
        for instruction in self.instructions:
            instruction.printTree(indent)

    @addToClass(AST.Assignment)
    def printTree(self, indent):
        TreePrinter.printIndented("=", indent)
        self.identifier.printTree(indent+1)
        self.value.printTree(indent+1)

    @addToClass(AST.Const)
    def printTree(self, indent):
        TreePrinter.printIndented(self.value, indent)

    @addToClass(AST.DoubleParenArithmetic)
    def printTree(self, indent):
        TreePrinter.printIndented("DOUBLE_PAREN_ARITHMETIC", indent)
        self.expression.printTree(indent + 1)

    @addToClass(AST.If)
    def printTree(self, indent):
        TreePrinter.printIndented("IF", indent)
        self.expression.printTree(indent + 1)
        self.instructions.printTree(indent + 1)
        if self.elseinstructions:
            TreePrinter.printIndented("ELSE", indent)
            self.elseinstructions.printTree(indent + 1)

    @addToClass(AST.While)
    def printTree(self, indent):
        TreePrinter.printIndented("WHILE", indent)
        self.expression.printTree(indent + 1)
        self.instructions.printTree(indent + 1)

    @addToClass(AST.CommandCall)
    def printTree(self, indent):
        TreePrinter.printIndented("COMMAND", indent)
        self.command.identifier.printTree(indent+1)
        try:
            self.arguments.printTree(indent + 1)
        except AttributeError:
            pass
        try:
            self.switches.printTree(indent + 1)
        except AttributeError:
            pass

    @addToClass(AST.ArgumentList)
    def printTree(self, indent):
        TreePrinter.printIndented("ARGS", indent)
        if self.argument_list:
            for argument in self.argument_list:
                argument.printTree(indent+2)

    @addToClass(AST.SwitchList)
    def printTree(self, indent):
        TreePrinter.printIndented("SWITCHES", indent)
        if self.switch_list:
            for argument in self.switch_list:
                argument.printTree(indent+2)

    @addToClass(AST.Echo)
    def printTree(self, indent):
        TreePrinter.printIndented("ECHO", indent)
        self.expression.printTree(indent+1)

    @addToClass(AST.Break)
    def printTree(self, indent):
        TreePrinter.printIndented("BREAK", indent)

    @addToClass(AST.Continue)
    def printTree(self, indent):
        TreePrinter.printIndented("CONTINUE", indent)

    @addToClass(AST.CommandSwitch)
    def printTree(self, indent):
        TreePrinter.printIndented(self.switch.identifier, indent)
