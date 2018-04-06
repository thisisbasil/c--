#!/usr/bin/env python3

'''
Basil Huffman
 bahuffma@gwmail.gwu.edu
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
types={0:"VAR_CODE_INT", 1:"VAR_CODE_FLOAT", 2:"VAR_CODE_BOOLEAN"}
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

    def _var_dec(self):
        next = self._getNextToken()
        if next not in self.symbols:
            if self.token == "int":
                _type = 0
            elif self.token == "float":
                _type = 1
            else:
                _type = 2
            self.symbols[next] = _type
            self._increment()
            if self._getNextTokenCode() == "semicolon":
                return


        # else, redef

    def _assign(self):
        if self.token in self.symbols

    def _stmt(self):
        code = reserved[self.token]
        if code in ["open_paren","close_paren"]:
            self._checkBrace()
        elif code == "type":
            self._var_dec()
        elif code == "write_stat":
            self._write_stat()
        else:
            self._assign()

    def begin(self):
        self.token = self.prog[self.i][self.j]
        while True:
            if self.token == "END":
                return
            if self.i >= len(self.prog):
                return

            if isComment(self.token):
                self.i += 1
                self.j = 0

            if self.token in reserved:
                self._stmt()
            self._increment()


    def start(self):
        for self.i in len(self.prog):
            line = self.prog[self.i]
            self.errors = ""
            for self.j in len(line):
                token = line[self.j]
                self.curr = token
                self._checkBrace(token)
                if isComment(token):
                    break
                #if token in reserved:

                self.j += 1
            if len(self.errors) != 0:
                self.flags.errors += 1
                print(repr(self.i).zfill(3)+" : "+self.errors)


    def end(self):
        if self.flags.errors == 0:
            print("Your program is type error free")
        else:
            print("Your program contains "+repr(self.errors)+" errors")


file_contents = open("test1.cmm", "r").read().strip().lower()
checker = TypeChecker(generateTokens(file_contents))
#checker.start()
checker.begin()
checker.end()
