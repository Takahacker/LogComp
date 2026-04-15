class Node:
    def __init__(self, value, children=[]):
        self.value = value
        self.children = children

    def evaluate(self, symbol_table):
        pass


class Variable:
    def __init__(self, value, var_type):
        self.value = value
        self.type = var_type


class Block(Node):
    def __init__(self, value, children=[]):
        super().__init__(value, children)

    def evaluate(self, symbol_table):
        for child in self.children:
            child.evaluate(symbol_table)


class Assignment(Node):
    def __init__(self, value, children=[]):
        super().__init__(value, children)

    def evaluate(self, symbol_table):
        var_name = self.children[0].value
        var_value = self.children[1].evaluate(symbol_table)
        symbol_table.set_value(var_name, var_value)


class NoOp(Node):
    def __init__(self, value, children=[]):
        super().__init__(value, children)

    def evaluate(self, symbol_table):
        pass


class Identifier(Node):
    def __init__(self, value, children=[]):
        super().__init__(value, children)

    def evaluate(self, symbol_table):
        return symbol_table.get_value(self.value)


class Print(Node):
    def __init__(self, value, children=[]):
        super().__init__(value, children)

    def evaluate(self, symbol_table):
        value = self.children[0].evaluate(symbol_table)
        if value.type == "bool":
            print("true" if value.value else "false")
        else:
            print(value.value)


class IntVal(Node):
    def __init__(self, value, children=[]):
        super().__init__(value, children)

    def evaluate(self, symbol_table):
        return Variable(self.value, "int")


class BinOp(Node):
    def __init__(self, value, children=[]):
        super().__init__(value, children)

    def evaluate(self, symbol_table):
        left = self.children[0].evaluate(symbol_table)
        right = self.children[1].evaluate(symbol_table)

        if self.value == "PLUS":
            if left.type == "int" and right.type == "int":
                return Variable(left.value + right.value, "int")
            else:
                raise Exception(f"[Semantic] Operação '+' não suportada entre tipos {left.type} e {right.type}")

        elif self.value == "MINUS":
            if left.type == "int" and right.type == "int":
                return Variable(left.value - right.value, "int")
            else:
                raise Exception(f"[Semantic] Operação '-' não suportada entre tipos {left.type} e {right.type}")

        elif self.value == "MULT":
            if left.type == "int" and right.type == "int":
                return Variable(left.value * right.value, "int")
            else:
                raise Exception(f"[Semantic] Operação '*' não suportada entre tipos {left.type} e {right.type}")

        elif self.value == "XOR":
            if left.type == "int" and right.type == "int":
                return Variable(left.value ^ right.value, "int")
            else:
                raise Exception(f"[Semantic] Operação '^' não suportada entre tipos {left.type} e {right.type}")

        elif self.value == "DIV":
            if left.type == "int" and right.type == "int":
                if right.value == 0:
                    raise Exception("[Semantic] division by zero")
                return Variable(left.value // right.value, "int")
            else:
                raise Exception(f"[Semantic] Operação '/' não suportada entre tipos {left.type} e {right.type}")

        elif self.value == "AND":
            if left.type == "bool" and right.type == "bool":
                return Variable(left.value and right.value, "bool")
            else:
                raise Exception(f"[Semantic] Operação 'and' não suportada entre tipos {left.type} e {right.type}")

        elif self.value == "OR":
            if left.type == "bool" and right.type == "bool":
                return Variable(left.value or right.value, "bool")
            else:
                raise Exception(f"[Semantic] Operação 'or' não suportada entre tipos {left.type} e {right.type}")

        elif self.value == "EQ":
            if left.type == right.type:
                return Variable(left.value == right.value, "bool")
            else:
                raise Exception(f"[Semantic] Operação '==' não suportada entre tipos {left.type} e {right.type}")

        elif self.value == "LT":
            if left.type == right.type:
                return Variable(left.value < right.value, "bool")
            else:
                raise Exception(f"[Semantic] Operação '<' não suportada entre tipos {left.type} e {right.type}")

        elif self.value == "GT":
            if left.type == right.type:
                return Variable(left.value > right.value, "bool")
            else:
                raise Exception(f"[Semantic] Operação '>' não suportada entre tipos {left.type} e {right.type}")

        elif self.value == "CONCAT":
            def to_str(v):
                if v.type == "bool":
                    return "true" if v.value else "false"
                return str(v.value)
            return Variable(to_str(left) + to_str(right), "str")

        else:
            raise Exception(f"Operador desconhecido: {self.value}")


class UnOp(Node):
    def __init__(self, value, children=[]):
        super().__init__(value, children)

    def evaluate(self, symbol_table):
        operand = self.children[0].evaluate(symbol_table)
        if self.value == "PLUS":
            return Variable(operand.value, operand.type)
        elif self.value == "MINUS":
            return Variable(-operand.value, "int")
        elif self.value == "NOT":
            return Variable(not bool(operand.value), "bool")
        else:
            raise Exception(f"Operador desconhecido: {self.value}")


class If(Node):
    def __init__(self, value, children=[]):
        super().__init__(value, children)

    def evaluate(self, symbol_table):
        if self.children[0].evaluate(symbol_table).value:
            self.children[1].evaluate(symbol_table)
        elif len(self.children) > 2:
            self.children[2].evaluate(symbol_table)


class While(Node):
    def __init__(self, value, children=[]):
        super().__init__(value, children)

    def evaluate(self, symbol_table):
        while self.children[0].evaluate(symbol_table).value:
            self.children[1].evaluate(symbol_table)


class Read(Node):
    def __init__(self, value, children=[]):
        super().__init__(value, children)

    def evaluate(self, symbol_table):
        return Variable(int(input()), "int")


class VarDec(Node):
    def __init__(self, value, children=[]):
        super().__init__(value, children)

    def evaluate(self, symbol_table):
        name = self.children[0].value
        var_type = self.value  # "number" or "string"

        type_map = {"number": "int", "string": "str", "boolean": "bool"}
        expected_type = type_map[var_type]

        if len(self.children) == 2:
            initial_value = self.children[1].evaluate(symbol_table)
            if initial_value.type != expected_type:
                raise Exception(
                    f"[Semantic] Tipo incompatível na declaração de '{name}': "
                    f"esperado '{var_type}', recebido '{initial_value.type}'"
                )
            symbol_table.create_variable(name, initial_value)
        else:
            defaults = {"int": Variable(0, "int"), "str": Variable("", "str"), "bool": Variable(False, "bool")}
            symbol_table.create_variable(name, defaults[expected_type])


class BoolVal(Node):
    def __init__(self, value, children=[]):
        super().__init__(value, children)

    def evaluate(self, symbol_table):
        return Variable(self.value, "bool")


class StringVal(Node):
    def __init__(self, value, children=[]):
        super().__init__(value, children)

    def evaluate(self, symbol_table):
        return Variable(self.value, "str")
