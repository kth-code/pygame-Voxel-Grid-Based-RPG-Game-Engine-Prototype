import pygame
from random import *
from math import *
from VoxelGame_BaseVars import *
from VoxelGame_Visuals import *
from VoxelGame_ATKProjectiles import *

from VoxelGame_Icons import *

class Unit():
    def __init__(self, x = 0, y = 0, faction = 0, rh = 0.5, ra = 0.5, size = [15,35],unsteppable_types = unsteppable_values):
        self.fm = tile_sprites.sprites()[0]
        #Tile Position
        self.x = x
        self.y = y
        self.offx = 0
        self.offy = 0
        self.offh = 0
        self.offx_list = [] #[0.04,25]
        self.offy_list = [] #[0.04,25]
        self.offh_list = [] #[0.04,25]
        #Targeted Height
        self.rh = rh #Relative Hit Pos
        self.ra = ra #Relative ATK Pos
        self.h = self.fm.tiles[y][x].h + self.rh #Actual Hit Pos
        self.a = self.fm.tiles[y][x].h + self.ra #Actual ATK Pos
        #Screen Position
        #u = pygame.Surface(size)
        self.rect = pygame.Rect([0,0],size)#u.get_rect()
        self.bottom = self.fm.tiles[self.y][self.x].centery + 6 * self.fm.v/self.fm.cv
        self.centerx = self.fm.tiles[self.y][self.x].centerx
        #Stats
        self.HP = 100#randint(1,10)#10
        self.MaxHP = 100
        self.Pntl_MinHP = 0 #Potential Min. DMG/Heal
        self.Pntl_MaxHP = 0 #Potential Max. DMG/Heal
        self.Pntl_CritHP = 0 #Potential Max Crit. DMG/Heal
        self.Pntl_SE = None #Potential Status Effect
        self.Pntl_Hit = 0

        self.HP_Segment = 1

        self.ATK = 0
        self.DEF = 0 #DEF Against All DMG; Shield %
        self.PhyDEF = 0 #DEF Against Physical DMG; Shield %
        self.MgcDEF = 0 #DEF Against Magical DMG; Shield %

        self.Base_ATK = 0
        self.Base_DEF = 0
        self.Base_PhyDEF = 0
        self.Base_MgcDEF = 0

        self.Add_ATK, self.Mlt_ATK = 0,1
        self.Add_DEF, self.Mlt_DEF = 0,1
        self.Add_PhyDEF, self.Mlt_PhyDEF = 0,1
        self.Add_MgcDEF, self.Mlt_MgcDEF = 0,1
        self.Add_Crit, self.Mlt_Crit = 0,1
        self.Add_Range, self.Mlt_Range = 0,1
        self.Add_Mvm, self.Mlt_Mvm = 0,1

        self.unsteppable = unsteppable_types
        for i in SE_UnitName:
            exec("self."+i+" = False")

        self.mv_tiles = []

        self.stat_lp = 0
        self.icon_lp = 0
        self.icon_no = 0

        self.visual_sprites = []

        self.hp_threshold = []
        self.hp_threshold_act = []

        self.MinDMG = 0
        self.MaxDMG = -9999
        
        self.cls = []
        self.category = []
        self.magic_type = []

        self.effect_loop = 0
        self.StatusEffect = []
        self.EffectTimer = []
        self.SEVisual = []
        self.SE_Values = []
        
        self.Property = []

        self.Resistance = [] #Immune to -ve Effects of that element + DMG Reduction (-n%) to ATKs of that element
        self.Weakness = [] #Effect Enhancement + DMG Increment (+n%) to ATKs of that element
        self.Resist_Value = []
        self.Weak_Value = []
        #Effect Immunity ≠ DMG Reduction

        self.ReactCD = 0
        self.ReactCount = 0

        #Action
        self.can_act = False
        self.playable = False
        self.action_pts = 0
        self.act_record = [] #Can unit use a certain action
        self.act_CD = [] #Cooldown

        #Graphics
        self.icon = pygame.Surface((25,25))
        self.icon.fill((0,255,255))
        self.i_rect = self.icon.get_rect()

        #Info
        self.weapons = []
        
        self.faction = faction
        self.name = ""
        self.info = [] #Flavour text & Unit data
        self.move_type = [] #Types of each moveset entry
        self.move_label = [] #Titles of each moveset entry
        self.move_stat = [] #Whether DMG needs to be displays
        self.move_mlt = [] #DMG Multiplier of entry
        self.move_SE = [] #Status Effect of entry (if any)
        self.move_cd = [] #Cooldown for moveset (if any)
        self.move_crit = [] #Critical % for moveset (if any)
        self.move_info = [] #Info text of each moveset entry
        self.move_range = [] #Highlights and Range & Clr of each moveset entry
        self.move_get_tile = [] #Function for getting tiles of effect
        self.move_icon = []
        self.colour = []
        self.imgs = [] #Images used in info text

    def HPChange(self,change,effect = None,timer = 0,value = None,source_type = 0,attacker = None,breach = False,crit = False,clr = None,impact_pt = [],react = True):
        base_change = change
        if effect:
            if self.CheckifAffinity(effect):
                change = abs(change) * 0.5
                effect = None
        res = 0
        if not breach:
            if self.CheckifEffect("Invincible") and change < 0:
                n = self.GetSEIndex("Invincible")
                self.SE_Values[n] -= 1
                change = 0
                effect = None
                if self.SE_Values[n] == 0:
                    self.StatusEffect.pop(n)
                    self.EffectTimer.pop(n)
                    self.SEVisual.pop(n)
                    self.SE_Values.pop(n)
                    self.Invincible = False
            elif self.CheckifProperty("Invincible") and change < 0:
                change = 0
            else:
                prct = 100 #percentage
                if effect:
                    if self.CheckifResist(effect):
                        #change *= 0.5
                        prct -= self.Get_ResistValue(effect)#50
                        clr = (210,210,210)
                        res = 1
                    elif self.CheckifWeak(effect):
                        #change *= 1.5
                        prct += self.Get_WeakValue(effect)#50
                        res = 2

                    if effect == "Shock" and self.CheckifEffect("Splash"):
                        prct += 25
                    elif effect == "Corruption":
                        effect = None
                        
                    if effect:
                        if timer > 0 and not self.CheckifImmune(effect):
                            if not value and effect == "Burn":
                                value = CorInt(base_change * 0.15)
                            self.ApplyStatusEffect(effect,timer,value,applyer = attacker)
                        elif effect and res == 0:
                            clr = SE_colour_set.get(effect)
                            effect = None
                
                if change < 0:
                    prct -= self.Get_DEF()
                    change = change * (prct/100)
                    #change = change * (1 - self.Get_DEF()/100)
                    if source_type == 0:
                        change = change * (1 - self.Get_PhyDEF()/100)
                    elif source_type == 1:
                        change = change * (1 - self.Get_MgcDEF()/100)
                    if change < self.MaxDMG:
                        change = self.MaxDMG
                    elif change > self.MinDMG:
                        change = 0
        change = CorInt(change)
        self.HP += change
        if not clr:
            if change > 0:
                clr = (142,255,132)
            elif effect:
                clr = SE_colour_set.get(effect)
            else:
                clr = (255,255,255)
        if change <= 0:
            if crit:
                if res == 0:
                    PopUpText(txt = "CRITICAL",x = self.rect.centerx, y = self.rect.centery - 20,clr = clr,font = stat_font12)
                elif res == 1:
                    PopUpText(txt = "RESISTANT CRITICAL",x = self.rect.centerx, y = self.rect.centery - 20,clr = clr,font = stat_font12)    
                elif res == 2:
                    PopUpText(txt = "EFFECTIVE CRITICAL",x = self.rect.centerx, y = self.rect.centery - 20,clr = clr,font = stat_font12)
            else:
                if res == 1:
                    PopUpText(txt = "RESISTANT",x = self.rect.centerx, y = self.rect.centery - 20,clr = clr,font = stat_font12)    
                elif res == 2:
                    PopUpText(txt = "EFFECTIVE",x = self.rect.centerx, y = self.rect.centery - 20,clr = clr,font = stat_font12)
            #e_img = SE_TextImg.get(effect)
            PopUpText(txt = str(change),x = self.rect.centerx, y = self.rect.centery,clr = clr)#,img = e_img)
            if (effect):
                PopUpText(txt = effect,x = self.rect.left + 64, y = self.rect.centery,clr = clr)
        else:
            PopUpText(txt = "+"+str(change),x = self.rect.centerx, y = self.rect.centery,clr = clr)
            for i in range(6):
                MagicSwirl(self,i * 60,h = randint(40,80),colour = (140,255,150),w = 15,grow = randint(2,3)/10,l = randint(10,30),slant = randint(1,3)/10)

        
        if self.HP > self.MaxHP:
            self.HP = self.MaxHP
        elif self.HP < 0:
            self.HP = 0

        if react:
            self.ReactAttack(change,effect)

        if change < 0 and attacker and self.CheckifEffect("Drain"):
            Healing_Orb(self,attacker,abs(change * self.GetSEValue("Drain")))
        if base_change < 0 and attacker and self.CheckifEffect("Reflect"):
            Reflect_Orb(self,attacker,CorInt(base_change * self.GetSEValue("Reflect")/100))
        if base_change < 0 and attacker and self.CheckifEffect("Thorns"):
            Thorns_Orb(self,attacker,CorInt(base_change * self.GetSEValue("Thorns")/100))

    def ApplyStatusEffect(self,effect,turn,value = None,stack_threshold = None,applyer = None):
        if SE_Default_Stack.get(effect,3) <= 2 and self.CheckifImmune(effect):
            return

        if SE_Default_Stack.get(effect) == 4: #4 - Check Weaknesses
            if effect in self.StatusEffect:
                n = self.StatusEffect.index(effect)
                if stack_threshold:
                    if self.EffectTimer[n] <= stack_threshold:
                        self.EffectTimer[n] += turn
                else:
                    self.EffectTimer[n] += turn
            else:
                elmt = SE_Elements.get(effect)
                self.ClearStatusEffect(elmt+" Resistance")
                self.StatusEffect.append(effect)
                self.EffectTimer.append(turn)
                self.SEVisual.append(True)
                if value == None:
                    value = SE_Default_Values.get(effect)
                if elmt in self.Resistance:
                    self.SE_Values.append([value,elmt not in self.Weakness,self.Resist_Value[self.Resistance.index(elmt)]])
                    self.Resist_Value.pop(self.Resistance.index(elmt))
                    self.Resistance.remove(elmt)
                else:
                    self.SE_Values.append([value,elmt not in self.Weakness,None])
                if elmt not in self.Weakness:
                    self.Weakness.append(elmt)
                    self.Weak_Value.append(0)
                self.Weak_Value[self.Weakness.index(elmt)] += value
                
        elif SE_Default_Stack.get(effect) == 3: #3 - Check Resistances
            if effect in self.StatusEffect:
                n = self.StatusEffect.index(effect)
                if stack_threshold:
                    if self.EffectTimer[n] <= stack_threshold:
                        self.EffectTimer[n] += turn
                else:
                    self.EffectTimer[n] += turn
            else:
                elmt = SE_Elements.get(effect)
                self.ClearStatusEffect(elmt+" Weakness")
                self.StatusEffect.append(effect)
                self.EffectTimer.append(turn)
                self.SEVisual.append(True)
                if value == None:
                    value = SE_Default_Values.get(effect)
                if elmt in self.Weakness:
                    self.SE_Values.append([value,elmt not in self.Resistance,self.Weak_Value[self.Weakness.index(elmt)]])
                    self.Weak_Value.pop(self.Weakness.index(elmt))
                    self.Weakness.remove(elmt)
                else:
                    self.SE_Values.append([value,elmt not in self.Resistance,None])
                if elmt not in self.Resistance:
                    self.Resistance.append(elmt)
                    self.Resist_Value.append(0)
                self.Resist_Value[self.Resistance.index(elmt)] += value
                    
        elif SE_Default_Stack.get(effect) == 2: #2 - Independent Stack
            if effect in self.StatusEffect:
                n = self.StatusEffect.index(effect)
                if stack_threshold:
                    if len(self.SE_Values[n]) >= stack_threshold:
                        return
                if turn > self.EffectTimer[n]:
                    self.EffectTimer[n] = turn
                if value == None:
                    value = SE_Default_Values.get(effect)
                self.SE_Values[n].append([value,turn,applyer])
            else:
                self.StatusEffect.append(effect)
                self.EffectTimer.append(turn)
                self.SEVisual.append(False)
                if value == None:
                    value = SE_Default_Values.get(effect)
                self.SE_Values.append([[value,turn,applyer]])
        elif SE_Default_Stack.get(effect) == 1: #1 - Time/Val Stack
            if effect in self.StatusEffect:
                n = self.StatusEffect.index(effect)
                if stack_threshold:
                    if self.EffectTimer[n] <= stack_threshold:
                        self.EffectTimer[n] += turn
                        self.SE_Values[n] += value
                else:
                    self.EffectTimer[n] += turn
                    self.SE_Values[n] += value
            else:
                self.StatusEffect.append(effect)
                self.EffectTimer.append(turn)
                self.SEVisual.append(False)
                if value == None:
                    value = SE_Default_Values.get(effect)
                self.SE_Values.append(value)
        else: #0 - Timer Stack
            if effect in self.StatusEffect:
                n = self.StatusEffect.index(effect)
                if stack_threshold:
                    if self.EffectTimer[n] <= stack_threshold:
                        self.EffectTimer[n] += turn
                else:
                    self.EffectTimer[n] += turn
            else:
                self.StatusEffect.append(effect)
                self.EffectTimer.append(turn)
                self.SEVisual.append(False)
                if value == None:
                    value = SE_Default_Values.get(effect)
                self.SE_Values.append(value)
        self.EffectPostTurnStat()

    def ReactAttack(self,dmg = 0,effect = None):
        pass

    def ReactCountdown(self):
        pass

    def text_sort(self):
        w = 400
        font = game_font16
        r = 0
        txt = []
        for i in range(len(self.info)):
            c_t,t = "",""
            d = self.info[i].split()
            c = 0
            img_w = 0
            while c < len(d):
                c_t = ""
                img_w = 0
                txt.append([])
                while font.size(c_t)[0] + img_w < w and c < len(d):
                    if "#" in d[c]:
                        nw = self.imgs[int(d[c][1:])].get_width()
                    elif "@" in d[c]:
                        nw = font.size(d[c][2:])[0]
                    else:
                        nw = font.size(d[c])[0]
                    if font.size(c_t)[0] + nw + img_w < w:
                        if "#" in d[c]:
                            txt[r].append(d[c] + " ")
                            img_w += self.imgs[int(d[c][1:])].get_width()
                            if c + 1 < len(d):
                                if d[c+1] not in [".",",","!"]:
                                    txt[r].append(" ")
                                    c_t += " "
                        elif "@" in d[c]:
                            if d[c][-1:] in [".",",","!"]:
                                txt[r].append(d[c][:-1] )
                                txt[r].append(d[c][-1:] + " ")
                            else:
                                txt[r].append(d[c] + " ")
                            c_t += d[c][2:] + " "
                        else:
                            txt[r].append(d[c] + " ")
                            c_t += d[c] + " "
                        c += 1
                    else:
                        break
                r += 1
        self.info = list(txt)
        for h in range(len(self.move_info)):
            r = 0
            txt = []
            for i in range(len(self.move_info[h])):
                c_t,t = "",""
                d = self.move_info[h][i].split()
                if self.move_info[h][i] == "/b":
                    txt.append([])
                    d = []
                    r += 1
                c = 0
                img_w = 0
                while c < len(d):
                    c_t = ""
                    img_w = 0
                    txt.append([])
                    while font.size(c_t)[0] + img_w < w and c < len(d):
                        if "#" in d[c]:
                            nw = self.imgs[int(d[c][1:])].get_width()
                        elif "@" in d[c]:
                            nw = font.size(d[c][2:])[0]
                        else:
                            nw = font.size(d[c])[0]
                        if font.size(c_t)[0] + nw + img_w < w:
                            if "#" in d[c]:
                                txt[r].append(d[c] + " ")
                                img_w += self.imgs[int(d[c][1:])].get_width()
                                if c + 1 < len(d):
                                    if d[c+1] not in [".",",","!"]:
                                        txt[r].append(" ")
                                        c_t += " "
                            elif "@" in d[c]:
                                if d[c][-1:] in [".",",","!"]:
                                    txt[r].append(d[c][:-1] )
                                    txt[r].append(d[c][-1:] + " ")
                                else:
                                    txt[r].append(d[c] + " ")
                                c_t += d[c][2:] + " "
                            else:
                                txt[r].append(d[c] + " ")
                                c_t += d[c] + " "
                            c += 1
                        else:
                            break
                    r += 1
            self.move_info[h] = list(txt)   

    def Set_ActRecord(self):
        for j in self.move_type:
            if j in ["Attack","Skill","Starstone","Movement","Inventory"]:
                self.act_record.append(False)
                self.act_CD.append(0)

    def Set_ActPts(self,v):
        self.action_pts += v
        if self.action_pts == 0 and not self.act_record[-1]:
            if self in self.fm.acting_units:
                self.fm.acting_units.remove(self)
        elif self.act_record.count(True) == 0:
            if self in self.fm.acting_units:
                pself.fm.acting_units.remove(self)

    def update_pos(self):
        if self.fm.tiles[self.y][self.x].type_id in self.unsteppable:
            self.HPChange(-self.MaxHP * 0.1, breach = True)
            if self.HP > 0:
                t = []
                for y in range(self.fm.d[1]):
                    for x in range(self.fm.d[0]):
                        tl = self.fm.tiles[y][x]
                        if tl.h == tl.th and self.fm.tiles[self.y][self.x].type_id not in self.unsteppable and not CheckifBlock(x,y) and not CheckifUnit(x,y):
                            t.append(tl)
                n = None
                md = 9999
                for i in t:
                    d = Distance_Pt([self.x,self.y],[i.x,i.y])
                    if d < md:
                        md = d
                        n = i
                self.x = n.x
                self.y = n.y
                PopUpText(txt = "Out of Bounds!",x = self.rect.centerx, y = self.rect.centery - 20)
                for i in range(4):
                    SquareCoil(n,clr = faction_clrs[self.faction], h = self.rect[3] + 5,start = i * - 10,spd = 1.5)
                
        if len(self.offx_list) > 0:
            self.offx += self.offx_list[0][0]
            self.offx_list[0][1] -= 1
            if self.offx_list[0][1] == 0:
                if len(self.offx_list[0]) > 2:
                    self.offx_list[0][2]()
                self.offx_list.pop(0)
        if len(self.offy_list) > 0:
            self.offy += self.offy_list[0][0]
            self.offy_list[0][1] -= 1
            if self.offy_list[0][1] == 0:
                if len(self.offy_list[0]) > 2:
                    self.offy_list[0][2]()
                self.offy_list.pop(0)
        if len(self.offh_list) > 0:
            self.offh += self.offh_list[0][0]
            self.offh_list[0][1] -= 1
            if self.offh_list[0][1] == 0:
                if len(self.offh_list[0]) > 2:
                    self.offh_list[0][2]()
                self.offh_list.pop(0)
        #self.rect.bottom = self.fm.tiles[self.y][self.x].bl[1] - 5 + (self.fm.ch - self.fm.h) * 0.3 * (self.fm.v/self.fm.cv) #self.fm.tiles[self.y][self.x].centery + 3 * (1 - self.fm.v/self.fm.cv)
        self.rect.bottom = self.fm.tiles[self.y][self.x].bl[1] - 0.2 * self.fm.h + (self.fm.ch - self.fm.h - self.offh) * 0.3 * (self.fm.v/self.fm.cv) - self.offy * self.fm.h - self.offh * self.fm.v
        self.rect.centerx = self.fm.tiles[self.y][self.x].centerx + self.offx * self.fm.w
        self.h = self.fm.tiles[self.y][self.x].h + self.rh
        self.a = self.fm.tiles[self.y][self.x].h + self.ra
        #self.centery = self.fm.tiles[self.y][self.x].centery
        self.centerx = self.rect.centerx
        self.centery = self.rect.centery

    def DrawBack(self):
        for i in self.visual_sprites:
            i.draw_b()

    def DrawFront(self):
        for i in self.visual_sprites:
            i.draw_f()

    def update(self):
        self.ReactCountdown()
        self.update_pos()
        for i in self.visual_sprites:
            i.update()
        if self.HP == 0:
            self.ClearAllStatusEffects()
            self.DefeatAnimation()
        self.Update_SEV() #Must be after update visual_sprites

    def DefeatAnimation(self):
        self.fm.RemoveUnit(self)

    def Get_Crit(self,n = 0):
        x = CorInt((self.move_crit[n] + self.Add_Crit) * self.Mlt_Crit)
        if x >= 100:
            return 100
        elif x <= 0:
            return 0
        return x

    def Get_Range(self,n = 0):
        if self.move_range[n][0] == 0:
            return 0
        x = CorInt((self.move_range[n][0] + self.Add_Range) * self.Mlt_Range)
        if x <= 1:
            return 1
        return x

    def Get_MvmRange(self):
        if self.move_type[-1] == "Movement":
            x = CorInt((self.move_range[-1][0] + self.Add_Mvm) * self.Mlt_Mvm)
            return x
        else:
            return 0

    def Get_ATK(self):
        return CorInt((self.Base_ATK + self.Add_ATK) * self.Mlt_ATK)

    def Get_DEF(self):
        return CorInt((self.Base_DEF + self.Add_DEF) * self.Mlt_DEF)

    def Get_PhyDEF(self):
        return CorInt((self.Base_PhyDEF + self.Add_PhyDEF) * self.Mlt_PhyDEF)

    def Get_MgcDEF(self):
        return CorInt((self.Base_MgcDEF + self.Add_MgcDEF) * self.Mlt_MgcDEF)

    def Get_ResistValue(self,effect):
        return self.Resist_Value[self.Resistance.index(SE_Elements.get(effect))] 

    def Get_WeakValue(self,effect):
        return self.Weak_Value[self.Weakness.index(SE_Elements.get(effect))] 

    def Get_DMG(self,m = 0,t = 0, crit = False):
        if t == 0:
            if randint(1,100) <= self.Get_Crit(m) or crit:
                return [-CorInt(self.Get_ATK() * self.move_mlt[m][1] * 1.5),True]
            else:
                return [-randint(CorInt(self.Get_ATK() * self.move_mlt[m][0]),CorInt(self.Get_ATK() * self.move_mlt[m][1])),False]
        elif t == 1:
            if self.Get_Crit(m) == 100 or crit:
                return [-CorInt(self.Get_ATK() * self.move_mlt[m][1] * 1.5),-CorInt(self.Get_ATK() * self.move_mlt[m][1] * 1.5),-CorInt(self.Get_ATK() * self.move_mlt[m][1] * 1.5)]
            elif self.Get_Crit(m) == 0:
                return [-CorInt(self.Get_ATK() * self.move_mlt[m][0]),-CorInt(self.Get_ATK()  * self.move_mlt[m][1]),-CorInt(self.Get_ATK() * self.move_mlt[m][1])]
            else:
                return [-CorInt(self.Get_ATK() * self.move_mlt[m][0]),-CorInt(self.Get_ATK()  * self.move_mlt[m][1]),-CorInt(self.Get_ATK() * self.move_mlt[m][1] * 1.5)]
        elif t == 2:
            if self.move_SE[m]:
                x = " " + self.move_SE[m] + " DMG"
            else:
                x = " DMG"
            if self.Get_Crit(m) == 100 or crit:
                return str(CorInt(self.Get_ATK() * self.move_mlt[m][1] * 1.5))+x
            else:
                if self.move_mlt[m][0] == self.move_mlt[m][1]:
                    return str(CorInt(self.Get_ATK() * self.move_mlt[m][0]))+x
                else:
                    return str(CorInt(self.Get_ATK() * self.move_mlt[m][0]))+" - "+str(CorInt(self.Get_ATK() * self.move_mlt[m][1]))+x
        elif t == 3:
            if self.Get_Crit(m) == 100 or crit:
                return str(CorInt(self.Get_ATK() * self.move_mlt[m][1] * 1.5))
            else:
                if self.move_mlt[m][0] == self.move_mlt[m][1]:
                    return str(CorInt(self.Get_ATK() * self.move_mlt[m][0])) + "        " + str(CorInt(self.Get_ATK() * self.move_mlt[m][1] * 1.5))
                else:
                    return str(CorInt(self.Get_ATK() * self.move_mlt[m][0]))+" - "+str(CorInt(self.Get_ATK() * self.move_mlt[m][1])) + "        " + str(CorInt(self.Get_ATK() * self.move_mlt[m][1] * 1.5))
                

    def ResetPntl(self):
        self.icon_lp = 0
        self.icon_no = 0
        self.Pntl_MinHP = 0
        self.Pntl_MaxHP = 0
        self.Pntl_CritHP = 0
        self.Pntl_Hit = 0
        self.Pntl_SE = None

    def Get_ActualDMG(self,change,effect = None,source_type = 0,breach = False,hit_no = 1):
        if effect:
            if self.CheckifAffinity(effect):
                change = abs(change) * 0.5
                effect = None

        if self.CheckifProperty("Invincible") and change < 0:
            change = 0
        elif self.Invincible and change < 0:
            if hit_no <= self.GetSEValue("Invincible") - self.Pntl_Hit:
                change = 0
            else:
                hit_no -= self.GetSEValue("Invincible") - self.Pntl_Hit
        if change < 0:
            prct = 100
            if effect:
                if self.CheckifResist(effect):
                    prct -= self.Get_ResistValue(effect)
                elif self.CheckifWeak(effect):
                    prct += self.Get_WeakValue(effect)
                if effect == "Shock" and self.CheckifEffect("Splash"):
                    prct += 25
                    
            if not breach and change < 0:
                prct -= self.Get_DEF()
                change = change * prct/100
                #change = change * (1 - self.Get_DEF()/100)
                if source_type == 0:
                    change = change * (1 - self.Get_PhyDEF()/100)
                elif source_type == 1:
                    change = change * (1 - self.Get_MgcDEF()/100)
                if change < self.MaxDMG:
                    change = self.MaxDMG
                elif change > self.MinDMG:
                    change = 0

        return CorInt(change) * hit_no

    def Update_SEV(self):
        for i in range(len(self.EffectTimer)):
            if not self.SEVisual[i]:
                self.SEVisual[i] = True
                self.AssignVisualSE(self.StatusEffect[i])

    def CheckifResist(self,effect):
        return SE_Elements.get(effect,"") in self.Resistance

    def CheckifWeak(self,effect):
        return SE_Elements.get(effect,"") in self.Weakness

    def CheckifEffect(self,effect):
        return effect in self.StatusEffect

    def CheckifImmune(self,effect):
