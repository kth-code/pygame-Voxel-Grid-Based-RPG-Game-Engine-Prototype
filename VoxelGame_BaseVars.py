import pygame
from random import *
from math import *

window_width = 1200#1500
window_height = 800#1000

fps = 60

game_window = pygame.display.set_mode((window_width,window_height))

font_path = "./_Font/"

game_font = font_path+'Quicksand-SemiBold.ttf'
game_font8 = pygame.font.Font(game_font,8)
game_font9 = pygame.font.Font(game_font,9)
game_font10 = pygame.font.Font(game_font,10)
game_font11 = pygame.font.Font(game_font,11)
game_font12 = pygame.font.Font(game_font,12)
game_font13 = pygame.font.Font(game_font,13)
game_font14 = pygame.font.Font(game_font,14)
game_font15 = pygame.font.Font(game_font,15)
game_font16 = pygame.font.Font(game_font,16)
game_font18 = pygame.font.Font(game_font,18)
game_font20 = pygame.font.Font(game_font,20)
game_font25 = pygame.font.Font(game_font,25)
game_font30 = pygame.font.Font(game_font,30)
game_font40 = pygame.font.Font(game_font,40)

title_font = font_path+'barlow-condensed.ttf'
title_font12 = pygame.font.Font(title_font,12)
title_font16 = pygame.font.Font(title_font,16)
title_font18 = pygame.font.Font(title_font,18)
title_font20 = pygame.font.Font(title_font,20)
title_font25 = pygame.font.Font(title_font,25)
title_font30 = pygame.font.Font(title_font,30)
title_font50 = pygame.font.Font(title_font,50)

stat_font = font_path+'barlow-semi_condensed.ttf'
stat_font8 = pygame.font.Font(stat_font,8)
stat_font12 = pygame.font.Font(stat_font,12)
stat_font14 = pygame.font.Font(stat_font,14)
stat_font16 = pygame.font.Font(stat_font,16)
stat_font18 = pygame.font.Font(stat_font,18)
stat_font20 = pygame.font.Font(stat_font,20)
stat_font25 = pygame.font.Font(stat_font,25)
stat_font75 = pygame.font.Font(stat_font,75)

key_font = font_path+'BlackHanSans-Regular.ttf'
key_font16 = pygame.font.Font(key_font,16)
key_font20 = pygame.font.Font(key_font,20)

tile_sprites = pygame.sprite.Group()

blocks_values = [1,2,3,4,5]
unbreakable_values = [1,4]
pits_values = [0]
unsteppable_values = [0,4]

def CheckNumberinRange(n,l,h): #Check if input (can be letters) is within numeric range
    NRange = []
    for i in range(h - l + 1):
        NRange.append(str(l+i))
    return str(n) in NRange

def CorInt(n): #Avoid Python cor to nearest 2 system
    if (abs(n) - int(abs(n))) < 0.5:
        return int(n)
    else:
        return int(int(n) + 1 * (n/abs(n)))

def RoundUp(n): #Avoid Python cor to nearest 2 system
    if int(n) == n:
        return int(n)
    else:
        return int(int(n) + 1 * (n/abs(n)))

def GenPN():
    return randint(1,2)*2-3

def GenRandomCords():
    return [randint(window_width/2-boundary_width/2,window_width/2+boundary_width/2),randint(window_height/2-boundary_height/2,window_height/2+boundary_height/2)]

def GenCordsinRange(centre,r):
    return [CorInt(centre[0] + cos(radians(randint(1,360)))*randint(0,r)),CorInt(centre[1] + sin(radians(randint(1,360)))*randint(0,r))]

def Move(d,m):
    return m * cos(d), -m * sin(d) #dx = (distance)(cos(radian)); dy = -(distance)(sin(radians)) {L > -; R > +; U > -; D > +}

def Direction(a,b):
    return atan2((a.rect.centery - b.rect.centery),(b.rect.centerx - a.rect.centerx)) #(ay-by) {#y-axis is flipped} /(bx-ax)

def Direction_Pt(a,b):
    return atan2((a[1] - b[1]),(b[0] - a[0])) #(ay-by) {#y-axis is flipped} /(bx-ax)

def Distance(a,b):
    return hypot((a.rect.centerx-b.rect.centerx),(a.rect.centery-b.rect.centery))

def Distance_Pt(a,b):
    return hypot((a[0]-b[0]),(a[1]-b[1]))

def Get_RClr(loop, base = 0,darken = 1):
    if loop <= 255:
        clr = [255*darken,(base + CorInt((255 - base)*loop/255))*darken,base*darken]
    elif loop <= 510:
        clr = [(base + CorInt((255 - base)*(510 - loop)/255))*darken,255*darken,base*darken]
    elif loop <= 765:
        clr = [base*darken,255*darken,(base + CorInt((255 - base)*(loop - 510)/255))*darken]
    elif loop <= 1020:
        clr = [base*darken,(base + CorInt((255 - base)*(1020 - loop)/255))*darken,255*darken]
    elif loop <= 1275:
        clr = [(base + CorInt((255 - base)*(loop - 1020)/255))*darken,base*darken,255*darken]
    elif loop <= 1530:
        clr = [255*darken,base*darken,(base + CorInt((255 - base)*(1530 - loop)/255))*darken]
    for i in range(3):
        clr[i] = CorInt(clr[i])
    return tuple(clr)

def Brighten(colour,brighten):
    b = []
    for i in colour:
        diff = 255 - i
        if RoundUp(i + diff*brighten/100) >= 255:
            b.append(255)
        else:
            b.append(RoundUp(i + diff*brighten/100))
    return tuple(b)

def Darken(colour,darken):
    b = []
    for i in colour:
        b.append(RoundUp(i - i*darken/100))
    return tuple(b)

