#include <iostream>
#include <stdlib.h>
#include <chrono>
#include "utils.h"

#define MAX_HORARIOS 1000

int main(){
    FILE* arquivo = fopen("./entries/Aula1000.txt", "r");

    if(arquivo == NULL){
        perror("Erro ao abrir o arquivo");
        return 1;
    }

    Horario horarios[MAX_HORARIOS];
    ler_arquivo(horarios, arquivo, MAX_HORARIOS);
    quick_sort(horarios, 0, MAX_HORARIOS - 1);

    vector<float> tempoMedio;
    vector<int> recursosMedio;
    vector<float> dpMedio;

    float tempoLocal = 0;

    for(int i = 0; i < 6; i++){
        auto tempo_inicio = std::chrono::high_resolution_clock::now();

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

        auto tempo_fim = std::chrono::high_resolution_clock::now();

        if(i != 0){
            std::chrono::duration<double> duracao = tempo_fim - tempo_inicio;
            tempoLocal += duracao.count();
        }

        if(i == 5){
            tempoLocal /= 5;
            tempoMedio.push_back(tempoLocal);
            std::cout << "Tempo Local: " << tempoLocal << "s" << std::endl;
            tempoLocal = 0;
        }

        for(Recurso recurso : recursos){
            std::cout << "Recurso: [";
            for(Horario horario : recurso.horarios){
                std::cout << "(" << horario.inicio << ", " << horario.fim << "), ";
            }
            std::cout << "]" << std::endl;
        }

    }
    return 0;
}