# lexical_analyzer_c--

 Basil Huffman
 bahuffma@gwmail.gwu.edu

 The following assumptions were made after reading the grammar and sample data,
 and speaking after with Dr. Bellaachia regarding clarification:

 - Comments are single line only, prefaced by //, all comments ignored i.e. stripped out
 - Only one statement allowed per line, except comments succeeding a statement
 - as corollary, multiple statements present in one line will be split into two lines:
  
 	```int a; boolean b;```
  
 	becomes

 	```
  int a;
 	boolean b;
  ```
  
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

     	```
      if bool_stmt :
     	{
     					// statement block
     	}
     	else: 			//optional
     	{
     					// optional statement block
     	}
     	end if;
      ```

   + the EOL of a while expression, which ends in ( do ). From what I gather, the syntax of a
     while statement is:

       ```
        while bool_stmt do
        {
    					// statement block
        }
        end while;
      ```
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