def MergeClrs(clrs):
    d = list(map(sum, zip(*clrs)))
    for i in range(3):
        d[i] = d[i]/len(clrs)
    return d

def GradientClrs(ac,bc,wa,wb):
    d = [0,0,0]
    for i in range(3):
        d[i] = CorInt(ac[i] * wa + bc[i] * wb)
        if d[i] > 255:
            d[i] = 255
    return d

faction_clrs = [(70,110,255),(155,70,255),(150,155,255)]
faction_bar_clrs = [(85,180,255),(190,115,255),(110,120,255)]

SE_colour_set = {"Burn": (255,115,115),#(255,30,0),
                 "Freeze": (190,230,255),
                 "Shock": (255,235,0),
                 "Splash": (135,165,255),
                 "Poison": (95,185,90),
                 "Drain": (210,160,255),
                 "Curse": (181,153,233),#(135,110,180),
                 "Blind": (153,106,245),#(126,65,161),#(135,110,180),
                 "Regeneration": (152,247,160),#(254,255,212),
                 "Invisible": (190,254,255),#(76,204,255),
                 "Invincible": (136,241,219),#(87,168,255),#(76,204,255),
                 "Quicken": (138,184,243),#(114,96,222),
                 "Strengthen": (255,233,94),#(255,223,20),
                 "Weaken": (216,99,228),#(208,0,229),
                 "Reinforce": (215,231,235),
                 "Vulnerable": (135,178,161),
                 "Lucky": (63,200,47),
                 "Unlucky": (138,54,213),
                 "Reflect": (162,231,255),
                 "Thorns": (212,88,240),#(186,114,255),
                 "Corruption": (135,30,200),#(79,26,146),
                 "Fire Resistance": (255,115,115),
                 "Ice Resistance": (190,230,255),
                 "Electric Resistance": (255,235,0),
                 "Water Resistance": (135,165,255),
                 "Poison Resistance": (95,185,90),
                 "Gust Resistance": (210,160,255),
                 "Shadow Resistance": (153,106,245),
                 "Fire Weakness": (255,115,115),
                 "Ice Weakness": (190,230,255),
                 "Electric Weakness": (255,235,0),
                 "Water Weakness": (135,165,255),
                 "Poison Weakness": (95,185,90),
                 "Gust Weakness": (210,160,255),
                 "Shadow Weakness": (153,106,245),
                 }

SE_Dcolour_set = {}
for i in list(SE_colour_set.keys()):
    SE_Dcolour_set.update({i: Darken(SE_colour_set.get(i),50)})

SE_Elements = {"Burn": "Fire",
               "Freeze": "Ice",
               "Shock": "Electric",
               "Splash": "Water",
               "Poison": "Poison",
               "Drain": "Gust",
               "Curse": "Corruption",
               "Blind": "Shadow",
               "Regeneration": "Light",
               "Invisible": "Ether",
               "Invincible": "Astral",
               "Quicken": "NIL",
               "Strengthen": "NIL",
               "Weaken": "NIL",
               "Reinforce": "NIL",
               "Vulnerable": "NIL",
               "Lucky": "NIL",
               "Unlucky": "NIL",
               "Reflect": "NIL",
               "Thorns": "NIL",
               "Corruption": "Corruption",
               "Fire Resistance": "Fire",
               "Ice Resistance": "Ice",
               "Electric Resistance": "Electric",
               "Water Resistance": "Water",
               "Poison Resistance": "Poison",
               "Gust Resistance": "Gust",
               "Shadow Resistance": "Shadow",
               "Fire Weakness": "Fire",
               "Ice Weakness": "Ice",
               "Electric Weakness": "Electric",
               "Water Weakness": "Water",
               "Poison Weakness": "Poison",
               "Gust Weakness": "Gust",
               "Shadow Weakness": "Shadow",
               }

SE_affect_set = {"Burn": "Burnt",
                 "Freeze": "Frozen",
                 "Shock": "Shocked",
                 "Splash": "Splashed",
                 "Poison": "Poisoned",
                 "Drain": "Drained",
                 "Curse": "Cursed",
                 "Blind": "Blinded",
                 "Regeneration": "Regenerative",
                 "Invisible": "Invisibility",
                 "Invincible": "Invincility",
                 "Quicken": "Quickened",
                 "Strengthen": "Strengthened",
                 "Weaken": "Weakened",
                 "Reinforce": "Reinforced",
                 "Vulnerable": "Vulnerable",
                 "Lucky": "Lucky",
                 "Unlucky": "Unlucky",
                 "Reflect": "Reflective",
                 "Thorns": "Thorned",
                 "Fire Resistance": "FireResistance",
                 "Ice Resistance": "IceResistance",
                 "Electric Resistance": "ElectricResistance",
                 "Water Resistance": "WaterResistance",
                 "Poison Resistance": "PoisonResistance",
                 "Gust Resistance": "GustResistance",
                 "Shadow Resistance": "ShadowResistance",
                 "Fire Weakness": "FireWeakness",
                 "Ice Weakness": "IceWeakness",
                 "Electric Weakness": "ElectricWeakness",
                 "Water Weakness": "WaterWeakness",
                 "Poison Weakness": "PoisonWeakness",
                 "Gust Weakness": "GustWeakness",
                 "Shadow Weakness": "ShadowWeakness",
                 }

SE_UnitName = []
for i in list(SE_affect_set):
    SE_UnitName.append(i.replace(" ","_"))

