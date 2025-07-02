caminho_arq = "entrada.txt"

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

def temRecursoDisponivel(inicio, fim):
    recursos_disponiveis = {} # Armazena as salas disponíveis
    
    print(f"  Testando {len(escalonamento)} recursos existentes...")
    
    for idx, recurso in enumerate(escalonamento):
        conflito = False

        for ocupado_inicio, ocupado_fim in recurso:
            # Duas aulas conflitam se há sobreposição no tempo
            # NÃO conflitam se: nova termina antes/quando existente começa OU nova começa depois/quando existente termina
            if not (fim <= ocupado_inicio or inicio >= ocupado_fim):
                conflito = True
                break
                
        if not conflito:
            tempo_total = 0
            for ocupado_inicio, ocupado_fim in recurso:
                tempo_total += ocupado_fim - ocupado_inicio
                
            recursos_disponiveis[idx] = tempo_total # Armazena o tempo total ocupado por esta sala
            
            print(f"Sala {idx+1} DISPONÍVEL para aula ({inicio},{fim})")
        # else:
        #     print(f"Recurso {idx+1} OCUPADO")
        
    if recursos_disponiveis:
        melhor_recurso = min(recursos_disponiveis, key=recursos_disponiveis.get)
        print(f"  → ESCOLHIDA: Sala {melhor_recurso+1}")
        return melhor_recurso
    else: 
        print(f"  → CRIANDO nova sala!")
        return False

while len(horarios_inicio) != 0:
    primeira = True
    menor = min(horarios_inicio)
    indice = horarios_inicio.index(menor)
    fim_horario = horarios_fim[indice]

    print(f"Analisando aula [{menor}, {fim_horario}]")
    
    recursoDisponivel = temRecursoDisponivel(menor, fim_horario)

    if recursoDisponivel is False:     
        escalonamento.append([(menor, fim_horario)])
    else:
        escalonamento[recursoDisponivel].append((menor, fim_horario))
    
    horarios_inicio.pop(indice)
    horarios_fim.pop(indice)

for i, recurso in enumerate(escalonamento):
    print(f"Sala {i + 1}: {recurso}")