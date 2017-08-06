#
# Compilador Lexico
# 
# Aluno      : Igor Leal Antunes (11211416)
# Disciplina : Construcao de compialdores - 2017.1
# Professor  : Clauirton de Albuquerque Siebra
#
#
# uso : 
#       utilizando pipe de arquivo:
#           > python3 app.py < nome_do_arquivo.txt

import sys
from Lexicon_compiler import Lexicon_compiler

def main(argv):

	print("File contents")
	
	file_contents = ""
	for line in sys.stdin:
		file_contents += line
	
	compiler = Lexicon_compiler(file_contents)
	compiler.run()
	compiler.print_result()

if __name__ == "__main__":
  	main(sys.argv)