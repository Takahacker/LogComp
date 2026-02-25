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
            self.next.type = "Number"
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
            raise Exception(f"[Lexer] Caractere inválido: {char}")

class Parser:
    lexer = Lexer()

    @staticmethod
    def parse_expression() -> int:
        Resultado = 0
        # condição inicial
        while Parser.lexer.position < len(Parser.lexer.source) and Parser.lexer.source[Parser.lexer.position].isspace():
            Parser.lexer.position += 1

        if Parser.lexer.next.type != "Number":
            raise Exception("[Parser] Primeiro token deve ser um Number")
        else:
            Resultado = Parser.lexer.next.value
            Parser.lexer.select_next()

        # Loop para processar os tokens restantes até o EOF
        while Parser.lexer.next.type != "EOF":
            if Parser.lexer.next.type == "PLUS":
                Parser.lexer.select_next()
                if Parser.lexer.next.type != "Number":
                    raise Exception("[Parser] Token após '+' deve ser um Number")
                Resultado += Parser.lexer.next.value
                Parser.lexer.select_next()
            elif Parser.lexer.next.type == "MINUS":
                Parser.lexer.select_next()
                if Parser.lexer.next.type != "Number":
                    raise Exception("[Parser] Token após '-' deve ser um Number")
                Resultado -= Parser.lexer.next.value
                Parser.lexer.select_next()
            else:
                raise Exception("[Parser] Token inválido")
        return Resultado
    

    @staticmethod
    def run() -> int:
        Parser.lexer = Lexer()
        Parser.lexer.source = sys.stdin.read()
        Parser.lexer.select_next()
        result = Parser.parse_expression()
        if Parser.lexer.next.type != "EOF":
            raise Exception("[Parser] Tokens não consumidos completamente")
        return result



def main():
    try:
        result = Parser.run()
        print(result)
    except Exception as e:
        print(str(e))  


if __name__ == "__main__":
    main()