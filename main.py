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

    def parse_expression() -> int:
        Resultado = 0
        # condição inicial
        if Parser.lexer.next.type != "Número":
            raise Exception("Primeiro token deve ser um número")
        else:
            Resultado = Parser.lexer.next.value
            Parser.lexer.select_next()

        # Loop para processar os tokens restantes até o EOF
        while Parser.lexer.next.type != "EOF":
            if Parser.lexer.next.type == "PLUS":
                Parser.lexer.select_next()
                if Parser.lexer.next.type != "Número":
                    raise Exception("Token após '+' deve ser um número")
                Resultado += Parser.lexer.next.value
                Parser.lexer.select_next()
            elif Parser.lexer.next.type == "MINUS":
                Parser.lexer.select_next()
                if Parser.lexer.next.type != "Número":
                    raise Exception("Token após '-' deve ser um número")
                Resultado -= Parser.lexer.next.value
                Parser.lexer.select_next()
            else:
                raise Exception("Token inválido")
        return Resultado
    

    @staticmethod
    def run() -> int:
        Parser.lexer = Lexer()
        Parser.lexer.source = sys.stdin.read()
        Parser.lexer.select_next()
        result = Parser.parse_expression()
        if Parser.lexer.next.type != "EOF":
            raise Exception("Tokens não consumidos completamente")
        return result



def main():
    result = Parser.run()
    print(result)  


if __name__ == "__main__":
    main()