import os
import time

# ANSI color codes for terminal output
GRAY = "\033[90m"
YELLOW = "\033[93m"
GREEN = "\033[92m"
RESET = "\033[0m"
BOLD = "\033[1m"
CYAN = "\033[96m"
RED = "\033[91m"
BLUE = "\033[94m"

slant_title = """
 _       __               ____   
| |     / /___  _________/ / /__ 
| | /| / / __ \/ ___/ __  / / _ \\
| |/ |/ / /_/ / /  / /_/ / /  __/
|__/|__/\____/_/_  \__,_/_/\___/ 
  / ___/____  / /   _____  _____ 
  \__ \/ __ \/ / | / / _ \/ ___/ 
 ___/ / /_/ / /| |/ /  __/ /     
/____/\____/_/ |___/\___/_/      
"""



def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_welcome():
    """Print a welcome message with instructions."""
    clear_screen()
    print(f"\n{BOLD}{GREEN}{slant_title}{RESET}")
    print(f"\nEste programa ajuda a encontrar possíveis respostas para o Wordle/Termo\ndo dia com base nas suas tentativas!")
    print("\nInstruções para o status de cada letra:")
    print(f" • Digite {GRAY}[0]{RESET} para letras {GRAY}CINZAS{RESET} (a letra não está na palavra)")
    print(f" • Digite {YELLOW}[1]{RESET} para letras {YELLOW}AMARELAS{RESET} (a letra tá na palavra, mas na posição errada)")
    print(f" • Digite {GREEN}[2]{RESET} para letras {GREEN}VERDES{RESET} (a letra na palavra e na posição correta)")
    
    print(f"\nExemplo: Para a palavra '{BOLD}TERMO{RESET}'")
    print(f"Se o resultado for: {GRAY}[T]{RESET}{YELLOW}[E]{RESET}{GREEN}[R]{RESET}{GRAY}[M]{RESET}{YELLOW}[O]{RESET}")
    print(f"Você deve digitar: 01200\n")
    print(f"{GREEN}Pressione Enter para começar...{RESET}")
    input()
    clear_screen()

def carregar_dicionario(arquivo: str) -> list:

    with open(arquivo, "r") as arq:
        linhas_do_arquivo = arq.readlines()

    palavras_limpas = [linha.strip().upper() for linha in linhas_do_arquivo]

    palavras_cinco_letras = [palavra for palavra in palavras_limpas if len(palavra) == 5]

    return(palavras_cinco_letras)

def colorir_palavra(palavra: str, status: str) -> str:
    """Retorna a palavra com cores baseadas no status."""
    resultado = ""
    for i, letra in enumerate(palavra):
        if i < len(status):
            if status[i] == "0":
                resultado += f"{GRAY}[{letra}]{RESET}"
            elif status[i] == "1":
                resultado += f"{YELLOW}[{letra}]{RESET}"
            elif status[i] == "2":
                resultado += f"{GREEN}[{letra}]{RESET}"
            else:
                resultado += letra
        else:
            resultado += letra
    return resultado

def input_usuario() -> tuple[list, list]:
    palavras = []
    status = []
    
    print(f"{BOLD}Digite suas tentativas (Ou ENTER para finalizar):{RESET}")
    print(f"({GRAY}0=CINZA{RESET}, {YELLOW}1=AMARELO{RESET}, {GREEN}2=VERDE{RESET})\n")

    for i in range(6):
        palavra = input(f"Palavra {i + 1}: ").strip().upper()
        if not palavra:
            break
            
        if len(palavra) != 5:
            print(f"{RED}A palavra deve ter 5 letras!{RESET}")
            i -= 1
            continue

        while True:
            estado = input(f"{GRAY}{BOLD}[0]{RESET}/{YELLOW}{BOLD}[1]{RESET}/{GREEN}{BOLD}[2]{RESET}): ").strip()
            if len(estado) == 5 and all(c in "012" for c in estado):
                break
            print(f"{RED}Status inválido! Digite 5 números (0, 1 ou 2).{RESET}")
        
        palavras.append(palavra)
        status.append(estado)
        
        # Show the word with colors to confirm
        print(f"Registrado: {colorir_palavra(palavra, estado)}\n")

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

