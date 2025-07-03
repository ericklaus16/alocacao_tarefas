import time
import tracemalloc
import matplotlib.pyplot as plt
from extra_functions import quick_sort, temRecursoDisponivel

caminho_arq = "entries/Aula5000.txt"

tempos = []
memorias = []
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
        print(f"\n======= RODADA {c + 1} =======")
        tempo_inicio = time.time()

    while len(horarios_inicio) != 0:
        primeira = True
        menor = horarios_inicio[0]
        fim_horario = horarios_fim[0]

        # print(f"Analisando tarefa [{menor}, {fim_horario}]")
        
        recursoDisponivel = temRecursoDisponivel(escalonamento, menor, fim_horario)

        if recursoDisponivel is False:     
            escalonamento.append([(menor, fim_horario)])
        else:
            escalonamento[recursoDisponivel].append((menor, fim_horario))
        
        horarios_inicio.pop(0)
        horarios_fim.pop(0)
    
    if(c != 0):
        tempo_fim = time.time()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        tempos.append(tempo_fim - tempo_inicio)
        memorias.append(peak / 1024)

        # print(f"Tempo de execução: {tempo_fim - tempo_inicio:.6f}s")
        # print(f"Memória utilizada: {peak / 1024:.2f}KB")

    print("")
    # for i, recurso in enumerate(escalonamento):
    #     print(f"Recurso {i + 1}: {recurso}")
        
    # print("\n=== ESTATÍSTICAS ===")
    # for i, recurso in enumerate(escalonamento):
    #     tempo_total = sum(fim - inicio for inicio, fim in recurso)
    #     print(f"Recurso {i + 1}: {len(recurso)} tarefas, {tempo_total} horas alocadas")

fig, ax1 = plt.subplots()

ax1.set_xlabel('Iterações')
ax1.set_ylabel('Tempo (s)', color='tab:blue')
tempo_line, = ax1.plot(iteracoes, tempos, marker='o', color='tab:blue', label='Tempo')
ax1.tick_params(axis='y', labelcolor='tab:blue')

ax2 = ax1.twinx() 
ax2.set_ylabel('Memória (KB)', color='tab:red')
memoria_line, = ax2.plot(iteracoes, memorias, marker='s', color='tab:red', label='Memória')
ax2.tick_params(axis='y', labelcolor='tab:red')

lines = [tempo_line, memoria_line]
labels = [line.get_label() for line in lines]
ax1.legend(lines, labels, loc='upper right') 

plt.title('Tempo e Memória por Iteração')
fig.tight_layout()
plt.show()