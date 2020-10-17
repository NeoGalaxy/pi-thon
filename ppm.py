"""
Module qui gère les images PPM
"""
#import time
from modules import better_io

DOWN = True
RIGHT = False

FONT1 = {
    'dimensions' : (2,7),
    'width' : (0.6),
    'space' : (1),
    '1' : [(1,-3.5,7,DOWN)],
    '2' : [(-1,-3.5,2,RIGHT),(1,-3.5,3.5,DOWN),(-1,0,2,RIGHT),(-1,0,3.5,DOWN),
           (-1,3.5,2,RIGHT)],
    '3' : [(-1,-3.5,2,RIGHT),(-1,0,2,RIGHT),(-1,3.5,2,RIGHT),(1,-3.5,7,DOWN)],
    '4' : [(-1,-3.5,3.5,DOWN),(-1,0,2,RIGHT),(1,-3.5,7,DOWN)],
    '5' : [(-1,-3.5,2,RIGHT),(-1,-3.5,3.5,DOWN),(-1,0,2,RIGHT),(1,0,3.5,DOWN),
           (-1,3.5,2,RIGHT)],
    '6' : [(-1,-3.5,2,RIGHT),(-1,-3.5,3.5,DOWN),(-1,0,2,RIGHT),(1,0,3.5,DOWN),
           (-1,3.5,2,RIGHT),(-1,0,3.5,DOWN)],
    '7' : [(-1,-3.5,2,RIGHT),(1,-3.5,7,DOWN)],
    '8' : [(-1,-3.5,7,DOWN),(-1,-3.5,2,RIGHT),(-1,0,2,RIGHT),
           (-1,3.5,2,RIGHT),(1,-3.5,7,DOWN)],
    '9' : [(-1,-3.5,3.5,DOWN),(-1,-3.5,2,RIGHT),(-1,0,2,RIGHT),
           (-1,3.5,2,RIGHT),(1,-3.5,7,DOWN)],
    '0' : [(-1,-3.5,7,DOWN),(-1,-3.5,2,RIGHT),(-1,3.5,2,RIGHT),(1,-3.5,7,DOWN)],
    '.' : [(-1,3.5,0,DOWN)]
}

class Image:
    """Classe créant et gérant une image"""
    def __init__(self, dimensions, colors = None):
        (width, height) = dimensions
        self.dimensions = (width, height)
        self.picture = [[0]*width for _ in range(height)]
        self.overlay = [[0]*width for _ in range(height)]
        self.groups_color = colors or [(255,255,255), (255,255,0), (0,0,255),
                                       (0,0,0)]
        self.closed = False

    def clean_overlay(self):
        """Cleans the overlay"""
        width, height = self.dimensions
        self.overlay = [[0]*width for _ in range(height)]

    def set_pixel(self, coords, group = 1, overlay = False):
        """Set given color to the given pixel (x,y),
        x from the top and y form the left"""
        if overlay:
            self.overlay[coords[0]][coords[1]] = group
        else:
            self.picture[coords[0]][coords[1]] = group

    def set_point(self, point, group = 1, overlay = False):
        """Set given color to the given coordinates (x,y)"""
        width, height = self.dimensions
        coords = (int(height*(point[1]+1)/2), int(width*(point[0]+1)/2))
        self.set_pixel(coords, group, overlay)

    def draw_pixel_line(self, pt_depart, length, line_width, is_downwards,
                        *args, **kargs):
        """Affiche une ligne dans l'image"""
        width,height = self.dimensions
        for coord_length in range(-(line_width//2), length+line_width-(line_width//2)):
            for coord_width in range(-(line_width//2),line_width-(line_width//2)):
                if is_downwards:
                    pt_courant = (pt_depart[0]+coord_length,
                                  pt_depart[1]+coord_width)
                else :
                    pt_courant = (pt_depart[0]+coord_width,
                                  pt_depart[1]+coord_length)
                if (0 <= pt_courant[0] < height and 0 <= pt_courant[1] < width):
                    self.set_pixel(pt_courant, *args, **kargs)

    def draw_line(self, pt_depart, length, line_width, is_downwards,
                  *args, **kargs):
        """Affiche une ligne dans l'image"""
        width, height = self.dimensions
        coords = (int(height*(pt_depart[1]+1)/2), int(width*(pt_depart[0]+1)/2))
        if is_downwards:
            length = int(height*length/2)
            line_width = int(width*line_width/2)
        else:
            length = int(width*length/2)
            line_width = int(height*line_width/2)
        self.draw_pixel_line(coords, length, line_width, is_downwards, *args, **kargs)

    def text(self, text, coords, size, *args, **kargs):
        """Affiche une ligne dans l'image"""
        size = size/100
        for index, letter in enumerate(text):
            letter_center = (
                coords[0] + size*(FONT1["dimensions"][0]+FONT1['space'])*(index-len(text)/2),
                coords[1])
            for param in FONT1[letter]:
                self.draw_line((letter_center[0] + param[0]*size,
                    letter_center[1] + param[1]*size), param[2]*size, FONT1['width']*size,
                    param[3], *args, **kargs)

    def export(self, path, color_res = 1):
        """write designated points into the file"""
        width, height = self.dimensions
        header = f"P3\n{width} {height}\n{color_res}\n"
        file = open(path, 'w',
            buffering = 100 + 12 * width * height + len(header))
        file.write(header)
        color_modif = color_res/255
        str_groups = [
                    ' '.join(str(int(0.5 + color * color_modif))
                            for color in grp)
                    for grp in self.groups_color]

        for line in self.picture:
            for pix in line:
                file.write(str_groups[pix] + ' ')
        file.close()

    def export_bin(self, path, progress=False, clean_progress=True, **kargs):
        """write designated points into the file"""
        width, height = self.dimensions
        header = (f"P6\n{width} {height} 255 ").encode('ASCII')
        file = open(path, 'wb', buffering = 100 + width * height + len(header))
        file.write(header)
        if progress:
            progress_bar = better_io.Progress(width * height, **kargs)
        index = 0
        for line_index in range(len(self.picture)):
            for pix_index in range(len(self.picture[line_index])):
                pix = self.overlay[line_index][pix_index]
                if pix == 0:
                    pix = self.picture[line_index][pix_index]
                file.write(bytes(self.groups_color[pix]))
                index += 1
                if progress:
                    progress_bar.memory = index
        if progress:
            progress_bar.stop(clean_progress)
        file.close()
        if progress:
            return progress_bar
        return None

if __name__ == '__main__':
    img = Image((800,800))
    img.text('123456789.0',(0,0),2, group = 2, overlay = True)
    img.draw_line((-1,0),1.9, 0.1, False, group = 1)
    img.export_bin('img.ppm', progress=True)
