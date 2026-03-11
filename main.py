class Token:
    def __init__(self, type="", value=0):
        self.type = type
        self.value = value


class Lexer:
    def __init__(self, source):
        self.source = source
        self.position = 0
        self.next = None

    def select_next(self):
        while self.position < len(self.source) and self.source[self.position].isspace():
            self.position += 1

        if self.position >= len(self.source):
            self.next = Token("EOF")
            return
        
        char = self.source[self.position]

        if char.isdigit():
            self.next = Token("INT", int(char))
            self.position += 1
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

        raise Exception(f"[Lexer] Caractere inválido: '{char}' na posição {self.position}")

class Node:
    def __init__(self, value, children=[]):
        self.value = value
        self.children = children
    def evaluate(self):
        pass

class IntVal(Node):
    def __init__(self, value,children=[]):
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

class Parser:
    lexer = None

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


    def parse_factor():
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


        raise Exception(f"[Parser] Token inesperado: {Parser.lexer.next.type}")
            

    def run(code):
        Parser.lexer = Lexer(code)
        Parser.lexer.select_next()

        if Parser.lexer.next.type == "EOF":
            raise Exception("[Parser] Expressão vazia")

        node_resultado = Parser.parse_expression()

        if Parser.lexer.next.type != "EOF":
            raise Exception("[Parser] Token inesperado após o final da expressão")


        return node_resultado


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Uso: python main.py \"expressão\"")
        sys.exit(1)

    try:
        result = Parser.run(sys.argv[1]).evaluate()
        print(result)
    except Exception as e:
        print(str(e))
        sys.exit(1) 