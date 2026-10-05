import pygame
from VoxelGame_BaseVars import *

icon_path = "./_Symbol/"

l = ["hp","atk","def","crit","target_range","duration","cd","aoe_range"]
for j in range(2):
    for i in range(4):
        exec(l[j * 4 + i].lower()+"_symbol = pygame.Surface((15,15))")
        exec(l[j * 4 + i].lower()+"_symbol.fill((255,255,255))") #Uses white rectangles as placeholders

l = ["phase","chain","spread","fragilize"]
for i in range(len(l)):
    exec(l[i].lower()+"_symbol = pygame.Surface((21,19))")
    exec(l[i].lower()+"_symbol.fill((255,255,255))") #Uses white rectangles as placeholders

l = list(SE_colour_set.keys())
j = 0
i = 0
for k in range(len(l)):
    if " " in l[k]:
        break
    exec(l[k].lower()+"_symbol = pygame.Surface((21,19))") #Uses coloured stars as placeholders
    exec(l[k].lower()+"_symbol.fill((128,128,128))")
    exec(l[k].lower()+"_symbol.set_colorkey((128,128,128))")
    pygame.draw.polygon(eval(l[k].lower()+"_symbol"), SE_colour_set[l[k]], [(0,10),(7,7),(10,0),(13,7),(20,10),(13,13),(10,19),(7,13)])
    
    i += 1
    if i == 4:
        i = 0
        j += 1

SE_Symbols = {"Burn": burn_symbol,
              "Freeze": freeze_symbol,
              "Shock": shock_symbol,
              "Splash": splash_symbol,
              "Poison": poison_symbol,
              "Drain": drain_symbol,
              "Curse": curse_symbol,
              "Blind": blind_symbol,
              "Regeneration": regeneration_symbol,
              "Invisible": invisible_symbol,
              "Invincible": invincible_symbol,
              "Quicken": quicken_symbol,
              "Strengthen": strengthen_symbol,
              "Weaken": weaken_symbol,
              "Reinforce": reinforce_symbol,
              "Vulnerable": vulnerable_symbol,
              "Lucky": lucky_symbol,
              "Unlucky": unlucky_symbol,
              "Reflect": reflect_symbol,
              "Thorns": thorns_symbol,
              "Fire Resistance": burn_symbol,
              "Ice Resistance": freeze_symbol,
              "Electric Resistance": shock_symbol,
              "Water Resistance": splash_symbol,
              "Poison Resistance": poison_symbol,
              "Gust Resistance": drain_symbol,
              "Shadow Resistance": blind_symbol,
              "Fire Weakness": burn_symbol,
              "Ice Weakness": freeze_symbol,
              "Electric Weakness": shock_symbol,
              "Water Weakness": splash_symbol,
              "Poison Weakness": poison_symbol,
              "Gust Weakness": drain_symbol,
              "Shadow Weakness": blind_symbol,
              }

SE_Gray_Symbols = {}
l = list(SE_colour_set.keys())
j = 0
i = 0

grey_star_temp = pygame.Surface((21,19))
grey_star_temp.fill((128,128,128))
grey_star_temp.set_colorkey((128,128,128))
pygame.draw.polygon(grey_star_temp, (175,175,175), [(0,10),(7,7),(10,0),(13,7),(20,10),(13,13),(10,19),(7,13)])

for k in range(len(l)):
    if " " in l[k]:
        break
    exec("grey"+l[k].lower()+"_symbol = grey_star_temp") #Greyed Stars as placeholders
    SE_Gray_Symbols.update({l[k]: eval("grey"+l[k].lower()+"_symbol")})
    i += 1
    if i == 4:
        i = 0
        j += 1

l = ["fire","ice","electric","water","poison","gust","shadow","terra","light","astral","ether","corruption"]
j = 0
i = 0
for k in range(len(l)):
    exec(l[k].lower()+"_symbol = pygame.Surface((21,19))")
    exec(l[k].lower()+"_symbol.fill((255,255,255))") #Use white rect as placeholders
    i += 1
    if i == 4:
        i = 0
        j += 1

l = ["Shock","Freeze","Poison","Burn","Splash","Drain","Blind","Curse"]
for i in range(len(l)):
    exec(l[i].lower()+"_text_symbol = pygame.Surface((121,38))") #121,38
    exec(l[i].lower()+"_text_symbol.fill(SE_colour_set[l[i]])")

SE_TextImg = {"Burn": burn_text_symbol,
              "Freeze": freeze_text_symbol,
              "Shock": shock_text_symbol,
              "Splash": splash_text_symbol,
              "Poison": poison_text_symbol,
              "Drain": drain_text_symbol,}

Element_Symbols = {"Fire": fire_symbol,
                   "Ice": ice_symbol,
                   "Electric": electric_symbol,
                   "Water": water_symbol,
                   "Poison": poison_symbol,
                   "Gust": gust_symbol,
                   "Shadow": shadow_symbol,
                   "Light": light_symbol,
                   "Terra": terra_symbol,
                   "Ether": ether_symbol,
                   "Astral": astral_symbol,
                   "Corruption": corruption_symbol}

SE_width = burn_symbol.get_width()
ES_width = fire_symbol.get_width()