def mostrar_resumo_restricoes(letras_proibidas, letras_posicao_errada, letras_posicao_certa):
    """Mostra um resumo das restrições processadas."""
    print(f"\n{BOLD}Resumo das Restrições:{RESET}")
    
    # Letras proibidas
    if letras_proibidas:
        print(f"- Letras ausentes: {GRAY}{', '.join(sorted(letras_proibidas))}{RESET}")
    
    # Letras em posições corretas (verdes)
    if letras_posicao_certa:
        print("- Letras confirmadas:")
        palavra_template = ["_", "_", "_", "_", "_"]
        for pos, letra in letras_posicao_certa.items():
            palavra_template[pos] = letra
        
        display = ""
        for i, letra in enumerate(palavra_template):
            if letra != "_":
                display += f"{GREEN}{letra}{RESET}"
            else:
                display += "_"
        print(f"  {display}")
    
    # Letras em posições erradas (amarelas)
    if letras_posicao_errada:
        print("- Letras presentes mas em posições erradas:")
        for letra, posicoes in letras_posicao_errada.items():
            pos_str = ", ".join(str(p+1) for p in posicoes)
            print(f"  {YELLOW}{letra}{RESET}: não nas posições {pos_str}")

def main():
    print_welcome()
    
    palavras, status = input_usuario()
    if not palavras or not status:
        print(f"{RED}Nenhuma palavra fornecida. Encerrando.{RESET}")
        return
    
    print(f"\n{CYAN}Carregando dicionário...{RESET}")
    try:
        arquivo = input(f"Nome do arquivo de dicionário (padrão: dicionario.txt): ").strip() or "dicionario.txt"
        dicionario = carregar_dicionario(arquivo)
        print(f"{GREEN}Dicionário carregado com {len(dicionario)} palavras de 5 letras!{RESET}")
    except FileNotFoundError:
        print(f"{RED}Arquivo não encontrado! Verifique o nome e o caminho.{RESET}")
        return
    
    # Initialize constraint sets
    letras_proibidas_total = set()
    posicoes_erradas_total = {}
    posicoes_certas_total = {}
    
    # Process constraints for each word-status pair
    for i in range(len(palavras)):
        letras_proibidas, posicoes_erradas, posicoes_certas = processar_restricoes(palavras[i], status[i])
        
        # Accumulate constraints
        letras_proibidas_total.update(letras_proibidas)
        
        # Merge position constraints
        for letra, posicoes in posicoes_erradas.items():
            if letra not in posicoes_erradas_total:
                posicoes_erradas_total[letra] = set()
            posicoes_erradas_total[letra].update(posicoes)
        
        # Update correct positions (greens take precedence)
        posicoes_certas_total.update(posicoes_certas)
    
    # Remove letters in correct positions from prohibited letters
    for posicao, letra in posicoes_certas_total.items():
        if letra in letras_proibidas_total:
            letras_proibidas_total.remove(letra)
    
    # Show summary of restrictions
    mostrar_resumo_restricoes(letras_proibidas_total, posicoes_erradas_total, posicoes_certas_total)
    
    print(f"\n{CYAN}Procurando palavras possíveis...{RESET}")
    time.sleep(0.5)  # Small delay for effect
    
    palavras_filtradas = filtrar_palavras(dicionario, letras_proibidas_total, posicoes_erradas_total, posicoes_certas_total)
    
    print(f"\n{BOLD}Resultado:{RESET}")
    print(f"Encontradas {BOLD}{GREEN}{len(palavras_filtradas)}{RESET} palavras possíveis:")
    
    if not palavras_filtradas:
        print(f"{RED}Nenhuma palavra encontrada que cumpra todas as restrições!{RESET}")
    elif len(palavras_filtradas) <= 20:
        for p in palavras_filtradas:
            print(f" • {p}")
    else:
        print(f"Mostrando as primeiras 20 palavras:")
        for p in palavras_filtradas[:20]:
            print(f" • {p}")
        print(f"...e mais {len(palavras_filtradas) - 20} palavras.")

if __name__ == "__main__":
    try:
        main()
        print(f"\n{BLUE}Obrigado por usar o Wordle Solver!! :D{RESET}")
    except KeyboardInterrupt:
        print(f"\n\n{YELLOW}Programa interrompido pelo usuário!! D:{RESET}")
    except Exception as e:
        print(f"\n{RED}Ocorreu um erro :/ ({e}){RESET}")