##        if effect not in SE_Elements.keys():
##            return False
        #print(SE_Alignment.get(effect,""))
        if "Effect Immunity" in self.Property:
            return True
        elif "Ailment Immunity" in self.Property and SE_Alignment.get(effect,"") == 1:
            return True
        elif SE_Alignment.get(effect,"") == 0:
            return False
        elif self.CheckifAffinity(effect):
            return True
        elif self.CheckifResist(effect):
            return True
        else:
            return False

    def CheckifProperty(self,prop):
        return prop in self.Property

    def CheckifAffinity(self,effect):
        return SE_Elements.get(effect,"")+" Affinity" in self.Property

    def GetSETimer(self,effect):
        return self.EffectTimer[self.GetSEIndex(effect)]

    def GetSEValue(self,effect):
        return self.SE_Values[self.GetSEIndex(effect)]

    def GetSEIndex(self,effect):
        return self.StatusEffect.index(effect)

    def AssignVisualSE(self,effect):
        if effect == "Burn":
            for i in range(5):
                for j in range(2):
                    SEV = StatusEffectVisual(self,effect, SCD = i)
        elif effect == "Freeze":
            SEV = StatusEffectVisual(self,effect)
        elif effect == "Shock":
            for i in range(3):
                SEV = StatusEffectVisual(self,effect)
        elif effect == "Splash":
            for i in range(4):
                for j in range(2):
                    SEV = StatusEffectVisual(self,effect, SCD = i)   
        elif effect == "Poison":
            for i in range(4):
                SEV = StatusEffectVisual(self,effect, SCD = i)
        elif effect == "Blind":
            for i in range(5):
                for j in range(2):
                    SEV = StatusEffectVisual(self,effect, SCD = i)
        elif effect == "Curse":
            SEV = StatusEffectVisual(self,effect)
        elif effect == "Strengthen":
            for i in range(2):
                for j in range(2):
                    SEV = StatusEffectVisual(self,effect, SCD = i)
        elif effect == "Weaken":
            for i in range(4):
                SEV = StatusEffectVisual(self,effect, SCD = i)  
        elif effect == "Reinforce":
            for i in range(5):
                SEV = StatusEffectVisual(self,effect, SCD = i)
        elif effect == "Vulnerable":
            for i in range(4):
                for j in range(2):
                    SEV = StatusEffectVisual(self,effect, SCD = i)    
        elif effect == "Quicken":
            SEV = StatusEffectVisual(self,effect)
        elif effect == "Regeneration":
            SEV = StatusEffectVisual(self,effect)
        elif effect == "Invincible":
            SEV = StatusEffectVisual(self,effect)
        elif effect == "Invisible":
            for i in range(6):
                SEV = StatusEffectVisual(self,effect, SCD = i)
        elif effect == "Reflect":
            SEV = StatusEffectVisual(self,effect)
        elif effect == "Thorns":
            SEV = StatusEffectVisual(self,effect)

    def ReduceSERes(self,effect):
        n = self.StatusEffect.index(effect)
        elmt = SE_Elements.get(effect)
        self.Resist_Value[self.Resistance.index(elmt)] -= self.SE_Values[n][0]
        if self.SE_Values[n][1]:
            self.Resist_Value.pop(self.Resistance.index(elmt))
            self.Resistance.remove(elmt)
        if self.SE_Values[n][2]:
            self.Weakness.append(elmt)
            self.Weak_Value.append(self.SE_Values[n][2])

    def ReduceSEWeak(self,effect):
        n = self.StatusEffect.index(effect)
        elmt = SE_Elements.get(effect)
        self.Weak_Value[self.Weakness.index(elmt)] -= self.SE_Values[n][0]
        if self.SE_Values[n][1]:
            self.Weak_Value.pop(self.Weakness.index(elmt))
            self.Weakness.remove(elmt)
        if self.SE_Values[n][2]:
            self.Resistance.append(elmt)
            self.Resist_Value.append(self.SE_Values[n][2])

    def SETimerCountDown(self,effect):
        n = self.GetSEIndex(effect)
        self.EffectTimer[n] -= 1
        if self.EffectTimer[n] == 0:
            if SE_Default_Stack.get(self.StatusEffect[n]) == 3:
                self.ReduceSERes(self.StatusEffect[n])
            elif SE_Default_Stack.get(self.StatusEffect[n]) == 4:
                self.ReduceSEWeak(self.StatusEffect[n])
            exec("self."+effect.replace(" ","_")+" = False")
            self.StatusEffect.pop(n)
            self.EffectTimer.pop(n)
            self.SEVisual.pop(n)
            self.SE_Values.pop(n)
            
    def EffectTimerCountdown(self):
        for i in range(len(self.EffectTimer)):
