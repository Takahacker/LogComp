import re
import sys

class PrePro:
    @staticmethod
    def filter(source):
        source = re.sub(r'--.*', '\n', source)
        return source
    
class Token:
    def __init__(self, type="", value=0):
        self.type = type
        self.value = value

class Lexer:
    def __init__(self, source):
        self.source = source
        self.position = 0
        self.next = None
        self.palavras_reservadas = set()
        self.palavras_reservadas.add("print")
        self.palavras_reservadas.add("if")
        self.palavras_reservadas.add("else")
        self.palavras_reservadas.add("while")
        self.palavras_reservadas.add("for")
        self.palavras_reservadas.add("do")
        self.palavras_reservadas.add("end")
        self.palavras_reservadas.add("then")
        self.palavras_reservadas.add("and")
        self.palavras_reservadas.add("or")
        self.palavras_reservadas.add("read")


    def select_next(self):
        while self.position < len(self.source) and self.source[self.position].isspace():
            self.position += 1

        if self.position >= len(self.source):
            self.next = Token("EOF")
            return

        char = self.source[self.position]

        if char.isalpha():
            start_pos = self.position
            while self.position < len(self.source) and (self.source[self.position].isalnum() or self.source[self.position] == '_'):
                self.position += 1
            identifier = self.source[start_pos:self.position]

            if identifier in self.palavras_reservadas:
                if identifier == "print":
                    self.next = Token("PRINT")
                elif identifier == "if":
                    self.next = Token("IF")
                elif identifier == "else":
                    self.next = Token("ELSE")
                elif identifier == "while":
                    self.next = Token("WHILE")
                elif identifier == "do":
                    self.next = Token("OPEN_BRA")
                elif identifier == "end":
                    self.next = Token("CLOSE_BRA")
                elif identifier == "then":
                    self.next = Token("OPEN_IF_BRA")   
                elif identifier == "and":
                    self.next = Token("AND")
                elif identifier == "or":
                    self.next = Token("OR")
                elif identifier == "read":
                    self.next = Token("READ")
            else:
                self.next = Token("IDEN", identifier)
            return

        if char == '=':
            if self.position + 1 < len(self.source) and self.source[self.position + 1] == '=':
                self.next = Token("EQ")
                self.position += 2
                return
            self.next = Token("ASSIGN")
            self.position += 1
            return
        
        if char == '\n':
            self.next = Token("EOL")
            self.position += 1
            return

        if char.isdigit():
            start_pos = self.position
            while self.position < len(self.source) and self.source[self.position].isdigit():
                self.position += 1
            self.next = Token("INT", int(self.source[start_pos:self.position]))
            return
        
        if char == '+':
            self.next = Token("PLUS")
            self.position += 1
            return
            
        if char == '-':
            self.next = Token("MINUS")
            self.position += 1
            return
        
        if char == '^':
            self.next = Token("XOR")
            self.position += 1
            return
            
        if char == '*':
            self.next = Token("MULT")
            self.position += 1
            return
            
        if char == '/':
            self.next = Token("DIV")
            self.position += 1
            return
            
        if char == '(':
            self.next = Token("OPEN_PAR")
            self.position += 1
            return
            
        if char == ')':
            self.next = Token("CLOSE_PAR")
            self.position += 1
            return
        if char == '<':
            self.next = Token("LT")
            self.position += 1
            return
        if char == '>':
            self.next = Token("GT")
            self.position += 1
            return
        
        raise Exception(f"[Lexer] Caractere inválido: '{char}' na posição {self.position}")

class SymbolTable:
    def __init__(self):
        self.table = {}

    def set_value(self, name, value):
        self.table[name] = value
    
    def get_value(self, name):
        if name not in self.table:
            raise Exception(f"[Semantic] Variável '{name}' não definida")
        return self.table[name]
    
class Node:
    def __init__(self, value, children=[]):
        self.value = value
        self.children = children
    def evaluate(self):
        pass

class Block(Node):
    def __init__(self, value, children =[]):
        super().__init__(value, children)
    def evaluate(self):
        for child in self.children:
            child.evaluate()

class Assignment(Node):
    def __init__(self, value, children =[]):
        super().__init__(value, children)
    def evaluate(self):
        var_name = self.children[0].value
        var_value = self.children[1].evaluate()
        Parser.symbol_table.set_value(var_name, var_value)

class NoOp(Node):
    def __init__(self, value, children =[]):
        super().__init__(value, children)
    def evaluate(self):        
        pass

class Identifier(Node):
    def __init__(self, value, children=[]):
        super().__init__(value, children)
    def evaluate(self):
        return Parser.symbol_table.get_value(self.value)

class Variable(Node):
    def __init__(self, value, children=[]):
        super().__init__(value, children)

class Print(Node):
    def __init__(self, value, children=[]):
        super().__init__(value, children)
    def evaluate(self):
        value = self.children[0].evaluate()
        print(value)

class IntVal(Node):
    def __init__(self, value, children=[]):
        super().__init__(value, children)
    def evaluate(self):
        return self.value
    
class BinOp(Node):
    def __init__(self, value, children=[]):
        super().__init__(value, children)
    def evaluate(self):
        left = self.children[0].evaluate()
        right = self.children[1].evaluate()
        if self.value == "PLUS":
            return left + right
        elif self.value == "MINUS":
            return left - right
        elif self.value == "XOR":
            return left ^ right
        elif self.value == "MULT":
            return left * right
        elif self.value == "DIV":
            if right == 0:
                raise Exception("[Semantic] division by zero")
            return left // right
        else:
            raise Exception(f"Operador desconhecido: {self.value}")

