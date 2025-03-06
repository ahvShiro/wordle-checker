import os
import time
from colors import Colors
from interface import Interface
from logic import Logic

def main():
    Interface.print_welcome()
    
    # instancias criadas
    logic = Logic()
    ui = Interface()
    
    # input do usuário pego e armazenado em uma tupla com 2 listas ([palavras], [status])
    palavras, status = ui.input_usuario()
    
    # se input não tiver palavras ou status, encerra o programa
    if not palavras or not status:
        print(f"{Colors.RED}Nenhuma palavra fornecida. Encerrando.{Colors.RESET}")
        return
    
    # define o caminho dos dicionarios
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')

    arquivo = ui.selecionar_dicionario(data_dir)

    # se o arquivo não existir, encerra proframa
    if not logic.carregar_dicionario(arquivo):
        print(f"{Colors.RED}Arquivo não encontrado! Verifique o nome e o caminho.{Colors.RESET}")
        return
    
    print(f"{Colors.GREEN}Dicionário carregado com {len(logic.dicionario)} palavras de 5 letras!{Colors.RESET}")
    
    letras_proibidas, posicoes_erradas, posicoes_certas = logic.consolidar_restricoes(palavras, status)
    
    ui.mostrar_resumo_restricoes(letras_proibidas, posicoes_erradas, posicoes_certas)
    
    print(f"\n{Colors.CYAN}Procurando palavras possíveis...{Colors.RESET}")
    time.sleep(1)  # delay dramatico
    
    # filtra possiveis candidatos a resposta baseado nas restricoes consolidadas
    palavras_filtradas = logic.filtrar_palavras(letras_proibidas, posicoes_erradas, posicoes_certas)
    
    ui.mostrar_resultados(palavras_filtradas)

if __name__ == "__main__":
    try:
        main()
        print(f"\n{Colors.BLUE}Obrigado por usar o Wordle Solver!! :D{Colors.RESET}")
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Programa interrompido pelo usuário!! D:{Colors.RESET}")
    except Exception as e:
        print(f"\n{Colors.RED}Ocorreu um erro :/ ({e}){Colors.RESET}")