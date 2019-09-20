import pygame
import Track

WINDOW_WIDTH = 1800
WINDOW_HEIGHT = 1000

pygame.init()

game_window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

pygame.display.set_caption("draw")

game_running = True

track = Track.Track('test.txt', (255, 255, 255))

l = 0
line = [None, None]
lines = []

while game_running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                line[l] = event.pos
                l = 1 - l
                if not l:
                    lines.append(line.copy())
    
    game_window.fill((0, 80, 80))

    track.draw(game_window, (0, 80, 80))

    for lin in lines:
        pygame.draw.line(game_window, (0,0,0), lin[0], lin[1], 2)
    
    pygame.display.update()

with open('test_rewards.txt', 'w') as f:
    f.write("%s\n" %len(lines))
    for line in lines:
        f.write('%s %s %s %s\n' %(line[0][0], line[0][1], line[1][0], line[1][1]))
