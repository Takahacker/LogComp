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
        # Ignora espaços
        while self.position < len(self.source) and self.source[self.position].isspace():
            self.position += 1

        # Fim da entrada
        if self.position >= len(self.source):
            self.next = Token()
            self.next.type = "EOF"
            return

        char = self.source[self.position]

        # Número inteiro
        if char.isdigit():
            num = ""
            while self.position < len(self.source) and self.source[self.position].isdigit():
                num += self.source[self.position]
                self.position += 1
            self.next = Token()
            self.next.type = "Number"
            self.next.value = int(num)
            return

        # Operador +
        elif char == '+':
            self.next = Token()
            self.next.type = "PLUS"
            self.position += 1
            return

        # Operador -
        elif char == '-':
            self.next = Token()
            self.next.type = "MINUS"
            self.position += 1
            return

        # Caractere inválido
        else:
            raise Exception()


class Parser:
    lexer = Lexer()

    @staticmethod
    def parse_expression() -> int:
        if Parser.lexer.next.type != "Number":
            raise Exception()

        result = Parser.lexer.next.value
        Parser.lexer.select_next()

        while Parser.lexer.next.type != "EOF":
            if Parser.lexer.next.type == "PLUS":
                Parser.lexer.select_next()
                if Parser.lexer.next.type != "Number":
                    raise Exception()
                result += Parser.lexer.next.value
                Parser.lexer.select_next()

            elif Parser.lexer.next.type == "MINUS":
                Parser.lexer.select_next()
                if Parser.lexer.next.type != "Number":
                    raise Exception()
                result -= Parser.lexer.next.value
                Parser.lexer.select_next()

            else:
                raise Exception()

        return result

    @staticmethod
    def run() -> int:
        Parser.lexer = Lexer()
        Parser.lexer.source = sys.stdin.read()
        Parser.lexer.select_next()

        result = Parser.parse_expression()

        if Parser.lexer.next.type != "EOF":
            raise Exception()

        return result


def main():
    try:
        result = Parser.run()
        print(result)
    except Exception:
        sys.exit(1)


if __name__ == "__main__":
    main()