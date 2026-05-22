class Code:
    instructions = []
    func_instructions = []
    in_func = False

    @staticmethod
    def append(code: str) -> None:
        if Code.in_func:
            Code.func_instructions.append(code)
        else:
            Code.instructions.append(code)

    @staticmethod
    def dump(filename: str) -> None:
        with open(filename, 'w') as file:
            file.write('section .data\n')
            file.write('  format_out: db "%d", 10, 0\n')
            file.write('  format_in: db "%d", 0\n')
            file.write('  scan_int: dd 0\n')
            file.write('\n')
            file.write('section .text\n')
            file.write('  extern printf\n')
            file.write('  extern scanf\n')
            file.write('  global _start\n')
            file.write('\n')
            if Code.func_instructions:
                file.write("\n".join(Code.func_instructions))
                file.write("\n\n")
            file.write('_start:\n')
            file.write('  push ebp\n')
            file.write('  mov ebp, esp\n')
            file.write("\n".join(Code.instructions))
            file.write("\n")
            file.write('  mov esp, ebp\n')
            file.write('  pop ebp\n')
            file.write('  mov eax, 1\n')
            file.write('  xor ebx, ebx\n')
            file.write('  int 0x80\n')


def _mem_ref(var):
    # shift > 0: local variable  → [ebp-shift]
    # shift < 0: function param  → [ebp+(-shift)]
    if var.shift < 0:
        return f"[ebp+{-var.shift}]"
    return f"[ebp-{var.shift}]"


class Variable:
    def __init__(self, value, var_type):
        self.value = value
        self.type = var_type
        self.shift = 0


class SymbolTable:
    def __init__(self):
        self.table = {}
        self.offset = 0

    def set_value(self, name, variable):
        if name not in self.table:
            raise Exception(f"[Semantic] Variável '{name}' não definida")
        if self.table[name].type != variable.type:
            raise Exception("[Semantic] Tipo incompatível")
        variable.shift = self.table[name].shift
        self.table[name] = variable

    def get_value(self, name):
        if name not in self.table:
            raise Exception(f"[Semantic] Variável '{name}' não definida")
        return self.table[name]

    def create_variable(self, name, variable):
        if name in self.table:
            raise Exception(f"[Semantic] Variável '{name}' já existe")
        self.offset += 4
        variable.shift = self.offset
        self.table[name] = variable


class Node:
    id = 0

    @staticmethod
    def new_id():
        Node.id += 1
        return Node.id

    def __init__(self, value, children=[]):
        self.value = value
        self.children = children
        self.id = Node.new_id()

    def evaluate(self, symbol_table):
        pass

    def generate(self, symbol_table):
        pass


class Block(Node):
    def __init__(self, value, children=[]):
        super().__init__(value, children)

    def evaluate(self, symbol_table):
        for child in self.children:
            child.evaluate(symbol_table)

    def generate(self, symbol_table):
        for child in self.children:
            child.generate(symbol_table)


class Assignment(Node):
    def __init__(self, value, children=[]):
        super().__init__(value, children)

    def evaluate(self, symbol_table):
        var_name = self.children[0].value
        var_value = self.children[1].evaluate(symbol_table)
        symbol_table.set_value(var_name, var_value)

    def generate(self, symbol_table):
        self.children[1].generate(symbol_table)
        var = symbol_table.get_value(self.children[0].value)
        Code.append(f"  mov {_mem_ref(var)}, eax")


class NoOp(Node):
    def __init__(self, value, children=[]):
        super().__init__(value, children)

    def evaluate(self, symbol_table):
        pass

    def generate(self, symbol_table):
        pass


class Identifier(Node):
    def __init__(self, value, children=[]):
        super().__init__(value, children)

    def evaluate(self, symbol_table):
        return symbol_table.get_value(self.value)

    def generate(self, symbol_table):
        var = symbol_table.get_value(self.value)
        Code.append(f"  mov eax, {_mem_ref(var)}")


class Print(Node):
    def __init__(self, value, children=[]):
        super().__init__(value, children)

    def evaluate(self, symbol_table):
        value = self.children[0].evaluate(symbol_table)
        if value.type == "bool":
            print("true" if value.value else "false")
        else:
            print(value.value)

    def generate(self, symbol_table):
        self.children[0].generate(symbol_table)
        Code.append("  push eax")
        Code.append("  push format_out")
        Code.append("  call printf")
        Code.append("  add esp, 8")


