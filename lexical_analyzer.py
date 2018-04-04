#!/usr/bin/env python3


'''
Basil Huffman
 bahuffma@gwmail.gwu.edu

 The following assumptions were made after reading the grammar and sample data,
 and speaking after with Dr. Bellaachia regarding clarification:

 - Comments are single line only, prefaced by //, all comments ignored i.e. stripped out
 - Only one statement allowed per line, except comments succeeding a statement
 - as corollary, multiple statements present in one line will be split into two lines:

 	int a; boolean b;

 	becomes

 	int a;
 	boolean b;

 	and line numbers will change accordingly

 - C-- is like Pascal in that the opening block contains nothing but declarations,
   while the second block acts as the programmatic code, in which variable declarations
   are not allowed
 - All blank lines are igored, line numbers are based on lines containing symbols
 - Syntax checking for tokens not residing inside of a block is limited to messages
   indicating as such, more in-depth syntax checking done within blocks
 - Statements do not span multiple lines i.e. all lines must terminate with a semicolon ( ; ),
   unless the line is one of the following special cases:
   + a comment
   + an open block ( { )
   + a close block ( } )
   + the EOL of an if expression, which ends in ( : ). From what I gather, the syntax of an if
     statement is:

     	if bool_stmt :
     	{
     					// statement block
     	}
     	else: 			//optional
     	{
     					// optional statement block
     	}
     	end if;

   + the EOL of a while expression, which ends in ( do ). From what I gather, the syntax of a
     while statement is:

        while bool_stmt do
        {
    					// statement block
        }
        end while;
 - as a corollary, a semicolon ( ; ) alone on a line in permitted, acts as a no-op and is
   allowed in both blocks
 - the first open bracket ( { ) triggers the var declaration block,
   all subsequent open braces are ignored. the first open brace after the var declaration
   block triggers the statement block
 - the first close bracket ( } ) triggers the end of the var declaration block. the
   final close bracket triggers the end of the statement block. if there is no terminating
   close bracket, a syntax error occurs
 - only two blocks exist: var declaration and statement. any blocks outside of these two
   will be considered syntax errors
 - sub-blocks can only be defined through if and while statements. a consequence of this is
   that no sub-blocks can exist within the var declaration block
 - subsequently, symbols will be undefined when encountered in an invalid statement
'''




import re
import sys
import string

#	Constants: reserved words table and types table
reserved = {'int':'type','boolean':'type','float':'type',
	    'if':'if_stmt','while':'while_stmt','do':'while_stmt','else':'if_stmt',
		'end':'if_stmt', ':':'if_stmt','=':'assign_op',
		'*':'multiply_op', '/':'multiply_op','%':'multiply_op',
		'+':'add_op','-':'add_op', ';':'semicolon',
		'read':'read_stat', 'print':'write_stat','and':'and_stmt',
		'or':'or_stmt','>':'rel_stmt','<':'rel_stmt','>=':'rel_stmt',
		'==':'rel_stmt','(':'open_paren',')':'close_paren',
		'{':'open_brace', '}':'close_brace', '//':'comment',';':'semicolon'}
types={"int":0,"boolean":1,"float":2}
codes={"undefined":"unrecognized symbol. ",
	   "wrong_block":"statement not permitted in block. ",
	   "begin_var":"beginning of var declaration block. ",
	   "end_var": "end of var declaration block. ",
	   "begin_stmt":"beginning of statement block. ",
	   "end_stmt":"end of statement block. ",
	   "no_symbol":"no valid variable symbol given. ",
	   "no_semi":"missing semicolon. ",
	   "invalid":"invalid symbol. ",
	   "redefined":"symbol already defined. "}
vblock=["int","float","//","boolean",";","}"]

"""
Syntax errors to check for:

- Proper nesting: check
- Proper characters in symbols: check
- No logic in var dec block:
- No var defn in prog block: check
- Proper if-then-else:
	+ no parenthesis (according to grammar)?:
	+ bool statement:
	+ must have colon and braces:
	+ "else:" :
 	+ end if:
- second block of code after var declaration:
- print/read parens: check.5

"""


def isOpen(token):
	if token == '(' or token == '{':
		return True
	return False

def isClose(token):
	if token == ')' or token == '}':
		return True;
	return False;

def matchingTokens(token1, token2):
	if token1 == '(' and token2 == ')':
		return True
	if token1 == '{' and token2 == '}':
		return True
	return False