##            if self.StatusEffect[i] in ["Strengthen","Weaken","Reinforce","Vulnerable"]:
##                self.GetSEValue_Independent(self.StatusEffect[i],countdown = True)
            if self.EffectTimer[i] > 0 and self.StatusEffect[i] not in ["Burn","Regeneration"]:
                self.EffectTimer[i] -= 1
        while 0 in self.EffectTimer:
            n = self.EffectTimer.index(0)
            if SE_Default_Stack.get(self.StatusEffect[n]) == 3:
                self.ReduceSERes(self.StatusEffect[n])
            elif SE_Default_Stack.get(self.StatusEffect[n]) == 4:
                self.ReduceSEWeak(self.StatusEffect[n])
            exec("self."+self.StatusEffect[n].replace(" ","_")+" = False")
            self.StatusEffect.pop(n)
            self.EffectTimer.pop(n)
            self.SEVisual.pop(n)
            self.SE_Values.pop(n)
        self.EffectPostTurnStat()

    def ClearStatusEffect(self,effect):
        if effect in self.StatusEffect:
            n = self.StatusEffect.index(effect)
            if SE_Default_Stack.get(self.StatusEffect[n]) == 3:
                self.ReduceSERes(self.StatusEffect[n])
            elif SE_Default_Stack.get(self.StatusEffect[n]) == 4:
                self.ReduceSEWeak(self.StatusEffect[n])
            self.StatusEffect.pop(n)
            self.EffectTimer.pop(n)
            self.SEVisual.pop(n)
            self.SE_Values.pop(n)

    def ClearAllStatusEffects(self):
        for i in range(len(self.EffectTimer)):
            if self.EffectTimer[i] > 0:
                self.EffectTimer[i] = 0
        while 0 in self.EffectTimer:
            n = self.EffectTimer.index(0)
            if SE_Default_Stack.get(self.StatusEffect[n]) == 3:
                self.ReduceSERes(self.StatusEffect[n])
            elif SE_Default_Stack.get(self.StatusEffect[n]) == 4:
                self.ReduceSEWeak(self.StatusEffect[n])
            self.StatusEffect.pop(n)
            self.EffectTimer.pop(n)
            self.SEVisual.pop(n)
            self.SE_Values.pop(n)
        self.EffectPostTurnStat()

    def MovesetCooldown(self):
        if self.faction == 0:
            if self.prmy_atk and self.prmy_atk.timer > 0:
                self.prmy_atk.timer -= 1
            if self.scdy_atk and self.scdy_atk.timer > 0:
                self.scdy_atk.timer -= 1
        for i in range(len(self.act_CD)):
            if self.act_CD[i] > 0:
                if self.move_type[i] == "Attack" and not self.Shock:
                    self.act_CD[i] -= 1
                elif self.move_type[i] in ["Skill","Starstone"] and not self.Poison:
                    self.act_CD[i] -= 1
        for i in range(len(self.act_CD)):
            if self.move_type[i] == "Attack" and self.Shock:
                self.act_record[i] = False
            elif self.move_type[i] in ["Skill","Starstone"] and self.Poison:
                self.act_record[i] = False
            elif self.Curse:
                self.act_record[i] = True#self.act_record[i] = False
            elif self.act_CD[i] > 0:
                self.act_record[i] = False    
            else:
                self.act_record[i] = True
        if self.Curse:
            print(self.act_record)

    def GetSEValue_Independent(self,effect,countdown = False):
        val = 0
        n = self.StatusEffect.index(effect)
        l = len(self.SE_Values[n])
        for i in range(l):
            val += self.SE_Values[n][l-1-i][0]
            if countdown:
                self.SE_Values[n][l-1-i][1] -= 1
                if self.SE_Values[n][l-1-i][1] == 0:
                    self.SE_Values[n].pop(l-1-i)
        return val
    
    def EffectEnact(self):
        for i in SE_UnitName:
            exec("self."+i+" = False")
        if "Burn" in self.StatusEffect:
            dmg = self.GetSEValue_Independent("Burn",countdown = True)
            if self.CheckifWeak("Burn"):
                dmg = CorInt(dmg * 1.5)
            self.HPChange(change = dmg, breach = True, clr = (255,115,115),react = False)
            self.SETimerCountDown("Burn")
        if "Regeneration" in self.StatusEffect:
            self.HPChange(change = self.MaxHP * self.GetSEValue("Regeneration"))
            self.SETimerCountDown("Regeneration")
        for i in ["Strengthen","Weaken","Reinforce","Vulnerable"]:
            if i in self.StatusEffect:
                self.GetSEValue_Independent(i,countdown = True)
        self.EffectPostTurnStat()

    def EffectPostTurnStat(self):
        self.Add_ATK, self.Mlt_ATK = 0,1
        self.Add_DEF, self.Mlt_DEF = 0,1
        self.Add_PhyDEF, self.Mlt_PhyDEF = 0,1
        self.Add_MgcDEF, self.Mlt_MgcDEF = 0,1
        self.Add_Crit, self.Mlt_Crit = 0,1
        self.Add_Range, self.Mlt_Range = 0,1
        self.Add_Mvm, self.Mlt_Mvm = 0,1
        for i in SE_UnitName:
            exec("self."+i+" = '"+i+"' in self.StatusEffect")
        if "Splash" in self.StatusEffect:
            self.Add_Mvm -= self.GetSEValue("Splash")
        if "Strengthen" in self.StatusEffect:
            self.Mlt_ATK += self.GetSEValue_Independent("Strengthen")
        if "Weaken" in self.StatusEffect:
            self.Mlt_ATK -= self.GetSEValue_Independent("Weaken")
        if "Reinforce" in self.StatusEffect:
            self.Add_DEF += self.GetSEValue_Independent("Reinforce")
        if "Vulnerable" in self.StatusEffect:
            self.Add_DEF += self.GetSEValue_Independent("Vulnerable")
        if "Reflect" in self.StatusEffect:
            self.Add_DEF += self.GetSEValue("Reflect")
        if "Quicken" in self.StatusEffect:
            self.Add_Mvm += self.GetSEValue("Quicken")
        if "Blind" in self.StatusEffect:
            self.Add_Range -= self.GetSEValue("Blind")
        if "Freeze" in self.StatusEffect:
            self.Mlt_Mvm = 0
        if "Curse" in self.StatusEffect:
            self.Mlt_Mvm = 0
            
    def StartTurn(self):
        self.EffectEnact()
        self.MovesetCooldown()
        self.mv_tiles = GetMovableRange(self.x,self.y,self.Get_MvmRange(),c = None,unit = self)

    def StartTurnAct(self):
        pass

    def EndTurn(self):
        self.EffectTimerCountdown()

    def EndTurnAct(self):
        pass
        
    def DrawParallelogram(self,r,clr,x = 0,offx = 1):
        pygame.draw.polygon(game_window,clr,[[r.left + x,r.bottom],
                                             [r.right + x,r.bottom],
                                             [r.right + r[3] * offx + x,r.top],
                                             [r.left + r[3] * offx + x,r.top]])

    def DrawDiamond(self,r,clr,w):
        pygame.draw.polygon(game_window,clr,[[r.left - w,r.top],
                                             [r.left,r.top + w],
                                             [r.left + w,r.top],
                                             [r.left,r.top - w]])

    def DrawSideDiamond(self,r,clr,w,offx = 0):
        pygame.draw.polygon(game_window,clr,[[r.left + offx,r.top + w],
                                             [r.left - w + offx,r.top],
                                             [r.left + offx,r.top - w],
                                             [r.left + offx - 5,r.top - w],
                                             [r.left - w + offx - 5,r.top],
                                             [r.left + offx - 5,r.top + w]])

    def DrawArrow(self,r,clr, offy = 1):
        pts = []
        
        #for i in [[0,-0.7],[0.2,0.25],[0.5,0.1],[0,0.7],[-0.5,0.1],[-0.2,0.25]]:
        for i in [[0,0.7],[0.5,0.2],[0.2,0.2],[0.2,-0.65],[-0.2,-0.65],[-0.2,0.2],[-0.5,0.2]]:
            pts.append([r.left + CorInt(r[3] * i[0]), r.top - CorInt(r[3] * i[1]) * offy])
        pygame.draw.polygon(game_window,clr,pts)

    def DrawPlus(self,r,clr):
        pts = []
        for i in [[0.2,0.5],[0.2,0.2],[0.5,0.2],[0.5,-0.2],[0.2,-0.2],[0.2,-0.5],[-0.2,-0.5],[-0.2,-0.2],[-0.5,-0.2],[-0.5,0.2],[-0.2,0.2],[-0.2,0.5]]:
            pts.append([r.left + CorInt(r[3] * i[0]), r.top - CorInt(r[3] * i[1])])
        pygame.draw.polygon(game_window,clr,pts)

    def DrawStrike(self,r,clr,clr2):
        pts = []
        for i in range(4):
            pts.append([r.left + CorInt(cos(radians(i * 90)) * r[3] * 0.6), r.top - CorInt(sin(radians(i * 90)) * r[3] * 0.6)])
        pygame.draw.polygon(game_window,clr,pts)
        pts = []
        for i in range(4):
            pts.append([r.left + CorInt(cos(radians(i * 90 + 45)) * r[3] * 0.6), r.top - CorInt(sin(radians(i * 90 + 45)) * r[3] * 0.6)])
        pygame.draw.polygon(game_window,clr,pts)
        pts = []
        for i in [[0.05,0.4],[-0.05,0.4],[-0.05,-0.1],[0.05,-0.1]]:
            pts.append([r.left + CorInt(r[3] * i[0]), r.top - CorInt(r[3] * i[1])])
        pygame.draw.polygon(game_window,clr2,pts)
        pts = []
        for i in [[0.05,-0.4],[-0.05,-0.4],[-0.05,-0.25],[0.05,-0.25]]:
            pts.append([r.left + CorInt(r[3] * i[0]), r.top - CorInt(r[3] * i[1])])
        pygame.draw.polygon(game_window,clr2,pts)

    def DrawCross(self,r,clr):
        pts = []
