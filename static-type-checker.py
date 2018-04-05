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
	string = re.sub(r';',' ;', string)
	string = re.sub(r'{', ' { ', string)
	string = re.sub(r'}', ' } ', string)
	#string = re.sub(r'\n+','\n',string)
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


def isComment(token):
    if token == "//":
        return True
    return False

class Flags:

    def __init__(self):
        self.errors = 0
        self.inVarBlock = False
        self.inProgBlock = False
        self.doneVarBlock = False
        self.doneProgBlock = False

class TypeChecker:

    def __init__(self, tokens):
        self.prog = tokens
        self.curr = ""
        self.next = ""
        self.flags = Flags()
        self.braceStack=[]

    def _checkBrace(self,token):
        if token not in ['{','}']:
            return

        if token == '{':
            self.braceStack.append(token)
            if len(self.braceStack) == 1:
                if not self.flags.doneVarBlock:
                    sys.stdout.write(" in var ")
                    self.flags.inVarBlock = True
                    self.flags.doneVarBlock = True
                elif not self.flags.doneProgBlock:
                    sys.stdout.write(" in prog ")
                    self.flags.inProgBlock = True
                    self.flags.doneProgBlock = True
        else:
            if len(self.braceStack) == 0:
                return
            self.braceStack.pop()
            if len(self.braceStack) == 0:
                if self.flags.inVarBlock:
                    sys.stdout.write(" leave var ")
                    self.flags.inVarBlock = False
                elif self.flags.inProgBlock:
                    self.flags.inProgBlock = False
                    sys.stdout.write(" leave prog ")


    def _VarBlock(self):
        i=1

    def _ProgBlock(self):
        i=1

    def _inTheVoid(self):
        i=1

    def getNext(self):
        tok="END"
        try:
            tok = self.prog[self.i][self.j + 1]
        except IndexError:
            try:
                tok = self.prog[self.i + 1][0]
            except IndexError:


    def start(self):
        self.i = -1
        for line in self.prog:
            i += 1
            errors = ""
            sys.stdout.write(repr(i).zfill(3)+" : ")
            self.j = 0
            for token in line:
                self.curr = token
                self._checkBrace(token)
                if isComment(token):
                    break
                if self.flags.inVarBlock:
                    self._VarBlock()
                elif self.flags.inProgBlock:
                    self._VarBlock()
                else:
                    self._inTheVoid()
                self.j += 1
            if len(errors) != 0:
                self.flags.errors += 1
            print()


    def end(self):
        if self.flags.errors == 0:
            print("Your program is type error free")
        else:
            print("Your program contains "+repr(self.errors)+" errors")


file_contents = open("test.cmm", "r").read().strip().lower()
checker = TypeChecker(generateTokens(file_contents))
checker.start()
checker.end()