class UnOp(Node):
    def __init__(self, value, children=[]):
        super().__init__(value, children)
    def evaluate(self):
        operand = self.children[0].evaluate()
        if self.value == "PLUS":
            return operand
        elif self.value == "MINUS":
            return -operand
        else:
            raise Exception(f"Operador desconhecido: {self.value}")

class If(Node):
    def __init__(self, value, children=[]):
        super().__init__(value, children)
    def evaluate(self):
        if self.children[0].evaluate():
            self.children[1].evaluate()
        elif  len(self.children) > 2:
            self.children[2].evaluate()

class While(Node):
    def __init__(self, value, children=[]):
        super().__init__(value, children)
    def evaluate(self):
        while self.children[0].evaluate():
            self.children[1].evaluate()


class Parser:
    lexer = None
    symbol_table = None
        

    @staticmethod
    def parse_program():
        Parser.symbol_table = SymbolTable()
        block = Block("BLOCK", [])
        while Parser.lexer.next.type != "EOF":
            block.children.append(Parser.parse_statement())
        return block    
    
    @staticmethod
    def parse_statement():
        if Parser.lexer.next.type == "EOL":
            Parser.lexer.select_next()
            return NoOp("NoOp")
        elif Parser.lexer.next.type == "IDEN":
            var_name = Parser.lexer.next.value
            Parser.lexer.select_next()
            if Parser.lexer.next.type != "ASSIGN":
                raise Exception("[Parser] Operador de atribuição esperado")
            Parser.lexer.select_next()
            return Assignment("ASSIGN", [Identifier(var_name), Parser.parse_expression()])

        elif Parser.lexer.next.type == "PRINT":
            Parser.lexer.select_next()
            if Parser.lexer.next.type != "OPEN_PAR":
                raise Exception("[Parser] Parêntese de abertura esperado após 'print'")
            Parser.lexer.select_next()
            expr_node = Parser.parse_expression()
            if Parser.lexer.next.type != "CLOSE_PAR":
                raise Exception("[Parser] Parêntese de fechamento esperado após expressão em 'print'")
            Parser.lexer.select_next()
            if Parser.lexer.next.type == "EOL":
                Parser.lexer.select_next()
            return Print("PRINT", [expr_node])
        
        else:
            raise Exception(f"[Parser] Token inesperado no início da instrução: {Parser.lexer.next.type}")



    @staticmethod
    def parse_expression():
        res = Parser.parse_term()
        while Parser.lexer.next.type in ("PLUS", "MINUS", "XOR"):
            if Parser.lexer.next.type == "PLUS":
                Parser.lexer.select_next()
                res = BinOp("PLUS", [res, Parser.parse_term()])
            elif Parser.lexer.next.type == "MINUS":
                Parser.lexer.select_next()
                res = BinOp("MINUS", [res, Parser.parse_term()])
            else:
                raise Exception(f"[Parser] Operador inesperado: {Parser.lexer.next.type}")
        
        return res

    @staticmethod
    def parse_term():
        res = Parser.parse_factor()

        while Parser.lexer.next.type in ("MULT", "DIV"):
            if Parser.lexer.next.type == "MULT":
                Parser.lexer.select_next()
                res = BinOp("MULT", [res, Parser.parse_factor()])
            elif Parser.lexer.next.type == "DIV":
                Parser.lexer.select_next()
                res = BinOp("DIV", [res, Parser.parse_factor()])
            else:                
                raise Exception(f"[Parser] Operador inesperado: {Parser.lexer.next.type}")
        return res

    @staticmethod
    def parse_factor():
        if Parser.lexer.next.type == "IDEN":
            node = Identifier(Parser.lexer.next.value)
            Parser.lexer.select_next()
            return node
        
        if Parser.lexer.next.type == "INT":
            node = IntVal(Parser.lexer.next.value)
            Parser.lexer.select_next()
            return node

        if Parser.lexer.next.type == "OPEN_PAR":
            Parser.lexer.select_next()
            node = Parser.parse_expression()
            if Parser.lexer.next.type != "CLOSE_PAR":
                raise Exception("[Parser] Parêntese de fechamento esperado")
            Parser.lexer.select_next()
            return node

        if Parser.lexer.next.type == "MINUS":
            Parser.lexer.select_next()
            return UnOp("MINUS", [Parser.parse_factor()])

        if Parser.lexer.next.type == "PLUS":
            Parser.lexer.select_next()
            return UnOp("PLUS", [Parser.parse_factor()])

        if Parser.lexer.next.type in ("EOL", "EOF"):
            raise Exception(f"[Parser] Expressão incompleta antes de {Parser.lexer.next.type}")

        raise Exception(f"[Parser] Token inesperado: {Parser.lexer.next.type}")
            

    @staticmethod
    def run(code):
        Parser.lexer = Lexer(code)
        Parser.lexer.select_next()
        return Parser.parse_program()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Read from file
        with open(sys.argv[1], "r") as f:
            code = f.read()
    else:
        # Read from terminal input
        code = input("Digite o código a ser interpretado (pressione Enter para finalizar):\n")
    
    try:
        code = PrePro.filter(code)
        ast = Parser.run(code)
        ast.evaluate()
    except Exception as e:
        print(e)
        sys.exit(1)