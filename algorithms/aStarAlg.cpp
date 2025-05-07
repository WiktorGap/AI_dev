#include <iostream>
#include <vector>
#include <stack>
#include <map>
#include <set>
#include <string>
#include <tuple>
#include <algorithm>
#include <climits>

using namespace std;

int main() {

    using stackData = tuple<string, int>;
    stack<stackData> s;
    int valDestination = -1;  
    int valLocalState;
    stackData start = make_tuple("BMW", 0);
    stackData actualState;
    set<string> visited;
    string checkVal;

    s.push(start);

    pair<int, map<string, int>> subVals;

    map<string, pair<int, map<string, int>>> graph = {
        {"Toyota", {0, {{"Silnik V4", 4}, {"Hamulce", 3}, {"Skrzynia biegów manualna", 2}}}},
        {"Audi", {1, {{"Silnik V6", 5}, {"Hamulce sportowe", 4}, {"Skrzynia biegów DSG", 4}}}},
        {"BMW", {2, {{"Silnik V6 Twin Turbo", 6}, {"Hamulce M Performance", 5}, {"Skrzynia automatyczna", 5}}}},
        {"Aston Martin", {3, {{"Silnik V8", 7}, {"Hamulce ceramiczne", 6}, {"Skrzynia biegów Tiptronic", 6}}}}
    };

    cout << "Przeglądanie modeli:\n";
    while (!s.empty()) {
        actualState = s.top();
        checkVal = get<0>(actualState);
        s.pop();

        if (visited.find(checkVal) == visited.end()) {
            visited.insert(checkVal);
            valLocalState = get<1>(actualState);

            subVals = graph[checkVal];
            int suma = subVals.first; 
            for (const auto& item : subVals.second) {
                suma += item.second;
            }
            
            cout << "Model: " << checkVal << "\n";
            cout << "  - Wartość bazowa: " << subVals.first << "\n";
            cout << "  - Suma części: " << suma - subVals.first << "\n";
            cout << "  - Łączna wartość: " << suma << "\n\n";
        }
    }


    map<string, int> sumaModeli;
    for (const auto& entry : graph) {
        int suma = entry.second.first;
        for (const auto& part : entry.second.second) {
            suma += part.second;
        }
        sumaModeli[entry.first] = suma;
    }

    map<string, int> konfiguracja;
    int total = 0;
    char wybor;
    
    cout << "\nTworzenie własnej konfiguracji:\n";
    do {
        string nazwa;
        int wartosc;
        
        cout << "Podaj nazwę części: ";
        cin >> nazwa;
        cout << "Podaj wartość części: ";
        cin >> wartosc;
        
        konfiguracja[nazwa] = wartosc;
        total += wartosc;
        
        cout << "Dodać kolejną część? (t/n): ";
        cin >> wybor;
    } while(tolower(wybor) == 't');

    string najlepszy;
    int min_roznica = INT_MAX;
    
    for (const auto& model : sumaModeli) {
        int roznica = abs(model.second - total);
        if (roznica < min_roznica) {
            min_roznica = roznica;
            najlepszy = model.first;
        }
    }

    cout << "\nTwoja konfiguracja: " << total << " punktów\n";
    cout << "Najlepsze dopasowanie: " << najlepszy 
         << " (" << sumaModeli[najlepszy] << " punktów)\n";

    int dolna, gorna;
    cout << "\nPodaj zakres poszukiwań (np. 10 20): ";
    cin >> dolna >> gorna;
    
    cout << "Modele w zakresie " << dolna << "-" << gorna << ":\n";
    for (const auto& model : sumaModeli) {
        if (model.second >= dolna && model.second <= gorna) {
            cout << "  - " << model.first << ": " << model.second << "\n";
        }
    }

    return 0;
}