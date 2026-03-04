# LogComp

[![Compilation Status](https://compiler-tester.insper-comp.com.br/svg/Takahacker/LogComp)](https://compiler-tester.insper-comp.com.br/svg/Takahacker/LogComp)

This repository is monitored by Compiler Tester for automatic compilation status.

![Diagrama Sintático](src/img/diagrama_sintatico2.jpg)

```ebnf
EXPRESSION = TERM, { ("+" | "-"), TERM } ;
TERM = FACTOR, { ("*" | "/"), FACTOR } ;
FACTOR = ("+" | "-"), FACTOR | "(", EXPRESSION, ")" | NUMBER ;
NUMBER = DIGIT, { DIGIT } ;
DIGIT = 0 | 1 | ... | 9 ;
```