#TODO: very ugly, condense
def generateTokens(string):
	retval=[]
	string = re.sub(r';',' ;\n', string)
	string = re.sub(r'{', ' {\n', string)
	string = re.sub(r'}', ' }\n', string)
	string = re.sub(r'\n+','\n',string)
	string = re.sub(r'==','__--__--__',string)
	string = re.sub(r'=', ' = ', string)
	string = re.sub(r'__--__--__',' == ', string)
	string = re.sub(r'\(',' ( ',string)
	string = re.sub(r'\)',' ) ',string)
	string = re.sub(r'\+',' + ',string)
	string = re.sub(r'//','__--__--__',string)
	string = re.sub(r'/',' / ',string)
	string = re.sub(r'__--__--__',' // ',string)
	string = re.sub(r'-',' - ',string)
	string = re.sub(r'\*',' * ',string)
	string = re.sub(r'%',' % ',string)
	string = re.sub(r'>',' > ',string)
	string = re.sub(r'<',' < ',string)
	string = re.sub(r':',' : ',string)
	string = re.sub(r'end while', 'end_while',string)
	string = re.sub(r'end if','end_if',string)
	temp = string.split('\n')
	for line in temp:
		retval.append(line.split())
	return retval

def checkSymbolName(symbol,search=re.compile(r'[^a-zA-z]').search):
	return not bool(search(symbol))

def isType(token):
	if token == 'int' or token == 'boolean' or token == 'float':
		return True
	return False

def is_float(n):
    is_number = True
    try:
        num = float(n)
        # check for "nan" floats
        is_number = num == num   # or use `math.isnan(num)`
    except ValueError:
        is_number = False
    return is_number

def checkNesting(stack,curr):
	if isOpen(curr):
		stack.append(curr)
	elif isClose(curr):
		if len(stack) == 0:
			sys.stdout.write(" ERROR: brace mismatch")
		else:
			temp = stack.pop()
			if not matchingTokens(temp,curr):
				sys.stdout.write(" ERROR: brace mismatch")
				stack.append(temp)
	return stack

def getNumTokens(tokens,i,j,numlines,numtokens):
	if j == (numtokens-1):
		if i < (numlines - 1):
			return tokens[i+1][0]
	else:
		next = tokens[i][j+1]

def isType(token):
	if token in ['int','float','boolean']:
		return True
	return False

class FlagTypes:

	def __init__(self):
		self.inVarDecl = False
		self.inStmtBlk = False
		self.doneVarDecl = False
		self.doneStmtBlk = False
		self.leavingBlock = False
		self.newline = False
		self.symbolToAdd = ""
		self.rp = False
		self.isAssign = False
		self.isIf = False
		self.isWhile = False
		self.braceStack=[]
		self.parenStack=[]


def commentedLine(token):
	if token == '//':
		return True
	return False