##        for i in [[0.15,0],[0.75,-0.6],[0.75,-0.75],[0.6,-0.75],
##                  [0,-0.15],[-0.6,-0.75],[-0.75,-0.75],[-0.75,-0.6],
##                  [-0.15,0],[-0.75,0.6],[-0.75,0.75],[-0.6,0.75],
##                  [0,0.15],[0.6,0.75],[0.75,0.75],[0.75,0.6]]:
        for i in [[0.2,0],[0.8,-0.6],[0.8,-0.8],[0.6,-0.8],
                  [0,-0.2],[-0.6,-0.8],[-0.8,-0.8],[-0.8,-0.6],
                  [-0.2,0],[-0.8,0.6],[-0.8,0.8],[-0.6,0.8],
                  [0,0.2],[0.6,0.8],[0.8,0.8],[0.8,0.6]]:
            pts.append([r.left + CorInt(r[3] * i[0]), r.top - CorInt(r[3] * i[1])])
        pygame.draw.polygon(game_window,clr,pts)

    def DrawHPBar(self):
        self.stat_lp = (self.stat_lp + 1)%180
        c = sin(radians(self.stat_lp))

        fc = (205,235,240)
        bc = (75,85,85)
        tc = (205,235,240)
        sc = (130,145,150)

        fcs = [(205,235,240),(50,180,78),(50,123,180),(180,50,50),(104,31,173),(212,88,240),(88,208,240)]
        
        se = []
        se_s = []
        if self.Pntl_SE:
            if self.CheckifAffinity(self.Pntl_SE):
                se.append(1)
            elif self.CheckifResist(self.Pntl_SE):
                se.append(2)
            elif self.CheckifWeak(self.Pntl_SE):
                se.append(3)
        
        if self.Pntl_MinHP <= 0 and 1 not in se:
            if self.CheckifProperty("Discharge"):
                se.append(4)
            if self.CheckifEffect("Thorns"):
                se.append(5)
            if self.CheckifEffect("Reflect"):
                se.append(6)

        if len(se) > 1:
            self.icon_lp += 1
            if self.icon_lp >= 90 or self.icon_no >= len(se):
                self.icon_lp = 0
                self.icon_no = (self.icon_no + 1)%len(se)
            fc = fcs[ se[self.icon_no] ]
            se_s = list(se)
            se = se[self.icon_no]
            for i in se_s:
                if se_s[0] == se:
                    se_s.pop(0)
                    break
                else:
                    se_s.append(se_s.pop(0))
            
        elif len(se) == 1:
            self.icon_lp = 0
            self.icon_no = 0
            se = se[0]
            fc = fcs[se]
        else:
            se = 0
            
        if se > 0:
            sc = Darken(fc,30)
        
        if self.fm.show_hp and self.fm.boundaries[self.y][self.x] != None:
            if self.fm.targets[self.y][self.x] != None:
                b = SHPB_rect
                f = SHPF_rect
            else:
                b = HPB_rect
                f = HPF_rect
            
            b.centerx = self.rect.centerx
            b.centery = self.rect.top - 15
            f.centerx = self.rect.centerx
            f.centery = self.rect.top - 15

            min_hp = self.HP + self.Pntl_MinHP
            max_hp = self.HP + self.Pntl_MaxHP
            crit_hp = self.HP + self.Pntl_CritHP
            if min_hp < 0:
                min_hp = 0
            elif min_hp > self.MaxHP:
                min_hp = self.MaxHP
            if max_hp < 0:
                max_hp = 0
            elif max_hp > self.MaxHP:
                max_hp = self.MaxHP
            if crit_hp < 0:
                crit_hp = 0
            elif crit_hp > self.MaxHP:
                crit_hp = self.MaxHP
                
            if self.fm.targets[self.y][self.x] != None:
                txt = stat_font12.render(str(self.HP),True,(255,255,255))
