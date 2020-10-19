#!/usr/bin/env python3
"""
Calcule pi en créant des points aléatoires dans ]-1,1[² et en vérifiant s'ils
sont dans le cercle de centre (0,0) et de rayon 1.
"""
from random import random

from modules import arg_parse
from modules import better_io

def new_point():
    """
    Renvoie un point aléatoire dans l'espace ]-1,1[²
    """
    return (2 * random() - 1, 2 * random() - 1)

def est_dans_unite(point):
    """
    Indique si la distance entre point et l'origine est
    inférieure ou égale à 1.
    """
    return point[0]*point[0] + point[1]*point[1] < 1

def main():
    """
    Fait la simulation.
    """

    # Parse les arguments et affiche une erreur ou une aide si besoin
    parsed_args = arg_parse.Parser(arguments = [
        {'name':'nb_points', 'req':True, 'type':arg_parse.positive_int,
         'descr':["Le nombre de points aléatoires à placer"]}
    ],
    options = [
        {'name':'h', 'descr':["Affiche cette aide"],
         'effect':arg_parse.disp_help},
        {'name':'no-prog', 'descr':['Désactive la barre de progression']}
    ],
    descr = "Calcule pi en créant nb_points points aléatoires dans [0,1]².")
    # Récupération des arguments
    nombre_de_points = parsed_args.arguments['nb_points']
    has_progress = 'no-prog' not in parsed_args.options

    # Lance la simulation
    compteur = 0
    if has_progress:
        progress_bar = better_io.Progress(nombre_de_points,
            pre_text='Génération des points : ', fps=60)

    for index_val in range(0, nombre_de_points) :
        compteur += est_dans_unite(new_point())
        if has_progress:
            progress_bar.set(index_val)

    if has_progress:
        progress_bar.stop()
    print(f'Compteur : {compteur}')
    print(f'Estimation de pi/4 : {compteur/nombre_de_points}')
    print(f'Estimation de pi : {4*compteur/nombre_de_points}')

if __name__ == "__main__":
    main()
