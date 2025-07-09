import matplotlib.ticker as ticker
import re

def quick_sort(vet, left, right):
    i = left
    j = right

    pivo = vet[(left + right) // 2]

    while i <= j:
        while vet[i] < pivo and i < right:
            i += 1
        while vet[j] > pivo and j > left:
            j -= 1

        if i <= j:
            y = vet[i]
            vet[i] = vet[j]
            vet[j] = y
            i += 1
            j -= 1

    if i > left:
        quick_sort(vet, left, j)

    if i < right:
        quick_sort(vet, i, right)


def temRecursoDisponivel(escalonamento, inicio, fim):
    for idx, recurso in enumerate(escalonamento):
        conflito = False
        for ocupado_inicio, ocupado_fim in recurso:
            # Duas tarefas conflitam se há sobreposição no tempo
            # NÃO conflitam se: nova termina antes/quando existente começa OU nova começa depois/quando existente termina
            if not (fim <= ocupado_inicio or inicio >= ocupado_fim):
                conflito = True
                break

        if not conflito:
            # print(f"Recurso {idx+1} DISPONÍVEL para tarefa ({inicio},{fim})")
            return idx  # Este recurso pode acomodar a nova tarefa
        # else:
        #     print(f"Recurso {idx+1} OCUPADO")

    # print(f"Nenhum recurso disponível para ({inicio},{fim}), criando novo recurso!")
    return False


def temRecursoDisponivelBalanceado(escalonamento, inicio, fim):
    recursos_disponiveis = {}

    for idx, recurso in enumerate(escalonamento):
        conflito = False

        for ocupado_inicio, ocupado_fim in recurso:
            if not (fim <= ocupado_inicio or inicio >= ocupado_fim):
                conflito = True
                break

        if not conflito:
            # Calcula tempo total ocupado neste recurso
            tempo_total = sum(fim - inicio for inicio, fim in recurso)
            recursos_disponiveis[idx] = tempo_total

    # Escolhe o recurso com MENOR tempo ocupado (mais balanceado)
    if recursos_disponiveis:
        melhor_recurso = min(recursos_disponiveis, # Verificar com o Andrezão se é correto usar o min aqui
                             key=recursos_disponiveis.get)
        return melhor_recurso
    else:
        return False


def extrai_numeros(arquivos):
    return [int(re.search(r'\d+', nome).group()) for nome in arquivos]

def plota(plt, arquivos, tempos, memorias, desvios_padroes, recursos, modo = "Clássico"):
    entradas = [int(re.search(r'\d+', nome).group()) for nome in arquivos]
    dados_ordenados = sorted(zip(entradas, tempos, memorias, desvios_padroes, recursos))
    entradas, tempos, memorias, desvios_padroes, recursos = zip(*dados_ordenados)

    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 10))
    
    # Gráfico 1 - Tempo
    ax1.plot(entradas, tempos, marker='o', color='tab:blue', label='Tempo')
    ax1.set_xlabel('Entradas')
    ax1.set_xticks(entradas)
    ax1.set_ylabel('Tempo (s)', color='tab:blue')
    ax1.tick_params(axis='y', labelcolor='tab:blue')
    ax1.set_title('Tempo de Execução por Iteração')
    ax1.grid(True, alpha=0.3)
    
    # Gráfico 2 - Memória
    ax2.plot(entradas, memorias, marker='s', color='tab:red', label='Memória')
    ax2.set_xlabel('# de Entradas')
    ax2.set_xticks(entradas)
    ax2.set_ylabel('Memória (KB)', color='tab:red')
    ax2.tick_params(axis='y', labelcolor='tab:red')
    ax2.set_title('Memória Utilizada por Iteração')
    ax2.grid(True, alpha=0.3)
    
    # Gráfico 3 - Desvio Padrão
    ax3.plot(entradas, desvios_padroes, marker='^', color='tab:green', label='Desvio Padrão')
    ax3.set_xlabel('Entradas')
    ax3.set_xticks(entradas)
    ax3.set_ylabel('Desvio Padrão (horas)', color='tab:green')
    ax3.tick_params(axis='y', labelcolor='tab:green')
    ax3.set_title('Desvio Padrão das Horas por Iteração')
    ax3.grid(True, alpha=0.3)
    
    # Gráfico 4 - Recursos Alocados
    ax4.plot(entradas, recursos, marker='8', color='tab:orange', label='Recursos Alocados')
    ax4.set_xlabel('Entradas')
    ax4.set_xticks(entradas)
    ax4.set_ylabel('Recursos Alocados', color='tab:orange')
    ax4.tick_params(axis='y', labelcolor='tab:orange')
    ax4.set_title('Recursos Alocados por Iteração')
    ax4.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    ax4.grid(True, alpha=0.3)
    
    # Título geral
    fig.suptitle(f'Análise de Performance do Algoritmo Greedy {modo}', fontsize=16)
    
    # Ajustar layout
    plt.tight_layout()
    plt.show()