##                txt = stat_font12.render(str(self.HP)+" > "+str(self.HP + self.Pntl_MinHP)+" - "+str(self.HP + self.Pntl_MaxHP),True,(255,255,255))
##                if max_hp == min_hp:
##                    txt = stat_font12.render(str(self.HP)+" >> "+str(min_hp),True,(255,255,255))
##                else:
##                    txt = stat_font12.render(str(self.HP)+" >> "+str(min_hp)+" - "+str(max_hp),True,(255,255,255))
                t = pygame.Rect(0,0,txt.get_width() + f[3],f[3])
                t.left = f.left + f[3]
                t.bottom = f.top
                self.DrawParallelogram(t,sc,offx = -1)
                game_window.blit(txt,t)
                    
                if se > 0:
                    se_txt = stat_font12.render(["Affinitive","Resistant","Weak","Strike Back","Thorns","Reflect"][se-1],True,(255,255,255))
                    se_r = pygame.Rect(0,0,se_txt.get_width() + f[3],f[3])
                    se_r.left = t.right
                    se_r.bottom = f.top
                    self.DrawParallelogram(se_r,Darken(sc,20),offx = -1)
                    game_window.blit(se_txt,se_r)
            
            if self.HP/self.MaxHP <= 0.3:
                clr_no = 3
            else:
                clr_no = self.faction
            clr = HP_Clr[clr_no]
            self.DrawParallelogram(f,fc)
            self.DrawParallelogram(b,bc)
            if self.HP > 0:
                r = pygame.Rect(0,0,CorInt(b[2] * self.HP/self.MaxHP),b[3])
                r.left = b.left
                r.centery = b.centery
                self.DrawParallelogram(r,clr)
            else:
                r = pygame.Rect(0,0,0,b[3])
                r.left = b.left
                r.centery = b.centery
                self.DrawParallelogram(r,clr)
            self.DrawDiamond(f,fc,f[3])
            for i in range(len(se_s)):
                self.DrawSideDiamond(f,fcs[se_s[i]],f[3],offx = -10 * i - 5 * (1 - self.icon_lp/90))

            if self.Pntl_CritHP != 0:
                if self.Pntl_CritHP < 0:
                    clr = GradientClrs(CritPHP_Clr[clr_no],HP_Clr[clr_no],c,1-c)
                    if crit_hp <= 0:
                        self.DrawParallelogram(r,clr)
                    else:
                        p = pygame.Rect(0,0,CorInt(b[2] * abs(self.Pntl_CritHP)/self.MaxHP),b[3])
                        p.right = r.right
                        p.centery = r.centery
                        self.DrawParallelogram(p,clr)
                else:
                    clr = GradientClrs(CritPHP_Clr[clr_no],(75,85,85),c,1-c)
                    if crit_hp >= self.MaxHP:
                        p = pygame.Rect(0,0,CorInt(b[2] * (1 - self.HP/self.MaxHP)),b[3])
                    else:
                        p = pygame.Rect(0,0,CorInt(b[2] * self.Pntl_CritHP/self.MaxHP),b[3])
                    p.left = r.right
                    p.centery = r.centery
                    self.DrawParallelogram(p,clr)
                    
            if self.Pntl_MaxHP != 0:
                if self.Pntl_MaxHP < 0:
                    clr = GradientClrs(MaxPHP_Clr[clr_no],HP_Clr[clr_no],c,1-c)
                    if max_hp <= 0:
                        self.DrawParallelogram(r,clr)
                    else:
                        p = pygame.Rect(0,0,CorInt(b[2] * abs(self.Pntl_MaxHP)/self.MaxHP),b[3])
                        p.right = r.right
                        p.centery = r.centery
                        self.DrawParallelogram(p,clr)
                else:
                    clr = GradientClrs(MaxPHP_Clr[clr_no],(75,85,85),c,1-c)
                    if max_hp >= self.MaxHP:
                        p = pygame.Rect(0,0,CorInt(b[2] * (1 - self.HP/self.MaxHP)),b[3])
                    else:
                        p = pygame.Rect(0,0,CorInt(b[2] * self.Pntl_MaxHP/self.MaxHP),b[3])
                    p.left = r.right
                    p.centery = r.centery
                    self.DrawParallelogram(p,clr)

            if self.Pntl_MinHP != 0:
                if self.Pntl_MinHP < 0:
                    clr = GradientClrs(MinPHP_Clr[clr_no],HP_Clr[clr_no],c,1-c)
                    if min_hp <= 0:
                        self.DrawParallelogram(r,clr)
                    else:
                        p = pygame.Rect(0,0,CorInt(b[2] * abs(self.Pntl_MinHP)/self.MaxHP),b[3])
                        p.right = r.right
                        p.centery = r.centery
                        self.DrawParallelogram(p,clr)
                else:
                    clr = GradientClrs(MinPHP_Clr[clr_no],(75,85,85),c,1-c)
                    if min_hp >= self.MaxHP:
                        p = pygame.Rect(0,0,CorInt(b[2] * (1 - self.HP/self.MaxHP)),b[3])
                    else:
                        p = pygame.Rect(0,0,CorInt(b[2] * self.Pntl_MinHP/self.MaxHP),b[3])
                    p.left = r.right
                    p.centery = r.centery
                    self.DrawParallelogram(p,clr)

            if self.Pntl_SE:
                if se == 1:
                    self.DrawPlus(f,tc)
                elif se == 2:
                    self.DrawArrow(f,tc,offy = -1)
                elif se == 3:
                    self.DrawArrow(f,tc)
            if se >= 4:
                self.DrawStrike(f,tc,fc)
                
            if min_hp <= 0:
                self.DrawCross(f,(255,100,100))

    def UpdateTilePos(self,nx,ny):
        self.x = nx
        self.y = ny

    def ShiftW(self):
        self.offx = 0

    def ShiftE(self):
        self.UpdateTilePos(self.x + 1,self.y)
        #self.x += 1
        self.offx = 0

    def ShiftN_P(self):
        self.UpdateTilePos(self.x,self.y - 1)
        #self.y -= 1
        self.offy = 0

    def ShiftN_H(self):
        self.offy = 0
        
    def ShiftS_P(self):
        self.offy = 0

    def ShiftS_H(self):
        self.UpdateTilePos(self.x,self.y + 1)
        #self.y += 1
        self.offy = 0

    def ShiftH(self):
        self.offh = 0

    def MoveUp(self):
        d = self.fm.tiles[self.y - 1][self.x].h - self.fm.tiles[self.y][self.x].h
        #self.offh_list.append([0.05 * d,20,self.ShiftH])
        if d >= 0:
            self.offh_list.append([0.1 * d,10])
            self.offh_list.append([0,10,self.ShiftH])
            self.offy_list.append([0.05,20,self.ShiftN_P])
        else:
            self.offy = -1
            self.offh -= d
            #self.offh_list.append([0,10])
            self.offh_list.append([0.05 * d,20,self.ShiftH])

            #self.offy_list.append([0.05,10])
            self.offy_list.append([0.05,20,self.ShiftN_H])
            
            self.UpdateTilePos(self.x,self.y - 1)
            #self.y -= 1

    def MoveDown(self):
        d = self.fm.tiles[self.y + 1][self.x].h - self.fm.tiles[self.y][self.x].h
