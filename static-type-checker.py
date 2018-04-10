#!/usr/bin/env python3

'''
Basil Huffman
 bahuffma@gwmail.gwu.edu

 Changes to grammar:

 In the given grammar, the following is given:

 read_expr --> "(" expr ")" ";"

 This makes no sense, as the following statement is allowed:

 read_expr(1.2+4);

 Hence, I am changing the grammar to:

 read_expr --> "(" var ")"

 Since this is a simple language, it will only allow one statement
 (or, in the case of loops and conditionals, one sub-statement) per
 line. So, in practice, this language is a hybrid of Pascal (var
 declaration block occurring before the pprogrammatic block), C
 (syntax and typing), and Python.

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
types={0:"var_code_int", 1:"var_code_float", 2:"var_code_boolean"}
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

def returnType(type):
    if type == "int":
        return 0
    elif type == "float":
        return 1
    return 2

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
        self.int = False
        self.bool = False
        self.float = False

    def resetType(self):
        self.int = False
        self.float = False
        self.bool = False

    def checkTypes(self):
        if self.int and not self.float and not self.bool:
            return True
        if self.float and not self.int and not self.bool:
            return True
        if self.bool and not self.int and not self.float:
            return True
        return False

class TypeChecker:

    def __init__(self, tokens):
        self.prog = tokens
        self.token = ""
        self.next = ""
        self.errors=""
        self.flags = Flags()
        self.braceStack=[]
        self.symbols={}
        self.i = self.j = 0

    # checks braces to determine which block you're in
    def _checkBrace(self):
        if self.token not in ['{','}']:
            return

        if self.token == '{':
            self.braceStack.append(self.token)
            if len(self.braceStack) == 1:
                if not self.flags.doneVarBlock:
                    #sys.stdout.write(" in var ")
                    self.flags.inVarBlock = True
                    self.flags.doneVarBlock = True
                elif not self.flags.doneProgBlock:
                    #sys.stdout.write(" in prog ")
                    self.flags.inProgBlock = True
                    self.flags.doneProgBlock = True
        else:
            if len(self.braceStack) == 0:
                return
            self.braceStack.pop()
            if len(self.braceStack) == 0:
                if self.flags.inVarBlock:
                    #sys.stdout.write(" leave var ")
                    self.flags.inVarBlock = False
                elif self.flags.inProgBlock:
                    self.flags.inProgBlock = False
                    #sys.stdout.write(" leave prog ")

    def _getNextToken(self):
        try:
            tok = self.prog[self.i][self.j + 1]
        except IndexError:
            try:
                tok = self.prog[self.i + 1][0]
            except IndexError:
                tok = ""
        return tok

    def _getNextTokenCode(self):
        tok = self._getNextToken()
        retval = ""
        if tok in reserved:
            retval = reserved[tok]
        elif tok in self.symbols:
            retval = types[self.symbols[tok]]

        return retval

    def _increment(self):
        size = len(self.prog[self.i])
        if self.j < (size-1):
            self.j += 1
        else:
            self.i += 1
            self.j = 0
        try:
            self.token = self.prog[self.i][self.j]
        except IndexError:
            self.token = "END"

    def _if_stmt(self):
        sys.stdout.write("if_stmt")

    def _while_stmt(self):
        sys.stdout.write("while_stmt")

    def _write_stat(self):
        sys.stdout.write("write_stat")

    # read --> "(" var ")"
    # var --> [A-Za-z]+
    def _read_stat(self):
        sys.stdout.write("read_stat")
        next = self._getNextTokenCode()
        if next != "open_paren":
            self.errors += " non-type error: missing '('."
        else:
            self._increment()
        next = self._getNextToken()
        if next not in self.symbols:
            self.errors += " error: contains variable not in symbol table."
            self.flags.errors += 1
        temp = self.prog[self.i]
        l = len(temp)
        while self.token != ')' and self.j < (l-2):
            self._increment()
        if self.token != ';':
            self.errors += " non-type error: missing ')'"

    # var_dec --> type var
    def _var_dec(self):
        sys.stdout.write("var_dec")
        type = returnType(self.token)
        next = self._getNextToken()
        if next not in self.symbols and next not in reserved and checkSymbolName(next):
            self.symbols[next] = types[type]
        else:
            if next in self.symbols:
                self.errors += " type error: variable redifinition."
                self.flags.errors += 1
            else:
                self.errors += " non-type error: disallowed variable name."

    def _assign(self):
        sys.stdout.write("assign")
        if not self.flags.checkTypes():
            self.errors += " type error: incompatible types"
            self.flags.errors += 1
        self.flags.resetType()

    def _program(self):
        if self.token == "{":
            self._checkBrace()
            print(repr(self.i+1).zfill(3)+" open_paren")
            self._increment()
        while(True):
            sys.stdout.write(repr(self.i+1).zfill(3)+" ")
            if self.token == "}":
                self._checkBrace()
                print("close_paren")
                break
            elif self.token == "if":
                self._if_stmt()
            elif self.token == "while":
                self._while_stmt()
            elif self.token == "sys.stdout.write":
                self._write_stat()
            elif self.token == "read":
                self._read_stat()
            elif isType(self.token):
                self._var_dec()
            elif self.token not in [' ',"end_while","end_if"]:
                self._assign()
            else:
                sys.stdout.write("Unknown statement: "+repr(self.prog[self.i]))
            self._skipToEndOfLine()
            print(self.errors)
            self.errors = ""
            self._increment()

    def _skipToEndOfLine(self):
        l = len(self.prog[self.i]) - 1
        while self.j < l:
            self._increment()

    def begin(self):
        temp = self.prog[self.i]
        while(len(temp) == 0):
            self.i += 1
            temp = self.prog[self.i]
        self.token = self.prog[self.i][self.j]
        while(self.token != '{'):
            self._increment()
        self._program()
        while (self.token != '{'):
            self._increment()
        self._program()


    def end(self):
        if self.flags.errors == 0:
            sys.stdout.write("Your program is type error free")
        else:
            sys.stdout.write("Your program contains "+repr(self.flags.errors)+" type error(s)")


file_contents = open("test1.cmm", "r").read().lower()
checker = TypeChecker(generateTokens(file_contents))
#checker.start()
checker.begin()
checker.end()
