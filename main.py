
def carregar_dicionario(arquivo: str) -> list:

    with open("dicio-br.txt", "r") as arq:
        linhas_do_arquivo = arq.readlines()

    palavras_limpas = [linha.strip().upper() for linha in linhas_do_arquivo]

    palavras_cinco_letras = [palavra for palavra in palavras_limpas if len(palavra) == 5]

    return(palavras_cinco_letras)


def input_usuario() -> tuple[list, list]:
    palavras = []
    status = []

    for i in range(6):

        while True:
            entrada_palavra = input(f"Digite a 1ª palavra: ")
        
            if len(entrada_palavra) != 5:
                print("A palavra precisa ter 5 letras!")
            else:
                break

        if entrada_palavra == "":
            entrada_palavra = None
            entrada_status = None
            continue
        
        palavras.append(entrada_palavra)
        
        while True:
            entrada_status = input(f"Digite o marcador da palavra (0: Cinza, 1: Amarelo, 2: Verde): ")

            if len(entrada_status) != 5:
                print("O número de marcadores deve condizer com o número de letras!")
            else:
                break

        status.append(entrada_status)
    
    return palavras, status



def processar_restricoes(palavra: list, status: list):
    letras_proibidas = set()
    posicoes_erradas = {}
    posicoes_certas = {}

    for posicao in range(len(palavra)):
        letra = palavra[posicao]
        status_letra = status[posicao]

        match status_letra[posicao]:
            case "0":
                letras_proibidas.add(letra)
            
            case "1":
                if letra not in posicoes_erradas:
                    posicoes_erradas[letra] = set()
                posicoes_erradas[letra].add(posicao)
            
            case "2":
                posicoes_certas[posicao] = letra
            
    return letras_proibidas, posicoes_erradas, posicoes_certas


def filtrar_palavras(dicionario, letras_proibidas, letras_posicao_errada, letras_posicao_certa):
    palavras_validas = []

    for palavra in dicionario:

        # Pente palavras com letras cinza
        if any(letra in letras_proibidas for letra in palavra):
            continue
        
        # Pente palavras onde o verde não bate
        if any(palavra[posicao] != letra for posicao, letra in letras_posicao_certa):
            continue

        valido = True

        for letra, posicoes_erradas in letras_posicao_errada.items():
            # A letra não está na palavra, cai fora
            if letra not in palavra:
                valido = False
                break

            # A letra não pode estar aí, cai fora
            if any(palavra[posicao] == letra for posicao in posicoes_erradas):
                valido = False
                break
        
        if valido:
            palavras_validas.append(palavra)

    return palavras_validas

def main():
    palavras, status = input_usuario()
    if not palavras or not status:
        return
    
    

    dicionario = carregar_dicionario(input("Digite o nome do arquivo do dicionário (em .txt): "))

    letras_proibidas, letras_posicao_errada, letras_posicao_certa = processar_restricoes(palavras, status)

    palavras_filtradas = filtrar_palavras(dicionario, letras_proibidas, letras_proibidas, letras_posicao_errada, letras_posicao_certa)

if __name__ == "__main__":
    main()
