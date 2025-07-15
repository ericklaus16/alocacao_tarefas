#include <iostream>
#include <stdlib.h>
#include <chrono>
#include <string>
#include <vector>
#include "utils.h"

int main(){
    std::vector<int> tamanhos = {10, 25, 50, 100, 150, 200, 300, 500, 750, 1000, 1500, 2000, 2500, 5000, 7500, 10000, 
                                    15000, 20000, 30000, 50000, 75000, 100000, 150000, 250000, 350000, 500000, 750000};
    
    for(int MAX_HORARIOS : tamanhos){
        std::cout << "\n=== Testando com " << MAX_HORARIOS << " horários ===" << std::endl;
        
        std::string nome_arquivo = "./entries/Aula" + std::to_string(MAX_HORARIOS) + ".txt";
        FILE* arquivo = fopen(nome_arquivo.c_str(), "r");

        if(arquivo == NULL){
            std::cout << "Arquivo não encontrado: " << nome_arquivo << std::endl;
            continue; 
        }

        vector<Horario> horarios(MAX_HORARIOS);
        ler_arquivo(horarios, arquivo, MAX_HORARIOS);
        quick_sort(horarios, 0, MAX_HORARIOS - 1);

        float tempoLocal = 0;
        int recursoLocal = 0;
        float dpLocal = 0;

        for(int i = 0; i < 6; i++){
            auto tempo_inicio = std::chrono::high_resolution_clock::now();

            int contador_horarios = 0;
            vector<Recurso> recursos;

            while(contador_horarios != MAX_HORARIOS){
                Horario menor = horarios[contador_horarios];

                int recursoDisponivel = temRecursoDisponivelBalanceado(recursos, menor);
            
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
                tempoLocal += duracao_mili.count();
                recursoLocal += recursos.size();
                dpLocal += desvioPadraoPopulacional(recursos);
            }
        }

        tempoLocal /= 5;
        recursoLocal /= 5;
        dpLocal /= 5;

        std::cout << "Tempo Local " << MAX_HORARIOS << ": " << tempoLocal << " milisegundos" << std::endl;
        std::cout << "Recurso Local " << MAX_HORARIOS << ": " << recursoLocal << std::endl;
        std::cout << "Desvio Padrao Local " << MAX_HORARIOS << ": " << dpLocal << std::endl;
    }
    
    return 0;
}