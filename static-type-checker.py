#!/usr/bin/env python3

'''
Basil Huffman
 bahuffma@gwmail.gwu.edu

 Changes to grammar:

 1. In the given grammar, the following is given:

    read_expr --> "(" expr ")" ";"

    This makes no sense, as the following statement is allowed:

    read_expr(1.2+4);

    Hence, I am changing the grammar to:

    read_expr --> "(" var ")" ";"

    Since this is a simple language, it will only allow one statement
    (or, in the case of loops and conditionals, one sub-statement) per
    line. e.g. 'if X: {' must be split, the '{' must occupy a line to itself,
    the same goes for 'while X do {' statements, where 'while X do' is on
    one line, '{' is on the next.

    So, in practice, this language is a hybrid of Pascal (var
    declaration block occurring before the pprogrammatic block), C
    (syntax and typing), and Python.

 2. strings (e.g. "a", 'a', "1.1", '1.1') within assignment statements (i.e. a = "1.1")
    are treated as both a type and a symbol

 3. only assignments are allowed for booleans

 4. Comments are preceded by '//' and may only occur at the beginning of a line

 5. for logic statements, a symbol not in the symbol table will generate an "incompatible
    types" type error as well as a "symbol not in table" error

 6. boolean assignments can only take the form of <bool> = (0|1), as the grammar disallows
    anything else. a better option would be to modify the grammar such that <bool> = <bool_stmt>,
    but there isn't enough time to add this rule and implement it

 Caveats:

 1. If there are any syntax/semantic errors e.g. no semicolon, improper variable name, the variable
    is *NOT* added to the symbol table

 2. Although semantic errors are sorta checked for in certain cases, due to time restrictions *** AS
    WELL AS A LACK OF RESPONSE VIS A VIS CLARIFICATION IN THIS REGARD FROM DR BELLAACHIA***, it is
    assumed that there will be **NO SYNTAX ERRORS*** and this will purely focus on type checking.
    At a later date, full syntax checking will be implemented (mainly in if and while)

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
        'or':'or_stmt','>':'rel_stmt','<':'rel_stmt','>=':'rel_stmt','!=':'rel_stmt',
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
    string = re.sub(r'>=','--__--__--',string)
    string = re.sub(r'!=','___---___---',string)
    string = re.sub(r'=', ' = ', string)
    string = re.sub(r'__--__--__',' == ', string)
    string = re.sub(r'--__--__--',' >= ', string)
    string = re.sub(r'___---___---',' != ',string)
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

def is_bool(n,tbl):
    if n in ['0','1']:
        return True
    if n in tbl and tbl[n] in ['var_code_boolean','boolean']:
        return True
    return False

def check(n,tbl):
        if n.isdigit():
            return 'int'
        else:
            try:
                float(n)
                return 'float'
            except ValueError:
                if n not in tbl:
                    return 'string'
                return tbl[n]

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
        self.string = False
        self.undef = True

    def resetType(self):
        self.int = False
        self.float = False
        self.bool = False
        self.string = False

    def checkTypes(self,token):
        if self.string:
            return False
        if self.int and not self.float and not self.bool:
            return True
        if self.float and not self.int and not self.bool:
            return True
        if self.bool and not self.int and not self.float:
            return True
        if not self.bool and not self.int and not self.float:
            return True
        if not self.float and self.int and self.bool and token in ['0','1']:
            return True
        return False

class TypeChecker:

    def __init__(self, tokens):
        self.prog = tokens
        self.token = ""
        self.errors=""
        self.flags = Flags()
        self.braceStack=[]
        self.parenStack=[]
        self.symbols={}
        self.i = self.j = 0
        self.width = len(str(len(self.prog)))
        self.val = ''

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
        retval = "UNDEF"
        toktype = check(tok,self.symbols)
        if tok in reserved:
            retval = reserved[tok]
        elif tok in self.symbols:
            temp = self.symbols[tok]
            try:
                retval = types[temp]
            except KeyError:
                retval = self._getNextToken()
        elif toktype == "int":
            retval = "int"
        elif toktype == "float":
            retval = "float"
        elif '"' in tok or "'" in tok:
            retval = "string"

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
            if self.i < len(self.prog):
                self.token = "COM"
            else:
                self.token = "END"
        if self.token == "COM":
            self._increment()

    # bool_stmt --> and_stmt | rel_stmt | boolean
    def _bool_stmt(self):
        if is_bool(self.token,self.symbols):
            self._increment()
            return

    def _check_and_stmts(self):
        line = self.prog[self.i]
        prev = 1
        stmts=[]
        temp=[]
        for i in range(1,len(line)):
            tok = line[i]
            if tok in ['and','or',':'] or i == (len(line)-1):
                stmts.append(temp)
                temp = []
                continue
            temp.append(line[i])
        i=1
        return stmts

    def _check_rel_stmts(self,and_stmt):
        stmts = []
        temp = []
        for i in range(len(and_stmt)):
            tok = and_stmt[i]
            if tok not in ['>','<','==','>=','!=','(',')']:
                temp.append(and_stmt[i])
            if tok in ['>','<','==','>=','!='] or i == (len(and_stmt)-1):
                stmts.append(temp)
                temp=[]
                continue
        return stmts

    def _checkSide(self,side):
        j=1
        float=0
        int = 0
        bool = 0
        bool_ = 0
        if isinstance(side,str):
            type = check(side,self.symbols)
            if type == 'int':
                int = 1
            elif type == 'float':
                float = 1
            if type == 'int' and side in ['0','1']:
                bool_ = 1
        else:
            for i in side:
                type = check(i, self.symbols)
                if type == 'string' and i not in ['+','-','*','/','%'] \
                and "symbol" not in self.errors:
                    self.errors += " type error: symbol not in symbol table."
                    self.flags.errors += 1
                    float = int = bool_ = 1
                    # error if not arithmetic
                    continue
                if type in ['int','var_code_int']:
                    int = 1
                elif type in ['float','var_code_float']:
                    float = 1
                if type == 'var_code_boolean':
                    bool_ = 1
            if (int + float + bool_) > 1 and "incompatible" not in self.errors:
                self.errors += " type error: incompatible types. "
                self.flags.errors += 1

        return float,int,bool_

    # similar to _if_stat but delimiters are while ... do ... end while
    def _while_stmt(self):
        if not self.flags.inProgBlock:
            no=1 #self.errors += "non-type error: statement only allowed in program block"

        and_stmts = self._check_and_stmts()

        for i in and_stmts:
            rel_stmt = self._check_rel_stmts(i)
            l = len(rel_stmt)
            if l == 1:# and not is_bool(i[0],self.symbols):
                if l == 1:  # and not is_bool(rel_stmt[0],self.symbols):
                    if not isinstance(rel_stmt[0], str):
                        temp = check(rel_stmt[0][0], self.symbols)
                    else:
                        temp = check(rel_stmt[0], self.symbols)
                if temp == 'int' and i[0] not in ['0','1'] \
                or temp in ['float','string'] \
                and "evaluate" not in self.errors:
                    self.flags.errors += 1
                    self.errors += " type error: expression must evaluate to boolean."
            else:
                rhs = rel_stmt[1]
                lhs = rel_stmt[0]
                floatr,intr,boolr = self._checkSide(rhs)
                r = floatr+intr
                floatl,intl,booll = self._checkSide(lhs)
                l=floatl+intl
                if "evaluate" in self.errors and \
                   "symbol" in  self.errors and \
                   "incompatible" in self.errors:
                    break
                ll = len(lhs)
                lr = len(rhs)
                if len(lhs) == len(rhs) and len(lhs) == 1:
                    if is_bool(lhs[0],self.symbols) and is_bool(rhs[0],self.symbols):
                        if i[1] in ['>','<','>='] and "expression" not in self.errors:
                            self.errors != " type error: expression must evaluate to boolean."
                    if is_bool(lhs[0],self.symbols) and rhs[0] not in ['0','1'] or \
                       is_bool(rhs[0],self.symbols) and lhs[0] not in ['0','1'] and \
                        "incompatible" not in self.errors:
                        self.errors += " type error: incompatible types."
                        self.flags.errors += 1
                if (floatr == 1 and floatl != 1) or (intr == 1 and intl != 1) \
                        or (boolr == 1 and booll == 1) and "expression" not in self.errors:
                    self.errors += " type error: expression must evaluate to boolean"
                    self.flags.errors += 1
                    continue


        self._skipToEndOfLine()
        if len(self.errors) != 0:
            print(repr(self.i+1).zfill(self.width)+self.errors)
            self.errors = ""
        if self.token != 'do':
            no=1 #self.errors += " non-type error: mising EOL token."
        self._increment()
        self._program()
        if self._getNextToken() != 'end_while':
            no=1 # self.errors += " non-type error: non-terminated IF statement."
        self._increment()


    def _if_stmt(self):
        if not self.flags.inProgBlock:
            no=1#self.errors += "non-type error: statement only allowed in program block"

        and_stmts = self._check_and_stmts()

        for i in and_stmts:
            rel_stmt = self._check_rel_stmts(i)
            l = len(rel_stmt)
            if l == 1:# and not is_bool(rel_stmt[0],self.symbols):
                if not isinstance(rel_stmt[0],str):
                    temp = check(rel_stmt[0][0],self.symbols)
                else:
                    temp = check(rel_stmt[0],self.symbols)
                if temp == 'int' and i[0] not in ['0','1'] \
                or temp in ['float','string'] \
                and "evaluate" not in self.errors:
                    self.flags.errors += 1
                    self.errors += " type error: expression must evaluate to boolean."
            else:
                rhs = rel_stmt[1]
                lhs = rel_stmt[0]
                floatr,intr,boolr = self._checkSide(rhs)
                r = floatr+intr
                floatl,intl,booll = self._checkSide(lhs)
                l=floatl+intl
                if "evaluate" in self.errors and \
                   "symbol" in  self.errors and \
                   "incompatible" in self.errors:
                    break
                ll = len(lhs)
                lr = len(rhs)
                if len(lhs) == len(rhs) and len(lhs) == 1:
                    if is_bool(lhs[0],self.symbols) and is_bool(rhs[0],self.symbols):
                        if i[1] in ['>','<','>='] and "expression" not in self.errors:
                            self.errors != " type error: expression must evaluate to boolean."
                    if is_bool(lhs[0],self.symbols) and rhs[0] not in ['0','1'] or \
                       is_bool(rhs[0],self.symbols) and lhs[0] not in ['0','1'] and \
                        "incompatible" not in self.errors:
                        self.errors += " type error: incompatible types."
                        self.flags.errors += 1
                if (floatr == 1 and floatl != 1) or (intr == 1 and intl != 1) \
                        or (boolr == 1 and booll == 1) and "expression" not in self.errors:
                    self.errors += " type error: expression must evaluate to boolean"
                    self.flags.errors += 1
                    continue


        self._skipToEndOfLine()
        if len(self.errors) != 0:
            print(repr(self.i+1).zfill(self.width)+self.errors)
            self.errors = ""
        if self.token != ':':
            no=1 #self.errors += " non-type error: mising EOL token."
        self._increment()
        self._program()
        if self._getNextToken() == 'else':
            self._increment()
            self._skipToEndOfLine()
            self._increment()
            self._program()
#            self._increment()
#        self._increment()
        if self._getNextToken() != 'end_if':
            no=1 # self.errors += " non-type error: non-terminated IF statement."
        self._increment()

    def _write_stat(self):
        self.flags.resetType()
        if not self.flags.inProgBlock:
            no=1#self.errors += "non-type error: statement only allowed in program block"
        self._expr()
        if not self.flags.checkTypes(self.token):
            self.errors += " type error: incompatible types."
            self.flags.errors += 1
        self.flags.resetType()


    # read --> "(" var ")"
    # var --> [A-Za-z]+
    def _read_stat(self):
        #sys.stdout.write("read_stat")
        next = self._getNextTokenCode()
        if next != "open_paren":
            no=1#self.errors += " non-type error: missing '('."
        else:
            self._increment()
        next = self._getNextToken()
        if next not in self.symbols and next != ';':
            self.errors += " type error: contains variable not in symbol table."
            self.flags.errors += 1
        temp = self.prog[self.i]
        l = len(temp)
        prev = self.token
        while self.token != ')' and self.j < (l-2):
            if next == ')' and prev == '(':
                no=1#self.errors += ' non-type error: missing variable. '
                self._increment()
                break
            self._increment()
            if self.token in ['=','-','+','*','/','%'] and "assignment" not in self.errors:
                no=1#self.errors += " non-type error: assignment/arithmetic not allowed. "
            elif self.token in ['>','<','>=','!=','=='] and "relational" not in self.errors:
                no=1#self.errors += " non-type error: relational statements not allowed."
            elif "symbol" not in self.errors and \
                    self.token not in self.symbols and self.token != ')':
                self.errors += " type error: contains variable not in symbol table. "
                self.flags.errors += 1

        if self.token != ';' and self.token != ')':
            no=1#self.errors += " non-type error: missing ')'"
        if not self.flags.inProgBlock:
            no=1#self.errors += " non-type error: statement only allowed in program block"

    # var_dec --> type var
    def _var_dec(self):
        #sys.stdout.write("var_dec")
        type = returnType(self.token)
        next = self._getNextToken()
        if next not in self.symbols and next not in reserved and checkSymbolName(next) \
                and self.flags.inVarBlock:
            self.symbols[next] = types[type]
        else:
            if next in self.symbols:
                self.errors += " type error: variable redifinition."
                self.flags.errors += 1
            else:
                no=1#self.errors += " non-type error: disallowed variable name."
        l = len(self.prog[self.i])
        while (self.j < (l-2)):
            self._increment()
            next = self._getNextTokenCode()
            if (next == "assign_op"):
                self.errors += " non-type error: assignment not allowed in declarations."
        if not self.flags.inVarBlock:
            no=1#self.errors += " non-type error: variable declarations only allowed" + \
            #               " in var declarations block"

    def _checkType(self):
        try:
            type = self.symbols[self.token]
            toktype = check(self.token,self.symbols)
            if toktype == "string" and self.token not in ["'",'"'] \
                    and self.token not in self.symbols:
                self.flags.string = True
            elif type == "var_code_int" or toktype == "int":
                self.flags.int = True
            elif type == "var_code_float" or toktype == "float":
                self.flags.float = True
            elif type == "var_code_boolean":
                self.flags.bool = True
        except KeyError:
            try:
                type = self.symbols[self._getNextToken()]
                toktype = check(self._getNextToken(),self.symbols)
                if toktype == "string" and self._getNextToken() not in ["'",'"'] \
                        and self.token not in self.symbols:
                    self.flags.string = True
                elif type == "var_code_int" or toktype == "int":
                    self.flags.int = True
                elif type == "var_code_float" or toktype == "float":
                    self.flags.float = True
                elif type == "var_code_boolean":
                    self.flags.bool = True
                return
            except KeyError:
                return
    # assign -> var "=" expr
    def _assign(self):
        self.flags.resetType()
        #sys.stdout.write("assign")
        type = ""
        l = len(self.prog[self.i])

        if self.token not in self.symbols:
            self.errors += " error: contains variable not in symbol table."

        self._checkType()

        next = self._getNextTokenCode()
        if self.flags.bool and "+" in self.prog[self.i] or '-' in self.prog[self.i] \
           or '*' in self.prog[self.i] or '/' in self.prog[self.i] or '%' in self.prog[self.i]:
            self.errors += " type error: boolean assignments cannot contain arithmetic."
            self.flags.errors +=1

        if next != "assign_op":
            #self.errors += " non-type error: assignment statement missing '='"
            if not self.flags.inProgBlock:
            #    self.errors += "non-type error: statement only allowed in program block"
                no=1
            return
        if self.j >= (l-2):
            no=1#self.errors += " non-type error: missing rvalue"
        else:
            self._increment()
            self._expr()
        self.val = self.token
        self._skipToEndOfLine()

        if not self.flags.checkTypes(self.val):
            self.errors += " type error: incompatible types."
            self.flags.errors += 1
        self.flags.resetType()
        if not self.flags.inProgBlock:
            no=1#self.errors += "non-type error: statement only allowed in program block"
        self.val = ''

    def _program(self):
        if self.token == "{":
            self._checkBrace()
            #print(repr(self.i+1).zfill(self.width)+" open_paren")
            self._increment()
        while(True):
            if self.token == "}":
                self._checkBrace()
                #print("close_paren")
                break
            elif self.token == "if":
                self._if_stmt()
            elif self.token == "while":
                self._while_stmt()
            elif self.token == "print":
                self._write_stat()
            elif self.token == "read":
                self._read_stat()
            elif isType(self.token):
                self._var_dec()
            elif self.token not in [' ',"end_while","end_if"] and self.token != "COM":
                self._assign()
            elif self.token != "COM":
                print("Unknown statement: "+repr(self.prog[self.i]))
            self._skipToEndOfLine()
            if len(self.errors) >  0:
                print(repr(self.i+1).zfill(self.width)+self.errors)
            self.errors = ""
            self._increment()

    def _skipToEndOfLine(self):
        l = len(self.prog[self.i]) - 1
        toktype = check(self.token,self.symbols)
        while self.j < l:
            if isType(self.token):
                self._checkType()
            elif toktype == "float":
                self.flags.float = True
            elif toktype == "int":#self.token.isdigit():
                self.flags.int = True
            self._increment()
        if self.token not in [';','COM'] and "EOL" not in self.errors:
            no=1#self.errors += " non-type error: missing EOL token."

    # id | var | "( expr ")"
    def _simple_expr(self):
        next = self._getNextTokenCode()
        if next in ["int","float","string"]:
            if next == "int":
                self.flags.int = True
            elif next == "string":
                self.flags.string = True
            else:
                self.flags.float = True
        elif next == "open_paren":
            self.parenStack.append(1)
            while next != "close_paren":
                if next == 'semicolon' and len(self.parenStack)>0:
                    no=1#self.errors += " non-type error: missing ')'"
                    self.parenStack[:]=[]
                    return
                self._increment()
                self._expr()
                next = self._getNextTokenCode()
            self.parenStack.pop()
        elif self._getNextToken() in self.symbols:
            self._checkType()
        elif next == "add_op" or next == "multiply_op" and "missing" not in self.errors \
                and check(self.token,self.symbols) != 'UNDEF':
            no=1#self.errors += " non-type error: malformed statement."
        if next not in ["add_op","multiply_op",'semicolon','','UNDEF']:
            self._increment()



    # mul_expr --> simple_expr {("\"|"%"|"*") simple_expr}
    def _mul_expr(self):
        self._simple_expr()
        next = self._getNextTokenCode()
        '''if next == "UNDEF" and next != "multiply_op" and next != "add_op" \
                or self.token not in self.symbols and \
                "symbol table" not in self.errors and \
                self.token not in self.symbols and check(self.token,self.symbols) != "string":'''
        if self.token not in self.symbols and check(self.token,self.symbols) == False:
            self.errors += " type error: contains variable not in symbol table."
            self.flags.errors += 1

        while next == "multiply_op":
            self._increment()
            next = self._getNextToken()
            if self.token in ['%','/'] and next in ['0','0.0'] and "zero" not in self.errors:
                no=1#self.errors += " non-type error: division by zero"
            self._mul_expr()
            next = self._getNextTokenCode()
        #self._increment()

    # add_expr --> mul_expr {("+"|"-" mul_expr}
    def _add_expr(self):
        self._mul_expr()
        #self._increment()
        next = self._getNextTokenCode()
        if next == "UNDEF" and "symbol table" not in self.errors:
            self.errors += " type error: contains variable not in symbol table."
            self.flags.errors += 1
        while next == "add_op":
            self._increment()
            self._mul_expr()
            next = self._getNextTokenCode()

    # expr --> add_expr
    def _expr(self):
        self._add_expr()

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
#        else:
#            sys.stdout.write("Your program contains "+repr(self.flags.errors)+" type error(s)")

def stripComments(contents):
    retval = []
    l1 = len(contents)
    for i in range(0,l1):
        line = []
        l2 = len(contents[i])
        for j in range(0,l2):
            if contents[i][j] != '//':
                line.append(contents[i][j])
            else:
                break
        retval.append(line)
    return retval

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("FILE",help="The file to analyze")
    args = parser.parse_args()
    file_contents = open(args.FILE,'r').read().lower()
    checker = TypeChecker(stripComments(generateTokens(file_contents)))
    checker.begin()
    checker.end()
    print()

if __name__ == '__main__':
    main()
