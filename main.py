from cache import Cache
from file_handler import FileHandler

cache = Cache("test", 0, 128, 1024, 4, 5, "LRU")

file = FileHandler("oficial.cache")
print(file.formata_end_operacao())

with open("oficial.cache", "r") as f:
    addresses = [adr.strip()[:8] for adr in f.readlines()]

for adr in addresses:
    cache.acessa_endereco(adr)

print(cache.hits)
print(cache.misses)



