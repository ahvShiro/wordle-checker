import time
from src.colors import Colors
from src.interface import Interface
from src.logic import Logic

def main():
    ui = Interface()
    logic = Logic()
    
    ui.print_welcome()
    
    palavras, status = ui.input_usuario()
    
    if not palavras or not status:
        print(f"{Colors.RED}Nenhuma palavra fornecida. Encerrando.{Colors.RESET}")
        return
    
    print(f"\n{Colors.CYAN}Carregando dicionário...{Colors.RESET}")
    
    arquivo = "../data/" + input(f"Nome do arquivo de dicionário (selecionando de ../data/): ").strip() or "../data/dicionario.txt"

    if not logic.carregar_dicionario(arquivo):
        print(f"{Colors.RED}Arquivo não encontrado! Verifique o nome e o caminho.{Colors.RESET}")
        return
    
    print(f"{Colors.GREEN}Dicionário carregado com {len(logic.dicionario)} palavras de 5 letras!{Colors.RESET}")
    
    # Consolidate constraints
    letras_proibidas, posicoes_erradas, posicoes_certas = logic.consolidar_restricoes(palavras, status)
    
    # Show summary
    ui.mostrar_resumo_restricoes(letras_proibidas, posicoes_erradas, posicoes_certas)
    
    print(f"\n{Colors.CYAN}Procurando palavras possíveis...{Colors.RESET}")
    time.sleep(0.5)  # Small delay for effect
    
    # Filter words
    palavras_filtradas = logic.filtrar_palavras(letras_proibidas, posicoes_erradas, posicoes_certas)
    
    # Show results
    ui.mostrar_resultados(palavras_filtradas)

if __name__ == "__main__":
    try:
        main()
        print(f"\n{Colors.BLUE}Obrigado por usar o Wordle Solver!! :D{Colors.RESET}")
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Programa interrompido pelo usuário!! D:{Colors.RESET}")
    except Exception as e:
        print(f"\n{Colors.RED}Ocorreu um erro :/ ({e}){Colors.RESET}")