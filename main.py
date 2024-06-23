from cache import Cache
from file_handler import FileHandler


arq_ent = FileHandler(str(input("Digite o nome do arquivo de entrada: ")))
pol_esc = int(input("Digite a política de escrita (0 - Write-Through, 1 - Write-Back): "))
tam_lin = int(input("Digite o tamanho da linha (deve ser potência de 2, em bytes): "))
num_lin = int(input("Digite o número de linhas (deve ser potência de 2): "))
assoc = int(input("Digite a associatividade por conjunto (deve ser potência de 2 (mínimo 1 e máximo igual ao número de linhas)): "))
hit_time = int(input("Digite o tempo de acesso quando encontra (hit time): "))
pol_subs = str(input("Digite a política de substituição ('LRU', 'LFU' ou 'A'): "))
temp_mem_principal = int(input("Digite o tempo de leitura/escrita da memória principal: "))

cache = Cache(pol_esc, tam_lin, num_lin, assoc, hit_time, pol_subs)

for test in arq_ent.formata_end_operacao():
    cache.acessa_endereco(test[0], test[1])

if cache.politica_escrita:
    cache.dirty_lines()

# GERAR ARQUIVO DE SAÍDA
if pol_esc == 0:
    pol_esc = 'Write-Through'
else:
    pol_esc = 'Write-Back'

if pol_subs == 'A':
    pol_subs = 'Aleatório'

with open(str(input("Digite o nome do arquivo de saída: ")) + '.txt', 'w') as f:
    f.write("============ PARÂMETROS DE ENTRADA ============\n")
    f.write(f"Política de Escrita: {pol_esc}\n"
            f"Tamanho da Linha: {tam_lin}\n"
            f"Número de Linhas: {num_lin}\n"
            f"Associatividade: {assoc}\n"
            f"Tempo de Acesso (hit time): {hit_time}\n"
            f"Política de Substituição: {pol_subs}\n"
            f"Tempo de Leitura/Escrita na Memória Principal: {temp_mem_principal}\n"
            f"===============================================\n\n")

    f.write("======== ENDEREÇOS NO ARQUIVO DE ENTRADA ========\n")
    f.write(f"Número de Endereços de Escrita: {arq_ent.num_escritas}\n"
            f"Número de Endereços de Leitura: {arq_ent.num_leituras}\n"
            f"Total de Endereços: {arq_ent.total}\n"
            f"================================================\n\n")

    f.write("=== ESCRITAS E LEITURAS NA MEMÓRIA PRINCIPAL ===\n")
    f.write(f"Total de Escritas: {cache.escritas_mp}\n"
            f"Total de Leituras: {cache.leituras_mp}\n"
            f"Total: {cache.escritas_mp + cache.leituras_mp}\n"
            f"===============================================\n\n")

    taxa_de_acerto_global = cache.hits * 100 / arq_ent.total
    f.write("========== TAXA DE ACERTO (HIT RATE) ==========\n")
    f.write(f"Taxa de Acerto de Leitura: {round(cache.hits_leitura * 100 / arq_ent.num_leituras, 4)}% ({cache.hits_leitura} certos)\n"
            f"Taxa de Acerto de Escrita: {round(cache.hits_escrita * 100 / arq_ent.num_escritas, 4)}% ({cache.hits_escrita} acertos)\n"
            f"Taxa de Acerto Global: {round(taxa_de_acerto_global, 4)}% ({cache.hits} acertos)\n"
            f"===============================================\n\n")

    tempo_de_acesso = round((taxa_de_acerto_global/100 * hit_time) + ((1 - taxa_de_acerto_global/100) * (hit_time + temp_mem_principal)), 4)
    f.write(f"Tempo Médio de Acesso da Cache (em ns): {tempo_de_acesso}\n")





