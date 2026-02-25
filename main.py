import sys

class Token:
    def __init__(self):
        self.type = ""
        self.value = 0

class Lexer:
    def __init__(self):
        self.source = ""
        self.position = 0
        self.next = Token()

    def select_next(self):
        while self.position < len(self.source) and self.source[self.position].isspace():
            self.position += 1
    
        if self.position >= len(self.source):
            self.next = Token()
            self.next.type = "EOF"
            return
        
        char = self.source[self.position]
        
        if char.isdigit():
            num = ""
            while self.position < len(self.source) and self.source[self.position].isdigit():
                num += self.source[self.position]
                self.position += 1
            self.next = Token()
            self.next.type = "Número"
            self.next.value = int(num)
    
        elif char == '+':
            self.next = Token()
            self.next.type = "PLUS"
            self.position += 1
        elif char == '-':
            self.next = Token()
            self.next.type = "MINUS"
            self.position += 1
        else:
            raise Exception(f"Caractere inválido: {char}")

class Parser:
    lexer = Lexer()

    def __init__(self):
        pass

    @staticmethod
    def parse_expression(lexer) -> int:
        Resultado = 0
        # condição inicial
        if lexer.next.type != "Número":
            raise Exception("Primeiro token deve ser um número")
        else:
            Resultado = lexer.next.value
            lexer.select_next()

        # Loop para processar os tokens restantes até o EOF
        while lexer.next.type != "EOF":
            if lexer.next.type == "PLUS":
                lexer.select_next()
                if lexer.next.type != "Número":
                    raise Exception("Token após '+' deve ser um número")
                Resultado += lexer.next.value
                lexer.select_next()
            elif lexer.next.type == "MINUS":
                lexer.select_next()
                if lexer.next.type != "Número":
                    raise Exception("Token após '-' deve ser um número")
                Resultado -= lexer.next.value
                lexer.select_next()
            else:
                raise Exception("Token inválido")
        return Resultado
    

    def run(self) -> int:
        Parser.lexer = Lexer()
        Parser.lexer.source = sys.stdin.read()
        Parser.lexer.select_next()
        result = Parser.parse_expression(Parser.lexer)
        if Parser.lexer.next.type != "EOF":
            raise Exception("Tokens não consumidos completamente")
        return result



def main():
    parser = Parser()
    result = parser.run()
    print(result)  


if __name__ == "__main__":
    main()