SE_Default_Values = {"Burn": 0.02,
                     "Freeze": None,
                     "Shock": None,
                     "Splash": 2,
                     "Poison": None,
                     "Drain": 0.3,
                     "Curse": None,
                     "Blind": 2,
                     "Regeneration": 0.1,
                     "Invisible": None,
                     "Invincible": 5,
                     "Quicken": 2,
                     "Strengthen": 0.5,
                     "Weaken": 0.5,
                     "Reinforce": 50,
                     "Vulnerable": -50,
                     "Lucky": 50,
                     "Unlucky": -50,
                     "Reflect": 15,
                     "Thorns": 30,
                     "Fire Resistance": 50,
                     "Ice Resistance": 50,
                     "Electric Resistance": 50,
                     "Water Resistance": 50,
                     "Poison Resistance": 50,
                     "Gust Resistance": 50,
                     "Shadow Resistance": 50,
                     "Fire Weakness": 50,
                     "Ice Weakness": 50,
                     "Electric Weakness": 50,
                     "Water Weakness": 50,
                     "Poison Weakness": 50,
                     "Gust Weakness": 50,
                     "Shadow Weakness": 50,
                     }

#0 - Timer Stack, 1 - Timer/Val Stack, 2 - Independent Stack, 3 - Check Resistances, 4 - Check Weaknesses
SE_Default_Stack = {"Burn": 2,
                    "Freeze": 0,
                    "Shock": 0,
                    "Splash": 0,
                    "Poison": 0,
                    "Drain": 0,
                    "Curse": 0,
                    "Blind": 0,
                    "Regeneration": 0,
                    "Invisible": 0,
                    "Invincible": 1,
                    "Quicken": 0,
                    "Strengthen": 2,
                    "Weaken": 2,
                    "Reinforce": 2,
                    "Vulnerable": 2,
                    "Lucky": 0,
                    "Unlucky": 0,
                    "Reflect": 0,
                    "Thorns": 0,
                    "Fire Resistance": 3,
                    "Ice Resistance": 3,
                    "Electric Resistance": 3,
                    "Water Resistance": 3,
                    "Poison Resistance": 3,
                    "Gust Resistance": 3,
                    "Shadow Resistance": 3,
                    "Fire Weakness": 4,
                    "Ice Weakness": 4,
                    "Electric Weakness": 4,
                    "Water Weakness": 4,
                    "Poison Weakness": 4,
                    "Gust Weakness": 4,
                    "Shadow Weakness": 4,
                    }

SE_Alignment = {"Burn": 1,
                "Freeze": 1,
                "Shock": 1,
                "Splash": 1,
                "Poison": 1,
                "Drain": 1,
                "Curse": 1,
                "Blind": 1,
                "Regeneration": 0,
                "Invisible": 0,
                "Invincible": 0,
                "Quicken": 0,
                "Strengthen": 0,
                "Weaken": 1,
                "Reinforce": 0,
                "Vulnerable": 1,
                "Lucky": 0,
                "Unlucky": 1,
                "Reflect": 0,
                "Thorns": 0,
                "Fire Resistance": 0,
                "Ice Resistance": 0,
                "Electric Resistance": 0,
                "Water Resistance": 0,
                "Poison Resistance": 0,
                "Gust Resistance": 0,
                "Shadow Resistance": 0,
                "Fire Weakness": 1,
                "Ice Weakness": 1,
                "Electric Weakness": 1,
                "Water Weakness": 1,
                "Poison Weakness": 1,
                "Gust Weakness": 1,
                "Shadow Weakness": 1,
                }

def Spritesheet_Img(sheet,x,y,w,h,scale = [],brightness = 0):
    image = pygame.Surface((w,h)).convert_alpha()
    image.blit(sheet,(0,0),(x,y,w,h))
    if len(scale) > 0:
        image = pygame.transform.scale(image,scale)
    if brightness != 0:
        x = pygame.Surface((image.get_width(),image.get_height())).convert_alpha()
        x.fill((abs(brightness),abs(brightness),abs(brightness),0))
        if brightness > 0:
            image.blit(x,(0,0),special_flags=pygame.BLEND_RGBA_ADD)
        else:
            image.blit(x,(0,0),special_flags=pygame.BLEND_RGBA_SUB)
    return image


def CheckifBlock(x,y):
    fm = tile_sprites.sprites()[0]
    if fm.objects[y][x]:
        return fm.objects[y][x].type_id in blocks_values
    else:
        return False

def CheckifPassable(x,y):
    fm = tile_sprites.sprites()[0]
    if fm.objects[y][x]:
        return fm.objects[y][x].passable
    else:
        return True

def CheckifSteppable(x,y):
    fm = tile_sprites.sprites()[0]
    return fm.tiles[y][x].type_id not in unsteppable_values

def CheckifUnit(x,y, faction = []):
    fm = tile_sprites.sprites()[0]
    if type(faction) != type([]):
        faction = [faction]
    for j in fm.units_list:
        if j.x == x and j.y == y:
            if faction != []:
                return j.faction in faction
            return True
    return False

def CheckLineofSight(atk,tar):
    fm = tile_sprites.sprites()[0]
    
    fm_desc, fm_v, fm_h = fm.desc, fm.v, fm.h
    fm.QuickSetTopView()

    #Get Necessary Tiles within Area
    area = []
    obst = []
    height = []
    collision = []
    a_t = fm.tiles[atk.y][atk.x]
    t_t = fm.tiles[tar.y][tar.x]
    a_pos = [fm.s_x + atk.x * fm.w, fm.s_y + atk.y * fm.w]
    t_pos = [fm.s_x + tar.x * fm.w, fm.s_y + tar.y * fm.w]
    sx = min(atk.x,tar.x)
    bx = max(atk.x,tar.x)
    sy = min(atk.y,tar.y)
    by = max(atk.y,tar.y)
    sh = min(atk.a,tar.h)
