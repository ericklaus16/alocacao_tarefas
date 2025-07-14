#include <iostream>
#include <stdlib.h>
#include "utils.h"

#define MAX_HORARIOS 10

int main(){
    FILE* arquivo = fopen("./entries/Aula10.txt", "r");

    if(arquivo == NULL){
        perror("Erro ao abrir o arquivo");
        return 1;
    }

    Horario horarios[MAX_HORARIOS];
    ler_arquivo(horarios, arquivo, MAX_HORARIOS);
    quick_sort(horarios, 0, MAX_HORARIOS - 1);

    printf("Horarios lidos:\n");
    for (int i = 0; i < MAX_HORARIOS; i++) {
        printf("Horario[%d]: Inicio = %d, Fim = %d\n", 
               i, horarios[i].inicio, horarios[i].fim);
    }

    int contador_horarios = 0;
    vector<Recurso> recursos;

    while(contador_horarios != MAX_HORARIOS){
        Horario menor = horarios[contador_horarios];

        int recursoDisponivel = temRecursoDisponivel(recursos, menor);
    
        if(recursoDisponivel == -1){
            Recurso recurso;
            recurso.horarios.push_back(menor);
            recursos.push_back(recurso);
        } else {
            recursos[recursoDisponivel].horarios.push_back(menor);
        }

        contador_horarios++;
    }

    for(Recurso recurso : recursos){
        std::cout << "Recurso: [";
        for(Horario horario : recurso.horarios){
            std::cout << "(" << horario.inicio << ", " << horario.fim << "), ";
        }
        std::cout << "]" << std::endl;
    }
    return 0;
}