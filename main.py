from cache import Cache
from file_handler import FileHandler

cache = Cache(0, 16, 32, 2, 5, "LRU")
cache1 = Cache(0, 16, 32, 2, 5, "A")
cache2 = Cache(0, 16, 32, 2, 5, "LFU")


file = FileHandler("oficial.cache")
for test in file.formata_end_operacao():
    cache.acessa_endereco(test[0], test[1])
    cache1.acessa_endereco(test[0], test[1])
    cache2.acessa_endereco(test[0], test[1])

if cache.politica_escrita:
    cache.dirty_lines()

