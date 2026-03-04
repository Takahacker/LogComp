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
            if self.position + 1 < len(self.source) and self.source[self.position + 1] == '*':
                self.next = Token("POW")
                self.position += 2
            else:
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


class Parser:
    lexer = None

    def parse_expression():

        res = Parser.parse_term()

        while Parser.lexer.next.type in ("PLUS", "MINUS", "XOR"):
            if Parser.lexer.next.type == "PLUS":
                Parser.lexer.select_next()
                res += Parser.parse_term()
            elif Parser.lexer.next.type == "MINUS":
                Parser.lexer.select_next()
                res -= Parser.parse_term()
            elif Parser.lexer.next.type == "XOR":
                Parser.lexer.select_next()
                res ^= Parser.parse_term()
            else:
                raise Exception(f"[Parser] Operador inesperado: {Parser.lexer.next.type}")
        
        return res

    def parse_term():
        res = Parser.parse_unary()

        while Parser.lexer.next.type in ("MULT", "DIV"):
            if Parser.lexer.next.type == "MULT":
                Parser.lexer.select_next()
                res *= Parser.parse_unary()
            elif Parser.lexer.next.type == "DIV":
                Parser.lexer.select_next()
                divisor = Parser.parse_unary()
                if divisor == 0:
                    raise Exception("division by zero")
                res //= divisor
            else:                
                raise Exception(f"[Parser] Operador inesperado: {Parser.lexer.next.type}")
        return res


    def parse_factor():
        if Parser.lexer.next.type == "INT":
            res = Parser.lexer.next.value
            Parser.lexer.select_next()
            return res

        if Parser.lexer.next.type == "OPEN_PAR":
            Parser.lexer.select_next()
            res = Parser.parse_expression()
            if Parser.lexer.next.type != "CLOSE_PAR":
                raise Exception("[Parser] Parêntese de fechamento esperado")
            Parser.lexer.select_next()
            return res

        raise Exception(f"[Parser] Token inesperado: {Parser.lexer.next.type}")
    
    def parse_pow():
        res = Parser.parse_factor()

        while Parser.lexer.next.type == "POW":
            Parser.lexer.select_next()
            res **= Parser.parse_factor()
        
        return res

    def parse_unary():
        if Parser.lexer.next.type == "MINUS":
            Parser.lexer.select_next()
            return -Parser.parse_unary()
        if Parser.lexer.next.type == "PLUS":
            Parser.lexer.select_next()
            return Parser.parse_unary()
        return Parser.parse_pow()
        

    def run(code):
        Parser.lexer = Lexer(code)
        Parser.lexer.select_next()

        if Parser.lexer.next.type == "EOF":
            raise Exception("[Parser] Expressão vazia")

        resultado = Parser.parse_expression()

        if Parser.lexer.next.type != "EOF":
            raise Exception("[Parser] Token inesperado após o final da expressão")


        return resultado


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Uso: python main.py \"expressão\"")
        sys.exit(1)

    try:
        resultado = Parser.run(sys.argv[1])
        print(resultado)
    except Exception as e:
        print(str(e))
        sys.exit(1)