class TokenClass:

	def __init__(self,tokens):
		self.tokens = self._stripComments(tokens)
		self.symbols = []
		self.i = self.j = -1
		self.curr = self.next = ""
		self.message = ""
		self.flags = FlagTypes()
		self.firstcomment = False
		self.nextToken = ""
		self.prevToken = ""
		self.syms = []
		self.isInt = False
		self.isBool = False
		self.isFloat = False


	def _stripComments(self,tokens):
		temp1 = []
		for i in tokens:
			temp2 = []
			for j in i:
				if j != '//':
					temp2.append(j)
				else:
					break
			if len(temp2) != 0:
				temp1.append(temp2)

		return temp1

	def _findNextToken(self):
		if self.next in reserved:
			self.nextToken = reserved[self.next]
		elif self.nextToken in self.symbols or isType(self.curr):
			self.nextToken = "var_code"
		else:
			self.nextToken = "undefined"

	def Next(self):

		if len(self.tokens) == 0:
			return False
		if self.i == -1 and self.j == -1:
			self.i = self.j = 0
			self.next = self.tokens[self.i][self.j]

		if self.next == "":
			return False

		self.curr = self.next
		try:
			self.j += 1
			self.next = self.tokens[self.i][self.j]
		except IndexError:
			try:
				self.j = 0
				self.i += 1
				self.flags.newline = True
				self.next = self.tokens[self.i][self.j]
			except IndexError:
				self.next = ""
		self._findNextToken()
		return True

	def _checkBlock(self):
		if self.curr not in ['{','}']:
			return True
		if self.curr == '{':
			self.flags.braceStack.append('{')
			if not self.flags.doneVarDecl:
				self.flags.doneVarDecl = self.flags.inVarDecl = True
				self.message += "\n- entering variable declaration block"
				return True
			elif not self.flags.doneStmtBlk and not self.flags.inVarDecl:
				self.flags.doneStmtBlk = self.flags.inStmtBlk = True
				self.message += "\n- enter statement block"
				return True
		elif self.curr == '}':
			if self.flags.inVarDecl:
				self.flags.inVarDecl = False
				self.flags.leavingBlock = True
				self.message += "\n- leaving variable declaration block"
				return True
			elif self.flags.inStmtBlk:
				self.flags.inStmtBlk = False
				self.flags.leavingBlock = True
				self.message += "\n- leaving statement block"
				return True
		return False

	def _checkSymbol(self):
		if self.curr not in reserved:
			if self.curr in self.symbols and "defined" not in self.message:
				self.message += "\n- symbol already defined"
			else:
				self.syms.append(self.curr)

	def _checkPrintRead(self):
		if self.curr == ')':
			try:
				self.flags.parenStack.pop()
			except IndexError:
				if "improper parenthesis nesting" not in self.message:
					self.message += "\n- improper parenthesis nesting"
		elif self.curr == '(':
			self.flags.parenStack.append('(')
		elif self.curr in ['read','print']:
			self.flags.rp = True
		elif self.curr != ';':
			if len(self.flags.parenStack) == 0 and "improper parenthesis nesting" not in self.message:
				self.message += "\n- improper parenthesis nesting"

	def _checkAssign(self):
		if self.curr == '=':
			self.flags.isAssign = True
		elif  self.curr in reserved:
			if self.curr not in ['+','-','*','/','%','(',')',';'] and "arithmetic" not in self.message:
				self.message += "\n- statement contains non arithmetic tokens"


	def _varErrors(self):
		self._checkSymbol()
		if self.curr in reserved and not isType(self.curr) and (self.i !=0 and self.j != 0):
			if "permitted" not in self.message:
				self.message += "\n- statement not permitted"

	def _stmtErrors(self):
		if isType(self.curr) and "permitted" not in self.message:
				self.message += "\n- statement not permitted"

	def checkCurr(self):
		#first, check block
		if not self._checkBlock():
			if "permitted" not in self.message:
				self.message += "\n- statement not permitted"
		if self.flags.inVarDecl:
			self._varErrors()
		elif self.flags.inStmtBlk:
			self._stmtErrors()
			if self.curr in ['read', 'print'] or self.flags.rp:
				self._checkPrintRead()
			if self.curr == '=' or self.flags.isAssign:
				self._checkAssign()
		#elif not isEndBlock:
		#	if "permitted" not in self.message:
		#		self.message += "\n- statement not permitted"

	def _printLine(self):
		if self.curr in ['end_while','end_if']:
			print('\n'+self.curr[:3]+'\tif_stmt')
			sys.stdout.write(self.curr[4:]+'\t'+reserved[self.curr[4:]])
			return
		sys.stdout.write('\n'+self.curr+'\t')
		if self.curr in reserved:
			sys.stdout.write(reserved[self.curr])
		elif self.curr.isdigit() or is_float(self.curr):
			sys.stdout.write("digit_code")
		elif self.flags.inVarDecl and self.j == 1:
			sys.stdout.write("undefined")
			if "undefined" not in self.message:
				self.message += "\n- undefined symbol"
		elif self.curr in self.symbols or self.flags.inVarDecl:
			sys.stdout.write("var_code")
		else:
			sys.stdout.write("undefined")
			if "undefined" not in self.message:
				self.message += "\n- undefined symbol"
		sys.stdout.write('\t')#+self.nextToken)

	def _checkAddSymbol(self):
		if len(self.syms) == 0:
			return
		#if len(self.syms) > 1 and "many" not in self.message:
		#	self.message += "\n- too many symbols"
		#elif self.syms[0] in self.symbols and "already" not in self.message:
		#	self.message += "\n- symbol already defined"
		#elif isType(self.syms[0]) or not checkSymbolName(self.syms[0]) \
		#	and "characters" not in self.message:
		#	self.message += "\n- symbol contains disallowed characters or reserved words"
		#elif "permitted" not in self.message:
		if len(self.message) == 0 and len(self.syms) == 1:
			self.symbols.append(self.syms[0])
		del self.syms[:]

	def _checkLastTokenVar(self):
		if self.curr not in [';','{']:
			self.message += "\n- missing semicolon"

	def _checkLastTokenStmt(self):
		if not self.flags.isIf and not self.flags.isWhile:
			if self.curr not in [';','{']:
				self.message += '\n- missing semicolon'

	def _stmtBlockLineCheck(self):
		if self.flags.rp:
			if len(self.flags.parenStack) > 0 and "improper parenthesis nesting" \
					not in self.message:
				self.message += "\n- improper parenthesis nesting"
			self.flags.rp = False
			del self.flags.parenStack[:]
		if self.flags.isAssign:
			self.flags.isAssign = False

	def checkLine(self):
		self._printLine()
		if self.flags.newline:
			if self.flags.inVarDecl:
				self._checkLastTokenVar()
				self._checkAddSymbol()
			elif self.flags.inStmtBlk:
				self._stmtBlockLineCheck()
				self._checkLastTokenStmt()
			elif "permitted" not in self.message and not self.flags.leavingBlock:
				self.message += "\n- statement not permitted"
			self.flags.newline = False
			self.flags.leavingBlock = False
			print("\nLine "+repr(self.i)+": "+self.message)
			self.message = ""

def main():
	string = open("test1.cmm", "r").read().strip().lower()
	tokens = TokenClass(generateTokens(string))
	while tokens.Next():
		tokens.checkCurr()
		tokens.checkLine()

if __name__ == '__main__':
	main()