import re
import sys
from nodes import *

class PrePro:
    @staticmethod
    def filter(source):
        source = re.sub(r'--.*', '\n', source)
        return source


class Token:
    def __init__(self, type="", value=None):
        self.type = type
        self.value = value


class Lexer:
    def __init__(self, source):
        self.source = source
        self.position = 0
        self.next = None
        self.reserved = {
            "print", "if", "else", "while", "do", "end",
            "then", "and", "or", "not", "read", "local",
            "true", "false"
        }

    def select_next(self):
        while self.position < len(self.source) and self.source[self.position] in (' ', '\t'):
            self.position += 1

        if self.position >= len(self.source):
            self.next = Token("EOF")
            return

        char = self.source[self.position]

        # STRING
        if char == '"':
            self.position += 1
            start = self.position

            while self.position < len(self.source) and self.source[self.position] != '"':
                self.position += 1

            if self.position >= len(self.source):
                raise Exception("[Lexer] String não fechada")

            value = self.source[start:self.position]
            self.position += 1
            self.next = Token("STRING", value)
            return

        # IDENTIFIER / RESERVED
        if char.isalpha() or char == '_':
            start = self.position

            while self.position < len(self.source) and (
                self.source[self.position].isalnum() or self.source[self.position] == '_'
            ):
                self.position += 1

            word = self.source[start:self.position]

            if word == "true":
                self.next = Token("BOOL", True)
                return
            if word == "false":
                self.next = Token("BOOL", False)
                return

            token_map = {
                "print": "PRINT",
                "if": "IF",
                "else": "ELSE",
                "while": "WHILE",
                "do": "OPEN_BRA",
                "end": "CLOSE_BRA",
                "then": "OPEN_IF_BRA",
                "and": "AND",
                "or": "OR",
                "not": "NOT",
                "read": "READ",
                "local": "VAR",
            }

            if word in token_map:
                self.next = Token(token_map[word])
            else:
                self.next = Token("IDEN", word)
            return

        # NUMBERS
        if char.isdigit():
            start = self.position
            while self.position < len(self.source) and self.source[self.position].isdigit():
                self.position += 1

            self.next = Token("INT", int(self.source[start:self.position]))
            return

        # OPERATORS
        if char == '=':
            if self.position + 1 < len(self.source) and self.source[self.position + 1] == '=':
                self.position += 2
                self.next = Token("EQ")
                return
            self.position += 1
            self.next = Token("ASSIGN")
            return

        if char == '\n':
            self.position += 1
            self.next = Token("EOL")
            return

        if char == '.':
            if self.position + 1 < len(self.source) and self.source[self.position + 1] == '.':
                self.position += 2
                self.next = Token("CONCAT")
                return
            else:
                raise Exception("[Lexer] '.' inesperado")

        simple_tokens = {
            '+': "PLUS",
            '-': "MINUS",
            '*': "MULT",
            '/': "DIV",
            '(': "OPEN_PAR",
            ')': "CLOSE_PAR",
            '<': "LT",
            '>': "GT",
            '^': "XOR",
        }

        if char in simple_tokens:
            self.position += 1
            self.next = Token(simple_tokens[char])
            return

        raise Exception(f"[Lexer] Caractere inválido: {char}")


class SymbolTable:
    def __init__(self):
        self.table = {}

    def set_value(self, name, variable):
        if name not in self.table:
            raise Exception(f"Variável '{name}' não definida")

        if self.table[name].type != variable.type:
            raise Exception("Tipo incompatível")

        self.table[name] = variable

    def get_value(self, name):
        if name not in self.table:
            raise Exception(f"Variável '{name}' não definida")
        return self.table[name]

    def create_variable(self, name, variable):
        if name in self.table:
            raise Exception(f"Variável '{name}' já existe")
        self.table[name] = variable