##    bh = max(atk.h,tar.h)
    sf = min(a_t.h,t_t.h)

    #print("==="+str(tar.x)+"==="+str(tar.y)+"===")
    
    for y in range(by - sy + 1):
        for x in range(bx - sx + 1):
            h_val = fm.tiles[sy + y][sx + x].h
            if fm.objects[sy + y][sx + x]:
                if fm.objects[sy + y][sx + x].type_id in blocks_values:
                    h_val += 1
            if h_val > sh:
                height.append([sx + x,sy + y,h_val - sf,fm.tiles[sy + y][sx + x].h - sf])
                #x,y,Net height,Base height

##    pr = False
##    if atk.h > tar.h:
##        pr = True
##        print(height)
                
    #Top View Check
    #print("Pre: "+str(height))
    test_rect = pygame.Rect((0,0,fm.w,fm.w))
    for i in list(height):
        test_rect.center = [fm.s_x + i[0] * fm.w, fm.s_y + i[1] * fm.w]
        clp = test_rect.clipline([a_pos,t_pos])
        if len(clp) == 0:
            height.remove(i)

    #print("Top: "+str(height)) 
    if len(height) == 0:
        fm.QuickSetView(fm_desc,fm_v,fm_h)
        return []#True
    
    #Front View Check
    v = 0
    for i in list(height):
        test_rect = pygame.Rect((0,0,fm.w,fm.w * i[2]))#fm.cv * i[2]))
        test_rect.centerx = fm.s_x + i[0] * fm.w
        test_rect.top = sf * fm.w
        clp = test_rect.clipline([a_pos[0], atk.h * fm.w],[t_pos[0], tar.h * fm.w])
        
        if not clp:
            height.remove(i)
            v -= 1
        else:
            test_rect = pygame.Rect((0,0,fm.w,fm.w * i[3]))
            test_rect.centerx = fm.s_x + i[0] * fm.w
            test_rect.top = sf * fm.w
            clp = test_rect.clipline([a_pos[0], atk.h * fm.w],[t_pos[0], tar.h * fm.w])
            if clp:
                height[v].append(True)
            else:
                height[v].append(False)
        v += 1

    #print("Front: "+str(height))
    if len(height) == 0:
        fm.QuickSetView(fm_desc,fm_v,fm_h)
        return []#True

    #Side View Check
    v = 0
    for i in list(height):
        test_rect = pygame.Rect((0,0,fm.w,fm.w * i[2]))#fm.cv * i[2]))
        test_rect.centerx = fm.s_y + i[1] * fm.w
        test_rect.top = sf * fm.w
        clp = test_rect.clipline([a_pos[1], atk.h * fm.w],[t_pos[1], tar.h * fm.w])
        if not clp:
            height.remove(i)
            v -= 1
        else:
            test_rect = pygame.Rect((0,0,fm.w,fm.w * i[3]))
            test_rect.centerx = fm.s_x + i[0] * fm.w
            test_rect.top = sf * fm.w
            clp = test_rect.clipline([a_pos[0], atk.h * fm.w],[t_pos[0], tar.h * fm.w])
            if clp:
                height[v].append(True)
            else:
                height[v].append(False)
        v += 1
            
    #print("Side: "+str(height))
    if len(height) == 0:
        fm.QuickSetView(fm_desc,fm_v,fm_h)
        return []#True
    else:
        test_rect = pygame.Rect((0,0,fm.w,fm.w))
        c = []
        for i in list(height):
            test_rect.center = [fm.s_x + i[0] * fm.w, fm.s_y + i[1] * fm.w]
            clp = test_rect.clipline([a_pos,t_pos])
##            print(clp)
##            print(test_rect.bottom)
            
            if CheckifBlock(i[0],i[1]):
                if i[4] or i[5]:
                    c.append([clp[0],i[0],i[1],0,Distance_Pt(a_pos,clp[0])]) #Terrain with Untouched cover above
                elif fm.objects[i[1]][i[0]].type_id in unbreakable_values:
                    c.append([clp[0],i[0],i[1],1,Distance_Pt(a_pos,clp[0])]) #Unbreakable Cover
                else:
                    c.append([clp[0],i[0],i[1],2,Distance_Pt(a_pos,clp[0])]) #Other Cover
            else:
                c.append([clp[0],i[0],i[1],0,Distance_Pt(a_pos,clp[0])]) #Terrain
        d = []
        swapped = False
        for i in range(len(c)-1):
            for j in range(len(c)-i-1):
                if c[j][4] > c[j + 1][4]:
                    swapped = True
                    c[j], c[j + 1] = c[j + 1], c[j]
            if not swapped:
                break
            
        for i in c:
            collision.append([i[0],i[1],i[2],i[3]])
            if not i[3]:
                break
        #print(collision)
        fm.QuickSetView(fm_desc,fm_v,fm_h)
        return collision#False

def GetEffectClr(effect):
    f = EffectClrs.get(effect)
    if f:
        return f()
    else:
        return GetMagicClr()
    #return eval("Get"+effect+"Clr()")

def GetMagicClr():
    return (randint(98,174),randint(98,194),255) #98, 218, 255  174, 98, 255

def GetMagicClrII():
    return (randint(204,215),randint(204,252),255)# 204, 252, 255   215, 204, 255 
    #(randint(170,200),220,randint(200,255)) 

def GetEtherClr():
    return (randint(138,177),233,randint(216,239)) # 177, 233, 216  138, 233, 239 

def GetBurnClr():
    return (255,randint(63,146),0)

def GetFreezeClr():
    return (randint(190,225),randint(230,250),randint(250,255))

def GetShockClr():
    if randint(0,1) == 0:
        return (255,randint(209,247),0) #255,247,0
    else:
        return (randint(120,150),randint(226,240),randint(223,237)) #150, 240, 237  120, 226, 223 

def GetSplashClr():
    return (randint(135,155),randint(165,210),255)

