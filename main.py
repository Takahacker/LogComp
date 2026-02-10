import sys

entrada = sys.argv[1]

soma = 0
num = ""
operacao = "+"
entrada = entrada.strip()


if entrada == "" or entrada[0] in "+-":
    raise Exception()

for char in entrada:
    if char == " ":
        continue

    if char.isdigit():
        num += char

    elif char in "+-":
        if num == "":
            raise Exception()

        if operacao == "+":
            soma += int(num)
        else:
            soma -= int(num)

        operacao = char
        num = ""

    else:
        raise Exception()

if num == "":
    raise Exception()

if operacao == "+":
    soma += int(num)
else:
    soma -= int(num)

print(soma)