entrada = input("Digite Operação: ")

soma = 0
num = ""
operacao = "+"
entrada = entrada.strip()


if entrada == "" or entrada[0] in "+-":
    print("Exception")
    exit()

for char in entrada:
    if char == " ":
        continue

    if char.isdigit():
        num += char

    elif char in "+-":
        if num == "":
            print("Exception")
            exit()

        if operacao == "+":
            soma += int(num)
        else:
            soma -= int(num)

        operacao = char
        num = ""

    else:
        print("Exception")
        exit()

if num == "":
    print("Exception")
    exit()

if operacao == "+":
    soma += int(num)
else:
    soma -= int(num)

print(soma)