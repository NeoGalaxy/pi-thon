"""
Module qui gère les images PPM
"""

class Image:
    """Classe créant et gérant une image"""
    def __init__(self, dimensions):
        (width, height) = dimensions
        self.dimensions = (width, height)
        self.picture = [[0]*width for _ in range(height)]
        self.groups_color = [(255,255,255), (255,255,0), (0,0,255)]
        self.closed = False

    def set_pixel(self, coords, group):
        """Set given color to the given pixel (x,y),
        x from the top and y form the left"""
        self.picture[coords[0]][coords[1]] = group

    def set_point(self, point, group):
        """Set given color to the given coordinates (x,y)"""
        width, height = self.dimensions
        coords = (int(height*(point[1]+1)/2), int(width*(point[0]+1)/2))
        self.set_pixel(coords, group)

    def export(self, path, color_res = 1):
        """write designated points into the file"""
        width, height = self.dimensions
        header = f"P3\n{width} {height}\n{color_res}\n"
        file = open(path, 'w', buffering = 100 + 12 * width * height + len(header))
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

    def export_bin(self, path):
        """write designated points into the file"""
        width, height = self.dimensions
        header = (f"P6\n{width} {height} 255 ").encode('ASCII')
        file = open(path, 'wb', buffering = 100 + width * height + len(header))
        file.write(header)
        for line in self.picture:
            for pix in line:
                file.write(bytes(self.groups_color[pix]))
        file.close()
