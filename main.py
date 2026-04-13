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
        self.palavras_reservadas = {
            "print", "if", "else", "while", "do", "end",
            "then", "and", "or", "not", "read"
        }

    def select_next(self):
        while self.position < len(self.source) and self.source[self.position] in (' ', '\t'):
            self.position += 1

        if self.position >= len(self.source):
            self.next = Token("EOF")
            return

        char = self.source[self.position]

        if char.isalpha() or char == '_':
            start_pos = self.position
            while self.position < len(self.source) and (self.source[self.position].isalnum() or self.source[self.position] == '_'):
                self.position += 1
            identifier = self.source[start_pos:self.position]

            if identifier in self.palavras_reservadas:
                token_map = {
                    "print": "PRINT",
                    "if":    "IF",
                    "else":  "ELSE",
                    "while": "WHILE",
                    "do":    "OPEN_BRA",
                    "end":   "CLOSE_BRA",
                    "then":  "OPEN_IF_BRA",
                    "and":   "AND",
                    "or":    "OR",
                    "not":   "NOT",
                    "read":  "READ",
                }
                self.next = Token(token_map[identifier])
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

        simple_tokens = {
            '+': "PLUS", '-': "MINUS", '*': "MULT", '/': "DIV",
            '(': "OPEN_PAR", ')': "CLOSE_PAR",
            '<': "LT", '>': "GT", '^': "XOR",
        }
        if char in simple_tokens:
            self.next = Token(simple_tokens[char])
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
    def __init__(self, value, children=[]):
        super().__init__(value, children)

    def evaluate(self):
        for child in self.children:
            child.evaluate()


class Assignment(Node):
    def __init__(self, value, children=[]):
        super().__init__(value, children)

    def evaluate(self):
        var_name = self.children[0].value
        var_value = self.children[1].evaluate()
        Parser.symbol_table.set_value(var_name, var_value)


class NoOp(Node):
    def __init__(self, value, children=[]):
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
        if   self.value == "PLUS":  return left + right
        elif self.value == "MINUS": return left - right
        elif self.value == "MULT":  return left * right
        elif self.value == "XOR":   return left ^ right
        elif self.value == "DIV":
            if right == 0:
                raise Exception("[Semantic] division by zero")
            return left // right
        elif self.value == "AND":   return int(bool(left) and bool(right))
        elif self.value == "OR":    return int(bool(left) or  bool(right))
        elif self.value == "EQ":    return int(left == right)
        elif self.value == "LT":    return int(left <  right)
        elif self.value == "GT":    return int(left >  right)
        else:
            raise Exception(f"Operador desconhecido: {self.value}")


class UnOp(Node):
    def __init__(self, value, children=[]):
        super().__init__(value, children)

    def evaluate(self):
        operand = self.children[0].evaluate()
        if   self.value == "PLUS":  return operand
        elif self.value == "MINUS": return -operand
        elif self.value == "NOT":   return int(not bool(operand))
        else:
            raise Exception(f"Operador desconhecido: {self.value}")


class If(Node):
    def __init__(self, value, children=[]):
        super().__init__(value, children)

    def evaluate(self):
        if self.children[0].evaluate():
            self.children[1].evaluate()
        elif len(self.children) > 2:
            self.children[2].evaluate()


class While(Node):
    def __init__(self, value, children=[]):
        super().__init__(value, children)

    def evaluate(self):
        while self.children[0].evaluate():
            self.children[1].evaluate()


