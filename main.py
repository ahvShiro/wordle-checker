from colorama import Fore, Style
from collections import OrderedDict

# PEDE O NOME DO ARQUIVO DO DICIONÁRIO  
while True:
    dicio_palavras = input("Nome do arquivo do dicionário (txt): ")
    try:
        with open(dicio_palavras, 'r'):
            break
    except FileNotFoundError:
        continue


letras_posicao_errada = []
letras_posicao_certa = []

# PEDE LETRAS CINZAS
letras_nao_na_palavra = input("Letras que não estão na palavra: ")

# PEDE LETRAS AMARELAS
for i in range(1, 5 + 1):
    temp = input(f"{Fore.YELLOW}Letras na posição errada [{i}ª coluna]: {Style.RESET_ALL}").upper()
    letras_posicao_errada.append("".join(OrderedDict.fromkeys(temp)))

# PEDE LETRAS VERDES
for i in range(1, 5 + 1):
    temp = input(f"{Fore.GREEN}Letras na posição certa [{i}ª coluna]: {Style.RESET_ALL}").upper()
    letras_posicao_certa.append("".join(OrderedDict.fromkeys(temp)))


linhas = []
with open(dicio_palavras, "r") as file:
    for i in file:
        i = i.strip()
        if len(i.strip()) == 5:
            linhas.append(i.upper())


for palavra in linhas:
    palavra_errada = False

    # Descarta todas as palavras que contém letras cinzas
    for letra_cinza in letras_nao_na_palavra:
        if(letra_cinza in palavra):
            palavra_errada = True
    
    # Descarta todas as palavras que não contém letras verdes ou amarelas
    for letra_necessaria in "".join(letras_posicao_errada + letras_posicao_certa):
        if(letra_necessaria not in palavra):
            palavra_errada = True
    
    

    if(palavra_errada):
        continue

    print(palavra)