##        self.offh_list.append([0.05 * d,20,self.ShiftH])
        if d > 0:
            self.offh_list.append([0.1 * d,10])
            self.offh_list.append([0,10,self.ShiftH])
            self.offy_list.append([-0.05,20,self.ShiftS_H])
        else:
            self.offy = 1
            self.offh -= d
            self.offh_list.append([0,10])
            self.offh_list.append([0.1 * d,10,self.ShiftH])
            self.offy_list.append([-0.05,20,self.ShiftS_P])
            self.UpdateTilePos(self.x,self.y + 1)
            #self.y += 1

    def MoveRight(self):
        self.offx_list.append([0.05,20,self.ShiftE])
        d = self.fm.tiles[self.y][self.x + 1].h - self.fm.tiles[self.y][self.x].h
        if d >= 0:
            self.offh_list.append([0.1 * d,10])
            self.offh_list.append([0,10,self.ShiftH])
        else:
            self.offh_list.append([0,10])
            self.offh_list.append([0.1 * d,10,self.ShiftH])
##        if d != 0:
##            self.offh_list.append([0.05 * d,20,self.ShiftH])
            

    def MoveLeft(self):
        self.offx_list.append([-0.05,20,self.ShiftW])
        d = self.fm.tiles[self.y][self.x - 1].h - self.fm.tiles[self.y][self.x].h

        if d >= 0:
            self.offh_list.append([0.1 * d,10])
            self.offh_list.append([0,10,self.ShiftH])
        else:
            self.offh_list.append([0,10])
            self.offh_list.append([0.1 * d,10,self.ShiftH])
        
##        if d != 0:
##            self.offh_list.append([0.05 * d,20,self.ShiftH])

        self.offh -= d
        self.offx = 1
        self.UpdateTilePos(self.x - 1,self.y)
        #self.x -= 1
    

HPB_rect = pygame.Rect(0,0,30,5)
HPF_rect = pygame.Rect(0,0,36,11)

SHPB_rect = pygame.Rect(0,0,110,10)
SHPF_rect = pygame.Rect(0,0,116,16)

HP_Clr = [(85,180,255),(190,115,255),(110,120,255),(255,115,115)]
MinPHP_Clr = []
MaxPHP_Clr = []
CritPHP_Clr = []
for i in HP_Clr:
    MinPHP_Clr.append(Brighten(i,20))
    MaxPHP_Clr.append(Brighten(i,40))
    CritPHP_Clr.append(Brighten(i,60))

affinity_clr = [(50,180,78),Brighten((50,180,78),20)]
resist_clr = [(50,123,180),Brighten((50,123,180),20)]
weak_clr = [(180,50,50),Brighten((180,50,50),20)]

class TestUnit(Unit):
    def __init__(self, x = 0, y = 0):
        Unit.__init__(self,x,y,faction = 1)
        self.name = "Practice Target"
        self.name_id = -1

        self.HP = 50
        self.MaxHP = 50

        self.Base_ATK = 10
        self.Add_ATK = 10
        self.Mlt_ATK = 1.5

        self.Mlt_Crit = 1
        
        self.info = ["Just a test dummy.","Lorem ipsum dolor sit amet, consectetur adipiscing elit. Mauris blandit purus eu ultrices sodales. Suspendisse venenatis eros eget varius posuere. Pellentesque vitae suscipit nibh."] #Flavour text & Unit data
        self.move_type = ["Ability","Movement"]
        self.move_label = ["Test Dummy",""]
        self.move_stat = [False,False]
        self.move_mlt = [None,None]
        self.move_SE = [None,None]
        self.move_cd = [0,0]
        self.move_crit = [0,0]
        self.move_info = [["Cannot act or move."],
                          []]
        self.move_range = [[0,0],[0,0]]
        self.move_get_tile = [None,GetMovableRange]
        self.colour = []
        self.imgs = []        
        self.text_sort()

        #self.can_act = True
        #self.Set_ActRecord()

        #self.rect = pygame.Rect([0,0],[50,100])

    def Draw(self):
        self.DrawBack()
        pygame.draw.rect(game_window,(200,100,255),self.rect)
        self.DrawHPBar()
        self.DrawFront()

from VoxelGame_Stage import *
from VoxelGame_Equipment import *
from VoxelGame_Skill import *
        
inventory = []


shocked_icon = pygame.Surface((55,55))
shocked_icon.fill(SE_colour_set["Shock"])
poisoned_icon = pygame.Surface((55,55))
poisoned_icon.fill(SE_colour_set["Poison"])
frozen_icon = pygame.Surface((55,55))
frozen_icon.fill(SE_colour_set["Freeze"])
cursed_icon = pygame.Surface((55,55))
cursed_icon.fill(SE_colour_set["Curse"])

l = ["shocked","poisoned","frozen","cursed"]
for i in range(len(l)):
    exec(l[i]+"_rect = "+l[i]+"_icon.get_rect()")

mvm_icon = pygame.Surface((40,42))
mvm_icon.fill((168, 90, 37))

class InventoryAct():
    def __init__(self):
        self.name = "Inventory"
        self.icon = pygame.Surface((30,30))
        self.icon.fill((129,116,240))
        self.i_rect = self.icon.get_rect()

class MovementAct():
    def __init__(self):
        self.name = "Movement"
        self.icon = movement_icon#mvm_icon
        self.i_rect = self.icon.get_rect()

inventory_act = InventoryAct()
movement_act = MovementAct()

