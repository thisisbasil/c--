# STATIC TYPE CHECKER


*Basil Huffman*

*bahuffma@gwmail.gwu.edu*

### The basic grammar:

```
program ----> {stmt}
stmt ----> var_dec ";" | assign ";" | read_stat ";" |
write_stat ";" | if_stmt ";" | while_stmt ";"
var_dec ----> type var ";"
assign ----> var "=" expr ";"
expr ----> add_expr
add_expr ----> mul_expr {("+"|"-") mul_expr}
mul_expr ----> simple_expr {("*"|"/"|"%") simple_expr }
simple_expr ----> id | var | "(" expr ")"
read_stat ----> "READ" "(" expr ")"
write_stat ----> "PRINT" "(" expr ")"
type ----> "int" | "float" | "boolean"
id ----> intnumber | floatnumber
intnumber ----> Digit | Digit intnumber
floatnumber: ----> intnumber "." intnumber
Digit ----> [0-9]+
boolean ----> "0" | "1"
var ----> [A-Z, a-z]+
block ----> program [ block ]
if_stmt ----> "if" bool_stmt ":" [block] [ "else:" [block] ] "end if" ";"
while_stmt ----> "while" bool_stmt "do" [block] "end while" ";"
bool_stmt ----> and_stmt | rel_stmt |boolean
and_stmt ----> bool_stmt {("and"|"or") bool_stmt}
rel_stmt ----> simple_expr (">"|"<"|">="|"==") simple_expr
```

 ###Changes to grammar:

 1. In the given grammar, the following is given:

    `read_expr --> "(" expr ")" ";"`

    This makes no sense, as the following statement is allowed:

    `read_expr(1.2+4);`

    Hence, I am changing the grammar to:

    `read_expr --> "(" var ")" ";"`

    Since this is a simple language, it will only allow one statement
    (or, in the case of loops and conditionals, one sub-statement) per
    line. e.g. 
    `if X: {` 
    
    must be split, the '{' must occupy a line to itself, e.g.
    ```
    if X:
    {
     ```
    the same goes for: 
    
    `while X do {` 
    
    is on one line, '{' is on the next e.g.

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
 
 7. If any arithmetic or logic operations are attempted within a `read( )` operation, 
    this will be treated as a type error

 ### Caveats:

 1. If there are any syntax/semantic errors e.g. no semicolon, improper variable name, the variable
    is *NOT* added to the symbol table

 2. Although semantic errors are somewhat checked for in certain cases (the only place where 
    it effects things is in declarations) due to time restrictions **AS WELL AS A 
    LACK OF RESPONSE VIS A VIS CLARIFICATION IN THIS REGARD FROM DR BELLAACHIA**, it is
    assumed that there will be **NO SYNTAX ERRORS** and this will purely focus on type 
    checking. At a later date, full syntax checking will be implemented (mainly in if and
    while)
    
    This mostly means that:
   
    1. There will only be **two** main blocks.
    2. **if/while** statements will **always** have the correct format. That is,
    
    ```
    if bool_stmt:
    {
    [block]
    }
    end if;
    ``` 
    
    and
    
    ```
    while bool_stmt do
    {
    [block]
    }
    end while;
    ```
    
    3. As a corollary to not allowing syntax errors, the program will always have the
       following format:
    
    ```
    {
        // Variable declaration block
        // Non-var declarations not allowed
        // As is currently implemented, type/syntax errors will
        //   negate putting the variable in the symbol table
    }
    
    {
        // Program block
        // Variable declarations not allows and will not add symbol
        //   to the symbol table
    }
    ```

### Execution

The type checker is run by:

`./static_type_checker.py <FILE>`

Two test files are included: test.cmm (the sample given in the spec) and test1.cmm. Both should cover
every type of type error.
