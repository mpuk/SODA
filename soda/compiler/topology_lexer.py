import ply.lex as lex
from soda.helpers import open_file
from logging import getLogger

logger = getLogger(__name__)


class TopologyLexer(object):
    keywords = (
        'EXTERNAL',
    )

    tokens = keywords + (
        'IP', 'STATE', 'DIGIT'
    )

    literals = [';', ',']

    # Tokens
    t_IP = r'(?:[0-9]{1,3}\.){3}[0-9]{1,3}'
    t_DIGIT = r'[0-9][0-9]*'

    # Ignored characters
    t_ignore = ' \t\n'

    def t_STATE(self, t):
        r'[a-zA-Z][a-zA-Z]*'
        if t.value in self.keywords:  # is this a keyword?
            t.type = t.value
            return t

        t.value = 'i_' + t.value
        return t

    def t_error(self, t):
        logger.info("Illegal character {0} at line {1}".format(t.value[0], t.lineno))
        t.lexer.skip(1)
        exit()

    def build(self, **kwargs):
        self._lexer = lex.lex(module=self, **kwargs)

    @open_file
    def lexical_analysis(self, file):
        for line in file:
            try:
                lex_input = line
            except EOFError:
                break

            self._lexer.input(lex_input)
            while True:
                token = self._lexer.token()
                if not token:
                    break
                logger.info("{0}".format(token))