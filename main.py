import sys

class Token:
    def __init__(self):
        self.type = ""
        self.value = 0


class Lexer:
    def __init__(self, source):
        self.source = source
        self.position = 0
        self.next = None

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
            return

        elif char == '+':
            self.next = Token()
            self.next.type = "PLUS"
            self.position += 1
            return

        elif char == '-':
            self.next = Token()
            self.next.type = "MINUS"
            self.position += 1
            return

        else:
            raise Exception(f"[Lexer] Caractere inválido: {char}")


class Parser:
    lexer = None
    
    def parse_expression():
        if Parser.lexer.next.type != "Number":
            raise Exception("[Parser] Primeiro token deve ser um Number")

        result = Parser.lexer.next.value
        Parser.lexer.select_next()

        while Parser.lexer.next.type != "EOF":
            if Parser.lexer.next.type == "PLUS":
                Parser.lexer.select_next()
                if Parser.lexer.next.type != "Number":
                    raise Exception("[Parser] Token após '+' deve ser um Number")
                result += Parser.lexer.next.value
                Parser.lexer.select_next()

            elif Parser.lexer.next.type == "MINUS":
                Parser.lexer.select_next()
                if Parser.lexer.next.type != "Number":
                    raise Exception("[Parser] Token após '-' deve ser um Number")
                result -= Parser.lexer.next.value
                Parser.lexer.select_next()

            else:
                raise Exception("[Parser] Token inválido")

        return result

    def run(code):
        Parser.lexer = Lexer(code)  
        Parser.lexer.select_next()

        result = Parser.parse_expression()

        if Parser.lexer.next.type != "EOF":
            raise Exception("[Parser] Tokens não consumidos completamente")

        return result


def main():
    try:
        code = sys.argv[1]
        result = Parser.run(code)
        print(result)
    except Exception as e:
        print(str(e))
        sys.exit(1)


if __name__ == "__main__":
    main()