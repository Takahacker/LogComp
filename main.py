class Token:
    def __init__(self, type="", value=0):
        self.type = type
        self.value = value

class Lexer:
    def __init__(self, source):
        self.source = source
        self.position = 0
        self.next = None

    def selectNext(self):
        while self.position < len(self.source) and self.source[self.position].isspace():
            self.position += 1

        if self.position >= len(self.source):
            self.next = Token("EOF")
            return

        char = self.source[self.position]

        if char.isdigit():
            num_str = ""
            while self.position < len(self.source) and self.source[self.position].isdigit():
                num_str += self.source[self.position]
                self.position += 1
            self.next = Token("INT", int(num_str))
            return

        if char == '+':
            self.next = Token("PLUS")
            self.position += 1
            return

        if char == '-':
            self.next = Token("MINUS")
            self.position += 1
            return

        raise Exception(f"Caractere inválido: '{char}' na posição {self.position}")

class Parser:
    lexer = None

    @staticmethod
    def parseExpression():
        if Parser.lexer is None:
            raise Exception("Lexer não inicializado")

        if Parser.lexer.next.type != "INT":
            raise Exception("Esperado um número inteiro no início da expressão")

        resultado = Parser.lexer.next.value
        Parser.lexer.selectNext()

        while Parser.lexer.next.type in ("PLUS", "MINUS"):
            operador = Parser.lexer.next.type
            Parser.lexer.selectNext()

            if Parser.lexer.next.type != "INT":
                raise Exception("Esperado um número inteiro após o operador")

            if operador == "PLUS":
                resultado += Parser.lexer.next.value
            else:
                resultado -= Parser.lexer.next.value

            Parser.lexer.selectNext()

        return resultado

    @staticmethod
    def run(code):
        Parser.lexer = Lexer(code)
        Parser.lexer.selectNext()

        if Parser.lexer.next.type == "EOF":
            return 0

        resultado = Parser.parseExpression()

        # Proíbe número seguido diretamente de número (sem operador)
        if Parser.lexer.next.type == "INT":
            raise Exception("Número seguido diretamente de outro número (falta operador)")

        # Se chegou aqui e não é EOF → outros caracteres inválidos
        if Parser.lexer.next.type != "EOF":
            raise Exception("Caracteres extras após o fim da expressão")

        return resultado

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print('Uso: python main.py "expressão"')
        sys.exit(1)

    try:
        resultado = Parser.run(sys.argv[1])
        print(resultado)
    except Exception as e:
        print("Erro:", str(e))
        sys.exit(1)