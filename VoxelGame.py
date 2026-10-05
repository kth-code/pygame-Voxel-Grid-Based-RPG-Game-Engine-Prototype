import pygame,sys
from random import *
from math import *

pygame.init()

from VoxelGame_BaseVars import *
from VoxelGame_Stage import *
from VoxelGame_Unit import *
from VoxelGame_ATKProjectiles import *
from VoxelGame_Dialogue import *
from VoxelGame_Visuals import *


pygame.display.set_caption("Voxel RPG")

clock = pygame.time.Clock()


##Creek
d = [8,6] #Dimension
h = [[3,3,2,2,2,1,1,0], #Terrain Height
     [2,1,0,0,1,1,0,0],
     [0,0,0,0,0,0,0,0],
     [0,0,0,0,0,1,1,0],
     [2,1,0,0,1,1,1,1],
     [4,3,1,0,0,0,1,1],]

o = [[2,0,0,0,6,6,6,0], #Objects
     [0,0,0,0,6,6,0,0],
     [0,0,0,0,0,0,0,0],
     [0,0,0,0,0,2,0,0],
     [0,1,0,0,0,0,0,0],
     [2,0,0,0,0,0,0,0],]

t = [[1,1,3,3,1,1,1,2], #Terrain Type
     [1,1,3,3,1,1,2,3],
     [3,3,3,3,3,3,3,3],
     [3,3,3,3,2,1,1,2],
     [1,1,2,2,1,1,1,1],
     [1,1,1,2,2,1,1,1],]

u = [[0,0,0,0,0,0,0,0], #Units
     [0,4,0,0,0,0,0,0],
     [0,0,0,0,0,0,0,0],
     [0,0,0,0,0,0,4,0],
     [0,0,0,0,0,4,0,1],
     [0,0,0,0,0,0,0,0],]

value = 24
fm = Field_Manager(40,34,value,d,6)

for y in range(d[1]):
    fm.tiles.append([])
    fm.objects.append([])  
    fm.highlights.append([])
    fm.targets.append([])
    fm.boundaries.append([])
    fm.glowframes.append([])
    for x in range(d[0]):
        tile = tile_spawn.get(t[y][x])(x,y,h[y][x])
        fm.tiles[y].append(tile)
        if o[y][x] == 0:
            fm.objects[y].append(None)
        elif o[y][x] == 1:
            fm.objects[y].append(Unbreakable_Cover(tile))
        elif o[y][x] == 2:
            fm.objects[y].append(Breakable_Cover(tile))
        elif o[y][x] == 3:
            fm.objects[y].append(Fragile_Cover(tile))
        elif o[y][x] == 6:
            fm.objects[y].append(Dark_Sludge(tile)) 
        else:
            fm.objects[y].append(None)
        fm.highlights[y].append([])
        fm.targets[y].append(None)
        fm.boundaries[y].append(None)
        fm.glowframes[y].append(None)
        unit = None
        if u[y][x] == 1:
            unit = Test_Mage(x,y)
        if u[y][x] == 4:
            unit = TestUnit(x,y)
        if unit:
            fm.AddUnit(unit)
                                                                                                   

fm.mode = 2
fm.Get_ActingUnits(1)



for i in fm.units_list:
    if i.faction == 0:
        m = i 
        break


loop = 0
p_count = 0

