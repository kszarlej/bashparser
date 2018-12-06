import sys
import ply.yacc as yacc
from BashParser import BashParser
from Interpreter import Interpreter

if __name__ == '__main__':
    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "test.sh"
        f = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    BashParser = BashParser()
    parser = yacc.yacc(module=BashParser)
    text = f.read()
    ast = parser.parse(text, lexer=BashParser.lexer, debug=True)
    ast.iaccept(Interpreter())
