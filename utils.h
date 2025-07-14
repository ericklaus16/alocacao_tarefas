#include <iostream>
#include <stdlib.h>
#include <vector>

using namespace std;

typedef struct {
    int inicio;
    int fim;
} Horario;

typedef struct {
    vector<Horario> horarios;
} Recurso;

void quick_sort(Horario* horarios, int left, int right){
    int i, j;
    Horario pivo, temp;

    if (left >= right) return; // Condição de parada

    i = left;
    j = right;

    pivo = horarios[(left + right) / 2];

    while(i <= j){
        while(horarios[i].inicio < pivo.inicio && i < right) 
            i++;

        while(horarios[j].inicio > pivo.inicio && j > left) 
            j--;

        if(i <= j){
            temp = horarios[i];
            horarios[i] = horarios[j];
            horarios[j] = temp;
            i++;
            j--;
        }
    }

    if(j > left){
        quick_sort(horarios, left, j);
    }

    if(i < right){
        quick_sort(horarios, i, right);
    }
}

void ler_arquivo(Horario* horarios, FILE* arquivo, int MAX_HORARIOS){
    for(int i = 0; i < MAX_HORARIOS; i++){
        if (fscanf(arquivo, "%d", &horarios[i].inicio) != 1) {
            fprintf(stderr, "Erro ao ler o início do horário %d\n", i);
            fclose(arquivo);
            return;
        }
    }

    for (int i = 0; i < MAX_HORARIOS; i++) {
        if (fscanf(arquivo, "%d", &horarios[i].fim) != 1) {
            fprintf(stderr, "Erro ao ler o fim do horário %d\n", i);
            fclose(arquivo);
            return;
        }
    }

    fclose(arquivo);
}

int temRecursoDisponivel(vector<Recurso> recursos, Horario horario){
    int idx = 0;
    for(Recurso recurso : recursos){
        bool conflito = false;

        for(Horario horario_ocupado : recurso.horarios){
            if(!(horario.fim <= horario_ocupado.inicio || horario.inicio >= horario_ocupado.fim)){
                conflito = true;
                break;
            }
        }

        if(!conflito){
            return idx;
        }

        idx++;
    }

    return -1;
}