"""
Module qui gère les images PPM
"""
#import time
from modules import better_io

DOWN = True
RIGHT = False

FONT0 = {
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

FONT1 = {
    'dimensions' : (2,7),
    'width' : (0.55),
    'space' : (1),
    '1' : [(0.6,-3.4,6.9,DOWN)],
    '2' : [(-1,-3.5,1.8,RIGHT),(1,-3.3,3.1,DOWN),(-0.8,0,1.6,RIGHT),
           (-1,0.2,3.3,DOWN),(-1,3.5,2,RIGHT)],
    '3' : [(-1,-3.5,1.8,RIGHT),(-0.5,0,1.5,RIGHT),(-1,3.5,1.8,RIGHT),
           (1,-3.3,6.6,DOWN)],
    '4' : [(-1,-3.5,3.3,DOWN),(-.8,0,1.8,RIGHT),(1,-3.4,6.9,DOWN)],
    '5' : [(-1,-3.5,2,RIGHT),(-1,-3.5,3.5,DOWN),(-1,0,1.8,RIGHT),
           (1,0.2,3.1,DOWN),(-1,3.5,1.8,RIGHT)],
    '6' : [(-.8,-3.5,1.6,RIGHT),(-1,-3.3,6.6,DOWN),(-1,0,1.8,RIGHT),
           (1,0.2,3.1,DOWN),(-.8,3.5,1.6,RIGHT)],
    '7' : [(-1,-3.5,1.8,RIGHT),(1,-3.3,6.8,DOWN)],
    '8' : [(-1,-3.3,6.6,DOWN),(-.8,-3.5,1.6,RIGHT),(-.8,0,1.6,RIGHT),
           (-.8,3.5,1.6,RIGHT),(1,-3.3,6.6,DOWN)],
    '9' : [(-1,-3.3,3.3,DOWN),(-.8,-3.5,1.6,RIGHT),(-.8,0,1.6,RIGHT),
           (-0.8,3.5,1.6,RIGHT),(1,-3.3,6.6,DOWN)],
    '0' : [(-1,-3.3,6.6,DOWN),(-.8,-3.5,1.6,RIGHT),(-.8,3.5,1.6,RIGHT),
           (1,-3.3,6.6,DOWN)],
    '.' : [(-1,3.5,0,DOWN)]
}

FONT2 = {
    'dimensions' : (2,7),
    'width' : (0.45),
    'space' : (1),
    '1' : [(1,-3,2.5,DOWN), (1,.5,2.5,DOWN)],
    '2' : [(-.5,-3.5,1,RIGHT),(1,-3,2.5,DOWN),(-.5,0,1,RIGHT),(-1,0.5,2.5,DOWN),
           (-.5,3.5,1,RIGHT)],
    '3' : [(-.5,-3.5,1,RIGHT),(-0.5,0,1,RIGHT),(-.5,3.5,1,RIGHT),
           (1,-3,2.5,DOWN),(1,.5,2.5,DOWN)],
    '4' : [(-1,-3,2.5,DOWN),(-.5,0,1,RIGHT),(1,-3,2.5,DOWN),(1,.5,2.5,DOWN)],
    '5' : [(-.5,-3.5,1,RIGHT),(-1,-3,2.5,DOWN),(-.5,0,1,RIGHT),(1,0.5,2.5,DOWN),
           (-.5,3.5,1,RIGHT)],
    '6' : [(-.5,-3.5,1,RIGHT),(-1,-3,2.5,DOWN),(-1,.5,2.5,DOWN),(-.5,0,1,RIGHT),
           (1,0.5,2.5,DOWN),
           (-.5,3.5,1,RIGHT)],
    '7' : [(-.5,-3.5,1,RIGHT),(1,-3,2.5,DOWN),(1,.5,2.5,DOWN)],
    '8' : [(-1,.5,2.5,DOWN),(-1,-3,2.5,DOWN),(-.5,-3.5,1,RIGHT),(-.5,0,1,RIGHT),
           (-.5,3.5,1,RIGHT),(1,-3,2.5,DOWN),(1,.5,2.5,DOWN)],
    '9' : [(-1,-3,2.5,DOWN),(-.5,-3.5,1,RIGHT),(-.5,0,1,RIGHT),
           (-0.5,3.5,1,RIGHT),(1,-3,2.5,DOWN),(1,.5,2.5,DOWN)],
    '0' : [(-1,.5,2.5,DOWN),(-1,-3,2.5,DOWN),(-.5,-3.5,1,RIGHT),
           (-.5,3.5,1,RIGHT),(1,-3,2.5,DOWN),(1,.5,2.5,DOWN)],
    '.' : [(-.5,3.5,0,DOWN)]
}

class Image:
    """Class managing an image"""
    def __init__(self, dimensions, colors = None):
        (width, height) = dimensions
        self.dimensions = (width, height)
        # A matrix containing the pixels
        self.picture = [[0]*width for _ in range(height)]
        # A matrix containing the pixels, and that wil overlay self.picture.
        self.overlay = [[0]*width for _ in range(height)]
        # The pixel will be sorted by group, allowing to modify te color of
        # many pixel at the same time and to reduce memory usage
        self.groups_color = colors or [(255,255,255), (255,255,0), (0,0,255),
                                       (0,0,0)]

    def clean_overlay(self):
        """
        Empty the overlay. Overlays the picture on the pixels of group other
        than 0.
        """
        width, height = self.dimensions
        self.overlay = [[0]*width for _ in range(height)]

    def set_pixel(self, coords, group = 1, overlay = False):
        """
        Set given group to the given pixel (x,y),
        x from the top and y form the left
        coords -> the coordinates of the pixel to set.
        group -> The group in which to set the pixel.
        overlay -> Whether the targeted pixel is on the overlay.
        """
        if overlay:
            self.overlay[coords[0]][coords[1]] = group
        else:
            self.picture[coords[0]][coords[1]] = group

    def set_point(self, point, group = 1, overlay = False):
        """
        Set given group to the pixel present at the coordinates (x,y), assuming
        the image spans a [-1,1]² space. For instance, (-1,-1) is
        the bottom left of the picture, (1,1) is top right, (0,0) the center.
        point -> The point to set.
        group -> The group in which to set the pixel.
        overlay -> Whether the targeted pixel is on the overlay.
        """
        width, height = self.dimensions
        coords = (int(height*(point[1]+1)/2), int(width*(point[0]+1)/2))
        self.set_pixel(coords, group, overlay)

    def draw_pixel_line(self, start_px, length, line_width, is_downwards,
                        *args, **kargs):
        """
        Draws a line in the image using set_point.
        start_px -> the starting pixel.
        length -> The length of the line in pixels. Cannot be negative yet.
        line_width -> The width of the line in pixels. Minimum is 1
        is_downwards -> Whether the line is draw downwards or rightwards.
                        Consider using the constants DOWN and RIGHT.
        Note : You can't make a line upwards or leftwards yet.
        The remaining arguments are passed on to the pixel drawing function.
        Consider using :
        group -> The group of the pixels in the line
        overlay -> Whether the line is on the overlay.
        """
        width,height = self.dimensions
        if line_width < 1: 
            line_width = 1
        for coord_length in range(-line_width//2,
                                        length + line_width - line_width//2):
            for coord_width in range(-line_width//2,
                                                line_width - line_width//2):
                if is_downwards:
                    pt_courant = (start_px[0]+coord_length,
                                  start_px[1]+coord_width)
                else :
                    pt_courant = (start_px[0]+coord_width,
                                  start_px[1]+coord_length)
                if (0 <= pt_courant[0] < height and 0 <= pt_courant[1] < width):
                    self.set_pixel(pt_courant, *args, **kargs)

    def draw_line(self, start_pt, length, line_width, is_downwards,
                  *args, **kargs):
        """
        Draws a line in the image. Works with coordinates in [-1,1]²
        start_pt -> the starting point.
        length -> The length of the line. Cannot be negative yet.
                  1 is half the width of the picture.
        line_width -> The width of the line.
                      1 is half the height of the picture.
        is_downwards -> Whether the line is draw downwards or rightwards.
                        Consider using the constants DOWN and RIGHT.
        Note : You can't make a line upwards or leftwards yet.
        The remaining arguments are passed on to the pixel drawing function.
        Consider using :
        group -> The group of the pixels in the line
        overlay -> Whether the line is on the overlay.
        """
        width, height = self.dimensions
        coords = (int(height*(start_pt[1]+1)/2), int(width*(start_pt[0]+1)/2))
        length = int(width*length/2)
        line_width = int(height*line_width/2)
        self.draw_pixel_line(coords, length, line_width, is_downwards, 
                             *args, **kargs)

    def text(self, text, coords, size, *args, font = None, **kargs):
        """
        Writes a text on the picture using given font. Some characters may not
        be supported by the font. Refer to the font itself.
        Defaults to FONT1, which supports the following characters :
        "123456789.0"
        text -> The text to write
        coords -> The coordinates of the middle of the text
        size -> The size of the text, in percent. 100 is the original size of
                the font (which might be way larger than the picture).
        font -> The font to use.
        The arguments after size and the other arguments will be passed on to
        the pixel drawing function.
        Consider using :
        group -> The group of the pixels in the text.
        overlay -> Whether the text is on the overlay.
        """
        if font is None:
            font = FONT1
        size = size/100
        for index, letter in enumerate(text):
            letter_center = (
                coords[0] + size*(font["dimensions"][0]
                          + font['space']) * (index-len(text)/2),
                coords[1])
            for param in font[letter]:
                self.draw_line((letter_center[0] + param[0]*size,
                    letter_center[1] + param[1]*size), param[2]*size,
                    font['width']*size, param[3], *args, **kargs)

    def export(self, path, color_res = 9):
        """
        Exports the image in a text ppm file (P3).
        path -> The path in which to export the image
        color_res -> The "color resolution". Indicates on how many the colors
                     have to be written. Consider using 9 for a file as small as
                     possible, 99 for a file ~50% bigger but with good color
                     resolution, and 255 for full resolution, but potentially
                     twice as big as for 9.
        """
        width, height = self.dimensions
        header = f"P3\n{width} {height}\n{color_res}\n"
        file = open(path, 'w')
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
        """
        Exports the image in a binary ppm file (P6).
        path -> The path in which to export the image
        progress -> Whether to display a progress bar or not. If set to True,
                    uses better_io.Progress to display a progress bar
        clean_progress -> Whether to clean the progress bar (i.e. stop it from
                          displaying) once the image exported. If set to False,
                          the progress bar will remain visible (but not
                          running anymore).
        Consider using 'pre_text', 'fps' and 'line' to customize the progress
        bar.
        pre_text -> the string displayed before the progress bar
        fps -> The rate at which the display is updated. Tests have shown that
               this values has minor impact on performances, unless the value
               is ridiculously high.
        line -> The number of the line starting from the bottom of the console
                on which the progress bar has to be shown
        """
        width, height = self.dimensions
        header = (f"P6\n{width} {height} 255 ").encode('ASCII')
        file = open(path, 'wb')
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
    img = Image((8000,8000))
    img.text('123456789.0',(0,-0.5),4.5, group = 2, overlay = True, 
                                                                font = FONT0)
    img.text('123456789.0',(0,0),4.5, group = 2, overlay = True, font = FONT1)
    img.text('123456789.0',(0,0.5),4.5, group = 2, overlay = True, 
                                                                font = FONT2)
    img.draw_line((-1,0),1.9, 0.1, False, group = 1)
    img.export_bin('img.ppm', progress=True)