class Parser:
    lexer = None

    @staticmethod
    def parse_program():
        block = Block("BLOCK", [])
        while Parser.lexer.next.type != "EOF":
            block.children.append(Parser.parse_statement())
        return block

    @staticmethod
    def parse_block():
        block = Block("BLOCK", [])

        while Parser.lexer.next.type not in ("CLOSE_BRA", "ELSE"):
            if Parser.lexer.next.type == "EOF":
                raise Exception("[Parser] Esperado 'end'")
            block.children.append(Parser.parse_statement())

        if Parser.lexer.next.type == "CLOSE_BRA":
            Parser.lexer.select_next()

        return block

    @staticmethod
    def parse_statement():
        if Parser.lexer.next.type == "EOL":
            Parser.lexer.select_next()
            return NoOp("NoOp")

        if Parser.lexer.next.type == "VAR":
            Parser.lexer.select_next()

            name = Parser.lexer.next.value
            Parser.lexer.select_next()

            var_type = Parser.lexer.next.value  # "number" or "string"
            Parser.lexer.select_next()

            if Parser.lexer.next.type == "ASSIGN":
                Parser.lexer.select_next()
                return VarDec(var_type, [Identifier(name), Parser.parse_bool_expression()])
            return VarDec(var_type, [Identifier(name)])

        if Parser.lexer.next.type == "IDEN":
            name = Parser.lexer.next.value
            Parser.lexer.select_next()

            Parser.lexer.select_next()
            return Assignment("ASSIGN", [Identifier(name), Parser.parse_bool_expression()])

        if Parser.lexer.next.type == "PRINT":
            Parser.lexer.select_next()
            Parser.lexer.select_next()
            expr = Parser.parse_bool_expression()
            Parser.lexer.select_next()
            return Print("PRINT", [expr])

        if Parser.lexer.next.type == "IF":
            Parser.lexer.select_next()
            Parser.lexer.select_next()

            cond = Parser.parse_bool_expression()
            Parser.lexer.select_next()
            Parser.lexer.select_next()

            then_block = Parser.parse_block()

            if Parser.lexer.next.type == "ELSE":
                Parser.lexer.select_next()
                else_block = Parser.parse_block()
                return If("IF", [cond, then_block, else_block])

            return If("IF", [cond, then_block])

        if Parser.lexer.next.type == "OPEN_BRA":
            Parser.lexer.select_next()
            return Parser.parse_block()

        if Parser.lexer.next.type == "WHILE":
            Parser.lexer.select_next()
            Parser.lexer.select_next()

            cond = Parser.parse_bool_expression()
            Parser.lexer.select_next()
            Parser.lexer.select_next()

            body = Parser.parse_block()
            return While("WHILE", [cond, body])

        raise Exception("[Parser] Statement inválido")

    @staticmethod
    def parse_bool_expression():
        res = Parser.parse_bool_term()

        while Parser.lexer.next.type == "OR":
            op = Parser.lexer.next.type
            Parser.lexer.select_next()
            res = BinOp(op, [res, Parser.parse_bool_term()])

        return res

    @staticmethod
    def parse_bool_term():
        res = Parser.parse_rel_expression()

        while Parser.lexer.next.type == "AND":
            op = Parser.lexer.next.type
            Parser.lexer.select_next()
            res = BinOp(op, [res, Parser.parse_rel_expression()])

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

        while Parser.lexer.next.type in ("PLUS", "MINUS", "CONCAT"):
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

        if tok.type == "INT":
            Parser.lexer.select_next()
            return IntVal(tok.value)

        if tok.type == "BOOL":
            Parser.lexer.select_next()
            return BoolVal(tok.value)

        if tok.type == "STRING":
            Parser.lexer.select_next()
            return StringVal(tok.value)

        if tok.type == "IDEN":
            Parser.lexer.select_next()
            return Identifier(tok.value)

        if tok.type == "OPEN_PAR":
            Parser.lexer.select_next()
            node = Parser.parse_bool_expression()
            Parser.lexer.select_next()
            return node

        if tok.type == "NOT":
            Parser.lexer.select_next()
            return UnOp("NOT", [Parser.parse_factor()])

        if tok.type == "PLUS":
            Parser.lexer.select_next()
            return UnOp("PLUS", [Parser.parse_factor()])

        if tok.type == "MINUS":
            Parser.lexer.select_next()
            return UnOp("MINUS", [Parser.parse_factor()])

        if tok.type == "READ":
            Parser.lexer.select_next()
            Parser.lexer.select_next()
            Parser.lexer.select_next()
            return Read("READ")

        raise Exception("[Parser] Fator inválido")

    @staticmethod
    def run(code):
        Parser.lexer = Lexer(code)
        Parser.lexer.select_next()
        return Parser.parse_program()


if __name__ == "__main__":
    symbol_table = SymbolTable()

    with open(sys.argv[1]) as f:
        code = f.read()
    code = PrePro.filter(code)

    ast = Parser.run(code)
    ast.evaluate(symbol_table)