def GetPoisonClr():
    if randint(0,2) < 2:
        if randint(0,1) < 1:
            return (randint(36,50),randint(113,126),randint(24,40))
        else:
            return (randint(65,80),randint(148,160),randint(15,27))
    else:
        return (randint(62,64),randint(92,112),randint(24,35))

def GetDrainClr():
    if randint(0,2) < 2:
        return (randint(201,206),randint(118,160),randint(237,245))
    else:
        return (randint(145,155),randint(87,94),randint(165,195))

def GetBlindClr(): #25, 39, 97  58, 66, 127 
    return (randint(25,58),randint(39,66),randint(97,127))

def GetCorruptionClr(): 
    return (randint(120,150),randint(15,25),randint(180,190))
##def GetCorruptionClr():
##    return (randint(58,71),randint(15,29),randint(97,148))

EffectClrs = {"Burn": GetBurnClr,
              "Freeze": GetFreezeClr,
              "Splash": GetSplashClr,
              "Shock": GetShockClr,
              "Poison": GetPoisonClr,
              "Drain": GetDrainClr,
              "Blind": GetBlindClr,
              "Ether": GetEtherClr,
              "Corruption": GetCorruptionClr}

def SetShockwave(x,y,r):
    fm = tile_sprites.sprites()[0]
    for i in range(fm.d[1]):
        if abs(i - y) <= r:
            for j in range(fm.d[0]):
                if fm.tiles[i][j].type_id != 0 and abs(j - x) <= r:
                    d = Distance_Pt([x,y],[j,i])
                    if d <= r + 0.5:
                        if len(fm.tiles[i][j].ch) == 0:
                            fm.tiles[i][j].h = fm.tiles[i][j].th
                            fm.tiles[i][j].ch.append([0,int(d + 1) * 10])
                            fm.tiles[i][j].ch.append([0.04,20])
                            #fm.tiles[i][j].ch.append([-0.04,20])

highlight_clrs = [(255,255,255),
                  (255,95,95), #1 Red
                  (255,185,95), #2 Orange
                  (255,255,95), #3 Yellow
                  (95,255,130), #4 Light-Green
                  (95,195,255), #5 Light-Blue
                  (95,105,255), #6 Blue
                  (185,95,255), #7 Purple
                  (244,95,255), #8 Magenta
                  ]

dark_highlight_clrs = []
for i in highlight_clrs:
    dark_highlight_clrs.append(Darken(i,40))

target_clrs = [(255,255,255),
               (240,125,125), #1 Red
               (240,180,125), #2 Orange
               (240,240,125), #3 Yellow
               (125,240,130), #4 Light-Green
               (125,225,240), #5 Light-Blue
               (125,155,240), #6 Blue
               (185,125,240), #7 Purple
               (225,125,240), #8 Magenta
               ]

def GetTilesInRange(x,y,r):
    fm = tile_sprites.sprites()[0]
    l = []
    for i in range(fm.d[1]):
        if abs(i - y) <= r:
            for j in range(fm.d[0]):
                if fm.tiles[i][j].type_id != 0 and abs(j - x) <= r:
                    if Distance_Pt([x,y],[j,i]) <= r + 0.5:
                        l.append(fm.tiles[i][j])
    return l

def GetUnitsInRange(x,y,r,f = [1],IgnoreInvisible = True):
    fm = tile_sprites.sprites()[0]
    l = []
    if f == None or f == []:
        for i in fm.units_list:
            if Distance_Pt([x,y],[i.x,i.y]) <= r + 0.5:
                if IgnoreInvisible or not i.Invisible:
                    l.append(i)
    else:
        for i in fm.units_list:
            if i.faction in f and Distance_Pt([x,y],[i.x,i.y]) <= r + 0.5:
                if IgnoreInvisible or not i.Invisible:
                    l.append(i)
    return l

def GetClosestUnitInRange(x,y,r,ef = [0],exclude = [],IgnoreInvisible = True):
    fm = tile_sprites.sprites()[0]
    l = None
    md = 9999
    for i in fm.units_list:
        d = Distance_Pt([x,y],[i.x,i.y])
        if (IgnoreInvisible or not i.Invisible) and i.faction not in ef and i not in exclude and d <= r + 0.5 and d < md:
            l = i
            md = d
    return l

def ClearAllTiles():
    ClearAllHighlightTiles()
    ClearAllBoundaryTiles()
    

def SetTargetTile(u,c = 5):
    fm = tile_sprites.sprites()[0]
    fm.targets[u.y][u.x] = c

def ClearTargetTile(u):
    fm = tile_sprites.sprites()[0]
    fm.targets[u.y][u.x] = None

def ClearAllTargetTiles():
    fm = tile_sprites.sprites()[0]
    for y in range(fm.d[1]):
        for x in range(fm.d[0]):
            fm.targets[y][x] = None

def DrawUnitSelect(u,l):
    fm = tile_sprites.sprites()[0]
    x = cos(radians(l)) * 10
    y = sin(radians(l)) * 10
    t = fm.tiles[u.y][u.x]
    c = target_clrs[fm.targets[u.y][u.x]]
    pts = [[t.bl[0] + 1,t.bl[1] - 1],
           [t.tl[0] + 1,t.tl[1] + 1],
           [t.tr[0] - 1,t.tr[1] + 1],
           [t.br[0] - 1,t.br[1] - 1]]
    cy = u.rect.top
    a_pts = [[u.rect.centerx, cy - 40 - y],
             [u.rect.centerx - x, cy - 60 - y],
             [u.rect.centerx + x, cy - 60 - y]]
    pygame.draw.lines(game_window,c,True,pts,width = 3)
    pygame.draw.polygon(game_window,c,a_pts)


