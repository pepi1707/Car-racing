import pygame

WINDOW_WIDTH = 1800
WINDOW_HEIGHT = 1000

pygame.init()

game_window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

pygame.display.set_caption("draw")

game_running = True

track_name = input()

track_lines = [[]]
cur = 0

while game_running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                track_lines[cur].append(event.pos)
            if event.button == 3:
                track_lines.append([])
                cur += 1

    game_window.fill((255, 255, 255))

    for track in track_lines:
        for i in range(len(track) - 1):
            pygame.draw.line(game_window, (0,0,0), track[i], track[i + 1], 2)

    pygame.display.update()
    

with open(track_name + '.txt', 'w') as f:
    f.write("%s\n" %(len(track_lines) - 1))
    for track in track_lines:
        if len(track) == 0:
            continue
        f.write("%s\n" %len(track))
        for x,y in track:
            f.write("%s %s\n" %(x,y))