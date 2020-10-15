"""
Module d'affichage de la progression
"""
import os
import sys
import time
from multiprocessing import shared_memory

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
        self.memory = shared_memory.SharedMemory(create=True, size=8)
        # Si la progression est terminée
        self.finished = shared_memory.SharedMemory(create=True, size=1)
        # La ligne sur laquelle afficher
        self.line = shared_memory.SharedMemory(create=True, size=2)
        self.line.buf[0:] = line.to_bytes(2, 'big')
        # Indique si les mémoires partagées sont fermées
        self.closed = False
        # La borne superieure (muable)
        self.end = end
        # Le texte avant la barre
        self.pre_text = pre_text
        # Le fork, permettant de tourner deux codes en parallèle
        if os.fork() != 0:
            # Le programme parent continue son exécution
            return
        # Le programme fils affiche tous les 1/fps la progression
        sleeptime = 1/fps
        while not self.finished.buf[0]:
            self.disp()
            time.sleep(sleeptime)
        self.__close(True)
        sys.exit(0)

    def monter(self, nb_lignes = 1):
        """Monte la barre de nb_lignes"""
        self.line.buf[0:] = (int.from_bytes(self.line.buf,'big')+nb_lignes
                             ).to_bytes(2, 'big')

    def descendre(self, nb_lignes = 1):
        """Descend la barre de nb_lignes"""
        self.line.buf[0:] = (int.from_bytes(self.line.buf,'big')-nb_lignes
                             ).to_bytes(2, 'big')

    def set(self, val):
        """Sets the progress bar"""
        self.memory.buf[0:] = val.to_bytes(8, 'big')

    def stop(self, clean = True):
        """Stops the progress bar and kills the fork"""
        self.finished.buf[0] = True
        if clean:
            disp_clean()
        else :
            self.disp()
            print('\n')
        self.memory.close()
        self.finished.close()
        self.line.close()

    def __close(self, unlink = False):
        """Stops the progress bar and kills the fork"""
        self.stored_memory = self.get_memory()
        self.stored_finished = self.get_finished()
        self.stored_line = self.get_line()
        self.closed = True
        self.memory.close()
        self.finished.close()
        self.line.close()
        if unlink:
            self.memory.unlink()
            self.finished.unlink()
            self.line.unlink()

    def get_memory(self):
        if self.closed:
            return self.stored_memory
        return int.from_bytes(self.memory.buf, 'big')

    def get_finished(self):
        if self.closed:
            return True
        return int.from_bytes(self.finished.buf, 'big')

    def get_line(self):
        if self.closed:
            return self.stored_line
        return int.from_bytes(self.line.buf, 'big')

    def disp(self):
        """Stops the progress bar and kills the fork"""
        disp_progress(int.from_bytes(self.memory.buf, 'big'), self.end,
            int.from_bytes(self.line.buf, 'big'), pre_text = self.pre_text)

def disp_progress(index, total, line_nb, pre_text = ''):
    """Affiche une barre de progression"""
    text = str(index) + '/' + str(total)
    width = get_cols() - 2 - len(text) - len(pre_text)
    progress_val = int(width * index / total)
    print('\r'+pre_text + '['+'#'*progress_val
            +' '*(width - progress_val) + ']' + text, end = '\r')

def disp_clean():
    """Affiche une barre de progression"""
    print('\x1b[0m' + ' '*get_cols(), end = '\r')
