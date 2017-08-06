class Element:

	def __init__(self, token, tokenType, line):
		self.token     = token
		self.tokenType = tokenType
		self.line      = line + 1

	def __str__(self):
		return "%s\t\t\t%s\t\t\t%d" % (self.token, self.tokenType, self.line)