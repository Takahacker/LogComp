import sys

entrada = sys.argv[1]

soma = 0
num = ""
operacao = "+"
pode_continuar_numero = False
entrada = entrada.strip()


if entrada == "" or entrada[0] in "+-":
    raise Exception()

for char in entrada:
    if char == " ":
        pode_continuar_numero = False
        continue

    if char.isdigit():
        if not pode_continuar_numero and num != "":
            raise Exception()
        num += char
        pode_continuar_numero = True

    elif char in "+-":
        if num == "":
            raise Exception()

        if operacao == "+":
            soma += int(num)
        else:
            soma -= int(num)

        operacao = char
        num = ""
        pode_continuar_numero = False

    else:
        raise Exception()

if num == "":
    raise Exception()

if operacao == "+":
    soma += int(num)
else:
    soma -= int(num)

print(soma)