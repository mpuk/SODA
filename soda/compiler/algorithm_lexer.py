import ply.lex as lex
from soda.helpers import open_file
from logging import getLogger, info

logger = getLogger(__name__)


class AlgorithmLexer(object):
    keywords = (
        'TERM', 'STATES', 'REGISTERS',
        'begin', 'end',
        'SEND', 'BECOME', 'READ'
    )

    tokens = keywords + (
        'NAME',
    )

    literals = ['=', ',', ';', '(', ')']

    # Ignored characters
    t_ignore = ' \t\n'

    def t_NAME(self, t):
        r'[a-zA-Z][a-zA-Z]*'
        if t.value in self.keywords:  # is this a keyword?
            t.type = t.value
        return t

    def t_error(self, t):
        logger.info("Illegal character {0} at line {1}".format(t.value[0], t.lineno))
        t.lexer.skip(1)

    def build(self, **kwargs):
        self._lexer = lex.lex(module=self, **kwargs)

    @open_file
    def lexical_analysis(self, file):
        logger.info("Started algorithm lexical analysis")

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

        logger.info("Ended algorithm lexical analysis")