class Read(Node):
    def __init__(self, value, children=[]):
        super().__init__(value, children)

    def evaluate(self):
        return int(input())


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
    def parse_block():
        block = Block("BLOCK", [])
        while Parser.lexer.next.type not in ("CLOSE_BRA", "ELSE"):
            if Parser.lexer.next.type == "EOF":
                raise Exception("[Parser] 'end' esperado antes do fim do arquivo")
            block.children.append(Parser.parse_statement())
        if Parser.lexer.next.type == "CLOSE_BRA":
            Parser.lexer.select_next()
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
                raise Exception("[Parser] Operador de atribuição '=' esperado")
            Parser.lexer.select_next()
            node = Assignment("ASSIGN", [Identifier(var_name), Parser.parse_bool_expression()])
            if Parser.lexer.next.type == "EOL":
                Parser.lexer.select_next()
            return node

        elif Parser.lexer.next.type == "PRINT":
            Parser.lexer.select_next()
            if Parser.lexer.next.type != "OPEN_PAR":
                raise Exception("[Parser] '(' esperado após 'print'")
            Parser.lexer.select_next()
            expr_node = Parser.parse_bool_expression()
            if Parser.lexer.next.type != "CLOSE_PAR":
                raise Exception("[Parser] ')' esperado após expressão em 'print'")
            Parser.lexer.select_next()
            if Parser.lexer.next.type == "EOL":
                Parser.lexer.select_next()
            return Print("PRINT", [expr_node])

        elif Parser.lexer.next.type == "IF":
            Parser.lexer.select_next()
            if Parser.lexer.next.type != "OPEN_PAR":
                raise Exception("[Parser] '(' esperado após 'if'")
            Parser.lexer.select_next()
            cond = Parser.parse_bool_expression()
            if Parser.lexer.next.type != "CLOSE_PAR":
                raise Exception("[Parser] ')' esperado após condição do 'if'")
            Parser.lexer.select_next()
            if Parser.lexer.next.type != "OPEN_IF_BRA":
                raise Exception("[Parser] 'then' esperado após condição do 'if'")
            Parser.lexer.select_next()
            while Parser.lexer.next.type == "EOL":
                Parser.lexer.select_next()
            then_block = Parser.parse_block()
            while Parser.lexer.next.type == "EOL":
                Parser.lexer.select_next()
            if Parser.lexer.next.type == "ELSE":
                Parser.lexer.select_next()
                while Parser.lexer.next.type == "EOL":
                    Parser.lexer.select_next()
                else_block = Parser.parse_block()
                while Parser.lexer.next.type == "EOL":
                    Parser.lexer.select_next()
                return If("IF", [cond, then_block, else_block])
            return If("IF", [cond, then_block])

        elif Parser.lexer.next.type == "WHILE":
            Parser.lexer.select_next()
            if Parser.lexer.next.type != "OPEN_PAR":
                raise Exception("[Parser] '(' esperado após 'while'")
            Parser.lexer.select_next()
            cond = Parser.parse_bool_expression()
            if Parser.lexer.next.type != "CLOSE_PAR":
                raise Exception("[Parser] ')' esperado após condição do 'while'")
            Parser.lexer.select_next()
            if Parser.lexer.next.type != "OPEN_BRA":
                raise Exception("[Parser] 'do' esperado após condição do 'while'")
            Parser.lexer.select_next()
            while Parser.lexer.next.type == "EOL":
                Parser.lexer.select_next()
            body = Parser.parse_block()
            while Parser.lexer.next.type == "EOL":
                Parser.lexer.select_next()
            return While("WHILE", [cond, body])

        elif Parser.lexer.next.type == "OPEN_BRA":
            Parser.lexer.select_next()
            while Parser.lexer.next.type == "EOL":
                Parser.lexer.select_next()
            node = Parser.parse_block()
            while Parser.lexer.next.type == "EOL":
                Parser.lexer.select_next()
            return node

        else:
            raise Exception(f"[Parser] Token inesperado no início da instrução: {Parser.lexer.next.type}")

    @staticmethod
    def parse_bool_expression():
        res = Parser.parse_bool_term()
        while Parser.lexer.next.type == "OR":
            Parser.lexer.select_next()
            res = BinOp("OR", [res, Parser.parse_bool_term()])
        return res

    @staticmethod
    def parse_bool_term():
        res = Parser.parse_rel_expression()
        while Parser.lexer.next.type == "AND":
            Parser.lexer.select_next()
            res = BinOp("AND", [res, Parser.parse_rel_expression()])
        return res

    @staticmethod
    def parse_rel_expression():
        res = Parser.parse_expression()
        if Parser.lexer.next.type in ("EQ", "LT", "GT"):
            op = Parser.lexer.next.type
            Parser.lexer.select_next()
            res = BinOp(op, [res, Parser.parse_expression()])
        return res

    @staticmethod
    def parse_expression():
        res = Parser.parse_term()
        while Parser.lexer.next.type in ("PLUS", "MINUS", "XOR"):
            op = Parser.lexer.next.type
            Parser.lexer.select_next()
            res = BinOp(op, [res, Parser.parse_term()])
        return res

    @staticmethod
    def parse_term():
        res = Parser.parse_factor()
        while Parser.lexer.next.type in ("MULT", "DIV"):
            op = Parser.lexer.next.type
            Parser.lexer.select_next()
            res = BinOp(op, [res, Parser.parse_factor()])
        return res

    @staticmethod
    def parse_factor():
        tok = Parser.lexer.next

        if tok.type == "PLUS":
            Parser.lexer.select_next()
            return UnOp("PLUS", [Parser.parse_factor()])

        if tok.type == "MINUS":
            Parser.lexer.select_next()
            return UnOp("MINUS", [Parser.parse_factor()])

        if tok.type == "NOT":
            Parser.lexer.select_next()
            return UnOp("NOT", [Parser.parse_factor()])

        if tok.type == "IDEN":
            node = Identifier(tok.value)
            Parser.lexer.select_next()
            return node

        if tok.type == "INT":
            node = IntVal(tok.value)
            Parser.lexer.select_next()
            return node

        if tok.type == "OPEN_PAR":
            Parser.lexer.select_next()
            node = Parser.parse_bool_expression()
            if Parser.lexer.next.type != "CLOSE_PAR":
                raise Exception("[Parser] ')' esperado")
            Parser.lexer.select_next()
            return node

        if tok.type == "READ":
            Parser.lexer.select_next()
            if Parser.lexer.next.type != "OPEN_PAR":
                raise Exception("[Parser] '(' esperado após 'read'")
            Parser.lexer.select_next()
            if Parser.lexer.next.type != "CLOSE_PAR":
                raise Exception("[Parser] ')' esperado após 'read('")
            Parser.lexer.select_next()
            return Read("READ")

        if tok.type in ("EOL", "EOF"):
            raise Exception(f"[Parser] Expressão incompleta antes de {tok.type}")

        raise Exception(f"[Parser] Token inesperado: {tok.type}")

    @staticmethod
    def run(code):
        Parser.lexer = Lexer(code)
        Parser.lexer.select_next()
        return Parser.parse_program()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        with open(sys.argv[1], "r") as f:
            code = f.read()
    else:
        code = sys.stdin.read()

    try:
        code = PrePro.filter(code)
        ast = Parser.run(code)
        ast.evaluate()
    except Exception as e:
        print(e)
        sys.exit(1)