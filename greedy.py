import os

import time
import tracemalloc
import matplotlib.pyplot as plt
import statistics

from extra_functions import quick_sort, temRecursoDisponivel, temRecursoDisponivelBalanceado, plota

tempos_classico = []
memorias_classico = []
recursos_classico = []
desvios_padroes_classico = []

arquivos = os.listdir('entries')

for arquivo in arquivos:
    caminho_arq = f"entries/{arquivo}"

    custo_medio_memoria_local = 0
    custo_medio_tempo_local = 0
    custo_medio_recurso_local = 0
    custo_medio_dp_local = 0

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

            custo_medio_tempo_local += (tempo_fim - tempo_inicio)
            custo_medio_memoria_local += peak / 1024
            custo_medio_recurso_local += len(escalonamento)

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
            
            custo_medio_dp_local += desvio_padrao

            # print(f"Tempo de execução: {tempo_fim - tempo_inicio:.6f}s")
            # print(f"Memória utilizada: {peak / 1024:.2f}KB")
        
        if (c == 5):
            tempos_classico.append(custo_medio_tempo_local / 5)
            memorias_classico.append(custo_medio_memoria_local / 5)
            recursos_classico.append(custo_medio_recurso_local / 5)
            desvios_padroes_classico.append(custo_medio_dp_local / 5)

        # print("")
        # for i, recurso in enumerate(escalonamento):
        #     print(f"Recurso {i + 1}: {recurso}")
            
        # print("\n=== ESTATÍSTICAS ===")
        # for i, recurso in enumerate(escalonamento):
        #     tempo_total = sum(fim - inicio for inicio, fim in recurso)
        #     print(f"Recurso {i + 1}: {len(recurso)} tarefas, {tempo_total} horas alocadas")

tempos_boosted = []
memorias_boosted = []
recursos_boosted = []
desvios_padroes_boosted = []

for arquivo in arquivos:
    caminho_arq = f"entries/{arquivo}"

    custo_medio_memoria_local = 0
    custo_medio_tempo_local = 0
    custo_medio_recurso_local = 0
    custo_medio_dp_local = 0

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
            
            recursoDisponivel = temRecursoDisponivelBalanceado(escalonamento, menor, fim_horario)

            if recursoDisponivel is False:     
                escalonamento.append([(menor, fim_horario)])
            else:
                escalonamento[recursoDisponivel].append((menor, fim_horario))
            
            horarios.pop(0)
        
        if(c != 0):
            tempo_fim = time.time()
            current, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            custo_medio_tempo_local += (tempo_fim - tempo_inicio)
            custo_medio_memoria_local += peak / 1024
            custo_medio_recurso_local += len(escalonamento)

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
            
            custo_medio_dp_local += desvio_padrao

            # print(f"Tempo de execução: {tempo_fim - tempo_inicio:.6f}s")
            # print(f"Memória utilizada: {peak / 1024:.2f}KB")
        
        if (c == 5):
            tempos_boosted.append(custo_medio_tempo_local / 5)
            memorias_boosted.append(custo_medio_memoria_local / 5)
            recursos_boosted.append(custo_medio_recurso_local / 5)
            desvios_padroes_boosted.append(custo_medio_dp_local / 5)

        # print("")
        # for i, recurso in enumerate(escalonamento):
        #     print(f"Recurso {i + 1}: {recurso}")
            
        # print("\n=== ESTATÍSTICAS ===")
        # for i, recurso in enumerate(escalonamento):
        #     tempo_total = sum(fim - inicio for inicio, fim in recurso)
        #     print(f"Recurso {i + 1}: {len(recurso)} tarefas, {tempo_total} horas alocadas")

plota(plt, arquivos, 
    tempos_classico, memorias_classico, desvios_padroes_classico, recursos_classico,
    tempos_boosted, memorias_boosted, desvios_padroes_boosted, recursos_boosted
    )