l = [["magic","burn","freeze","shock","splash","poison","drain","blind","corruption"],
     [],
     ["magic","burn","freeze","shock","splash","poison","drain","blind","corruption"],
     ["heal","restrict","silence","reflect","invincible","bubble","shatter","disable","strengthen","weaken","reinforce","vulnerable"],
     ["quicken","invinsible","portal_ambush","redistribute","vortex"],
     ["movement","trailblaze","teleport","dash","jump","climb","flight"],
     ["true_invincibility","fire_affinity","electric_affinity","poison_affinity","ice_affinity","water_affinity","shadow_affinity","gust_affinity","ailment_immunity","effect_immunity"],
     ["unseen","unhealable"],
     ["astral_copy","astral_shift","field_shifter","field_breaker","aggravate","submerge"],
     ["status_transfer","last_blow","vengeance","aggravate"],]
t = ["_projectile",
     "",
     "_shockwave",
     "",
     "",
     "",
     "",
     "",
     "",
     ""]
for i in range(len(l)):
    for j in range(len(l[i])):
        exec(l[i][j].lower()+t[i]+"_icon = pygame.Surface((25,25))")
        exec(l[i][j].lower()+t[i]+"_icon.set_colorkey((0,255,0))")
        exec(l[i][j].lower()+t[i]+"_icon.fill((0,255,0))")
        if l[i][j] == "movement":
            pygame.draw.polygon(movement_icon, (255,255,255), [(12,0),(15,5),(9,5)])
            pygame.draw.polygon(movement_icon, (255,255,255), [(25,12),(20,15),(20,9)])
            pygame.draw.polygon(movement_icon, (255,255,255), [(12,25),(15,20),(9,20)])
            pygame.draw.polygon(movement_icon, (255,255,255), [(0,12),(5,15),(5,9)])
            pygame.draw.rect(movement_icon, (255,255,255), [11,5,3,15])
            pygame.draw.rect(movement_icon, (255,255,255), [5,11,15,3])
        elif l[i][j] == "heal":
            pygame.draw.rect(heal_icon, (152,247,160), [8,0,10,25])
            pygame.draw.rect(heal_icon, (152,247,160), [0,8,25,10])
        elif i == 0:
            if j == 0:
                tmp_clr = (255,255,255)
            else:
                tmp_clr = SE_colour_set[l[i][j].capitalize()];
            pygame.draw.polygon(eval(l[i][j].lower()+t[i]+"_icon"), tmp_clr, [(0,0),(12,5),(25,0),(20,12),(25,25),(12,20),(0,25),(5,12)])
        else:
            pygame.draw.polygon(eval(l[i][j].lower()+t[i]+"_icon"), (255,255,255), [(0,12),(7,7),(12,0),(17,7),(25,12),(17,17),(12,25),(7,17)])
        #Star as placeholder icon

Projectile_Icons = {"Magic": magic_projectile_icon,
                    None: magic_projectile_icon,
                    "Burn": burn_projectile_icon,
                    "Freeze": freeze_projectile_icon,
                    "Shock": shock_projectile_icon,
                    "Splash": splash_projectile_icon,
                    "Poison": poison_projectile_icon,
                    "Drain": drain_projectile_icon,
                    "Blind": blind_projectile_icon,
                    "Corruption": corruption_projectile_icon,}

l = ["attack","skill","defense","mvm","resistance","weakness"]
for j in range(len(l)):
    exec(l[j].lower()+"_icon = pygame.Surface((23,23))")
    exec(l[j].lower()+"_icon.fill((255,255,255))") #Uses white rect as placeholders

missing_icon = pygame.Surface((18,18))
pygame.draw.rect(missing_icon, (255,0,255), (0,0,9,9))
pygame.draw.rect(missing_icon, (255,0,255), (9,9,9,9))

key_icons = []
small_key_icons = []
l = [["a","b","c","d","e"],["f","g","h","i","j"],["k","l","m","n","o"],["p","q","r","s","t"],["u","v","w","x","y"],["z"],
     ["0","1","2","3","4"],["5","6","7","8","9"],
     ["space","up","right","down","left"]]
for i in range(len(l)):
    for j in range(len(l[i])):
        exec("key_icon_"+l[i][j]+" = pygame.Surface((25,25))")
        eval("key_icon_"+l[i][j]+".set_colorkey((0,255,0))")
        exec("key_icon_"+l[i][j]+".fill((0,255,0))")
        pygame.draw.circle(eval("key_icon_"+l[i][j]), (255,255,255), (5,5), 5)
        pygame.draw.circle(eval("key_icon_"+l[i][j]), (255,255,255), (20,5), 5)
        pygame.draw.circle(eval("key_icon_"+l[i][j]), (255,255,255), (5,20), 5)
        pygame.draw.circle(eval("key_icon_"+l[i][j]), (255,255,255), (20,20), 5)
        pygame.draw.polygon(eval("key_icon_"+l[i][j]), (255,255,255), [(0,5),(5,0),(20,0),(25,5),(25,20),(20,25),(5,25),(0,20)])
        
        if (i != len(l) - 1):
            text = game_font16.render(l[i][j].upper(),True,(0,0,0))
        else:
            text = game_font16.render([" ", "^", "v","<",">"][j],True,(0,0,0))
        textRect = text.get_rect()
        textRect.centerx,textRect.centery = 12, 13
        exec("key_icon_"+l[i][j]+".blit(text,textRect)")
        
        key_icons.append(eval("key_icon_"+l[i][j]))
