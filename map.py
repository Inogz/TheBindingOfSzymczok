
#map class   222
class Map:
    def __init__(self):

        # Dimensions

        self.width = 0
        self.height = 0
        self.map = []

    def initialize_map(self, width, height):
        self.width = width
        self.height = height

        for i in range(width):
            self.map.append([])
            for j in range(height):
                self.map[i].append(0)



    def draw_map(self):
        for line in self.map:
            print(line)




map = Map()
map.initialize_map(100,100)
map.draw_map()