import time
import tracemalloc
import matplotlib.pyplot as plt
import statistics

from extra_functions import quick_sort, temRecursoDisponivel, plota

caminho_arq = "entries/Aula1000.txt"

tempos = []
memorias = []
recursos = []
desvios_padroes = []
iteracoes = ['2ª', '3ª', '4ª', '5ª', '6ª']

for c in range(6):
    tempo_inicio = 0
    tempo_fim = 0

    escalonamento = []

    horarios = []

    with open(caminho_arq, 'r') as arq:
        linhas = arq.readlines()
        horarios_inicio = list(map(int, linhas[0].strip().split(" ")))
        horarios_fim = list(map(int, linhas[1].strip().split(" ")))
        
        horarios = list(zip(horarios_inicio, horarios_fim))

    if c != 0:
        # print(horarios)
        quick_sort(horarios, 0, len(horarios) - 1)
        # print(horarios)

        tracemalloc.start()
        tempo_inicio = time.time()

    while len(horarios) != 0:
        menor = horarios[0][0]
        fim_horario = horarios[0][1]

        # print(f"Analisando tarefa [{menor}, {fim_horario}]")
        
        recursoDisponivel = temRecursoDisponivel(escalonamento, menor, fim_horario)

        if recursoDisponivel is False:     
            escalonamento.append([(menor, fim_horario)])
        else:
            escalonamento[recursoDisponivel].append((menor, fim_horario))
        
        horarios.pop(0)
    
    if(c != 0):
        tempo_fim = time.time()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        tempos.append(tempo_fim - tempo_inicio)
        memorias.append(peak / 1024)
        recursos.append(len(escalonamento))

        horas_por_recurso = []
        for recurso in escalonamento:
            horas_total = sum(fim - inicio for inicio, fim in recurso)
            # print(horas_total)
            horas_por_recurso.append(horas_total)


        if len(horas_por_recurso) > 1:
            desvio_padrao = statistics.pstdev(horas_por_recurso)
            # print(desvio_padrao)
        else:
            desvio_padrao = 0.0
        
        desvios_padroes.append(desvio_padrao)

        # print(f"Tempo de execução: {tempo_fim - tempo_inicio:.6f}s")
        # print(f"Memória utilizada: {peak / 1024:.2f}KB")

    # print("")
    # for i, recurso in enumerate(escalonamento):
    #     print(f"Recurso {i + 1}: {recurso}")
        
    # print("\n=== ESTATÍSTICAS ===")
    # for i, recurso in enumerate(escalonamento):
    #     tempo_total = sum(fim - inicio for inicio, fim in recurso)
    #     print(f"Recurso {i + 1}: {len(recurso)} tarefas, {tempo_total} horas alocadas")

plota(plt, iteracoes, tempos, memorias, desvios_padroes, recursos)