def SetBoundaryTiles(x,y,r,c = 5, exclude = 0):
    fm = tile_sprites.sprites()[0]
    for i in range(fm.d[1]):
        if abs(i - y) <= r:
            for j in range(fm.d[0]):
                if fm.tiles[i][j].type_id != 0 and abs(j - x) <= r:
                    if Distance_Pt([x,y],[j,i]) <= r + 0.5:
                        if exclude == -1 or not CheckifUnit(j,i,exclude):
                            fm.boundaries[i][j] = c

def ClearAllBoundaryTiles():
    fm = tile_sprites.sprites()[0]
    for y in range(fm.d[1]):
        for x in range(fm.d[0]):
            fm.boundaries[y][x] = None

def ClearBoundaryTiles(x,y,r):
    fm = tile_sprites.sprites()[0]
    for i in range(fm.d[1]):
        if abs(i - y) <= r:
            for j in range(fm.d[0]):
                if abs(j - x) <= r:
                    if Distance_Pt([x,y],[j,i]) <= r + 0.5:
                        fm.boundaries[i][j] = None

def DrawTileBound(t):
    fm = tile_sprites.sprites()[0]
    e_pts = []
    clrs = []
    n,e,s,w,sl,sr = False,False,False,False,False,False
    if t.x == 0:
        e_pts.append([[t.tl[0] + 1,t.tl[1]],
                      [t.bl[0] + 1,t.bl[1]]])
        w = True
        clrs.append(True)
    elif fm.boundaries[t.y][t.x-1] == None: 
        e_pts.append([[t.tl[0] + 1,t.tl[1]],
                      [t.bl[0] + 1,t.bl[1]]])
        w = True
        clrs.append(True)
    if t.x == t.fm.d[0] - 1:
        e_pts.append([[t.tr[0] - 1,t.tr[1]],
                      [t.br[0] - 1,t.br[1]]])
        e = True
        clrs.append(True)
    elif fm.boundaries[t.y][t.x + 1] == None:
        e_pts.append([[t.tr[0] - 1,t.tr[1]],
                      [t.br[0] - 1,t.br[1]]])
        e = True
        clrs.append(True)
    if t.y == 0:
        e_pts.append([[t.tl[0],t.tl[1] + 1],
                      [t.tr[0],t.tr[1] + 1]])
        n = True
        clrs.append(True)
    elif fm.boundaries[t.y - 1][t.x] == None:
        e_pts.append([[t.tl[0],t.tl[1] + 1],
                      [t.tr[0],t.tr[1] + 1]])
        n = True
        clrs.append(True)
    if t.y == t.fm.d[1] - 1:
        e_pts.append([[t.bl[0],t.bl[1] - 1],
                      [t.br[0],t.br[1] - 1]])
        s = True
        clrs.append(True)
    elif fm.boundaries[t.y + 1][t.x] == None:
        e_pts.append([[t.bl[0],t.bl[1] - 1],
                      [t.br[0],t.br[1] - 1]])
        s = True
        clrs.append(True)

    if t.x != 0 and t.y != 0:
        if fm.boundaries[t.y - 1][t.x - 1] == None:
            e_pts.append([[t.tl[0] + 1,t.tl[1]],
                          [t.tl[0] + 1,t.tl[1] + 2]])
            n,w = True,True
            clrs.append(True)
    if t.x != t.fm.d[0] - 1 and t.y != 0:
        if fm.boundaries[t.y - 1][t.x + 1] == None:
            e_pts.append([[t.tr[0] - 1,t.tr[1]],
                          [t.tr[0] - 1,t.tr[1] + 2]])
            n,e = True,True
            clrs.append(True)
    if t.x != t.fm.d[0] - 1 and t.y != t.fm.d[1] - 1:
        if fm.boundaries[t.y + 1][t.x + 1] == None:
            e_pts.append([[t.br[0] - 1,t.br[1] - 2],
                          [t.br[0] - 1,t.br[1]]])
            s,e = True,True
            clrs.append(True)
    if t.x != 0 and t.y != t.fm.d[1] - 1:
        if fm.boundaries[t.y + 1][t.x - 1] == None:
            e_pts.append([[t.bl[0] + 1,t.bl[1] - 2],
                          [t.bl[0] + 1,t.bl[1]]])
            s,w = True,True
            clrs.append(True)


    if t.y < t.fm.d[1] - 1 and w:
        dt = fm.tiles[t.y + 1][t.x]
        if t.x > 0:
            dlt = fm.tiles[t.y + 1][t.x - 1]
            if dlt.h < t.h and fm.boundaries[dlt.y][dlt.x] and (fm.boundaries[t.y][t.x - 1] == None or fm.boundaries[dlt.y][dlt.x] == None):#fm.boundaries[t.y][t.x - 1] == None:
                e_pts.insert(0,[[t.bl[0] + 1,t.bl[1]],
                                [t.bl[0] + 1,t.bl[1] + (t.h - dt.h) * fm.v]])
                clrs.insert(0,False)
            elif dt.h < t.h and fm.boundaries[dt.y][dt.x] and (fm.boundaries[t.y][t.x - 1] == None or fm.boundaries[dlt.y][dlt.x] == None):#fm.boundaries[t.y][t.x - 1] == None:
                e_pts.insert(0,[[t.bl[0] + 1,t.bl[1]],
                                [t.bl[0] + 1,t.bl[1] + (t.h - dt.h) * fm.v]])
                clrs.insert(0,False)
        elif dt.h < t.h and fm.boundaries[dt.y][dt.x]:
            e_pts.insert(0,[[t.bl[0] + 1,t.bl[1]],
                            [t.bl[0] + 1,t.bl[1] + (t.h - dt.h) * fm.v]])
            clrs.insert(0,False)

    if t.y < t.fm.d[1] - 1 and e:
        dt = fm.tiles[t.y + 1][t.x]
        if t.x < t.fm.d[0] - 1:
            drt = fm.tiles[t.y + 1][t.x + 1]
            if drt.h < t.h and fm.boundaries[drt.y][drt.x] and (fm.boundaries[t.y][t.x + 1] == None or fm.boundaries[drt.y][drt.x] == None):
                e_pts.insert(0,[[t.br[0] - 1,t.br[1]],
                                [t.br[0] - 1,t.br[1] + (t.h - dt.h) * fm.v]])
                clrs.insert(0,False)
            elif dt.h < t.h and fm.boundaries[dt.y][dt.x] and (fm.boundaries[t.y][t.x + 1] == None or fm.boundaries[drt.y][drt.x] == None):
                e_pts.insert(0,[[t.br[0] - 1,t.br[1]],
                                [t.br[0] - 1,t.br[1] + (t.h - dt.h) * fm.v]])
                clrs.insert(0,False)
        elif dt.h < t.h and fm.boundaries[dt.y][dt.x]:
            e_pts.insert(0,[[t.br[0] - 1,t.br[1]],
                            [t.br[0] - 1,t.br[1] + (t.h - dt.h) * fm.v]])
            clrs.insert(0,False)

    for i in range(len(e_pts)):
        if clrs[i]:
            pygame.draw.line(game_window,highlight_clrs[fm.boundaries[t.y][t.x]],e_pts[i][0],e_pts[i][1],width = 3)
        else:
            pygame.draw.line(game_window,dark_highlight_clrs[fm.boundaries[t.y][t.x]],e_pts[i][0],e_pts[i][1],width = 3)

