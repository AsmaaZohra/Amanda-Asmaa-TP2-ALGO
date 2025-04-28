#include "MinCostRechargeCalculator.h"
#include <vector>
#include <math.h>
#include <iostream>
#include <algorithm> // for std::min

// Nom(s) étudiant(s) / Name(s) of student(s): Amanda Dorval et Asmaa Skou

// ce fichier contient les definitions des methodes de la classe MinCostRechargeCalculator
// this file contains the definitions of the methods of the MinCostRechargeCalculator class

using namespace std;

MinCostRechargeCalculator::MinCostRechargeCalculator() {
}

int MinCostRechargeCalculator::CalculateMinCostRecharge(const vector<int>& RechargeCost) {
    int n = RechargeCost.size(); // nombre de bornes par lequel le camion va passer
    vector<int> tabProgDyn(n + 2, INT_MAX); // tabProgDyn[i] qui prend le cout min à la position i

    // cas de base (départ du camion quand n=0 et coût borne=0)
    tabProgDyn[0] = 0;

    // cas de récurrence (parcourir les bornes 1 à n et trajet du camion (n+1))
    for (int i = 1; i <= n + 1; i++) {

        // on vérifie les 3 positions avant soit j = i-1, j = 1-2, j = i-3
        for (int j = 1; j <= 3 && i - j >= 0; j++) {

            // si tabProgDyn[i-j] on peut y accéder alors pas besoin de la valeur maximale
            if (tabProgDyn[i - j] != INT_MAX) {

                // si i est le trajet du camion soit i == n+1 donc pas de recharge à faire
                if (i == n + 1) {
                    tabProgDyn[i] = min(tabProgDyn[i], tabProgDyn[i - j]);
                } else {

                    // sinon si i est pas le trajet on va ajouter le cout de la borne i-1
                    tabProgDyn[i] = min(tabProgDyn[i], tabProgDyn[i - j] + RechargeCost[i - 1]);
                }
            }
        }
    }

    // retourne le coût minimal pour faire le trajet complet
    return tabProgDyn[n + 1];
}







