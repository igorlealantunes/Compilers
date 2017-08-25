
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
        self._current = self._elements[self._current_index]

        print ("Reading : " + self._current.token)
        
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

        caller = getframeinfo(stack()[1][0])
        print ("%s:%d - %s" % (caller.filename, caller.lineno, ""))

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
        #self._subprogram_declaration()
        #self._compound_command()

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

    def _subprogram_declaration(self):
        pass

    def _subprogram_declaration_v2(self):
        pass







