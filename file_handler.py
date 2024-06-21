class FileHandler:
    def __init__(self, filename: str):
        self.filename = filename

    def formata_end_operacao(self):
        linhas = []
        with open(self.filename, "r") as arq:
            for linha in arq.readlines():
                linhas.append(linha.strip("\n").split(" "))

        return linhas