def SetGlowTiles(x,y,r,c = 5):
    fm = tile_sprites.sprites()[0]
    for i in range(fm.d[1]):
        if abs(i - y) <= r:
            for j in range(fm.d[0]):
                if fm.tiles[i][j].type_id != 0 and abs(j - x) <= r:
                    if Distance_Pt([x,y],[j,i]) <= r + 0.5:
                        fm.glowframes[i][j] = c

def ClearAllGlowTiles():
    fm = tile_sprites.sprites()[0]
    for y in range(fm.d[1]):
        for x in range(fm.d[0]):
            fm.glowframes[y][x] = None

def ClearGlowTiles(x,y,r):
    fm = tile_sprites.sprites()[0]
    for i in range(fm.d[1]):
        if abs(i - y) <= r:
            for j in range(fm.d[0]):
                if abs(j - x) <= r:
                    if Distance_Pt([x,y],[j,i]) <= r + 0.5:
                        fm.glowframes[i][j] = None

def DrawTileGlow(t,lp):
    lp = lp % 90 // 18
    fm = tile_sprites.sprites()[0]
    n,e,s,w,sl,sr = False,False,False,False,False,False

    if t.x == 0:
        w = True
    elif fm.glowframes[t.y][t.x-1] == None: 
        w = True
    if t.x == t.fm.d[0] - 1:
        e = True
    elif fm.glowframes[t.y][t.x + 1] == None:
        e = True
    if t.y == 0:
        n = True
    elif fm.glowframes[t.y - 1][t.x] == None:
        n = True
    if t.y == t.fm.d[1] - 1:
        s = True
    elif fm.glowframes[t.y + 1][t.x] == None:
        s = True

##    if t.y < t.fm.d[1] - 1 and w:
##        dt = fm.tiles[t.y + 1][t.x]
##        if t.x > 0:
##            dlt = fm.tiles[t.y + 1][t.x - 1]
##            if dlt.h < t.h and fm.glowframes[dlt.y][dlt.x]:
##                sl = True
##                sld = t.h - dlt.h
##            elif dt.h < t.h and fm.glowframes[dt.y][dt.x]:
##                sl = True
##                sld = t.h - dt.h
##        elif dt.h < t.h and fm.glowframes[dt.y][dt.x]:
##            sl = True
##            sld = t.h - dt.h
##
##    if t.y < t.fm.d[1] - 1 and e:
##        dt = fm.tiles[t.y + 1][t.x]
##        if t.x < t.fm.d[0] - 1:
##            drt = fm.tiles[t.y + 1][t.x + 1]
##            if drt.h < t.h and fm.glowframes[drt.y][drt.x]:
##                sr = True
##                srd = t.h - drt.h
##            elif dt.h < t.h and fm.glowframes[dt.y][dt.x]:
##                sr = True
##                srd = t.h - dt.h
##        elif dt.h < t.h and fm.glowframes[dt.y][dt.x]:
##            sr = True
##            srd = t.h - dt.h
        
    dc = 5
    sh = 2
    tw,th = fm.w,fm.h
    if n:
        r = lp
        for i in range(dc):
            pygame.draw.circle(game_window,highlight_clrs[fm.glowframes[t.y][t.x]],[t.tl[0] + tw * (i + 0.5)/dc,t.tl[1] + sh],1+(dc-r)/2)
            r = (r - 1)%dc
    if e:
        r = lp
        for i in range(dc):
            pygame.draw.circle(game_window,highlight_clrs[fm.glowframes[t.y][t.x]],[t.tr[0] - sh,t.tl[1] + th * (i + 0.5)/dc],1+(dc-r)/2)
            r = (r - 1)%dc
    if s:
        r = lp
        for i in range(dc):
            pygame.draw.circle(game_window,highlight_clrs[fm.glowframes[t.y][t.x]],[t.br[0] - tw * (i + 0.5)/dc,t.br[1] - sh],1+(dc-r)/2)
            r = (r - 1)%dc
    if w:
        r = lp
        for i in range(dc):
            pygame.draw.circle(game_window,highlight_clrs[fm.glowframes[t.y][t.x]],[t.bl[0] + sh,t.bl[1] - th * (i + 0.5)/dc],1+(dc-r)/2)
            r = (r - 1)%dc