class IntVal(Node):
    def __init__(self, value, children=[]):
        super().__init__(value, children)

    def evaluate(self, symbol_table):
        return Variable(self.value, "int")

    def generate(self, symbol_table):
        Code.append(f"  mov eax, {self.value}")


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

    def generate(self, symbol_table):
        if self.value == "CONCAT":
            return

        self.children[1].generate(symbol_table)  # right → eax
        Code.append("  push eax")
        self.children[0].generate(symbol_table)  # left → eax
        Code.append("  pop ecx")

        if self.value == "PLUS":
            Code.append("  add eax, ecx")
        elif self.value == "MINUS":
            Code.append("  sub eax, ecx")
        elif self.value == "MULT":
            Code.append("  imul ecx")
        elif self.value == "DIV":
            Code.append("  cdq")
            Code.append("  idiv ecx")
        elif self.value == "AND":
            Code.append("  and eax, ecx")
        elif self.value == "OR":
            Code.append("  or eax, ecx")
        elif self.value == "XOR":
            Code.append("  xor eax, ecx")
        elif self.value == "EQ":
            Code.append("  cmp eax, ecx")
            Code.append("  mov eax, 0")
            Code.append("  mov ecx, 1")
            Code.append("  cmove eax, ecx")
        elif self.value == "LT":
            Code.append("  cmp eax, ecx")
            Code.append("  mov eax, 0")
            Code.append("  mov ecx, 1")
            Code.append("  cmovl eax, ecx")
        elif self.value == "GT":
            Code.append("  cmp eax, ecx")
            Code.append("  mov eax, 0")
            Code.append("  mov ecx, 1")
            Code.append("  cmovg eax, ecx")


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
            if operand.type != "bool":
                raise Exception(f"[Semantic] Operação 'not' não suportada para tipo '{operand.type}'")
            return Variable(not bool(operand.value), "bool")
        else:
            raise Exception(f"Operador desconhecido: {self.value}")

    def generate(self, symbol_table):
        self.children[0].generate(symbol_table)
        if self.value == "MINUS":
            Code.append("  neg eax")
        elif self.value == "NOT":
            Code.append("  xor eax, 1")
        # PLUS: no-op


class If(Node):
    def __init__(self, value, children=[]):
        super().__init__(value, children)

    def evaluate(self, symbol_table):
        cond = self.children[0].evaluate(symbol_table)
        if cond.type != "bool":
            raise Exception(f"[Semantic] Condição do 'if' deve ser bool, recebido '{cond.type}'")
        if cond.value:
            self.children[1].evaluate(symbol_table)
        elif len(self.children) > 2:
            self.children[2].evaluate(symbol_table)

    def generate(self, symbol_table):
        uid = self.id
        self.children[0].generate(symbol_table)
        Code.append("  cmp eax, 0")
        if len(self.children) == 3:
            Code.append(f"  je else_{uid}")
            self.children[1].generate(symbol_table)
            Code.append(f"  jmp exit_{uid}")
            Code.append(f"else_{uid}:")
            self.children[2].generate(symbol_table)
        else:
            Code.append(f"  je exit_{uid}")
            self.children[1].generate(symbol_table)
        Code.append(f"exit_{uid}:")


class While(Node):
    def __init__(self, value, children=[]):
        super().__init__(value, children)

    def evaluate(self, symbol_table):
        while True:
            cond = self.children[0].evaluate(symbol_table)
            if cond.type != "bool":
                raise Exception(f"[Semantic] Condição do 'while' deve ser bool, recebido '{cond.type}'")
            if not cond.value:
                break
            self.children[1].evaluate(symbol_table)

    def generate(self, symbol_table):
        uid = self.id
        Code.append(f"loop_{uid}:")
        self.children[0].generate(symbol_table)
        Code.append("  cmp eax, 0")
        Code.append(f"  je exit_{uid}")
        self.children[1].generate(symbol_table)
        Code.append(f"  jmp loop_{uid}")
        Code.append(f"exit_{uid}:")


