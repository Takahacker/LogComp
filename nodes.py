class Node:
    def __init__(self, value, children=[]):
        self.value = value
        self.children = children

    def evaluate(self, symbol_table):
        pass


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


class Variable(Node):
    def __init__(self, value, children=[]):
        super().__init__(value, children)
        


class Print(Node):
    def __init__(self, value, children=[]):
        super().__init__(value, children)

    def evaluate(self, symbol_table):
        value = self.children[0].evaluate(symbol_table)
        print(value)


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

        if   self.value == "PLUS":
            if right.type == "INT" and left.type == "INT":  
                return Variable(left.value + right.value, "int")
            else: 
                raise Exception(f"[Semantic] Operação '+' não suportada entre tipos {left.type} e {right.type}")
        elif self.value == "MINUS":
            if right.type == "INT" and left.type == "INT":  
                return Variable(left.value - right.value, "int")
            else:
                raise Exception(f"[Semantic] Operação '-' não suportada entre tipos {left.type} e {right.type}")

        elif self.value == "MULT":  
            if right.type == "INT" and left.type == "INT":
                return Variable(left.value * right.value, "int")
            else:
                raise Exception(f"[Semantic] Operação '*' não suportada entre tipos {left.type} e {right.type}")
        elif self.value == "XOR":   
            if right.type == "INT" and left.type == "INT":
                return Variable(left.value ^ right.value, "int")
            else:
                raise Exception(f"[Semantic] Operação '^' não suportada entre tipos {left.type} e {right.type}")
            
        elif self.value == "DIV":
            if right == 0:
                raise Exception("[Semantic] division by zero")
            return Variable(left.value // right.value, "int")
        
        # AND , OR Bool op Bool
        elif self.value == "AND":  
            if right.type == "bool" and left.type == "bool":
                return Variable(left.value and right.value, "bool")
            else:
                raise Exception(f"[Semantic] Operação 'and' não suportada entre tipos {left.type} e {right.type}")
        elif self.value == "OR":    
            if right.type == "bool" and left.type == "bool":
                return Variable(left.value== right.value, "bool")
            else:
                raise Exception(f"[Semantic] Operação 'or' não suportada entre tipos {left.type} e {right.type}")
            

        # Type1 == Type2 , return bool
        elif self.value == "EQ":    
            if right.type == left.type:
               if right == left:
                   return Variable(left.value== right.value, right.type)
            else:
                raise Exception(f"[Semantic] Operação '==' não suportada entre tipos {left.type} e {right.type}")

        elif self.value == "LT":    
            if right.type == left.type:
                return Variable(left.value <  right.value, "bool")
            else:
                raise Exception(f"[Semantic] Operação '<' não suportada entre tipos {left.type} e {right.type}")
        elif self.value == "GT":    
            if right.type == left.type:
                return Variable(left.value >  right.value, "bool")
            else:
                raise Exception(f"[Semantic] Operação '>' não suportada entre tipos {left.type} e {right.type}")    
        else:
            raise Exception(f"Operador desconhecido: {self.value}")


class UnOp(Node):
    def __init__(self, value, children=[]):
        super().__init__(value, children)

    def evaluate(self, symbol_table):
        operand = self.children[0].evaluate(symbol_table)
        if   self.value == "PLUS":  return Variable(operand.value, operand.type)
        elif self.value == "MINUS": return Variable(-operand.value, "int")
        elif self.value == "NOT":   return Variable(int(not bool(operand.value)), "bool")
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
        if len(self.children) == 1:
            symbol_table.set_value(self.value, self.children[0].evaluate(symbol_table))
                                   

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
