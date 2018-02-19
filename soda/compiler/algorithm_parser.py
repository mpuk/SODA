import ply.yacc as yacc
from soda.helpers import open_file


class AlgorithmParser(object):
    def p_algorithm(self, p):
        ''' algorithm : first_section second_section'''

    def p_first_section(self, p):
        ''' first_section : first_section_line
                          | first_section_line first_section'''

    def p_first_section_line(self, p):
        ''' first_section_line : STATES '=' states_list ';'
                               | REGISTERS '=' register_list ';'
                               | TERM '=' term_list ';' '''

    def p_states_list(self, p):
        ''' states_list  : state_term
                         | states_list ',' state_term'''

    def p_state_term(self, p):
        ''' state_term : NAME'''
        self.behavior.states.append(p[1])

    def p_register_list(self, p):
        ''' register_list : register_term
                          | register_list ',' register_term'''

    def p_register_term(self, p):
        ''' register_term : NAME'''
        self.behavior.registers.append(p[1])

    def p_term_list(self, p):
        ''' term_list : term_term
                      | term_list ',' term_term'''

    def p_term_term(self, p):
        ''' term_term : NAME'''
        self.behavior.term_states.append(p[1])

    def p_second_section(self, p):
        ''' second_section : second_section_state_behavior
                          | second_section_state_behavior second_section'''

    def p_second_section_state_behavior(self, p):
        ''' second_section_state_behavior : NAME begin commands end'''
        self.behavior.states_behaviors[p[1]] = self.state_commands[::-1]
        self.state_commands = []

    def p_commands(self, p):
        ''' commands : command
                     | command commands'''
        self.state_commands.append(p[1])

    def p_command(self, p):
        ''' command : READ
                    | SEND '(' NAME ')'
                    | BECOME '(' NAME ')' '''
        p[0] = (p[1], p[3] if 3 < len(p) else None)

    def p_error(self, p):
        print("Syntax error in input! -> {}".format(p))

    def build(self, lexer, behavior):
        self.lexer = lexer
        self.behavior = behavior
        self.tokens = lexer.tokens
        self._parser = yacc.yacc(module=self)
        self.state_commands = []

    @open_file
    def parsing(self, file):
        def get_token():
            while True:
                token = self.lexer._lexer.token()
                if token is not None:
                    return token
                try:
                    line = next(file)
                    self.lexer._lexer.input(line)
                except StopIteration:
                    return None

        print ("Started algorithm parsing...")
        self._parser.parse("", lexer=self.lexer._lexer, tokenfunc=get_token)
        print ("Ended algorithm parsing...")