class Read(Node):
    def __init__(self, value, children=[]):
        super().__init__(value, children)

    def evaluate(self, symbol_table):
        return Variable(int(input()), "int")

    def generate(self, symbol_table):
        Code.append("  push scan_int")
        Code.append("  push format_in")
        Code.append("  call scanf")
        Code.append("  add esp, 8")
        Code.append("  mov eax, dword [scan_int]")


class VarDec(Node):
    def __init__(self, value, children=[]):
        super().__init__(value, children)

    def evaluate(self, symbol_table):
        name = self.children[0].value
        var_type = self.value

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

    def generate(self, symbol_table):
        name = self.children[0].value
        type_map = {"number": "int", "string": "str", "boolean": "bool"}
        expected_type = type_map[self.value]

        if expected_type == "str":
            return

        var = Variable(0, expected_type)
        symbol_table.create_variable(name, var)
        Code.append(f"  sub esp, 4")

        if len(self.children) == 2:
            self.children[1].generate(symbol_table)
            Code.append(f"  mov {_mem_ref(var)}, eax")


class BoolVal(Node):
    def __init__(self, value, children=[]):
        super().__init__(value, children)

    def evaluate(self, symbol_table):
        return Variable(self.value, "bool")

    def generate(self, symbol_table):
        Code.append(f"  mov eax, {1 if self.value else 0}")


class StringVal(Node):
    def __init__(self, value, children=[]):
        super().__init__(value, children)

    def evaluate(self, symbol_table):
        return Variable(self.value, "str")

    def generate(self, symbol_table):
        pass


class ReturnException(Exception):
    def __init__(self, value):
        self.value = value


class FuncTable:
    table = {}

    @staticmethod
    def declare(name, node):
        FuncTable.table[name] = node

    @staticmethod
    def get(name):
        if name not in FuncTable.table:
            raise Exception(f"[Semantic] Função '{name}' não definida")
        return FuncTable.table[name]


class FuncDec(Node):
    def __init__(self, name, params, body):
        super().__init__(name, [body])
        self.params = params  # list of param name strings

    def evaluate(self, symbol_table):
        FuncTable.declare(self.value, self)

    def generate(self, symbol_table):
        func_name = self.value
        body = self.children[0]

        func_st = SymbolTable()
        # Parameters: first arg at [ebp+8], second at [ebp+12], ...
        # Store with negative shift so _mem_ref maps to [ebp+|shift|]
        for i, param in enumerate(self.params):
            param_var = Variable(0, "int")
            param_var.shift = -(8 + i * 4)
            func_st.table[param] = param_var

        Code.in_func = True
        Code.append(f"{func_name}:")
        Code.append(f"  push ebp")
        Code.append(f"  mov ebp, esp")

        body.generate(func_st)

        # Implicit return for functions that fall off the end
        Code.append(f"  mov esp, ebp")
        Code.append(f"  pop ebp")
        Code.append(f"  ret")
        Code.in_func = False


class FuncCall(Node):
    def __init__(self, name, args):
        super().__init__(name, args)

    def evaluate(self, symbol_table):
        func = FuncTable.get(self.value)
        if len(func.params) != len(self.children):
            raise Exception(
                f"[Semantic] Função '{self.value}' espera {len(func.params)} "
                f"argumentos, recebeu {len(self.children)}"
            )
        local_st = SymbolTable()
        for i, param in enumerate(func.params):
            arg_val = self.children[i].evaluate(symbol_table)
            local_st.create_variable(param, arg_val)
        try:
            func.children[0].evaluate(local_st)
            return Variable(0, "int")
        except ReturnException as e:
            return e.value

    def generate(self, symbol_table):
        # Push arguments right-to-left (cdecl): first arg ends up at [ebp+8]
        for arg in reversed(self.children):
            arg.generate(symbol_table)
            Code.append(f"  push eax")
        Code.append(f"  call {self.value}")
        if self.children:
            Code.append(f"  add esp, {len(self.children) * 4}")
        # Return value is in eax


class Return(Node):
    def __init__(self, value, children=[]):
        super().__init__(value, children)

    def evaluate(self, symbol_table):
        val = self.children[0].evaluate(symbol_table)
        raise ReturnException(val)

    def generate(self, symbol_table):
        self.children[0].generate(symbol_table)
        Code.append(f"  mov esp, ebp")
        Code.append(f"  pop ebp")
        Code.append(f"  ret")
