class FileHandler:
    def __init__(self, filename: str):
        self.filename = filename
        self.linhas = []
        self.num_escritas = 0
        self.num_leituras = 0
        self.total = 0

    def formata_end_operacao(self) -> None:
        """
        Cria uma lista de operações a partir de um arquivo.

        :return: Retorna uma lista contendo todas os endereços e operações.
        """
        with open(self.filename, "r") as arq:
            for i, linha in enumerate(arq.readlines()):
                self.linhas.append(linha.strip("\n").split(" "))

                if self.linhas[i][1] == 'W':
                    self.num_escritas += 1
                else:
                    self.num_leituras += 1

            self.total = i + 1

        return
