# ------------------------------------------------------------
# tokens.py
#
# tokenizer for a bash interpreter.
# ------------------------------------------------------------
import ply.lex as lex
import sys


class Lexer(object):

    def input(self, text):
        self.lexer.input(text)

    def build(self):
        self.lexer = lex.lex(object=self)

    def token(self):
        return self.lexer.token()

    tokens = (
        'VARIABLE',
        'CHAR',
        'IDENTIFIER',
        'SEMICOLON',
        'DOLLAR',
        'AMPERSAND',
        'NEWLINE',
        'NUMBER',
        'STRING',
        'EQUALS',
        'ASSIGNMENT',

        # comparations
        'EQ',
        'NEQ',
        'LT',
        'GT',
        'LTE',
        'GTE',
        'TEST_EQ',
        'TEST_NEQ',
        'TEST_GT',
        'TEST_LT',
        'BOOLEAN',

        # brackets/braces/parens
        'LBRACE',
        'RBRACE',
        'LPAREN',
        'RPAREN',
        'LBRACKET',
        'RBRACKET',
        'DOUBLE_LPAREN',
        'DOUBLE_RPAREN',
        'DOUBLE_LBRACKET',
        'DOUBLE_RBRACKET',

        # arithmetic
        'INCREMENT',
        'DECREMENT',
        'PLUS',
        'MINUS',
        'TIMES',
        'DIVIDE',

        # LOOPS
        'FOR',
        'WHILE',
        'DO',
        'DONE',
        'BREAK',


        # CONDITIONALS
        'IF',
        'FI',
        'THEN',
        'ECHO',
        'ELSE',
        'IN',
        'CONTINUE',

        # MISC
        'SHABANG',
        'LINE_COMMENT'
    )

    # Regular expression rules for simple tokens
    t_SHABANG            = r'\#\!\/bin\/bash'
    t_TEST_EQ            = r'-eq'
    t_TEST_NEQ           = r'-ne'
    t_TEST_GT            = r'-gt'
    t_TEST_LT            = r'-lt'
    t_PLUS               = r'\+'
    t_MINUS              = r'-'
    t_TIMES              = r'\*'
    t_DIVIDE             = r'/'
    t_EQUALS             = r'=='
    t_DOLLAR             = r'\$'
    t_AMPERSAND          = r'\&'
    t_SEMICOLON          = r';'
    t_LT                 = r"\<"
    t_GT                 = r"\>"
    t_LTE                = r"\<\="
    t_GTE                = r"\>\="
    t_LBRACE             = r"{"
    t_RBRACE             = r"}"
    t_LPAREN             = r'\('
    t_RPAREN             = r'\)'
    t_LBRACKET           = r"\["
    t_RBRACKET           = r"\]"
    t_DOUBLE_LPAREN      = r"\(\("
    t_DOUBLE_RPAREN      = r"\)\)"
    t_DOUBLE_LBRACKET    = r"\[\["
    t_DOUBLE_RBRACKET    = r"\]\]"
    t_INCREMENT          = r"\+\+"
    t_DECREMENT          = r"\-\-"
    t_ASSIGNMENT         = r"="

    # Reserved words:
    reserved_keywords = {
        'if':    'IF',
        'then':  'THEN',
        'else':  'ELSE',
        'for':   'FOR',
        'while': 'WHILE',
        'in':    'IN',
        'fi':    'FI',
        'do':    'DO',
        'done':  'DONE',
        'echo':  'ECHO',
        'break': 'BREAK',
        'continue': 'CONTINUE'
    }

    def t_NUMBER(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    def t_LINE_COMMENT(self, t):
        r'\#.*'
        pass

    def t_IDENTIFIER(self, t):
        r"[a-zA-Z]([a-zA-Z0-9])*"
        if t.value.lower() in self.reserved_keywords:
            t.type = self.reserved_keywords[t.value.lower()]
            return t

        if t.value.lower() == 'true':
            t.type = 'BOOLEAN'
            return t

        t.type = 'IDENTIFIER'
        return t

    def t_VARIABLE(self, t):
        r'\$[A-Za-z_?-@#][\w_]*'
        return t

    def t_STRING(self, t):
        r"(\"([^\\\"]|(\\.))*\")|(\'([^\\\']|(\\.))*\')"
        escaped = 0
        str = t.value[1:-1]
        new_str = ""
        for i in range(0, len(str)):
            c = str[i]
            if escaped:
                if c == "n":
                    c = "\n"
                elif c == "t":
                    c = "\t"
                new_str += c
                escaped = 0
            else:
                if c == "\\":
                    escaped = 1
                else:
                    new_str += c
        t.value = new_str
        return t

    # Define a rule so we can track line numbers
    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    # A string containing ignored characters (spaces and tabs)
    t_ignore  = ' \t'

    # Error handling rule
    def t_error(self, t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)


if __name__ == '__main__':
    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "test.sh"
        f = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    lexer = Lexer()
    lexer.build()
    lexer.input(f.read())
    while True:
        token = lexer.token()
        if not token:
            break
        print(token)
