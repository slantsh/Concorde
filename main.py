import pygame
import time


pygame.init()
timer=pygame.time.Clock()
screen=pygame.display.set_mode([1280,720])
font = pygame.font.Font('assets/NotoSans-VariableFont_wdth,wght.ttf', 48)
color_inactive = pygame.Color('lightskyblue3')
color_active = pygame.Color('dodgerblue2')
color = color_inactive
current_bpm=60
CHORDS= {
    "C": ["C", "E", "G"],
    "Cm": ["C", "D#", "G"],
    "D": ["D", "F#", "A"],
    "Dm": ["D", "F", "A"],
    "E": ["E", "G#", "B"],
    "Em": ["E", "G", "B"],
    "F": ["F", "A", "C"],
    "Fm": ["F", "G#", "C"],
    "G": ["G", "B", "D"],
    "Gm": ["G", "A#", "D"],
    "A": ["A", "C#", "E"],
    "Am": ["A", "C", "E"],
    "B": ["B", "D#", "F#"],
    "Bm": ["B", "D", "F#"]
}

CHORDLIST=list(CHORDS.keys())
CHORDLIST.sort()




def player(c):
        s=[]
        pygame.mixer.stop()
        for i in c:
            s.append(pygame.mixer.Sound('assets/notes/'+i+'.wav'))
        for x,j in enumerate(s):
            pygame.mixer.Channel(x).play(j)

plus=pygame.transform.scale(pygame.image.load('assets/plus.png'),(80,80))
minus=pygame.transform.scale(pygame.image.load('assets/minus.png'),(80,80))
plusrect=pygame.Rect([1110, 460, 80, 80])
minusrect=pygame.Rect([1110, 610, 80, 80])

progression=[]
def tracker():
    if len(progression)>4:
        progression.pop()

playing=False
last_play_time=time.time()
play_index=0

running=True
while running:
    timer.tick(60)
    screen.fill('black')
    c=0
    buttonlist=[]
    for y in [450,600]:
        for i in range(7):
            if CHORDS[CHORDLIST[c]] in progression:
                rectcolor=color_active
            else:
                rectcolor=color_inactive
            pygame.draw.rect(screen,rectcolor,[20+(i*150),y,100,100],border_radius=12) 
            buttonlist.append(pygame.Rect([20+(i*150),y,100,100]) )       
            clabel=font.render(CHORDLIST[c],True,'black')
            c+=1
            screen.blit(clabel,[30+(i*150),y])
    pygame.draw.rect(screen,'darkgray',[20,20,1240,410],border_radius=12)

    playbutton=pygame.Rect([1140,40,100,100])
    pygame.draw.rect(screen,'#81FE9A',playbutton,border_radius=12)

    stopbutton=pygame.Rect([1140,160,100,100])
    pygame.draw.rect(screen,'#FE8181',stopbutton,border_radius=12)


    bpm_box = pygame.Rect(1100, 450, 100, 250)
    bpm_label=font.render(str(current_bpm),True,'black')
    pygame.draw.rect(screen,color_inactive,bpm_box,border_radius=12)
    screen.blit(bpm_label,(1115, 540, 100, 250))
    screen.blit(plus,plusrect)
    screen.blit(minus,minusrect)



    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False
        if event.type==pygame.MOUSEBUTTONDOWN:
            global pos
            pos=pygame.mouse.get_pos()
            for index,b in enumerate(buttonlist):
                if b.collidepoint(pos):
                    chord_to_play=CHORDS[CHORDLIST[index]]
                    progression.append(chord_to_play)
                    if len(progression) > 4:
                        del progression[0]
            if playbutton.collidepoint(pos):
                playing=True
        if pygame.mouse.get_pressed()[0]:
            if plusrect.collidepoint(pos):
                current_bpm+=1
            if minusrect.collidepoint(pos):
                current_bpm-=1

    
    if playing:
        current_time = time.time()  
        if current_time - last_play_time >= 60/current_bpm:  
            if play_index < len(progression):
                player(progression[play_index])  
                play_index += 1  
                last_play_time = current_time 
            else:
                play_index = 0  
        if stopbutton.collidepoint(pygame.mouse.get_pos()):
            if event.type==pygame.MOUSEBUTTONDOWN:
                playing=False
        
        



    pygame.display.flip()
pygame.quit()











