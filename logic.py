from typing import Dict, List, Set, Tuple

class Logic:
    def __init__(self):
        self.dicionario = []
    
    def carregar_dicionario(self, arquivo: str) -> bool:
        """Carrega palavras de 5 letras do arquivo de dicionário."""
        try:
            with open(arquivo, "r") as arq:
                linhas_do_arquivo = arq.readlines()
            
            palavras_limpas = [linha.strip().upper() for linha in linhas_do_arquivo]
            self.dicionario = [palavra for palavra in palavras_limpas if len(palavra) == 5]
            return True
        except FileNotFoundError:
            return False

    def processar_restricoes(self, palavra: str, status: str) -> Tuple[Set[str], Dict[str, Set[int]], Dict[int, str]]:
        """Processa restrições de uma tentativa."""
        letras_proibidas = set()
        posicoes_erradas = {}
        posicoes_certas = {}

        for posicao in range(len(palavra)):
            letra = palavra[posicao]
            status_letra = status[posicao]

            if status_letra == "0":
                letras_proibidas.add(letra)
            elif status_letra == "1":
                if letra not in posicoes_erradas:
                    posicoes_erradas[letra] = set()
                posicoes_erradas[letra].add(posicao)
            elif status_letra == "2":
                posicoes_certas[posicao] = letra
                
        return letras_proibidas, posicoes_erradas, posicoes_certas

    def filtrar_palavras(self, letras_proibidas, letras_posicao_errada, letras_posicao_certa):
        """Filtra palavras do dicionário com base nas restrições."""
        palavras_validas = []

        for palavra in self.dicionario:
            # Pente palavras com letras cinza
            if any(letra in letras_proibidas for letra in palavra if letra not in 
                  [letra for pos, letra in letras_posicao_certa.items()]):
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

    def consolidar_restricoes(self, palavras: List[str], status: List[str]):
        """Consolida restrições de múltiplas tentativas."""
        letras_proibidas_total = set()
        posicoes_erradas_total = {}
        posicoes_certas_total = {}
        
        # Process constraints for each word-status pair
        for i in range(len(palavras)):
            letras_proibidas, posicoes_erradas, posicoes_certas = self.processar_restricoes(palavras[i], status[i])
            
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
        
        return letras_proibidas_total, posicoes_erradas_total, posicoes_certas_total
