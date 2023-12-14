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

        for line in self.map:
            print(line)

    def draw_map(self):
        pass
