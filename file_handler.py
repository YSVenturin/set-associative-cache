class FileHandler:
    def __init__(self, filename: str):
        self.filename = filename
        self.linhas = []
        self.num_escritas = 0
        self.num_leituras = 0
        self.total = 0

    def formata_end_operacao(self):
        with open(self.filename, "r") as arq:
            for linha in arq.readlines():
                self.linhas.append(linha.strip("\n").split(" "))

        self.contador()

        return self.linhas

    def contador(self):
        for linha in self.linhas:
            if linha[1] == 'W':
                self.num_escritas += 1
            else:
                self.num_leituras += 1

        self.total = self.num_escritas + self.num_leituras
