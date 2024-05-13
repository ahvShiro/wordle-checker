from sys import argv

# Checa se o usuário colocou um dicionário como argumento
if (len(argv) != 2):
    print(f"Uso: {argv[0]} <dicionário>")


linhas = []
with open(argv[1], "r") as f:
    for i in f:
        i = i.strip()
        if len(i.strip()) == 5:
            linhas.append(i.upper())

for palavras in linhas:
    print("")