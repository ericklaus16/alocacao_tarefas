import time
import tracemalloc
import matplotlib.pyplot as plt
import statistics

from extra_functions import quick_sort, temRecursoDisponivelBalanceado, plota

caminho_arq = "entries/Aula100.txt"

tempos = []
memorias = []
desvios_padroes = []
iteracoes = ['2ª', '3ª', '4ª', '5ª', '6ª']

for c in range(6):
    tempo_inicio = 0
    tempo_fim = 0

    horarios_inicio = []
    horarios_fim = []

    escalonamento = []

    contador = 0
    with open(caminho_arq, 'r') as arq:
        for linha in arq:
            if contador == 0:
                horarios_inicio = list(map(int, linha.strip().split(" ")))
                contador += 1
            else:
                horarios_fim = list(map(int, linha.strip().split(" ")))

    if c != 0:
        quick_sort(horarios_inicio, 0, len(horarios_inicio) - 1)
        quick_sort(horarios_fim, 0, len(horarios_fim) - 1)
        tracemalloc.start()
        tempo_inicio = time.time()

    while len(horarios_inicio) != 0:
        menor = horarios_inicio[0]
        fim_horario = horarios_fim[0]

        # print(f"Analisando tarefa [{menor}, {fim_horario}]")

        recursoDisponivel = temRecursoDisponivelBalanceado(
            escalonamento, menor, fim_horario)

        if recursoDisponivel is False:
            escalonamento.append([(menor, fim_horario)])
        else:
            escalonamento[recursoDisponivel].append((menor, fim_horario))

        horarios_inicio.pop(0)
        horarios_fim.pop(0)

    if (c != 0):
        tempo_fim = time.time()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        tempos.append(tempo_fim - tempo_inicio)
        memorias.append(peak / 1024)

        horas_por_recurso = []
        for recurso in escalonamento:
            horas_total = sum(fim - inicio for inicio, fim in recurso)
            horas_por_recurso.append(horas_total)

        if len(horas_por_recurso) > 1:
            desvio_padrao = statistics.stdev(horas_por_recurso)
        else:
            desvio_padrao = 0.0

        desvios_padroes.append(desvio_padrao)

        # print(f"Tempo de execução: {tempo_fim - tempo_inicio:.6f}s")
        # print(f"Memória utilizada: {peak / 1024:.2f}KB")

    print("")
    # for i, recurso in enumerate(escalonamento):
    #     print(f"Recurso {i + 1}: {recurso}")

    # print("\n=== ESTATÍSTICAS ===")
    # for i, recurso in enumerate(escalonamento):
    #     tempo_total = sum(fim - inicio for inicio, fim in recurso)
    #     print(f"Recurso {i + 1}: {len(recurso)} tarefas, {tempo_total} horas alocadas")

plota(plt, iteracoes, tempos, memorias, desvios_padroes)
