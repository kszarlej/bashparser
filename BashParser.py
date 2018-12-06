import ply.yacc as yacc
from Lexer import Lexer
import sys
import AST
import TreePrinter


class BashParser(object):

    def __init__(self):
        self.lexer = Lexer()
        self.lexer.build()

    tokens = Lexer.tokens

    precedence = (
        ("left", 'PLUS', 'MINUS'),
        ("left", 'TIMES', 'DIVIDE'),
    )

    def p_program(self, p):
        """program : instructions"""

        p[0] = AST.Program(p[1])
        p[0].printTree(0)

    def p_instructions(self, p):
        """ instructions : instruction instructions
                         | instruction """
        if len(p) == 2:
            p[0] = AST.Instructions(p[1], None)

        if len(p) == 3:
            p[0] = AST.Instructions(p[1], p[2])

    def p_instruction_assignment(self, p):
        """instruction : identifier ASSIGNMENT expression
                       | identifier ASSIGNMENT double_paren_dollar_prefix_expression
        """
        p[0] = AST.Assignment(p[1], p[3])

    def p_instruction_if(self, p):
        """instruction : IF condition SEMICOLON THEN instructions SEMICOLON FI
                       | IF condition SEMICOLON THEN instructions SEMICOLON ELSE instructions SEMICOLON FI
        """
        if len(p) == 8:
            p[0] = AST.If(p[2], p[5], None)
        elif len(p) == 11:
            p[0] = AST.If(p[2], p[5], p[8])

    def p_instruction_while(self, p):
        '''instruction : WHILE condition SEMICOLON DO instructions DONE
        '''
        p[0] = AST.While(p[2], p[5])

    def p_instruction_echo(self, p):
        """instruction : ECHO expression
        """
        p[0] = AST.Echo(p[2])

    def p_instruction_break(self, p):
        """ instruction : BREAK """
        p[0] = AST.Break()

    def p_instruction_continue(self, p):
        """ instruction : CONTINUE """
        p[0] = AST.Continue()

    def p_double_paren_dollar_prefix_expression(self, p):
        """ double_paren_dollar_prefix_expression : DOLLAR DOUBLE_LPAREN expression DOUBLE_RPAREN
        """
        if len(p) == 5:
            p[0] = AST.DoubleParenArithmetic(p[3])

    def p_double_paren_expression(self, p):
        """ instruction : DOUBLE_LPAREN expression DOUBLE_RPAREN
        """

        if len(p) == 4:
            p[0] = AST.DoubleParenArithmetic(p[2])

    def p_identifier(self, p):
        """identifier : IDENTIFIER"""
        p[0] = AST.Identifier(p[1])

    def p_comparators(self, p):
        """comparators : TEST_EQ
                       | TEST_NEQ
                       | TEST_LT
                       | TEST_GT
                       | EQUALS
                       | GT
                       | GTE
                       | LT
                       | LTE
                       """
        p[0] = p[1]

    def p_condition(self, p):
        """ condition : expression
                      | DOUBLE_LBRACKET expression DOUBLE_RBRACKET
                      | LBRACKET expression RBRACKET
        """

        if len(p) == 4:
            p[0] = p[2]
        else:
            p[0] = p[1]

    def p_expression(self, p):
        """expression : identifier
                      | identifier DECREMENT
                      | identifier INCREMENT
                      | const
                      | expression PLUS expression
                      | expression MINUS expression
                      | expression TIMES expression
                      | expression DIVIDE expression
                      | expression comparators expression
                      | LPAREN expression RPAREN"""

        if len(p) == 2:
            p[0] = p[1]
        elif len(p) == 4:
            if p[1] == '(' and p[3] == ')':
                p[0] = p[2]
            else:
                print("p2 {0}, p1 {1}, p3: {2}".format(p[2],p[1],p[3]))
                p[0] = AST.BinExpr(p[2], p[1], p[3])
        elif len(p) == 3:
            if p[2] == '--':
                p[0] = AST.BinExpr('-', p[1], AST.Number(1))
            elif p[2] == '++':
                p[0] = AST.BinExpr('+', p[1], AST.Number(1))

    def p_const_number(self, p):
        """const : NUMBER"""
        p[0] = AST.Number(p[1])

    def p_const_string(self, p):
        """const : STRING"""
        p[0] = AST.String(p[1])

    def p_variable(self, p):
        """const : VARIABLE"""
        p[0] = AST.Variable(p[1])

    def p_const_boolean(self, p):
        """const : BOOLEAN"""
        p[0] = AST.Boolean(p[1])

    ###
    #  Command Call
    ###
    def p_instruction_command_call(self, p):
        """ instruction : command switch_list argument_list
                        | command argument_list
                        | command switch_list
                        | command """

        if len(p) == 2:
            p[0] = AST.CommandCall(p[1], None, None)

        if len(p) == 3:
            if isinstance(p[2], AST.ArgumentList):
                p[0] = AST.CommandCall(p[1], None, p[2])
            elif isinstance(p[2], AST.SwitchList):
                p[0] = AST.CommandCall(p[1], p[2], None)
            else:
                p[0] = AST.CommandCall(p[1], None, None)
        if len(p) == 4:
            p[0] = AST.CommandCall(p[1], p[2], p[3])

    def p_command(self, p):
        """ command : identifier """
        p[0] = AST.Identifier(p[1])

    def p_command_switch(self, p):
        """ switch : MINUS identifier """
        p[0] = AST.CommandSwitch(p[2])

    def p_command_switch_list(self, p):
        """ switch_list : switch switch_list"""
        p[0] = AST.SwitchList([p[1]] + p[2].switch_list)

    def p_command_switch_list_first(self, p):
        """ switch_list : switch """
        p[0] = AST.SwitchList([p[1]])

    def p_command_argument(self, p):
        """ argument : const """
        p[0] = p[1]

    def p_command_argument_list(self, p):
        """ argument_list : argument argument_list"""
        p[0] = AST.ArgumentList([p[1]] + p[2].argument_list)

    def p_command_argument_list_first(self, p):
        """ argument_list : argument """
        p[0] = AST.ArgumentList([p[1]])

    def p_error(self, p):
        print("Syntax error in input! Token: {0}".format(p))
