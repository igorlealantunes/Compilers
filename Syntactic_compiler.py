
from Element import Element
from inspect import getframeinfo, stack
import sys 

class Syntactic_compiler:
    
    def __init__(self, elements):
        self._elements = elements

        # Stores the current element that the compiler is processing
        self._current = self._elements[0]   
        self._current_index = 0

        # not sure if needed, (could we use _current ?)
        self._last_compared_element = None

        # Stores the last elements used to validate in the function _compare_token and _compare_class
        self._last_compared_array = []

    def _read_next(self):
        self._current_index += 1

        try:
            self._current = self._elements[self._current_index]
        except:
            print ("\n\n DONE\n")
            sys.exit()


        print ("Reading : " + self._current.token + " - " + self._current.tokenType)
        
    def _compare_token(self, to_compare_array):

        self._last_compared_array = to_compare_array

        if self._current.token in to_compare_array:
            self._last_compared_element = self._current
            return True
        else:
            return False

    def _compare_class(self, to_compare_array):

        self._last_compared_array = to_compare_array

        if self._current.tokenType in to_compare_array:
            self._last_compared_element = self._current
            return True
        else:
            return False

    def _generate_error(self, message = ""):

        if message == "":
            message = "\nError In line " + str(self._current.line) + "! \n\tExpected ==> " +  ' OR '.join(self._last_compared_array) + "\n\tFound    ==> " + self._current.token + " ( "+ self._current.tokenType+" ) "

        print(message)

        print ("\n\t CALL STACK : \n")
        for i in range(0, 10):
            try :
                caller = getframeinfo(stack()[i][0])
                print ("%s:%d - %s" % (caller.filename, caller.lineno, ""))
            except:
                pass
                
        sys.exit()

    # initial program call
    def run(self):
        self._program()

    """
        Start definiton of filtering methods
    """
    def _program(self):

        if self._compare_token(["program"]):
            self._read_next()

            if self._compare_class(["Indentifier"]):
                self._read_next()

                if self._compare_token([";"]):  
                    self._read_next()
                
                else:
                    self._generate_error()
            else:
                self._generate_error()
        else:
            self._generate_error()


        self._variable_declaration()
        self._subprogram_declaration_v2()
        self._compound_command()

    def _variable_declaration(self):
        if self._compare_token(["var"]):
            self._read_next()
            self._variable_list_declaration()

    def _variable_list_declaration(self):
        self._identifier_list()

        if self._compare_token([":"]):
            self._read_next()
            
            if self._compare_token(["integer", "real", "boolean"]):
                self._read_next()
                
                if self._compare_token([";"]):
                    self._read_next()

                    if self._compare_class(["Indentifier"]): 
                        #self._read_next() not needed
                        self._identifier_list_v2()

                        self._variable_list_declaration()
                    
                else: # error ;
                    self._generate_error()
            else: #error integer, real, boolean
                self._generate_error()
        else: # error :
            self._generate_error()

    def _identifier_list(self):
        # if there are identifiers to read => search for more
        if self._compare_class(["Indentifier"]): 
            self._read_next()
            self._identifier_list_v2()
        else:
            self._generate_error()

    def _identifier_list_v2(self):
        if self._compare_token([","]):
            self._read_next()
            
            if self._compare_class(["Indentifier"]):
                self._read_next()
                self._identifier_list_v2()
            else:
                self._generate_error()

    def _subprogram_declaration_v2(self):

        if self._compare_token(["procedure"]):
            self._subprogram_declaration()

    def _subprogram_declaration(self):
        if self._compare_token(["procedure"]):
            self._read_next()
            
            if self._compare_class(["Indentifier"]):
                self._read_next()

                # Check if there are arguments (optional)
                self._arguments()

                if self._compare_token([";"]):
                    self._read_next()
                else: # error missing ;
                    self._generate_error()

            else: # error missing procedure name
                self._generate_error()

        self._variable_declaration()
        self._subprogram_declaration_v2()
        self._compound_command()

    def _subprogram_variable_list_declaration(self):
        self._identifier_list()

        if self._compare_token([":"]):
            self._read_next()
            
            if self._compare_token(["integer", "real", "boolean"]):
                self._read_next()

                if self._compare_token([";"]):
                    self._read_next()

                    if self._compare_class(["Indentifier"]): 
                        #self._read_next() not needed
                        self._identifier_list_v2()

                        self._subprogram_variable_list_declaration()

            else: #error integer, real, boolean
                self._generate_error()
        else: # error :
            self._generate_error()

    def _arguments(self):

        if self._compare_token(["("]):
            self._read_next()

            self._subprogram_variable_list_declaration()

            if self._compare_token([")"]):
                self._read_next()

            else:# missing )
                self._generate_error()

    def _compound_command(self):
        
        if self._compare_token(["begin"]):

            self._read_next()
            self._optional_commands()

            #self._read_next()
            if self._compare_token(["end"]):

                self._read_next()
                if self._compare_token([";", "."]):
                    self._read_next()
                    
                    # to read more
                    if self._compare_token(["procedure"]): 
                        self._subprogram_declaration_v2()

                else: #missing ; or .
                    self._generate_error()

            else: # missing end
                self._generate_error()
        else:
            self._generate_error()

    def _optional_commands(self):

        self._command_list()

    def _command_list(self):

        self._command()
        self._command_list_v2()

    def _command_list_v2(self):

        if self._compare_token([";"]):
            self._read_next()

            self._command()

            if self._compare_token([";"]):
                self._command_list_v2()

    def _procedure(self):

        #if self._compare_class(["Indentifier"]):
            #self._read_next()

            self._procedure_v2()

    def _procedure_v2(self):

        if self._compare_token(["("]):
            self._read_next()

            self._list_expression()

            if self._compare_token([")"]):
                self._read_next()
            else:
                self._generate_error()

    def _command(self):

        if self._compare_class(["Indentifier"]):

            self._read_next()

            if self._compare_token([":="]):
                self._read_next()

                self._expression()

            else: # procedimento
                self._procedure()

        elif self._compare_token(["begin"]):
            self._compound_command()

        elif self._compare_token(["if"]):
            self._read_next()
            self._expression()

            if self._compare_token(["then"]):
                self._read_next()
                self._command()

                self._else_part()

            else:
                self._generate_error()

        elif self._compare_token(["while"]):
            self._read_next()
            self._expression()

            if self._compare_token(["do"]):
                self._read_next()
                self._command()
            else:
                self._generate_error()
        
        elif self._compare_token(["else"]): # de sinal
            self._read_next()
            self._command()
        
        else:
            self._generate_error("Command error l." + str(self._current.line))

    def _else_part(self):

        if self._compare_token(["else"]): # de sinal
            self._read_next()
            self._command()

    def _expression(self):

        self._simple_expression()
        self._relational_operator()

    def _simple_expression(self):

        if self._compare_token(["+", "-"]): # de sinal
            self._read_next()
        
        self._term()
        self._simple_expression_v2()

    def _simple_expression_v2(self):
        if self._compare_token(["+", "-", "or"]): # aditivos
            self._read_next()

            self._term()

            if self._compare_token(["+", "-", "or"]): # aditivos
                self._read_next()
                self._simple_expression_v2()

    def _relational_operator(self):

        if self._compare_token(["=", "<", ">", "<=", ">=", "<>"]): # relacionais
            self._read_next()
            self._simple_expression()

    def _term_v2(self):

        if self._compare_token(["*", "/", "and"]): # muliplicativos
            self._read_next()
            self._factor()

            if self._compare_token(["*", "/", "and"]): # muliplicativos
                self._term_v2()

    def _term(self):

        self._factor()
        self._term_v2()

    def _factor(self):

        if self._compare_class(['Indentifier']):
            self._read_next()
            self._factor_v2()
        elif self._compare_class(["Integer Number"]):
            self._read_next()
        elif self._compare_class(["Real Number"]):
            self._read_next()
        elif self._compare_token(["True", "False"]):
            self._read_next()
        elif self._compare_token(["("]):
            self._read_next()
            self._expression()

            if self._compare_token([")"]):
                self._read_next()
            else:
                self._generate_error()

        elif self._compare_token(["not"]):
            self._read_next()
            self._factor()

        else:
            self._generate_error(" ERROR - Expected : Indentifier OR Integer Number OR Real Number OR Boolean OR not OR Expression line " + str(self._current.line))

    def _factor_v2(self):

        if self._compare_token(["("]):
            self._read_next()
            self._list_expression()

            if self._compare_token([")"]):
                self._read_next()
            else:
                self._generate_error()

    def _list_expression(self):
        self._expression()
        self._list_expression_v2()

    def _list_expression_v2(self):

        if self._compare_token([","]):
            self._read_next()
            self._expression()

            if self._compare_token([","]):
                self._list_expression_v2()
