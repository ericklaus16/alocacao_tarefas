#include <iostream>
#include <stdlib.h>
#include <cmath>
#include <numeric>
#include <vector>

using namespace std;

typedef struct {
    int inicio;
    int fim;
} Horario;

typedef struct {
    vector<Horario> horarios;
} Recurso;

void quick_sort(vector<Horario>& horarios, int left, int right){
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

void ler_arquivo(vector<Horario>& horarios, FILE* arquivo, int MAX_HORARIOS){
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

int temRecursoDisponivel(const vector<Recurso>& recursos, const Horario& horario){
    for(size_t idx = 0; idx < recursos.size(); idx++){
        bool conflito = false;
        const auto& recurso_horarios = recursos[idx].horarios;

        if(recurso_horarios.empty()){
            return idx;
        }

        for(const auto& horario_ocupado : recurso_horarios){
            if(!(horario.fim <= horario_ocupado.inicio || horario.inicio >= horario_ocupado.fim)){
                conflito = true;
                break; 
            }
        }

        if(!conflito){
            return idx;
        }
    }
    return -1;
}

double desvioPadraoPopulacional(const std::vector<Recurso>& recursos) {
    if (recursos.empty()) {
        return 0.0; // Retorna 0 para evitar divisão por zero se o vetor estiver vazio
    }

    // Passo 1: Calcular as horas totais de cada recurso
    std::vector<double> horas_por_recurso;
    for (const auto& recurso : recursos) {
        double horas_total = 0.0;
        for (const auto& horario : recurso.horarios) {
            horas_total += (horario.fim - horario.inicio);
        }
        horas_por_recurso.push_back(horas_total);
    }

    // Passo 2: Calcular a média das horas
    double sum = std::accumulate(horas_por_recurso.begin(), horas_por_recurso.end(), 0.0);
    double mean = sum / horas_por_recurso.size();

    // Passo 3: Calcular a soma dos quadrados das diferenças em relação à média
    double sq_sum = 0.0;
    for (const auto& horas : horas_por_recurso) {
        sq_sum += (horas - mean) * (horas - mean);
    }

    // Passo 4: Calcular a variância
    double variance = sq_sum / horas_por_recurso.size();

    // Passo 5: Calcular o desvio padrão (raiz quadrada da variância)
    double std_dev = std::sqrt(variance);

    return std_dev;
}