def DisplayVar():
    if fm.acting_unit:
        y = 300
        txt = game_font20.render("Unit Mode: "+str(fm.acting_unit.mode),True,(255,255,255))
        rect = txt.get_rect()
        rect.top = y
        game_window.blit(txt,rect)
        y += rect[3]
        txt = game_font20.render("Field Mode: "+str(fm.mode),True,(255,255,255))
        rect = txt.get_rect()
        rect.top = y
        game_window.blit(txt,rect)
        y += rect[3]
        txt = game_font20.render("Field Desc: "+str(fm.desc),True,(255,255,255))
        rect = txt.get_rect()
        rect.top = y
        game_window.blit(txt,rect)
        y += rect[3]
        txt = game_font20.render("Act Pts: "+str(fm.acting_unit.action_pts),True,(255,255,255))
        rect = txt.get_rect()
        rect.top = y
        game_window.blit(txt,rect)
        y += rect[3]

        txt = game_font20.render("Charge CD: "+str(fm.acting_unit.prmy_atk.timer),True,(255,255,255))
        rect = txt.get_rect()
        rect.top = y
        game_window.blit(txt,rect)
        y += rect[3]

        txt = game_font20.render("Charged: "+str(fm.acting_unit.prmy_atk.charge),True,(255,255,255))
        rect = txt.get_rect()
        rect.top = y
        game_window.blit(txt,rect)
        y += rect[3]
        
        x = ""
        for i in fm.acting_unit.act_CD:
            x += str(i)+" "
        txt = game_font20.render("CDs: "+x,True,(255,255,255))
        rect = txt.get_rect()
        rect.top = y
        game_window.blit(txt,rect)
        y += rect[3]
        
        x = ""
        for i in fm.acting_unit.act_record:
            x += str(i)+" "
        txt = game_font20.render("Records: "+x,True,(255,255,255))
        rect = txt.get_rect()
        rect.top = y
        game_window.blit(txt,rect)
        y += rect[3]

## Create dialog: Dialogue_Box(Field_Manager, speakers of each page, dialogue of each page, colour of each page's speaker's name frame, coloured textlist, image list
## Text Formatting: @{N}text will change the colour of that word to the N-th colour in extra_clr, i.e. the "coloured text list"
## Image Formatting: #{N} will display the image stored in imgs, i.e. the "image list"

##db = Dialogue_Box(fm,
##                  ["Character 1","System","Character 1"],
##                  ["Hello world. It is nice to meet you!",
##                   "#0 @0Burn is a @1status @1effect. It deals #0 @0Fire @0damage to you!",
##                   "Gotta be careful! Or @2heal @2up when necessary",
##                   ],
##                  [[(255,255,255),faction_clrs[0]],
##                   [(255,255,255),(180,180,180)],
##                   [(255,255,255),faction_clrs[0]],],
##                  
##                  extra_clr = [SE_colour_set["Burn"],(255,0,0),(152,247,160)],
##                  imgs = [burn_symbol])

##Dialogue_Box(fm,
##             ["System"],
##             ["Practice begins! #0 @0Break @0all @0targets!"],
##             [[(255,255,255),faction_clrs[0]]],
##             extra_clr = [(255,0,0)],
##             imgs = [burn_symbol])

while True:
    fm.AdjustStartPt()
    game_window.fill([0,0,0])
    
    clock.tick(fps)
    for event in pygame.event.get():                                                                                                                                                                                                          
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    for t in tile_sprites:
        t.update()
        t.draw()

    if m.HP > 0 and fm.mode >= 1:
        y = 20
        text = title_font25.render("Test Environment",True,(255,255,255))
        textRect = text.get_rect()
        textRect.left,textRect.top = 20, y
        DrawTextFrame(textRect,(67,95,226))
        game_window.blit(text,textRect)
        y += textRect[3] + 10

        text = game_font18.render("Break All Targets",True,(255,255,255))
        textRect = text.get_rect()
        textRect.left,textRect.top = 20, y
        game_window.blit(text,textRect)
        pygame.draw.line(game_window,(255,255,255),[textRect.left + 10,textRect.bottom + 2],[textRect.right - 10,textRect.bottom + 2],width = 1)
        DrawDiamond(textRect.left + 6,textRect.bottom + 2,2)
        DrawDiamond(textRect.left,textRect.bottom + 2,3)
        DrawDiamond(textRect.right - 6 ,textRect.bottom + 2,2)
        DrawDiamond(textRect.right,textRect.bottom + 2,3)
        y += textRect[3] + 10


        if len(fm.teams_list[1]) == 0:
            text = stat_font18.render("Objective Completed",True,(255,255,255))
        else:
            text = stat_font18.render(str(fm.total_count[1]-len(fm.teams_list[1]))+" / "+str(fm.total_count[1]) + " Defeated",True,(255,255,255))
        textRect = text.get_rect()
        textRect.left,textRect.top = 20, y
        game_window.blit(text,textRect)
        y += textRect[3] + 10

    keystate = pygame.key.get_pressed()
    pygame.display.flip()
    loop = (loop + 1)%360

