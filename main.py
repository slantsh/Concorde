import pygame
import time

pygame.init()
timer=pygame.time.Clock()
screen=pygame.display.set_mode([1280,720])
font = pygame.font.Font('assets/NotoSans-VariableFont_wdth,wght.ttf', 48)

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



progression=[]
def tracker(t):
    if len(progression)>4:
        progression.pop()

playing=False
last_play_time=time.time()
play_index=0

run=True
while run==True:
    timer.tick(60)
    screen.fill('black')
    c=0
    buttonlist=[]
    for y in [450,600]:
        for i in range(7):
            pygame.draw.rect(screen,'white',[20+(i*150),y,100,100],border_radius=12) 
            buttonlist.append(pygame.Rect([20+(i*150),y,100,100]) )       
            clabel=font.render(CHORDLIST[c],True,'black')
            c+=1
            screen.blit(clabel,[30+(i*150),y])
    pygame.draw.rect(screen,'grey',[20,20,1240,410],border_radius=12)

    playbutton=pygame.Rect([1140,40,100,100])
    pygame.draw.rect(screen,'#81FE9A',playbutton,border_radius=12)

    stopbutton=pygame.Rect([1140,160,100,100])
    pygame.draw.rect(screen,'#FE8181',stopbutton,border_radius=12)
    


    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            run=False
        if event.type==pygame.MOUSEBUTTONDOWN:
            pos=pygame.mouse.get_pos()
            for index,b in enumerate(buttonlist):
                if b.collidepoint(pos):
                    chord_to_play=CHORDS[CHORDLIST[index]]
                    progression.append(chord_to_play)
                    if len(progression) > 4:
                        del progression[0]

            if playbutton.collidepoint(pos):
                playing=True
            
    if playing:
        current_time = time.time()  
        if current_time - last_play_time >= 1:  
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