class Playable_Unit(Unit):
    def __init__(self,x = 0,y = 0):
        Unit.__init__(self,x,y,faction = 0)

        self.cd = 0
        self.mode = 0 #0: Movement; 1: Prmy ATK; 2: Scdy ATK, 3: Skill; 4: Starstone, 5: Item
        self.draw_lp = 100

        self.dis_opt_stat = []
        self.dis_opt_w = 0
        self.dis_opt_h = 0
        self.prev_dis_opt = -1
        
        self.playable = True

    def DrawOptions(self,lp = True):
        if lp and self.draw_lp > 0:
            self.draw_lp -= 5
        icon = [movement_act,self.prmy_atk,self.scdy_atk,self.skl,self.star_skl,inventory_act]
        l = len(icon)
        d = l - icon.count(None)
        x = window_width/2 - ((d - 1) * 55)/2
        rect = pygame.Rect((0,0,45,45))
        rect.bottom = window_height - 20 + self.draw_lp
        side = pygame.Rect((0,0,45,30))
        side.bottom = rect.bottom
        v = -1
        c = 0
        for i in range(l):
            if icon[i]:
                if self.Curse and i != 5:
                    clr = (120,120,120)#clr = (123,50,195)
                    avail = 6
                elif self.Freeze and i == 0:
                    clr = (120,120,120)#clr = (116,226,240)
                    avail = 5
                elif self.Poison and i in [3,4]:
                    clr = (120,120,120)#clr = (45,169,74)
                    avail = 4
                elif self.Shock and i in [1,2]:
                    clr = (120,120,120)#clr = (208,186,65)
                    avail = 3
                elif i < 5 and self.act_CD[c - 1] > 0:
                    clr = (120,120,120)
                    avail = 1
                elif i < 5 and not self.act_record[c - 1]:
                    clr = (120,120,120)
                    avail = 2
                elif i == 5 and len(inventory) == 0:
                    clr = (120,120,120)
                    avail = 2
                else:
                    clr = (130,180,245)#(96,158,229)
                    avail = 0
                rect.centerx = x
                side.centerx = x
                if d == 1:
                    edge = pygame.Rect((0,0,15,15))
                    edge.bottom = side.top
                    edge.centerx = side.centerx
                    pygame.draw.circle(game_window,clr,[edge.left,edge.bottom],15)
                    pygame.draw.circle(game_window,clr,[edge.right,edge.bottom],15)
                elif c == 0:
                    edge = pygame.Rect((0,0,30,15))
                    edge.bottom = side.top
                    edge.right = side.right
                    pygame.draw.circle(game_window,clr,[edge.left,edge.bottom],15)
                elif c == d - 1:
                    edge = pygame.Rect((0,0,30,15))
                    edge.bottom = side.top
                    edge.left = side.left
                    pygame.draw.circle(game_window,clr,[edge.right,edge.bottom],15)
                else:
                    edge = pygame.Rect((0,0,45,15))
                    edge.bottom = side.top
                    edge.centerx = side.centerx
                pygame.draw.rect(game_window,clr,side)
                pygame.draw.rect(game_window,clr,edge)
                icon[i].i_rect.center = rect.center
                game_window.blit(icon[i].icon,icon[i].i_rect)

                if avail == 3:
                    shocked_rect.center = rect.center
                    game_window.blit(shocked_icon,shocked_rect)
                elif avail == 4:
                    poisoned_rect.center = rect.center
                    game_window.blit(poisoned_icon,poisoned_rect)
                elif avail == 5:
                    frozen_rect.center = rect.center
                    game_window.blit(frozen_icon,frozen_rect)
                elif avail == 6:
                    cursed_rect.center = rect.center
                    game_window.blit(cursed_icon,cursed_rect)
                
                if 0 < i < 6:
                    if avail == 0:
                        key = eval("key_icon_"+str(i))
                        k_rect = key.get_rect()
                        k_rect.centerx = rect.centerx
                        k_rect.centery = rect.bottom + 5
                        game_window.blit(key,k_rect)
                    elif self.act_CD[c - 1] > 0:
                        img = cd_symbol
                        i_rect = img.get_rect()
                        text = stat_font16.render(str(self.act_CD[c - 1]),True,(255,255,255))
                        textRect = text.get_rect()
                        m_rect = pygame.Rect(0,0,textRect[2] + i_rect[2] + 5,20)
                        m_rect.centerx = rect.centerx
                        m_rect.centery = rect.bottom + 5

                        textRect.right = m_rect.right
                        textRect.centery = m_rect.centery
                        i_rect.right = textRect.left - 5
                        i_rect.centery = m_rect.centery
                        DrawSmoothFrame(m_rect,(80,80,80))
                        game_window.blit(text,textRect)
                        game_window.blit(img,i_rect)
                
                if rect.collidepoint(pygame.mouse.get_pos()):
                    #v = i
                    if i != self.prev_dis_opt:
                        if i == 0:
                            self.dis_opt_stat = []
                            self.dis_opt_h = 0
                            if avail == 6:
                                txt = game_font14.render("Cursed! Cannot move!",True,(167,119,218))
                                t_rect = txt.get_rect()
                                self.dis_opt_h += t_rect[3]
                                self.dis_opt_stat.append([txt,t_rect])
                            elif avail == 5:
                                txt = game_font14.render("Frozen! Cannot move!",True,(116,226,240))
                                t_rect = txt.get_rect()
                                self.dis_opt_h += t_rect[3]
                                self.dis_opt_stat.append([txt,t_rect])
                            elif self.Splash:
                                txt = game_font14.render("Splashed! Movement ranged down!",True,(142,180,248))
                                t_rect = txt.get_rect()
                                self.dis_opt_h += t_rect[3]
                                self.dis_opt_stat.append([txt,t_rect])
                            else:
                                txt = game_font14.render("Move around!",True,(255,255,255))
                                t_rect = txt.get_rect()
                                self.dis_opt_h += t_rect[3]
                                self.dis_opt_stat.append([txt,t_rect])
                        elif i < 3:
                            self.dis_opt_stat = []
                            self.dis_opt_h = 0
                            if avail == 6:
                                txt = game_font14.render("Cursed! Cannot attack!",True,(167,119,218))
                                t_rect = txt.get_rect()
                                self.dis_opt_h += t_rect[3]
                                self.dis_opt_stat.append([txt,t_rect])
                            elif avail == 3:
                                txt = game_font14.render("Shocked! Cannot attack!",True,(208,186,65))
                                t_rect = txt.get_rect()
                                self.dis_opt_h += t_rect[3]
                                self.dis_opt_stat.append([txt,t_rect])
                            else:
                                txt = stat_font14.render(self.Get_DMG(m = i - 1,t = 3),True,(255,255,255))
                                t_rect = txt.get_rect()
                                self.dis_opt_h += t_rect[3]
                                self.dis_opt_stat.append([txt,t_rect])
                                if icon[i].SE and icon[i].timer == 0:
                                    txt = game_font14.render(icon[i].SE + " Ready!",True,(255,255,255))
                                    t_rect = txt.get_rect()
                                    self.dis_opt_h += t_rect[3]
                                    self.dis_opt_stat.append([txt,t_rect])
                        elif i < 5:
                            self.dis_opt_stat = []
                            self.dis_opt_h = 0
                            if avail == 6:
                                txt = game_font14.render("Cursed! Cannot use!",True,(167,119,218))
                                t_rect = txt.get_rect()
                                self.dis_opt_h += t_rect[3]
                                self.dis_opt_stat.append([txt,t_rect])
                            elif avail == 4:
                                txt = game_font14.render("Poisoned! Cannot use!",True,(45,169,74))
                                t_rect = txt.get_rect()
                                self.dis_opt_h += t_rect[3]
                                self.dis_opt_stat.append([txt,t_rect])
                            else:
                                for j in icon[i].short_desc:
                                    txt = game_font14.render(j,True,(255,255,255))
                                    t_rect = txt.get_rect()
                                    self.dis_opt_h += t_rect[3]
                                    self.dis_opt_stat.append([txt,t_rect])
                        elif i == 5:
                            self.dis_opt_stat = []
                            self.dis_opt_h = 0
                            if len(inventory) > 0:
                                txt = game_font14.render("Use an Item!",True,(255,255,255))
                                t_rect = txt.get_rect()
                                self.dis_opt_h += t_rect[3]
                                self.dis_opt_stat.append([txt,t_rect])
                            else:
                                txt = game_font14.render("Empty Inventory!",True,(255,255,255))
                                t_rect = txt.get_rect()
                                self.dis_opt_h += t_rect[3]
                                self.dis_opt_stat.append([txt,t_rect])
                        w = []
                        for j in self.dis_opt_stat:
                            w.append(j[1][2])
                        w.append(stat_font16.size(icon[i].name)[0])
                        self.dis_opt_w = max(w) + 20
                    text = stat_font16.render(icon[i].name,True,(255,255,255))
                    textRect = text.get_rect()
                    y = rect.top - 10 - self.dis_opt_h#textRect[3] * len(self.dis_opt_stat)
                    textRect.centerx = window_width/2
                    textRect.bottom = y
                    m_rect = pygame.Rect(0,0,self.dis_opt_w,textRect[3])
                    m_rect.centerx = textRect.centerx
                    m_rect.bottom = y
                    DrawSmoothFrame(m_rect,clr, ss = False)
                    game_window.blit(text,textRect)
                    if len(self.dis_opt_stat) > 0:
                        m_rect = pygame.Rect(0,0,self.dis_opt_w,self.dis_opt_h)
                        m_rect.centerx = textRect.centerx
                        m_rect.top = textRect.bottom
                        DrawSmoothFrame(m_rect,Darken(clr,40), sn = False)
                        for i in self.dis_opt_stat:
                            y += i[1][3]
                            i[1].centerx = textRect.centerx
                            i[1].bottom = y
                            game_window.blit(i[0],i[1])

                c += 1
                x += 55
        self.prev_dis_opt = v

