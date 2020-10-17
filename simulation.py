#!/usr/bin/env python3
"""
Calcule pi en créant des points aléatoires dans [0,1]² et en vérifiant s'ils
sont dans le cercle ((0,0),1).
"""
from random import random

from modules import arg_parse
from modules import better_io

def new_point():
    """Renvoie un point aléatoire"""
    return (2 * random() - 1, 2 * random() - 1)

def est_dans_unite(point):
    """Indique si la distance entre point et l'origine est
    inférieure ou égale à 1."""
    return point[0]**2 + point[1]** 2 < 1

def main():
    """Fais une simulation"""

    # Parse l'argument et affiche une erreur et une aide s'il y a un problème
    parsed_args = arg_parse.Parser(arguments = [
       {'name':'nb_points', 'req':True, 'type':arg_parse.positive_int,
        'descr':["Le nombre de points aléatoires à placer"]}
    ],
    options = [
        #{'name':'h', 'descr':["Affiche cette aide"]}
    ],
    descr = "Calcule pi en créant nb_points points aléatoires dans [0,1]².")
    nombre_de_points = parsed_args.arguments['nb_points']

    # Lance la simulation
    compteur = 0
    progress_bar = better_io.Progress(nombre_de_points,
        pre_text = 'Génération des points : ')

    for index_val in range(0, nombre_de_points) :
        compteur += est_dans_unite(new_point())
        progress_bar.set(index_val)

    progress_bar.stop()
    print(f'Compteur : {compteur}')
    print(f'Estimation de pi/4 : {compteur/nombre_de_points}')
    print(f'Estimation de pi : {4*compteur/nombre_de_points}')

if __name__ == "__main__":
    main()
