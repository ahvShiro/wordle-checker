def carregar_dicionario(arquivo: str) -> list:

    with open(arquivo, "r") as arq:
        linhas_do_arquivo = arq.readlines()

    palavras_limpas = [linha.strip().upper() for linha in linhas_do_arquivo]

    palavras_cinco_letras = [palavra for palavra in palavras_limpas if len(palavra) == 5]

    return(palavras_cinco_letras)


def input_usuario() -> tuple[list, list]:
    palavras = []
    status = []

    for i in range(6):
        palavra = input(f"Digite a palavra {i + 1} (ou pressione Enter para parar): ").strip().upper()
        if not palavra:
            break

        estado = input(f"Digite o status da palavra {i + 1}: ").strip()
        if len(estado) != len(palavra) or not estado.isdigit():
            print("Status inválido! Deve conter apenas 5 números (0, 1 ou 2).")
            return None, None

        palavras.append(palavra)
        status.append(estado)

    return palavras, status


def processar_restricoes(palavra: str, status: str):
    # Change from 'list' to 'str' since you're passing strings, not lists
    letras_proibidas = set()
    posicoes_erradas = {}
    posicoes_certas = {}

    for posicao in range(len(palavra)):
        letra = palavra[posicao]
        status_letra = status[posicao]

        match status_letra:
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
        if any(palavra[posicao] != letra for posicao, letra in letras_posicao_certa.items()):
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
    
    letras_proibidas_total = set()
    posicoes_erradas_total = {}
    posicoes_certas_total = {}
    
    for i in range(len(palavras)):
        letras_proibidas, posicoes_erradas, posicoes_certas = processar_restricoes(palavras[i], status[i])
        
        letras_proibidas_total.update(letras_proibidas)
        
        for letra, posicoes in posicoes_erradas.items():
            if letra not in posicoes_erradas_total:
                posicoes_erradas_total[letra] = set()
            posicoes_erradas_total[letra].update(posicoes)
        
        posicoes_certas_total.update(posicoes_certas)
    
    for posicao, letra in posicoes_certas_total.items():
        if letra in letras_proibidas_total:
            letras_proibidas_total.remove(letra)
    
    palavras_filtradas = filtrar_palavras(dicionario, letras_proibidas_total, posicoes_erradas_total, posicoes_certas_total)
    
    print(f"Encontradas {len(palavras_filtradas)} palavras possíveis:")
    if len(palavras_filtradas) <= 20:
        print(palavras_filtradas)
    else:
        print(f"Mostrando as primeiras 20 palavras: {palavras_filtradas[:20]}")

if __name__ == "__main__":
    main()