##    if sl:
##        r = lp 
##        v = fm.v * sld
##        for i in range(dc):
##            pygame.draw.circle(game_window,highlight_clrs[fm.glowframes[t.y][t.x]],[t.bl[0] + sh,t.bl[1] + v - v * (i + 0.5)/dc],1+(dc-r)/2)
##            r = (r - 1)%dc
##
##    if sr:
##        r = lp 
##        v = fm.v * srd
##        for i in range(dc):
##            pygame.draw.circle(game_window,highlight_clrs[fm.glowframes[t.y][t.x]],[t.br[0] - sh,t.br[1] + v * (i + 0.5)/dc],1+(dc-r)/2)
##            r = (r - 1)%dc

def SetHighlightTiles(x,y,r,c = 5):
    fm = tile_sprites.sprites()[0]
    for i in range(fm.d[1]):
        if abs(i - y) <= r:
            for j in range(fm.d[0]):
                if fm.tiles[i][j].type_id != 0 and abs(j - x) <= r:
                    if Distance_Pt([x,y],[j,i]) <= r + 0.5:
                        fm.highlights[i][j].append(c)

def ClearAllHighlightTiles():
    fm = tile_sprites.sprites()[0]
    for y in range(fm.d[1]):
        for x in range(fm.d[0]):
            fm.highlights[y][x] = []

def ClearHighlightTiles(x,y,r, c = None):
    fm = tile_sprites.sprites()[0]
    if c:
        for i in range(fm.d[1]):
            if abs(i - y) <= r:
                for j in range(fm.d[0]):
                    if abs(j - x) <= r:
                        if c in fm.highlights[i][j] and Distance_Pt([x,y],[j,i]) <= r + 0.5:
                            fm.highlights[i][j].remove(c)
    else:
        for i in range(fm.d[1]):
            if abs(i - y) <= r:
                for j in range(fm.d[0]):
                    if abs(j - x) <= r:
                        if Distance_Pt([x,y],[j,i]) <= r + 0.5:
                            fm.highlights[i][j] = []

def GetMovableRange(x,y,r,c = 6,unit = None):
    fm = tile_sprites.sprites()[0]
    #t = []
    a = []
    v = []
    s = []
    for i in range(fm.d[1]):
        a.append([])
        v.append([])
        for j in range(fm.d[0]):
            a[i].append(x == j and y == i)
            if abs(i - y) <= r and abs(j - x) <= r:
                if not CheckifPassable(j,i):
                    v[i].append(False)
                elif not CheckifSteppable(j,i):
                    v[i].append(False)
                elif CheckifUnit(j,i):
                    v[i].append(False)
                elif Distance_Pt([x,y],[j,i]) <= r + 0.5:
                    v[i].append(True)
                else:
                    v[i].append(False)
            else:
                v[i].append(False)
    s.append(fm.tiles[y][x])
    a[y][x] = True
    if unit and [unit.x,unit.y] != [x,y]:
        s.append(fm.tiles[unit.y][unit.x])
        a[unit.y][unit.x] = True
    ch = True
    l = 0
    while ch:
        ch = False
        for i in range(fm.d[1]):
            if l % 2 == 1:
                p = fm.d[1] - 1 - i
            else:
                p = i
            if abs(p - y) <= r:
                for j in range(fm.d[0]):
                    if l % 2 == 0:
                        q = fm.d[0] - 1 - j
                    else:
                        q = j
                    if v[p][q] and not a[p][q]:
                        t = fm.tiles[p][q]
                        if q != 0 and a[p][q-1] and abs(t.h - fm.tiles[p][q-1].h) <= 1:
                            a[p][q] = True
                            s.append(t)
                            ch = True
                        elif q != fm.d[0] - 1 and a[p][q+1] and abs(t.h - fm.tiles[p][q+1].h) <= 1:
                            a[p][q] = True
                            s.append(t)
                            ch = True
                        elif p != 0 and a[p-1][q] and abs(t.h - fm.tiles[p-1][q].h) <= 1:
                            a[p][q] = True
                            s.append(t)
                            ch = True
                        elif p != fm.d[1] - 1 and a[p+1][q] and abs(t.h - fm.tiles[p+1][q].h) <= 1:
                            a[p][q] = True
                            s.append(t)
                            ch = True
        l += 1
        #a.append(fm.tiles[unit.y][unit.x])
##        print("<"+str(l)+">")
##        for i in range(fm.d[1]):
##            for j in range(fm.d[0]):
##                if i == y and j == x:
##                    print(" ", end = "")
##                else:
##                    print(1 if a[i][j] else 0, end = "")
##            print("")

##        for i in range(fm.d[1]):
##            if abs(i - y) <= r:
##                for j in range(fm.d[0]):
##                    if v[i][j] and not a[i][j]:
##                        t = fm.tiles[i][j]
##                        if j != 0 and a[i][j-1] and abs(t.h - fm.tiles[i][j-1].h) <= 1:
##                            a[i][j] = True
##                            s.append(t)
##                            c = True
##                        elif j != fm.d[0] - 1 and a[i][j+1] and abs(t.h - fm.tiles[i][j+1].h) <= 1:
##                            a[i][j] = True
##                            s.append(t)
##                            c = True
##                        elif i != 0 and a[i-1][j] and abs(t.h - fm.tiles[i-1][j].h) <= 1:
##                            a[i][j] = True
##                            s.append(t)
##                            c = True
##                        elif i != fm.d[1] - 1 and a[i+1][j] and abs(t.h - fm.tiles[i+1][j].h) <= 1:
##                            a[i][j] = True
##                            s.append(t)
##                            c = True
    if c:
        for i in range(fm.d[1]):
            for j in range(fm.d[0]):
                if a[i][j]:
                    fm.boundaries[i][j] = c
                    fm.highlights[i][j].append(c)
    return s
