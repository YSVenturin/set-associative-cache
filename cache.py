import math
from random import randint
from collections import OrderedDict


class CacheLinha:
    def __init__(self):
        self.valida = False
        self.rotulo = None


class CacheConjuntos:
    def __init__(self, associatividade: int):
        self.linhas = [CacheLinha() for _ in range(associatividade)]
        self.dados_do_conjunto = OrderedDict()
        for _ in range(associatividade):
            self.dados_do_conjunto[_] = 0


class Cache:
    def __init__(self, politica_escrita: int, tamanho_linha: int, numero_linhas: int, associatividade: int,
                 hit_time: int, politica_substituicao: str):

        self.politica_escrita = politica_escrita
        self.tamanho_linha = tamanho_linha
        self.numero_linhas = numero_linhas
        self.associatividade = associatividade
        self.hit_time = hit_time
        self.politica_substituicao = politica_substituicao
        self.num_conjuntos = numero_linhas // associatividade
        self.conjuntos = [CacheConjuntos(associatividade) for _ in range(self.num_conjuntos)]
        self.TAMANHO_ENDERECO = 32
        self.bits_conjunto = self.bits_conjunto()
        self.bits_palavra = self.bits_palavra()
        self.bits_rotulo = self.TAMANHO_ENDERECO - self.bits_conjunto - self.bits_palavra

        self.hits = 0
        self.misses = 0

    def bits_conjunto(self) -> int:
        """
        :return: Retorna o número de bits necessários para representar todos os conjuntos.
        """
        return int(math.log2(self.num_conjuntos))

    def bits_palavra(self) -> int:
        """
        :return: Retorna o número de bits necessários para representar o tamanho da linha.
        """
        return int(math.log2(self.tamanho_linha))

    def encontra_index_conjunto(self, endereco: int) -> int:
        """
        :param endereco:
        :return: Retorna em qual conjunto o endereço se encontra.
        """

        index = (endereco // self.tamanho_linha) % self.num_conjuntos
        return index

    def encontra_rotulo(self, endereco: int) -> int:
        """
        :param endereco:

        :return: Retorna o rótulo do determinado endereço.
        """

        rotulo = (endereco >> (self.bits_palavra + self.bits_conjunto))
        return rotulo

    def politica_escrita_cont(self):
        # Write-Through
        if self.politica_escrita == 0:
            pass
        # Write-Back
        else:
            pass


    def acessa_endereco(self, endereco):
        int_end = int(endereco, 16)
        index_conjunto = self.encontra_index_conjunto(int_end)
        rotulo = self.encontra_rotulo(int_end)

        conjunto = self.conjuntos[index_conjunto]
        for i, linha in enumerate(conjunto.linhas):
            if linha.rotulo == rotulo and linha.valida:
                conjunto.dados_do_conjunto[i] += 1
                conjunto.dados_do_conjunto.move_to_end(i)
                self.hits += 1

                return True  # Hit de Cache

        if self.politica_substituicao == "LFU":
            min_value = min(conjunto.dados_do_conjunto.values())

            min_key = None
            for key in conjunto.dados_do_conjunto:
                if conjunto.dados_do_conjunto[key] == min_value:
                    min_key = key
                    break

            conjunto.dados_do_conjunto[min_key] += 1
            conjunto.linhas[min_key].valida = True
            conjunto.linhas[min_key].rotulo = rotulo

        elif self.politica_substituicao == "LRU":
            lru_key = list(conjunto.dados_do_conjunto.keys())[0]
            conjunto.dados_do_conjunto.move_to_end(lru_key)
            conjunto.dados_do_conjunto[lru_key] += 1

            conjunto.linhas[lru_key].valida = True
            conjunto.linhas[lru_key].rotulo = rotulo

        else:
            random_key = randint(0, self.associatividade - 1)
            conjunto.linhas[random_key].valida = True
            conjunto.linhas[random_key].rotulo = rotulo

        self.misses += 1
        return False  # Miss de cache
