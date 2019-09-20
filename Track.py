import pygame

class Track(object):

    def __init__(self, track_name, colour):
        self.borders = []
        self.colour = colour
        with open(track_name + '.txt', 'r') as f:
            num = int(f.readline())
            for i in range(num):
                self.borders.append([])
                n = int(f.readline())
                for j in range(n):
                    z = f.readline()
                    for k in range(len(z)):
                        if z[k] == ' ':
                            x, y = int(z[:k]), int(z[k + 1:])
                            break
                    self.borders[i].append((x,y))
        
        self.rewards = []
    	with open(track_name + '_rewards.txt', 'r') as f:
            num = int(f.readline())
            for i in range(num):
                line = f.readline().split(' ')
                for i in range(len(line)):
                    line[i] = int(line[i])
                rewards.append([(line[0], line[1]), (line[2], line[3])])

        
    def draw(self, game_window, bg_colour):
        pygame.draw.polygon(game_window, self.colour, self.borders[0])
        for i in range(1, len(self.borders)):
            pygame.draw.polygon(game_window, bg_colour, self.borders[i])