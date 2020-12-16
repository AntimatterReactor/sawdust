from sly import Lexer, Parser


class sawdustLexer(Lexer):
    tokens = {
        'NAME', 'NUMBER', 'STRING',
        'OUTPUT', 'CONSOLE', 'FILE'
    }
    ignore = ' \t'
    literals = {'=', '+', '-', '*', '/', '(', ')', '@'}

    # Tokens
    NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'

    NAME['output'] = OUTPUT
    NAME['console'] = CONSOLE
    NAME['file'] = FILE

    @_(r'".*"')
    def STRING(self, t):
        t.value = t.value[1:len(t.value)-1]
        return t

    @_(r'\d+')
    def NUMBER(self, t):
        t.value = int(t.value)
        return t

    @_(r'\n+')
    def newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print("Illegal character '%s'" % t.value[0])
        self.index += 1


class sawdustParser(Parser):
    tokens = sawdustLexer.tokens

    precedence = (
        ('left', '+', '-'),
        ('left', '*', '/'),
        ('right', 'UMINUS'),
    )

    def __init__(self):
        self.names = {}

    @_('NAME "=" expr')
    def statement(self, p):
        self.names[p.NAME] = p.expr

    @_('OUTPUT "@" CONSOLE expr')
    def statement(self, p):
        print(p.expr)

    @_('expr')
    def statement(self, p):
        pass

    @_('expr "+" expr')
    def expr(self, p):
        return p.expr0 + p.expr1

    @_('expr "-" expr')
    def expr(self, p):
        return p.expr0 - p.expr1

    @_('expr "*" expr')
    def expr(self, p):
        return p.expr0 * p.expr1

    @_('expr "/" expr')
    def expr(self, p):
        return p.expr0 / p.expr1

    @_('"-" expr %prec UMINUS')
    def expr(self, p):
        return -p.expr

    @_('"(" expr ")"')
    def expr(self, p):
        return p.expr

    @_('STRING')
    def expr(self, p):
        return p.STRING

    @_('NUMBER')
    def expr(self, p):
        return p.NUMBER

    @_('NAME')
    def expr(self, p):
        try:
            return self.names[p.NAME]
        except LookupError:
            print("Undefined name '%s'" % p.NAME)
            return 0


if __name__ == '__main__':
    lexer = sawdustLexer()
    parser = sawdustParser()
    parser.parse(lexer.tokenize(''))
