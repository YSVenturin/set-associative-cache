import math
from random import randint
from collections import OrderedDict
from typing import Callable


class CacheLinha:
    def __init__(self):
        self.valida = False
        self.rotulo = None
        self.db = False


class CacheConjunto:
    def __init__(self, associatividade: int):
        self.linhas = [CacheLinha() for _ in range(associatividade)]
        self.frequencia_ordenada = OrderedDict()
        for _ in range(associatividade):
            self.frequencia_ordenada[_] = 0


class Cache:
    subs_func: Callable[[CacheConjunto], int] | None
    esc_func: Callable[[str, bool, CacheLinha], bool] | None

    def __init__(self, politica_escrita: int, tamanho_linha: int, numero_linhas: int, associatividade: int,
                 hit_time: int, politica_substituicao: str):

        # Configurações da Cache
        self.politica_escrita = politica_escrita
        self.tamanho_linha = tamanho_linha
        self.numero_linhas = numero_linhas
        self.associatividade = associatividade
        self.hit_time = hit_time
        self.politica_substituicao = politica_substituicao
        self.num_conjuntos = numero_linhas // associatividade
        self.conjuntos = [CacheConjunto(associatividade) for _ in range(self.num_conjuntos)]

        # Separação de Bits por Endereço
        self.TAMANHO_ENDERECO = 32
        self.bits_conjunto = self.bits_conjunto()
        self.bits_palavra = self.bits_palavra()
        self.bits_rotulo = self.TAMANHO_ENDERECO - self.bits_conjunto - self.bits_palavra

        # Contadores
        self.hits = 0
        self.misses = 0
        self.leituras_mp = 0
        self.escritas_mp = 0
        self.hits_escrita = 0
        self.hits_leitura = 0

        # Conjunto de Funções
        self.pol_subs_func = {
            "LRU": self.subs_lru,
            "LFU": self.subs_lfu,
            "A": self.subs_aleatorio
        }
        self.subs_func = self.pol_subs_func.get(self.politica_substituicao)

        self.pol_esc_func = {
            0: self.esc_write_through,
            1: self.esc_write_back
        }
        self.esc_func = self.pol_esc_func.get(self.politica_escrita)

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

    def esc_write_through(self, operacao: str, hit: bool, _linha: CacheLinha) -> bool:
        if operacao == 'W':
            self.escritas_mp += 1

        if not hit:
            self.leituras_mp += 1

        return False

    def esc_write_back(self, operacao: str, hit: bool, linha: CacheLinha) -> bool:

        if not hit:
            self.leituras_mp += 1

        if operacao == 'R':
            if not hit and linha.db:
                self.escritas_mp += 1

            return False

        if operacao == 'W':
            if not hit and linha.db:
                self.escritas_mp += 1

            return True

    @staticmethod
    def subs_lru(conjunto: CacheConjunto) -> int:
        key_to_change = list(conjunto.frequencia_ordenada.keys())[0]
        conjunto.frequencia_ordenada.move_to_end(key_to_change)

        return key_to_change

    @staticmethod
    def subs_lfu(conjunto: CacheConjunto) -> int:
        key_to_change = None

        for i, linha in enumerate(conjunto.linhas):
            if not linha.valida:
                key_to_change = i
                return key_to_change

        min_value = min(conjunto.frequencia_ordenada.values())

        for key, freq in conjunto.frequencia_ordenada.items():
            if freq == min_value:
                key_to_change = key
                break

        return key_to_change

    def subs_aleatorio(self, _conjunto: CacheConjunto) -> int:
        key_to_change = randint(0, self.associatividade - 1)

        return key_to_change

    def dirty_lines(self) -> None:
        for conjunto in self.conjuntos:
            for linha in conjunto.linhas:
                if linha.db:
                    linha.db = False
                    self.escritas_mp += 1

        return

    def acessa_endereco(self, endereco: str, operacao: str) -> bool:
        """
        Acessa um endereço na cache e realiza a operação especificada.

        :param endereco: Número Hexadecimal que corresponde ao endereço de memória a ser acessado.
        :param operacao: 'W' ou 'R', correspondedo se será uma escrita (W) ou leitura (R).

        :return: Retorna True caso tenha um Hit de cache e False caso contrário.
        """

        int_end = int(endereco, 16)
        index_conjunto = self.encontra_index_conjunto(int_end)
        rotulo = self.encontra_rotulo(int_end)

        conjunto = self.conjuntos[index_conjunto]

        for i, linha in enumerate(conjunto.linhas):
            if linha.rotulo == rotulo and linha.valida:
                conjunto.frequencia_ordenada[i] += 1
                conjunto.frequencia_ordenada.move_to_end(i)
                self.hits += 1

                if operacao == 'W':
                    self.hits_escrita += 1
                else:
                    self.hits_leitura += 1

                linha.db = self.esc_func(operacao, True, linha)
                return True  # Hit de Cache

        key_to_change = self.subs_func(conjunto)
        conjunto.linhas[key_to_change].valida = True
        conjunto.linhas[key_to_change].rotulo = rotulo
        conjunto.linhas[key_to_change].db = self.esc_func(operacao, False, conjunto.linhas[key_to_change])

        self.misses += 1
        return False  # Miss de cache
