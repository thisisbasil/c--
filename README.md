# static type checker


Basil Huffman
 bahuffma@gwmail.gwu.edu

 Changes to grammar:

 1. In the given grammar, the following is given:

    `read_expr --> "(" expr ")" ";"`

    This makes no sense, as the following statement is allowed:

    `read_expr(1.2+4);`

    Hence, I am changing the grammar to:

    `read_expr --> "(" var ")"`

    Since this is a simple language, it will only allow one statement
    (or, in the case of loops and conditionals, one sub-statement) per
    line. e.g. 
    `if X: {` 
    
    must be split, the '{' must occupy a line to itself, e.g.
    ```
    if X:
    {
     ```
    the same goes for 'while X do {' statements, where 
    
    `while X do {` 
    
    is onxone line, '{' is on the next e.g.

    ```
    while X do
    {
    ```

    So, in practice, this language is a hybrid of Pascal (var
    declaration block occurring before the pprogrammatic block), C
    (syntax and typing), and Python.

 2. strings (e.g. "a", 'a', "1.1", '1.1') within assignment statements (i.e. a = "1.1")
    are treated as both a type and a symbol

 3. only assignments are allowed for booleans

 4. Comments are preceded by '//' and may only occur at the beginning of a line. they are
    stripped completely from the file

 5. for logic statements, a symbol not in the symbol table will generate an "incompatible
    types" type error as well as a "symbol not in table" error

 6. boolean assignments can only take the form of `<bool> = (0|1)`, as the grammar disallows
    anything else. a better option would be to modify the grammar such that boolean = bool_stmt,
    but there isn't enough time to add this rule and implement it

 Caveats:

 1. If there are any syntax/semantic errors e.g. no semicolon, improper variable name, the variable
    is *NOT* added to the symbol table

 2. Although semantic errors are sorta checked for in certain cases (the only place where 
    it effects things is in declarations) due to time restrictions **AS WELL AS A 
    LACK OF RESPONSE VIS A VIS CLARIFICATION IN THIS REGARD FROM DR BELLAACHIA**, it is
    assumed that there will be **NO SYNTAX ERRORS** and this will purely focus on type 
    checking. At a later date, full syntax checking will be implemented (mainly in if and
    while)


The type checker is run by:

`./static_type_checker.py <FILE>`
