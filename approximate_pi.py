#!/usr/bin/env python3
"""
Calcule pi en créant des points aléatoires dans [0,1]² et en vérifiant s'ils
sont dans le cercle ((0,0),1). Exporte les résultats en images ppm.
"""
import os
from modules import arg_parse
from modules import better_io
from ppm import Image
import simulation as sim

def check_dirs(chemin):
    """Vérifie si les dirs dans le chemin existent et les créent sinon"""
    done = ''
    for directory in chemin.split('/')[:-1]:
        done += directory + '/'
        if not os.path.isdir(done):
            if not os.path.exists(done):
                os.mkdir(done)
            else:
                raise OSError(f"'{done}' exists and is not a directory")



def main():
    """Fais une simulation"""

    # Parse l'argument et affiche une erreur et une aide s'il y a un problème
    parsed_args = arg_parse.Parser(arguments = [
        {'name':'size', 'req':True, 'type':arg_parse.positive_int,
         'descr':["La taille des images"]},
        {'name':'nb_points', 'type':arg_parse.positive_int,
         'descr':["Le nombre de points aléatoires à placer"]},
        {'name':'nb_chiffres', 'type':arg_parse.positive_int,
         'descr':["Le nombre de chiffres après la virgule de l'estimation de "
                 +"pi à afficher"]}
    ],
    options = [
        {'name':'o', 'default':'results/', 'args':[{'name':'file'}],
         'descr':["Le nom de base des fichiers où les images seront déposées.",
                  "Peut contenir des dossiers. Si le les dossiers n'existent",
                  "pas, les créent.", "Défault : results/"]}
    ],
    descr = "Calcule pi en créant nb_points points aléatoires dans [0,1]².")
    nombre_de_points = parsed_args.arguments['nb_points']
    image = Image([parsed_args.arguments['size']]*2)

    #print(parsed_args.options, parsed_args.arguments)

    prefix = parsed_args.options['o'][0]
    check_dirs(prefix)

    # Lance la simulation
    compteur = 0
    progress_bar = better_io.Progress(nombre_de_points,
        pre_text = 'Génération des points: ')
    for i in range(nombre_de_points):
        point = sim.new_point()
        dans_unite = sim.est_dans_unite(point)
        compteur += dans_unite
        image.set_point(point, 1 + dans_unite)
        progress_bar.set(i)
    progress_bar.set(nombre_de_points)
    progress_bar.stop(clean = False)
    image.export_bin(prefix+'0.ppm', progress = True)

if __name__ == "__main__":
    main()
