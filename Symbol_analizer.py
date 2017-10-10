#
# Compilador Lexico
# 
# TODO : Colocar a analise no sintatico
# 
# 
# Aluno      : Igor Leal Antunes (11211416)
# Disciplina : Construcao de compialdores - 2017.1
# Professor  : Clauirton de Albuquerque Siebra

from Element import Element
import sys

class Symbol_analizer:
    
    def __init__(self):
        self.list = []
        self.token = "$"
        self.x = 0

    def begin_scope(self):
        self.list.append(self.token)
        self.print("Novo escopo...")

    def end_scope(self):
        
        i = len(self.list) - 1
        while self.list[i] != self.token:
            self.list.pop()
            self.print()
            i -= 1

        self.list.pop()

        self.print("After removal...")

    def add_symbol(self, symbol):
        self.list.append(symbol)
        self.print("Added symbol: " + symbol)

    def process_symbol(self, symbol, current_line = ""):

        if self.x == 0:
            self.add_symbol(symbol)
        else:
            print("\tChecking is declared: " + symbol)
            if not self.is_declared(symbol):
                error = "Symbol not declared !: " + symbol + (" On Line: " + str(current_line) ) if current_line != "" else "" 
                self._generate_error(error)

    def is_declared(self, symbol):
        return symbol in self.list

    def print(self, txt = ""):

        if txt != "":
            print(txt+"\n")

        r = "STACK: "
        
        for s in self.list:
            r += str(s) + ', '
        
        print(r+'\n')

    def _generate_error(self, message = ""):
        print ("\n\n\tERROR : " + message)
        sys.exit()

    def increment_x(self):
        self.x += 1
        print("\n\n\t\tx: " + str(self.x))

    def decrement_x(self):
        self.x -= 1
        print("\n\n\t\tx: " + str(self.x))
