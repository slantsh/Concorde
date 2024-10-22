import pygame
import time
import getchords

pygame.init()

timer = pygame.time.Clock()
screen = pygame.display.set_mode([1280, 720])
font = pygame.font.Font('assets/NotoSans-VariableFont_wdth,wght.ttf', 48)
icon= pygame.image.load('assets/windowicon.png')
pygame.display.set_icon(icon)
pygame.display.set_caption("Concorde")

current_bpm = 60
line_pos = -160

chord_dict=getchords.fetch_chords()

chord_list = list(chord_dict.keys())
chord_list.sort()
color_inactive = pygame.Color('lightskyblue3')
color_active = pygame.Color('white')


def player(c):
    s = []
    pygame.mixer.stop()
    for i in c:
        s.append(pygame.mixer.Sound('assets/notes/' + i + '.wav'))
    for x, j in enumerate(s):
        pygame.mixer.Channel(x).play(j)


progression = []
playing = False
last_play_time = time.time()
play_index = 0

running = True
while running:
    timer.tick(60)
    screen.fill('black')
    c = 0
    buttonlist = []

    # Drawing chord buttons
    for y in [450, 600]:
        for i in range(7):
            if chord_dict[chord_list[c]] in progression:
                rectcolor = color_active
            else:
                rectcolor = color_inactive

            pygame.draw.rect(screen, rectcolor, [20 + (i * 150), y, 100, 100], border_radius=12)
            buttonlist.append(pygame.Rect([20 + (i * 150), y, 100, 100]))
            clabel = font.render(chord_list[c], True, 'black')
            c += 1
            screen.blit(clabel, [30 + (i * 150), y])

    pygame.draw.rect(screen, color_inactive, [20, 20, 1240, 410], border_radius=12)

    # Play and Stop buttons
    playbutton_rect = pygame.Rect([1100, 40, 100, 100])
    pygame.draw.rect(screen, '#81FE9A', playbutton_rect, border_radius=12)

    stopbutton_rect = pygame.Rect([1100, 160, 100, 100])
    pygame.draw.rect(screen, '#FE8181', stopbutton_rect, border_radius=12)

    # BPM display and adjustment
    bpm_rect = pygame.Rect(1100, 450, 100, 250)
    bpm_label = font.render(str(current_bpm), True, 'black')
    pygame.draw.rect(screen, color_inactive, bpm_rect, border_radius=12)
    screen.blit(bpm_label, (1115, 540, 100, 250))

    plus = pygame.transform.scale(pygame.image.load('assets/plus.png'), (80, 80))
    minus = pygame.transform.scale(pygame.image.load('assets/minus.png'), (80, 80))
    plus_rect = pygame.Rect([1110, 460, 80, 80])
    minus_rect = pygame.Rect([1110, 610, 80, 80])
    screen.blit(plus, plus_rect)
    screen.blit(minus, minus_rect)

    # Progression line
    for i in [120, 400, 680, 960]:
        pygame.draw.rect(screen, "black", [i, 20, 10, 410])
    pygame.draw.rect(screen, "white", [line_pos, 20, 10, 410])

    # Event handling
    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for index, b in enumerate(buttonlist):
                if b.collidepoint(pos):
                    chord_to_play = chord_dict[chord_list[index]]
                    if chord_to_play not in progression:
                        progression.append(chord_to_play)
                    else:
                        progression.remove(chord_to_play)
                    if len(progression) > 4:
                        del progression[0]
            if playbutton_rect.collidepoint(pos):
                playing = True
            if plus_rect.collidepoint(pos):
                current_bpm = min(current_bpm + 1, 300)
            if minus_rect.collidepoint(pos):
                current_bpm = max(current_bpm - 1, 30)

    # Handle playback
    if playing:
        current_time = time.time()
        time_between = current_time - last_play_time

        if time_between >= 60 / current_bpm:
            if play_index < len(progression):
                player(progression[play_index])
                play_index += 1
                last_play_time = current_time
                line_pos += 280
            else:
                play_index = 0
                line_pos = -160

        if stopbutton_rect.collidepoint(pygame.mouse.get_pos()):
            if event.type == pygame.MOUSEBUTTONDOWN:
                playing = False

    pygame.display.flip()
pygame.quit()