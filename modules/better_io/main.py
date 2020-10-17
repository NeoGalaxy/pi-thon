"""
Module d'affichage de la progression
"""
import os
import sys
import time
import threading
#from multiprocessing import shared_memory

def get_cols():
    """Gives the number of columns in the terminal"""
    try:
        size = os.get_terminal_size()
        return size.columns
    except OSError:
        return 80

def get_lines():
    """Gives the number of lines in the terminal"""
    try:
        size = os.get_terminal_size()
        return size.lines
    except OSError:
        return 40

class Progress:
    """Creates a progressbar using a fork not to impact perfs"""
    def __init__(self, end, pre_text = 'Loading : ', fps = 10, line = 0):
        # La valeur à affucher
        self.memory = 0
        # Si la progression est terminée
        self.finished = False
        # La ligne sur laquelle afficher
        self.line = line
        # La borne superieure
        self.end = end
        # Le texte avant la barre
        self.pre_text = pre_text
        # Le fork, permettant de tourner deux codes en parallèle
        def child():
            sleeptime = 1/fps
            while not self.finished:
                self.disp()
                time.sleep(sleeptime)
            sys.exit(0)
        thr = threading.Thread(target = child)
        thr.start()

    def monter(self, nb_lignes = 1):
        """Monte la barre de nb_lignes"""
        self.line += nb_lignes

    def descendre(self, nb_lignes = 1):
        """Descend la barre de nb_lignes"""
        self.line -= nb_lignes

    def set(self, val):
        """Sets the progress bar"""
        self.memory = val

    def stop(self, clean = True):
        """Stops the progress bar and kills the fork"""
        self.finished = True
        self.memory = self.end
        if clean:
            disp_clean(self.line)
        else:
            self.disp()

    def disp(self):
        """Stops the progress bar and kills the fork"""
        disp_progress(self.memory, self.end,
            self.line, pre_text = self.pre_text)

def disp_progress(index, total, line_nb, pre_text = ''):
    """Affiche une barre de progression"""
    text = str(index) + '/' + str(total)
    width = get_cols() - 2 - len(text) - len(pre_text)
    progress_val = int(width * index / total)
    height = get_lines()
    print(f'\033[s\033[{height - line_nb};0f'+pre_text + '['+'#'*progress_val
          +' '*(width - progress_val) + ']' + text, end = f'\033[u\r')

def disp_clean(line = 0):
    """Affiche une barre de progression"""
    print(f'\033[s\033[{get_lines() - line};0f\033[K\033[u', end = '\r')

if __name__ == '__main__':
    print()
    print()
    p1 = Progress(1000, 'P1 : ', 10, 0)
    p2 = Progress(1000, 'P2 : ', 10, 1)
    for _ in range(10):
        p1.memory += 100
        p2.memory += 5
        time.sleep(0.1)
    p2.stop()
    p1.stop()
