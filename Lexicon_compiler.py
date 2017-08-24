#
# Compilador Lexico
# 
# Aluno      : Igor Leal Antunes (11211416)
# Disciplina : Construcao de compialdores - 2017.1
# Professor  : Clauirton de Albuquerque Siebra

from Element import Element
import sys

class Lexicon_compiler:
	
	def __init__(self, text):
		
		self._program_text = text
		self._key_words  = ["program", "var", "integer", "real", "boolean", "procedure", "begin", "end", "if", "then", "else", "while", "do", "not"]
		
		self._delimiters = [";", ".", ":", "(", ")", ","]
		self._operators  = ["<", ">", "<=", ">=", "<>", "+", "-", "*", "/", ":="]
		
		self._comment_opening_tag = "{"
		self._comment_closing_tag = "}"

		self._is_commenting = False

		self._elements = []

	def __str__(self):
		r = "Token\t\t\tClassification\t\t\tLine\n\n"
		
		for s in self._elements:
			r += str(s) + '\n'
		
		return r

	def print_result(self):
		print(self)

	def run(self):
		
		#print("Running...")

		line_num = 0
		for line in self._program_text.split("\n"):
		   
			line_length = len(line)
			i = 0

			while( i < line_length):
				"""
				print (" line: " + line)
				print (" line_length : " + str(line_length) )
				print (" i : " + str(i) )
				print (" is commenting : " + str(self._is_commenting) )
				"""

				#self.print_result()

				# checks if is closing a comment without opening
				if(line[i] == self._comment_closing_tag and (not self._is_commenting)):
					print("ERRO! COMENTARIO NAO INICIADO, LINHA %d" % line_num)
					sys.exit(1)

				# checks if the comment has stared or still in the middle of it
				if(line[i] == self._comment_opening_tag or self._is_commenting ):
					i = self._validate_comments(line_num, i)

					if( i >= line_length):
						continue
					

				# In case when the compiler is still reading a comment.
				# Ex . block comment (many lines)
				if(self._is_commenting):
					break

				if(line[i] == "/" and line[i+1] == "/"):
					break;

				#checar se eh numero
				if(str.isdigit(line[i]) or line[i] == '.'):

					i = self._validate_numbers(line_num, i)

					if( i >= line_length):
						continue
					

				if(line[i] in self._operators or line[i] in ["=", ":"]):
					i = self._validate_operators(line_num, i)
					if( i >= line_length):
						continue
					

				#checar se a palavra eh composta por letras ou underline
				if(str.isalpha(line[i]) or (line[i] == '_')):
					i = self._validate_words(line_num, i)

					if( i >= line_length):
						continue

				#checa os operadores e delimitadores
				if( line[i] in self._delimiters ):
					i = self._validate_delimiters(line_num, i)
					if( i >= line_length):
						continue

				if(self.checkValidation(line, i)):

					print("Linha : " + line )
					print("ERRO %s NAO FAZ PARTE DO ALFABETO, LINHA %d, COLUNA %d" % (line[i], line_num + 1, i))
					sys.exit(1)
					
				i += 1
					
			# end while
			
			line_num += 1

	def checkValidation(self, line, i):
		return ( (not str.isalpha(line[i]) ) and
		 		 (not str.isdigit(line[i]) ) and
		 		 (not self.isBlank(line[i])) and 
		 		 (not (line[i] in self._delimiters)) and
		 		 (not (line[i] in self._operators or line[i] in ["=", ":"]) ) and 
		 		 (line[i] != self._comment_opening_tag) and (line[i] != self._comment_closing_tag))

	def isBlank(self, a):
		return ((a == ' ') or (a == '\t') or (a == '\n') )

	def _validate_comments(self, line_num, i):

		#print("-- VALIDTE COMMENTS -- ")
		
		line = self._program_text.splitlines()[line_num]
		line_length = len(line)

		#print(" validade comments line " + line)
		#print(" validade comments i" + str(i))
		
		# searches for opening comments
		if(line[i] == self._comment_opening_tag):
			i += 1
			self._is_commenting = True

		# pass through all the comment until reaches the end '}' or the line ends
		while((i < line_length) and (line[i] != self._comment_closing_tag) ):
			i += 1

		# enters only if the comment has not being closed => block comment
		if(i != line_length):
			i += 1
			self._is_commenting = False

		return i

	def _validate_words(self, line_num, i):

		#print("-- VALIDTE WORDS -- ")

		line = self._program_text.splitlines()[line_num]
		line_length = len(line)

		#print(" _validate_words line " + line)
		#print(" i " + str(i))
		#print(" line_length " + str(line_length))
		
		word = line[i]
		i += 1

		while(i < line_length and (str.isalpha(line[i]) or str.isdigit(line[i]) or line[i] == '_' ) ):
			word += line[i]
			i += 1

		#checar se eh reservado ou se eh identificador ou operador (and e or)
		if(word in self._key_words):
			self._elements.append(Element(word, "Reserved Word", line_num))
		#elif(word in self._operators):
		#	self._elements.append(Element(word, "Operator", line_num))
		else:
			self._elements.append(Element(word, "Indentifier", line_num))

		return i

	def _validate_numbers(self, line_num, i):

		#print("-- VALIDTE NUMBERS -- ")

		line = self._program_text.splitlines()[line_num]
		line_length = len(line)

		line_from_i = ""

		j = i
		while( j < line_length ):
			line_from_i += line[j]
			j+=1

		number = line[i]
		i += 1

		if "i+" in line_from_i or "i-" in line_from_i:

			while( i < line_length and str.isdigit(line[i]) ):
				number += line[i]
				i += 1

			if line[i] == "i":
				number += line[i]
				i += 1
				if line[i] == "+" or line[i] == "-":
					number += line[i]
					i += 1

			while( i < line_length and str.isdigit(line[i]) ):
				number += line[i]
				i += 1

			self._elements.append(Element(number, "Numero complexo", line_num))

			return i

		# fim checa de complexo

		while( i < line_length and str.isdigit(line[i])):
			number += line[i]
			i += 1
		
		if( number.startswith(".") and str.isdigit(number[1:]) ):
			
			while(i + 1 < line_length and str.isdigit(line[i + 1])):
				number += line[i]
				i += 1

			self._elements.append(Element(number, "Real Number", line_num))

		#checar se eh inteiro ou real
		elif(i < line_length and line[i] == '.' and str.isdigit(line[i+1])):
			number += line[i]
			i += 1

			while( i < line_length and str.isdigit(line[i])):
				number += line[i]
				i += 1

			self._elements.append(Element(number, "Real Number", line_num))
		elif (i < line_length):
			self._elements.append(Element(number, "Integer Number", line_num))
		else:
			i -= 1

		return i

	def _validate_operators(self, line_num, i):

		#print("-- VALIDTE OPERATORS -- ")

		line = self._program_text.splitlines()[line_num]
		line_length = len(line)

		# take care with erros if undefined in line[i + 1]
		if( line[i] + line[i + 1] in [':=', '>=', '<='] ):
			self._elements.append(Element(line[i] + line[i + 1], "Operators", line_num))
			i += 1
		elif( line[i] in self._operators):
			self._elements.append(Element(line[i], "Operators", line_num))
			#i += 1	
			
		return i

	def _validate_delimiters(self, line_num, i):

		#print("-- VALIDTE DELIMITERS -- ")

		line = self._program_text.splitlines()[line_num]
		line_length = len(line)

		if( i + 1 < line_length and (line[i] + line[i + 1] in self._delimiters) ):
			self._elements.append(Element(line[i] + line[i + 1], "Delimiters", line_num))
			#i += 1
		elif( line[i] in self._delimiters):
			self._elements.append(Element(line[i], "Delimiters", line_num))
			#i += 1

		return i

	def _is_blank(self, line_num, i):
		line = self._program_text.splitlines()[line_num]

		return ((line[i] == ' ') or (line[i] == '\t') or (line[i] == '\n') )

	def get_elements(self):
		return self._elements
