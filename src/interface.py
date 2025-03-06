import os
from colors import Colors

SLANT_TITLE = """
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

class Interface:
    @staticmethod
    def clear_screen():
        """Clear the terminal screen."""
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def print_welcome():
        """Print a welcome message with instructions."""
        Interface.clear_screen()
        print(f"\n{Colors.BOLD}{Colors.GREEN}{SLANT_TITLE}{Colors.RESET}")
        print(f"\nEste programa ajuda a encontrar possíveis respostas para o Wordle/Termo\ndo dia com base nas suas tentativas!")
        print("\nInstruções para o status de cada letra:")
        print(f" • Digite {Colors.GRAY}[0]{Colors.RESET} para letras {Colors.GRAY}CINZAS{Colors.RESET} (a letra não está na palavra)")
        print(f" • Digite {Colors.YELLOW}[1]{Colors.RESET} para letras {Colors.YELLOW}AMARELAS{Colors.RESET} (a letra tá na palavra, mas na posição errada)")
        print(f" • Digite {Colors.GREEN}[2]{Colors.RESET} para letras {Colors.GREEN}VERDES{Colors.RESET} (a letra na palavra e na posição correta)")
        
        print(f"\nExemplo: Para a palavra '{Colors.BOLD}TERMO{Colors.RESET}'")
        print(f"Se o resultado for: {Colors.GRAY}[T]{Colors.RESET}{Colors.YELLOW}[E]{Colors.RESET}{Colors.GREEN}[R]{Colors.RESET}{Colors.GRAY}[M]{Colors.RESET}{Colors.YELLOW}[O]{Colors.RESET}")
        print(f"Você deve digitar: 01200\n")
        print(f"{Colors.GREEN}Pressione Enter para começar...{Colors.RESET}")
        input()
        Interface.clear_screen()
    
    @staticmethod
    def colorir_palavra(palavra: str, status: str) -> str:
        """Retorna a palavra com cores baseadas no status."""
        resultado = ""
        for i, letra in enumerate(palavra):
            if i < len(status):
                if status[i] == "0":
                    resultado += f"{Colors.GRAY}[{letra}]{Colors.RESET}"
                elif status[i] == "1":
                    resultado += f"{Colors.YELLOW}[{letra}]{Colors.RESET}"
                elif status[i] == "2":
                    resultado += f"{Colors.GREEN}[{letra}]{Colors.RESET}"
                else:
                    resultado += letra
            else:
                resultado += letra
        return resultado
    
    @staticmethod
    def input_usuario() -> tuple[list, list]:
        palavras = []
        status = []
        
        print(f"{Colors.BOLD}Digite suas tentativas (Ou ENTER para finalizar):{Colors.RESET}")
        print(f"({Colors.GRAY}0=CINZA{Colors.RESET}, {Colors.YELLOW}1=AMARELO{Colors.RESET}, {Colors.GREEN}2=VERDE{Colors.RESET})\n")

        for i in range(6):
            palavra = input(f"Palavra {i + 1}: ").strip().upper()
            if not palavra:
                break
                
            if len(palavra) != 5:
                print(f"{Colors.RED}A palavra deve ter 5 letras!{Colors.RESET}")
                i -= 1
                continue

            while True:
                estado = input(f"{Colors.GRAY}{Colors.BOLD}[0]{Colors.RESET}/{Colors.YELLOW}{Colors.BOLD}[1]{Colors.RESET}/{Colors.GREEN}{Colors.BOLD}[2]{Colors.RESET}): ").strip()
                if len(estado) == 5 and all(c in "012" for c in estado):
                    break
                print(f"{Colors.RED}Status inválido! Digite 5 números (0, 1 ou 2).{Colors.RESET}")
            
            palavras.append(palavra)
            status.append(estado)
            
            # Show the word with colors to confirm
            print(f"Registrado: {Interface.colorir_palavra(palavra, estado)}\n")

        return palavras, status
    
    @staticmethod
    def mostrar_resumo_restricoes(letras_proibidas, letras_posicao_errada, letras_posicao_certa):
        """Mostra um resumo das restrições processadas."""
        print(f"\n{Colors.BOLD}Resumo das Restrições:{Colors.RESET}")
        
        # Letras proibidas
        if letras_proibidas:
            print(f"- Letras ausentes: {Colors.GRAY}{', '.join(sorted(letras_proibidas))}{Colors.RESET}")
        
        # Letras em posições corretas (verdes)
        if letras_posicao_certa:
            print("- Letras confirmadas:")
            palavra_template = ["_", "_", "_", "_", "_"]
            for pos, letra in letras_posicao_certa.items():
                palavra_template[pos] = letra
            
            display = ""
            for i, letra in enumerate(palavra_template):
                if letra != "_":
                    display += f"{Colors.GREEN}{letra}{Colors.RESET}"
                else:
                    display += "_"
            print(f"  {display}")
        
        # Letras em posições erradas (amarelas)
        if letras_posicao_errada:
            print("- Letras presentes mas em posições erradas:")
            for letra, posicoes in letras_posicao_errada.items():
                pos_str = ", ".join(str(p+1) for p in posicoes)
                print(f"  {Colors.YELLOW}{letra}{Colors.RESET}: não nas posições {pos_str}")
    
    @staticmethod
    def mostrar_resultados(palavras_filtradas):
        """Mostra os resultados da pesqInterfacesa."""
        print(f"\n{Colors.BOLD}Resultado:{Colors.RESET}")
        print(f"Encontradas {Colors.BOLD}{Colors.GREEN}{len(palavras_filtradas)}{Colors.RESET} palavras possíveis:")
        
        if not palavras_filtradas:
            print(f"{Colors.RED}Nenhuma palavra encontrada que cumpra todas as restrições!{Colors.RESET}")
        elif len(palavras_filtradas) <= 20:
            for p in palavras_filtradas:
                print(f" • {p}")
        else:
            print(f"Mostrando as primeiras 20 palavras:")
            for p in palavras_filtradas[:20]:
                print(f" • {p}")
            print(f"...e mais {len(palavras_filtradas) - 20} palavras.")
    
    @staticmethod
    def selecionar_dicionario(data_dir):
        """Allow user to select a dictionary file from available options."""
        print(f"\n{Colors.CYAN}Carregando dicionário...{Colors.RESET}")
        
        arquivos_disponiveis = [f for f in os.listdir(data_dir) if os.path.isfile(os.path.join(data_dir, f))]

        print(f"{Colors.CYAN}Dicionários disponíveis:{Colors.RESET}")
        for idx, arquivo in enumerate(arquivos_disponiveis, start=1):
            print(f"{idx}. {arquivo}")

        escolha = input(f"Escolha o número do arquivo de dicionário (padrão: 1): ").strip()
        if escolha.isdigit() and 1 <= int(escolha) <= len(arquivos_disponiveis):
            arquivo = os.path.join(data_dir, arquivos_disponiveis[int(escolha) - 1])
        else:
            arquivo = os.path.join(data_dir, "dicionario.txt")
        
        return arquivo

