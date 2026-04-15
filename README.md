# LogComp

[![Compilation Status](https://compiler-tester.insper-comp.com.br/svg/Takahacker/LogComp)](https://compiler-tester.insper-comp.com.br/svg/Takahacker/LogComp)

This repository is monitored by Compiler Tester for automatic compilation status.

![Diagrama Sintático](src/img/diagrama_sintatico2.2.png)

```ebnf
PROGRAM = { STATEMENT } ;
STATEMENT = ( "local", IDENTIFIER, ["=", BOOLEXPRESSION]
            | IDENTIFIER, "=", BOOLEXPRESSION
            | "print", "(", BOOLEXPRESSION, ")"
            | "if", "(", BOOLEXPRESSION, ")", "then", BLOCK, ["else", BLOCK], "end"
            | "while", "(", BOOLEXPRESSION, ")", "do", BLOCK, "end"
            | ε
            ), "\n" ;
BLOCK = { STATEMENT } ;
BOOLEXPRESSION = EXPRESSION, { ("and" | "or"), EXPRESSION } ;
EXPRESSION = TERM, { ("+" | "-"), TERM } ;
TERM = FACTOR, { ("*" | "/"), FACTOR } ;
FACTOR = INT | BOOL | STRING | IDENTIFIER | "(", BOOLEXPRESSION, ")" | "read", "(", ")" ;
INT = DIGIT, {DIGIT} ;
BOOL = "true" | "false" ;
STRING = '"', {CHARACTER}, '"' ;
IDENTIFIER = LETTER, {LETTER | DIGIT | "_"} ;
DIGIT = "0" | "1" | ... | "9" ;
LETTER = "a" | "b" | ... | "z" | "A" | "B" | ... | "Z" ;

```