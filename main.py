
def carregar_dicionario(arquivo: str) -> list:

    with open("dicio-br.txt", "r") as a:
        linhas_do_arquivo = a.readlines()

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



def processar_restricoes(palavras: list, status: list):
    return 0

def filtrar_palavras(dicionario, letras_proibidas, letras_posicao_errada, letras_posicao_certa):
    return 0

def main():
    return 0

if __name__ == "__main__":
    main()
