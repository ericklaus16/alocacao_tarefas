#include <iostream>
#include <stdlib.h>
#include <chrono>
#include "utils.h"

#define MAX_HORARIOS 250000

int main(){
    FILE* arquivo = fopen("./entries/Aula250000.txt", "r");

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
    int recursoLocal = 0;
    float dpLocal = 0;

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
            auto duracao_mili = std::chrono::duration_cast<std::chrono::milliseconds>(tempo_fim - tempo_inicio);
            // double duracao_segundos = duracao_micro.count() / 250000000.0;
            tempoLocal += duracao_mili.count();

            recursoLocal += recursos.size();
            dpLocal += desvioPadraoPopulacional(recursos);
        }

        if(i == 5){
            tempoLocal /= 5;
            tempoMedio.push_back(tempoLocal);

            recursoLocal /= 5;
            recursosMedio.push_back(recursoLocal);

            dpLocal /= 5;
            dpMedio.push_back(dpLocal);

            std::cout << "Tempo Local " << MAX_HORARIOS << ": " << tempoLocal << " milisegundos" << std::endl;
            std::cout << "Recurso Local " << MAX_HORARIOS << ": " << recursoLocal << std::endl;
            std::cout << "Desvio Padrao Local " << MAX_HORARIOS << ": " << dpLocal << std::endl;
            tempoLocal = 0;
        }
    }
    return 0;
}