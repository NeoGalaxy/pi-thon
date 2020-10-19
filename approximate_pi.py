#!/usr/bin/env python3
"""
Calcule pi en créant des points aléatoires dans [0,1]² et en vérifiant s'ils
sont dans le cercle ((0,0),1). Exporte les résultats en images ppm.
"""
import os
import subprocess
from modules import arg_parse
from modules import better_io
from ppm import Image
import simulation as sim


def check_dirs(path):
    """
    Vérifie que les dossiers dans le chemin path existent.
    Les créent si besoin.
    Lance un 'OSError' si un dossier ne peut être créé.
    path doit être de la forme 'chemin/vers/le/ficher', et tous les
    noms suivis d'un '/' seront considérés tels des dossiers.
    Fonctionne avec les chemins relatifs et absolus.
    """
    done = '' # La partie du chemin lue
    for directory in path.split('/')[:-1]: # On itère à travers
        done += directory + '/'
        if not os.path.isdir(done):
            if not os.path.exists(done):
                os.mkdir(done)
            else:
                raise OSError(f"'{done}' exists and is not a directory")

def get_args():
    """
    Utilise le module arg_parse pour parser les arguments en ligne de commande.
    Les arguments obligatoires sont :
      size_image (la taille des images)
      nb_points (le nombre de points à placer)
      nb_chiffres (le nombre de chiffres de pi)
    Les options sont :
      -o <chemin> (le préfixe des images à générer)
      -v <nombre> (le niveau de verbose du programme)
      -fps <nombre> (le nombre de print par secondes des barres de progression)
    """
    # Parse l'argument et affiche une erreur et une aide s'il y a un problème
    parsed_args = arg_parse.Parser(arguments=[
        {'name': 'size_image', 'type': arg_parse.positive_int,
         'descr': ["La taille des images"]},
        {'name': 'nb_points', 'type': arg_parse.positive_int,
         'descr': ["Le nombre de points aléatoires à placer"]},
        {'name': 'nb_chiffres', 'type': arg_parse.positive_int,
         'descr': ["Le nombre de chiffres après la virgule de l'estimation de "
                   + "pi à afficher"]}
    ], options=[
        {'name': 'o', 'default': ['img'], 'args':[{'name': 'file'}],
         'descr': [
            "Le préfixe des images à créer.",
            "Peut contenir des dossiers et/ou le début du nom des fichiers.",
            "Si le les dossiers sur le chemin n'existent pas, les créent.",
            "Défault : img (afin de pouvoir respecter les consignes)"
        ]},
        {'name': 'v', 'default': [2], 'args':[
            {'name': 'level', 'type': arg_parse.non_neg_int}],
         'descr': ["Le niveau de verbose du programme."
                                      " Permet de savoir le programme en est.",
                   "0 -> rien",
                   "1 -> Affichage de la progression de la "
                                                        "génération de points",
                   "2 -> Affichage de la progression des générations d'images",
                   "3 -> Affichages de niveau débug.",
                   "Une verbose de 0 améliore légèrement l'exécution.",
                   "Note : L'implémentation des niveaux 1 et 2 utilise des "
                                                                    "threads,",
                   "       limitant l'impact de l'affichage sur les "
                                                               "performances.",
                   "Défault : 2"]},
        {'name': 'fps', 'default': [60],
         'args':[{'name': 'freq', 'type': arg_parse.positive_float}],
            'descr': [
            "Le nombre de mise à jour des barres de progressions par secondes.",
            "Grâce à une implémentation par threading, ce paramètre a un",
            "impact minime sur les performances.",
            "Défault : 60"
        ]},
        {'name': 'h', "effect": arg_parse.disp_help,
         'descr': ["Affiche cette aide"]}
    ], descr="Calcule pi en créant nb_points points aléatoires dans [0,1]².")
    return (parsed_args.arguments, parsed_args.options)

def simulation(image, args, images_prefix, verbose, fps):
    """
    Lance la simulation, et génère les images.
    Affiche des barres de progression en fonction du niveau de verbose.
    """
    compteur = 0
    progression = 0
    image_names = []
    if verbose > 1:
        print()
    if verbose > 0:
        print()
        better_io.set_cursor(0)
        progress_bar = better_io.Progress(args['nb_points'],
            line=1, pre_text='Génération des points: ', fps=fps)

    reste = args['nb_points'] % 10
    for numero_image in range(10):
        for _ in range(reste + args['nb_points']//10):
            point = sim.new_point()
            dans_unite = point[0]*point[0] + point[1]*point[1] < 1#sim.est_dans_unite(point)
            compteur += dans_unite
            image.set_point(point, 1 + dans_unite)
            progression += 1
            if verbose > 0:
                progress_bar.memory = progression
        reste = 0
        estim_pi = f"{4*compteur/progression:.{args['nb_chiffres']}f}"

        if verbose > 1:
            progress_bar.disp()
        image_names.append(images_prefix +
            str(numero_image) + '_' + estim_pi.replace('.', '-') + '.ppm')
        image.text(estim_pi, (0,0), 2, group = 3, overlay = True)
        image.export_bin(image_names[-1], fps=fps,
                         progress=verbose > 1, line=2, clean_progress=False,
                         pre_text=f'Génération image {numero_image}: ')
        image.clean_overlay()
    if verbose > 0:
        progress_bar.set(args['nb_points'])
        progress_bar.stop(clean=False)
    return image_names



def main():
    """
    Programme principal.
    Parse les arguments, lance la simulation et crée le gif
    """

    args, options = get_args() # On récupère les arguments

    # Récupération de certains arguments
    image = Image([args['size_image']]*2)
    images_prefix = options['o'][0]
    verbose = options['v'][0]

    # vérifiaction du chemin des images
    check_dirs(images_prefix)

    # Lance la simulation et récupère le chemin des images générées
    image_names = simulation(image, args, images_prefix, verbose,
                             options['fps'][0])

    # Génération du gif
    if verbose > 0:
        print(f"Génération du gif '{images_prefix+'simulation.gif'}'...")
    cmd = ['convert', '-delay', '100', '-loop', '0']+image_names \
        + [images_prefix+'.gif']
    if verbose > 2:
        print('> Lancement de la commande', cmd)
    ret = subprocess.call(cmd)
    if verbose > 2:
        print('> Retour :', ret)
    if verbose > 0:
        print("Gif généré.")


if __name__ == "__main__":
    main()
