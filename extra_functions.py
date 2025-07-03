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