class Test_Mage(Playable_Unit):
    def __init__(self, x = 0, y = 0):
        Playable_Unit.__init__(self,x,y)
        self.name = "Mage"
        self.name_id = -1

        self.Base_ATK = 10
        #self.Add_ATK = 10
        #self.Mlt_ATK = 1.5

        self.HP = 75
        self.MaxHP = 150

        self.Mlt_Crit = 1

        self.ATK = self.Get_ATK()#(self.Base_ATK + self.Add_ATK) * self.Mlt_ATK

        self.Resistance = []#["Fire","Water","Electric","Poison","Ice","Gust","Shadow","Light","Ether","Astral","Corruption","Terra"]
        self.Weakness = []#["Fire","Water","Electric","Poison","Ice","Gust","Shadow","Light","Ether","Astral","Corruption","Terra"]
        self.Resist_Value = []#[50,50,50,50,50,50,50,50,50,50,50,50]
        self.Weak_Value = []#[50,50,50,50,50,50,50,50,50,50,50,50]

        self.mv_highlight = False

        self.info = ["A mage with a high elemental affinity. Adapt at attacking units behind cover with ethereal spells. His attacks can be embued with Status Effects with a relatively lower cooldown."]
        self.move_type = []
        self.move_label = []
        self.move_stat = []
        self.move_mlt = []
        self.move_SE = []
        self.move_cd = []
        self.move_crit = []
        self.move_info = []
        self.move_range = []
        self.move_get_tile = []
        self.colour = []
        self.imgs = []

        self.prmy_atk = Test_Wand(self,ID = 0)
        self.scdy_atk = Test_Launcher(self,ID = 1)
        self.skl = Apply_Quicken(self,ID = 2)
        self.star_skl = Heal_30(self,ID = 3)#None
        self.moveset = [self.prmy_atk,self.scdy_atk,self.skl,self.star_skl]
    
        self.move_type.append("Movement")
        self.move_label.append("")
        self.move_stat.append(False)
        self.move_mlt.append(None)
        self.move_SE.append(None)
        self.move_cd.append(0)
        self.move_crit.append(0)
        self.move_info.append([])
        self.move_range.append([4,6])
        self.move_get_tile.append(GetMovableRange)

        self.text_sort()

        self.icon.fill((100,130,255))

        self.can_act = True
        self.Set_ActRecord()

    def Draw(self):
        keystate = pygame.key.get_pressed()
        if self.HP > 1 and keystate[pygame.K_g]:
            self.HP -= 1
        elif self.HP < self.MaxHP and keystate[pygame.K_h]:
            self.HP += 1

        self.DrawBack()
        pygame.draw.rect(game_window,(100,130,255),self.rect)
        self.DrawHPBar()
        self.DrawFront()

    def CheckSpace(self,x,y):
        if x < 0 or x > self.fm.d[0] - 1:
            return False
        if y < 0 or y > self.fm.d[1] - 1:
            return False
        nt = self.fm.tiles[y][x]
        ct = self.fm.tiles[self.y][self.x]
        if nt not in self.mv_tiles:
            return False
        if abs(ct.h - nt.h) > 1:
            return False
        return True

    def StartTurn(self):
        if self.faction == 0:
            self.draw_lp = 100
        self.EffectEnact()
        self.MovesetCooldown()
        self.st = self.fm.tiles[self.y][self.x]
        self.mv_highlight = False

    def EndTurn(self):
        self.mv_highlight = True
        self.mv_tiles = []
        self.EffectTimerCountdown()

    def Act(self):
        if self.cd == 0:
            keystate = pygame.key.get_pressed()
            if self.mode == 0:
                        
                if not self.mv_highlight:
                    if self.Get_MvmRange() > 0 and self.act_record[-1]:
                        self.mv_tiles = GetMovableRange(self.st.x,self.st.y,self.Get_MvmRange(),c = None,unit = self)
                        for i in self.mv_tiles:
                            self.fm.boundaries[i.y][i.x] = 6
                    self.mv_highlight = True
                if keystate[pygame.K_m]:
                    ClearAllTiles()
                    self.mv_highlight = False
                    self.fm.mode = 0
                    self.fm.focus = self.fm.info_cursor
                    self.fm.info_cursor.cd = 10
                    self.fm.info_cursor.x = self.x
                    self.fm.info_cursor.y = self.y
                    self.fm.info_cursor.mode = 0
                    self.fm.info_cursor.CheckSpace()
##                    if self.fm.info_cursor.show in self.fm.instructions:
##                        self.fm.instructions.remove(self.fm.info_cursor.show)
##                        self.fm.instructions.append(self.fm.info_cursor.hide)
##                        self.fm.info_cursor.mode = 1
                elif keystate[pygame.K_SPACE]:
                    self.fm.desc = not self.fm.desc
                    self.cd = 20
                elif keystate[pygame.K_a]:
                    self.fm.RotateAnticlockwise()
                    self.cd = 20
                elif keystate[pygame.K_d]:
                    self.fm.RotateClockwise()
                    self.cd = 20
                elif keystate[pygame.K_1] and self.prmy_atk and self.act_record[0]: #Primary ATK
                    if not self.fm.desc:
                        self.fm.desc = not self.fm.desc
                        #self.fm.QuickSetTopView()
                    ClearAllTiles()
                    self.fm.show_hp = True
                    self.mv_highlight = False
                    self.mode = 1
                    self.cd = 20
                    self.prmy_atk.Get_Target()
                elif keystate[pygame.K_2] and self.scdy_atk and self.act_record[1]: #Secondary ATK
                    if not self.fm.desc:
                        self.fm.desc = not self.fm.desc
                    ClearAllTiles()
                    self.fm.show_hp = True
                    self.mv_highlight = False
                    self.mode = 2
                    self.cd = 20
                    self.scdy_atk.Get_Target()
                elif keystate[pygame.K_3] and self.skl and self.act_record[2]: #Regular Skill
##                    if not self.fm.desc:
##                        self.fm.desc = not self.fm.desc
                    ClearAllTiles()
                    self.mv_highlight = False
                    self.mode = 3
                    self.cd = 20
                    self.skl.Get_Target()
                elif keystate[pygame.K_4] and self.star_skl and self.act_record[3]: #Starstone Skill
                    ClearAllTiles()
                    self.fm.show_hp = True
                    self.mv_highlight = False
                    self.mode = 4
                    self.cd = 20
                    self.star_skl.Get_Target()
                elif keystate[pygame.K_5] and len(inventory) > 0 and self.act_record[4]: #Item
                    ClearAllTiles()
                    self.fm.show_hp = True
                    self.mv_highlight = False
                    self.mode = 5
                    self.cd = 20
                elif keystate[pygame.K_UP] and self.act_record[-1] and self.CheckSpace(self.x,self.y - 1):#self.y - 1 >= 0 and self.fm.tiles[self.y - 1][self.x] in self.mv_tiles:
                    self.MoveUp()
                    self.cd = 20
                elif keystate[pygame.K_RIGHT] and self.act_record[-1] and self.CheckSpace(self.x + 1,self.y):#self.x + 1 < self.fm.d[0] and self.fm.tiles[self.y][self.x + 1] in self.mv_tiles:
                    self.MoveRight()
                    self.cd = 20
                elif keystate[pygame.K_DOWN] and self.act_record[-1] and self.CheckSpace(self.x,self.y + 1):#self.y + 1 < self.fm.d[1] and self.fm.tiles[self.y + 1][self.x] in self.mv_tiles:
                    self.MoveDown()
                    self.cd = 20
                elif keystate[pygame.K_LEFT] and self.act_record[-1] and self.CheckSpace(self.x - 1,self.y):#self.x - 1 >= 0 and self.fm.tiles[self.y][self.x - 1] in self.mv_tiles:
                    self.MoveLeft()
                    self.cd = 20
            elif self.mode == 1:
                self.prmy_atk.Select_Target()
            elif self.mode == 2:
                self.scdy_atk.Select_Target()
            elif self.mode == 3:
                self.skl.Select_Target()
            elif self.mode == 4:
                self.star_skl.Select_Target()
            elif keystate[pygame.K_0]:
                ClearAllHighlightTiles()
                self.mv_highlight = False
                self.mode = 0
                self.cd = 20
        else:
            self.cd -= 1

    def OptionsDisplay(self):
        if self.mode == 0:
            #self.DrawOptions()
            if self.prmy_atk and self.prmy_atk.draw_lp < 200:
                self.prmy_atk.draw_lp += 10
                self.prmy_atk.DrawOptions(lp = False)
            elif self.scdy_atk and self.scdy_atk.draw_lp < 200:
                self.scdy_atk.draw_lp += 10
                self.scdy_atk.DrawOptions(lp = False)
            elif self.skl and self.skl.draw_lp < 200:
                self.skl.draw_lp += 10
                self.skl.DrawOptions(lp = False)
            elif self.star_skl and self.star_skl.draw_lp < 200:
                self.star_skl.draw_lp += 10
                self.star_skl.DrawOptions(lp = False)    
            else:
                self.DrawOptions()
        elif self.mode != 0:
            if self.draw_lp < 100:
                self.draw_lp += 5
                self.DrawOptions(lp = False)
            else:
                if self.mode == 1:
                    self.prmy_atk.DrawOptions()
                elif self.mode == 2:
                    self.scdy_atk.DrawOptions()
                elif self.mode == 3:
                    self.skl.DrawOptions()
                elif self.mode == 4:
                    self.star_skl.DrawOptions()
