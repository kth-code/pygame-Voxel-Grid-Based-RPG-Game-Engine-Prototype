import pygame
from random import *
from math import *
from VoxelGame_BaseVars import *
from VoxelGame_Visuals import *
from VoxelGame_InfoCursor import *

class Overview_Unit():
    #paths = [[sx,sy,ex,ey,time], ...]
    def __init__(self,paths = []):#,wait = 10):
        self.fm = tile_sprites.sprites()[0]
        self.c = 0
        self.paths = paths
        self.x = self.paths[self.c][0]
        self.y = self.paths[self.c][1]
        self.offx = 0
        self.offy = 0

        self.dx = self.paths[self.c][2] - self.paths[self.c][0]
        self.dy = self.paths[self.c][1] - self.paths[self.c][3]

        #self.wait = wait
        self.loop = 0

        self.fm.focus = self
        self.fm.mode = -2
        self.fm.visual_sprites.append(self)

    def update(self):
        if self.loop <= self.paths[self.c][4]:
            self.offx = self.dx * self.loop/self.paths[self.c][4]
            self.offy = self.dy * self.loop/self.paths[self.c][4]
            self.loop += 1
        else:
            if self.c == len(self.paths) - 1:
                self.fm.visual_sprites.remove(self)
                self.fm.mode = 2
                self.fm.focus = None
            else:
                self.c += 1
                self.x = self.paths[self.c][0]
                self.y = self.paths[self.c][1]
                self.offx = 0
                self.offy = 0

                self.dx = self.paths[self.c][2] - self.paths[self.c][0]
                self.dy = self.paths[self.c][1] - self.paths[self.c][3]

                self.loop = 0

    def draw(self):
        pass

intro_clrs = [[(88,194,240),(88,157,240),(78,112,211),(126,212,255)],
              [(165,91,212),(147,69,211),(121,56,192),(185,126,255)],
              [(144,245,211),(112,241,184),(65,215,149),(133,240,180)]]#(136,69,219)]]

#transparent_screen = pygame.Surface((window_width,window_height)).convert_alpha()

class Unit_Introduction():
    def __init__(self,name = ["Test Unit"],msg = ["Lorum Ipsum"],clr = [[0]],focus = [None]):#,wait = 10):
        self.fm = tile_sprites.sprites()[0]
        self.t_font = game_font20

        self.names = name
        self.msgs = msg
##        self.descs = list(txt)
        self.clrs = clr
        self.foci = focus
        self.count = -1

        self.next()
        self.fm.mode = -2
        self.fm.visual_sprites.append(self)

    def next(self):
        self.count += 1
        if len(self.names) == self.count:
            self.fm.visual_sprites.remove(self)
            self.fm.mode = 2
            self.fm.focus = None
        else:
            self.d_lp = 100
            self.drop = False
            self.name = title_font50.render(self.names[self.count],True,(255,255,255))#self.names[self.count]
            self.name = pygame.transform.rotate(self.name,4.76)
            self.n_rect = self.name.get_rect()
            
            self.msg = title_font50.render(self.msgs[self.count],True,(255,255,255))#self.names[self.count]
            self.msg = pygame.transform.rotate(self.msg,4.76)
            self.m_rect = self.msg.get_rect()
            
            self.clr = self.clrs[self.count]
            if len(self.clr) == 1:
                self.clr = intro_clrs[self.clr[0]]
            #transparent_screen.fill(self.clr[3])
            self.fm.focus = self.foci[self.count]

    def update(self):
        if self.drop:
            self.d_lp += 2
            #transparent_screen.set_alpha(100-self.d_lp)
            if self.d_lp >= 100:
                self.next()
        elif self.d_lp > 0:
            self.d_lp -= 2
            if self.d_lp <= 0:
                self.d_lp = 0
            #transparent_screen.set_alpha(100-self.d_lp)
        else:
            keystate = pygame.key.get_pressed()
            if keystate[pygame.K_z]:
                self.drop = True
        
    def draw(self):
        
        #game_window.blit(transparent_screen,(0,0))
        w = [0,500,700]
        h = [125,75,50]
        for i in range(3):
            pygame.draw.polygon(game_window,self.clr[2-i],[[0,0],
                                                           [window_width - w[i],- self.d_lp],
                                                           [0,h[i] - self.d_lp * 2]])
            pygame.draw.polygon(game_window,self.clr[2-i],[[window_width,window_height],
                                                           [w[i],window_height + self.d_lp],
                                                           [window_width,window_height - h[i] + self.d_lp * 2]])
        if self.d_lp == 0 and not self.drop:
            rect = key_icon_z.get_rect()
            rect.left, rect.bottom = 10,window_height - 10
            text = title_font20.render("Confirm",True,(255,255,255))
            textRect = text.get_rect()
            textRect.left = rect.right + 5
            textRect.centery = rect.centery
            game_window.blit(text,textRect)
            game_window.blit(key_icon_z,rect)
            
        self.n_rect.left = 20
        self.n_rect.bottom = 125 - self.d_lp * 2
        game_window.blit(self.name,self.n_rect)

        self.m_rect.right = window_width - 20
        self.m_rect.top = window_height - 130 + self.d_lp * 2#window_height - 150 + self.d_lp * 2
        game_window.blit(self.msg,self.m_rect)

        
            
#Mode:
#Non Battle
#-1: Pre, -2: Visual Cues, -3: Dialogue,-4: Victory Screen, -5: Lose Screen
#In Battle
#0: Data Check, 1: Hero Turn, 2: Enemy Turn
class Field_Manager(pygame.sprite.Sprite):
    def __init__(self, w, h, v, d,c = 6):
        pygame.sprite.Sprite.__init__(self)
        self.tiles = []
        self.objects = []
        self.highlights = []
        self.targets = []
        self.boundaries = []
        self.glowframes = []
        self.units_list = [] #For unit head count
        self.teams_list = [[],[],[]]
        self.total_count = [0,0,0] 

        self.w = w #Width of tile
        self.h = h #Height of tile
        self.v = v #Difference between height of Tile(h = 0), Tile(h = 1)

        self.ch = c
        self.cv = c * 4

        self.dir = 0 #N 0, E 90, S 180, W 270
        
        self.d = d
        s = [int(window_width/2 - self.w * (self.d[0]/2 - 0.5)),int(window_height/2 - self.h * (self.d[1]/2 - 0.5))]
        self.s_x = s[0] #Centre x pos of tile(0,0)
        self.s_y = s[1] #Centre y pos of tile(0,0)
        tile_sprites.add(self)

        self.visual_sprites = []

        self.cd = 0
        self.desc = False
        self.turnable = True

        self.show_hp = False

        self.focus = None #Unit to lock centre

        self.acting_units = []#units for current turn
        self.acting_unit = None
        self.a_cd = 0

        self.t_lp = 0

        self.projectile_count = 0

        self.info_cursor = Info_Cursor()
        self.mode = 0

        self.instructions = []

    def AddUnit(self,unit):
        self.units_list.append(unit)
        self.teams_list[unit.faction].append(unit)
        self.total_count[unit.faction] += 1

    def RemoveUnit(self,unit):
        self.units_list.remove(unit)
        self.teams_list[unit.faction].remove(unit)
        if unit == self.focus:
            self.foucs = None
            self.AdjustStartPt()

    def GetUnit(self,x,y):
        for i in self.units_list:
            if i.x == x and i.y == y:
                return i

    def Get_ActingUnits(self,faction = 0):
        self.acting_units = []
        for i in self.units_list:
            if i.can_act and i.faction == faction and i.HP > 0:
                self.acting_units.append(i)
                i.action_pts = 2

    def QuickSetTopView(self):
        self.desc = True
        self.v = 0
        self.h = self.w
        self.AdjustStartPt()

    def QuickSetSideView(self):
        self.desc = False
        self.v = self.cv
        self.h = self.w - self.ch
        self.AdjustStartPt()

    def QuickSetView(self,desc,v,h):
        self.desc = desc
        self.v = v
        self.h = h
        self.AdjustStartPt()
        
    def AdjustStartPt(self):
        s = [int(window_width/2 - self.w * (self.d[0]/2 - 0.5)),int(window_height/2 - self.h * (self.d[1]/2 - 0.5))]
        if self.focus:
            s[0] += self.w * (self.d[0]/2 - 0.5 - self.focus.x - self.focus.offx) 
            s[1] += self.h * (self.d[1]/2 - 0.5 - self.focus.y + self.focus.offy) 
        self.s_x = s[0]
        self.s_y = s[1]

    def Update_Objects(self):
        for y in range(self.d[1]):
            for x in range(self.d[0]):
                if self.objects[y][x]:
                    self.objects[y][x].origin = self.tiles[y][x]

    def RotateAnticlockwise(self):
        x,y = self.info_cursor.x, self.info_cursor.y
        self.info_cursor.x = y
        self.info_cursor.y = self.d[0] - 1 - x

        for i in self.units_list:
            x,y = i.x,i.y
            i.x = y
            i.y = self.d[0] - 1 - x
        
        self.tiles = list(zip(*self.tiles))[::-1]
        self.objects = list(zip(*self.objects))[::-1]
        self.highlights = list(zip(*self.highlights))[::-1]
        self.targets = list(zip(*self.targets))[::-1]
        self.boundaries = list(zip(*self.boundaries))[::-1]
        self.glowframes = list(zip(*self.glowframes))[::-1]
            
        self.d.reverse()

        for i in range(self.d[1]):
            self.tiles[i] = list(self.tiles[i])
            self.objects[i] = list(self.objects[i])
            self.highlights[i] = list(self.highlights[i])
            self.targets[i] = list(self.targets[i])
            self.boundaries[i] = list(self.boundaries[i])
            self.glowframes[i] = list(self.glowframes[i])
                
        for y in range(len(self.tiles)):
            for x in range(len(self.tiles[y])):
                self.tiles[y][x].x = x
                self.tiles[y][x].y = y
                if self.objects[y][x]:
                    self.objects[y][x].x = x
                    self.objects[y][x].y = y
        self.AdjustStartPt()
        self.dir = (self.dir - 90)%360

    def RotateClockwise(self):
        x,y = self.info_cursor.x, self.info_cursor.y
        self.info_cursor.x = self.d[1] - 1 - y
        self.info_cursor.y = x

        for i in self.units_list:
            x,y = i.x,i.y
            i.x = self.d[1] - 1 - y
            i.y = x
        
        new_field = []
        for i in range(len(self.tiles[0])):
            li = list(map(lambda x: x[i], self.tiles))
            li.reverse()
            new_field.append(li)
        self.tiles = new_field
        
        new_field = []
        for i in range(len(self.objects[0])):
            li = list(map(lambda x: x[i], self.objects))
            li.reverse()
            new_field.append(li)
        self.objects = new_field

        new_field = []
        for i in range(len(self.highlights[0])):
            li = list(map(lambda x: x[i], self.highlights))
            li.reverse()
            new_field.append(li)
        self.highlights = new_field

        new_field = []
        for i in range(len(self.targets[0])):
            li = list(map(lambda x: x[i], self.targets))
            li.reverse()
            new_field.append(li)
        self.targets = new_field

        new_field = []
        for i in range(len(self.boundaries[0])):
            li = list(map(lambda x: x[i], self.boundaries))
            li.reverse()
            new_field.append(li)
        self.boundaries = new_field

        new_field = []
        for i in range(len(self.glowframes[0])):
            li = list(map(lambda x: x[i], self.glowframes))
            li.reverse()
            new_field.append(li)
        self.glowframes = new_field

        self.d.reverse()
        
        for y in range(len(self.tiles)):
            for x in range(len(self.tiles[y])):
                self.tiles[y][x].x = x
                self.tiles[y][x].y = y
                if self.objects[y][x]:
                    self.objects[y][x].x = x
                    self.objects[y][x].y = y

        self.AdjustStartPt()
        self.dir = (self.dir + 90)%360    

    def DrawBasicInstructions(self):
        if self.turnable:
            for i in self.instructions:
                game_window.blit(i[0],i[1])
                game_window.blit(i[2],i[3])

    def AddInstructions(self,i):
        if i not in self.instructions:
            self.instructions.append(i)

    def RemoveInstructions(self,i):
        if i in self.instructions:
            self.instructions.remove(i)

    def CheckTileWithinScreen(self,t):
        if t.br[1] < 0:
            return False
        elif t.tl[1] > window_height:
            return False
        elif t.tr[0] < 0:
            return False
        elif t.bl[0] > window_width:
            return False
        return True

    def update(self):
        if self.mode < 0:
            if self.mode >= -2:
                self.AdjustStartPt()
                for y in range(self.d[1]):
                    for x in range(self.d[0]):
                        self.tiles[y][x].Update_Height()
                for y in range(self.d[1]):
                    for x in range(self.d[0]):
                        self.tiles[y][x].update()
                for y in self.objects:
                    for x in y:
                        if x:
                            x.update()
                
                for i in self.units_list:
                    i.update()
                for y in self.visual_sprites:
                    y.update()
                if len(self.visual_sprites) > 0:
                    self.visual_sprites[0].update()
        else:
            self.Update_Battlefield()

    def draw(self):
        if self.mode < 0:
            if self.mode == -1:
                self.Draw_Battlefield()
            elif self.mode == -2:
                self.Draw_Battlefield()
        else:
            self.Draw_Battlefield()

    def Update_Battlefield(self):
        if self.desc:
            if self.v > 0:       
                self.v -= 1
                self.h += 0.25
        else:
            if self.v < self.cv:       
                self.v += 1
                self.h -= 0.25
        self.AdjustStartPt()
        
        for y in range(self.d[1]):
            for x in range(self.d[0]):
                self.tiles[y][x].Update_Height()
        for y in range(self.d[1]):
            for x in range(self.d[0]):
                self.tiles[y][x].update()
        for y in self.objects:
            for x in y:
                if x:
                    x.update()
        if self.mode == 0:
            self.info_cursor.update()
        for x in self.units_list:
            x.update()
        for y in self.visual_sprites:
            y.update()
##        for i in self.acting_units:
##            if i.action_pts == 0:
##                self.acting_units.remove(i)

        if self.a_cd == 0 and self.projectile_count == 0:
            if self.mode == 1:
                if len(self.acting_units) == 0:
                    self.mode = 2
                    self.a_cd = fps#3 * fps
                    TurnDisplay("Enemies'  Turn!",clr = faction_clrs[1],d = 2)
                    for i in self.units_list:
                        if i.faction == 0:
                            i.EndTurnAct()
                    for i in self.units_list:
                        if i.faction == 0:
                            i.EndTurn()
                    for i in self.units_list:
                        if i.faction == 1:
                            i.StartTurnAct()
                    for i in self.units_list:
                        if i.faction == 1:
                            i.StartTurn()
                    self.Get_ActingUnits(1)
                    for i in self.acting_units:
                        i.Set_ActPts(0)
                if self.acting_unit:
                    self.acting_unit.Act()
            elif self.mode == 2:
                if len(self.acting_units) == 0:
                    self.mode = 1
                    self.a_cd = fps#3 * fps
                    TurnDisplay("Your  Turn!",clr = faction_clrs[0],d = 1)
                    for i in self.units_list:
                        if i.faction == 1:
                            i.EndTurnAct()
                    for i in self.units_list:
                        if i.faction == 1:
                            i.EndTurn()
                    for i in self.units_list:
                        if i.faction == 0:
                            i.StartTurnAct()
                    for i in self.units_list:
                        if i.faction == 0:
                            i.StartTurn()
                    self.Get_ActingUnits(0)
                    for i in self.acting_units:
                        i.Set_ActPts(0)
                    if len(self.acting_units) > 0:
                        self.acting_unit = self.acting_units[0]
                        self.focus = self.acting_unit
                        self.acting_unit.mode = 0
        elif self.projectile_count == 0:
            self.a_cd -= 1

    def Draw_Battlefield(self):
        t = []
        self.t_lp = (self.t_lp + 2)%360
        for y in self.tiles:
            for i in y:
                if self.CheckTileWithinScreen(i):
                    i.DrawSurface()
                    i.DrawHighlight()
                    i.DrawSide()
                    i.DrawEdges()
                    if i.marking:
                        i.DrawMarking()
                    if self.boundaries[i.y][i.x]:
                        DrawTileBound(self.tiles[i.y][i.x])
                    if self.glowframes[i.y][i.x]:
                        DrawTileGlow(self.tiles[i.y][i.x],self.t_lp)
                    if self.targets[i.y][i.x]:
                        for j in self.units_list:
                            if j.x == i.x and j.y == i.y:
                                DrawUnitSelect(j,self.t_lp)
                                break
            for i in y:
                if self.CheckTileWithinScreen(i):
                    for j in i.visual_sprites:
                        j.draw_b()
                    if self.objects[i.y][i.x]:
                        self.objects[i.y][i.x].Draw()
            for i in y:
                if self.CheckTileWithinScreen(i):
                    if self.mode == 0:
                        if i.y == self.info_cursor.y and i.x == self.info_cursor.x:
                            self.info_cursor.Draw()
                    for j in self.units_list:
                        if j.x == i.x and j.y == i.y:
                            j.Draw()
##                    if self.units[i.y][i.x]:
##                        self.units[i.y][i.x].Draw()
                    for j in i.visual_sprites:
                        j.draw_f()
        self.DrawBasicInstructions()
        if self.mode == 0:
            if self.info_cursor.unit:
                self.info_cursor.DrawInfo()
        elif self.mode == 1:
            if self.acting_unit:
                self.acting_unit.OptionsDisplay()
        for i in self.visual_sprites:
            i.draw()

unit = pygame.Surface((10,30))
unit.fill((0,200,255))
u_rect = unit.get_rect()

class Tile(pygame.sprite.Sprite):
    def __init__(self, x = 0, y = 0, h = 0):
        pygame.sprite.Sprite.__init__(self)
        self.x = x #x WEST (0) TO EAST
        self.y = y #z NORTH (0) TO SOUTH
        self.h = h#-randint(0,20)/20#h #y BOTTOM (0) TO TOP
        self.th = h
        self.ch = []
        
        self.t_clr = (126,200,80)
        self.s_clr = (112,84,62)
        self.e_clr = (80,148,37)

        self.empty = False
        self.thickness = 0
        self.marking = False
        
        fm = tile_sprites.sprites()[0]
        self.centerx = fm.s_x + self.x * fm.w
        self.centery = fm.s_y + self.y * fm.h - fm.v * self.h
        self.tl = [self.centerx - CorInt(fm.w/2),self.centery - CorInt(fm.h/2)]
        self.bl = [self.centerx - CorInt(fm.w/2),self.centery + CorInt(fm.h/2)]
        self.tr = [self.centerx + CorInt(fm.w/2),self.centery - CorInt(fm.h/2)]
        self.br = [self.centerx + CorInt(fm.w/2),self.centery + CorInt(fm.h/2)]
        self.t_pts = [self.tl,self.bl,self.br,self.tr]
        self.s_pts = []
        self.e_pts = []

        self.rect = pygame.Rect(0,0,fm.w,100)

        self.visual_sprites = []

        self.StatusEffect = []
        self.EffectTimer = []
        self.SEVisual = []
        self.SE_Values = []

        self.Burn = False
        self.Freeze = False
        self.Shock = False
        self.Poison = False
        self.Splash = False
        self.Blind = False

        self.water = False

        self.fm = fm

    def update(self):
        self.GetSurfaces()
        self.GetEdges()
        for i in self.visual_sprites:
            i.update() 
        self.Update_SEV() #Must be after update visual_sprites

    def Update_Height(self):
        if len(self.ch) > 0:
            self.ch[0][1] -= 1
            self.h += self.ch[0][0]
            if self.ch[0][1] == 0:
                self.ch.pop(0)
        else:
            if self.h != self.th:
                if self.h > self.th:
                    self.h -= 0.05
                elif self.h < self.th:
                    self.h += 0.05
                if abs(self.h - self.th) < 0.05:
                    self.h = int(self.th * 100)/100

    def Update_SEV(self):
        for i in range(len(self.EffectTimer)):
            if not self.SEVisual[i]:
                self.SEVisual[i] = True
                self.AssignVisualSE(self.StatusEffect[i])

    def ApplyStatusEffect(self,effect,turn,value = None):
        if effect in self.StatusEffect:
            self.EffectTimer[self.StatusEffect.index(effect)] += turn
        else:
            exec("self."+effect+" = True")
            self.StatusEffect.append(effect)
            self.EffectTimer.append(turn)
            self.SEVisual.append(False)
            if value == None:
                value = SE_Default_Values.get(effect)
            self.SE_Values.append(value)

    def EffectTimerCountdown(self):
        for t in range(len(self.EffectTimer)):
            self.EffectTimer[t] -= 1
        while 0 in self.EffectTimer:
            n = self.EffectTimer.index(0)
            exec("self."+self.StatusEffect[n]+" = False")
            self.StatusEffect.pop(n)
            self.EffectTimer.pop(n)
            self.SEVisual.pop(n)
            self.SE_Values.pop(n)

    def AssignVisualSE(self,effect):
        if effect == "Burn":
            #SEV = TileStatusEffectVisual(self,effect)
            for i in range(4):
                SEV = TileStatusEffectVisual(self,effect, SCD = i)
        elif effect == "Freeze":
            for i in range(2):
                SEV = TileStatusEffectVisual(self,effect, SCD = i)
        elif effect == "Shock":
            SEV = TileStatusEffectVisual(self,effect)
        elif effect == "Poison":
            for i in range(3):
                SEV = TileStatusEffectVisual(self,effect, SCD = i)
        elif effect == "Splash":
            for i in range(3):
                SEV = TileStatusEffectVisual(self,effect, SCD = i)
        elif effect == "Drain":
            for i in range(2):
                SEV = TileStatusEffectVisual(self,effect, SCD = i)
        elif effect == "Blind":
            SEV = TileStatusEffectVisual(self,effect)

    def GetSurfaces(self):
        self.centerx = self.fm.s_x + self.x * self.fm.w
        self.centery = self.fm.s_y + self.y * self.fm.h - self.fm.v * self.h
        self.rect.centerx = self.centerx
        self.rect.bottom = self.centery

        self.tl = [self.centerx - self.fm.w/2 + 1,self.centery - self.fm.h/2 + 1]
        self.bl = [self.centerx - self.fm.w/2 + 1,self.centery + self.fm.h/2]
        self.tr = [self.centerx + self.fm.w/2,self.centery - self.fm.h/2 + 1]
        self.br = [self.centerx + self.fm.w/2,self.centery + self.fm.h/2]

        self.t_pts = [self.tl,self.bl,self.br,self.tr]
        self.s_pts = []
        if self.y < self.fm.d[1] - 1:
            if self.fm.tiles[self.y + 1][self.x].empty and not self.empty:
                self.s_pts = [self.bl,
                              self.br,
                              [self.br[0],self.br[1] + self.fm.v * (self.h + 1)],
                              [self.bl[0],self.bl[1] + self.fm.v * (self.h + 1)]]
            else:
                dh = self.h - self.fm.tiles[self.y + 1][self.x].h
                if self.empty and dh > self.thickness:
                    dh = self.thickness
                if dh > 0:
                    self.s_pts = [self.bl,
                                  self.br,
                                  [self.br[0],self.br[1] + self.fm.v * dh],
                                  [self.bl[0],self.bl[1] + self.fm.v * dh]]
        elif self.empty:
            self.s_pts = [self.bl,
                          self.br,
                          [self.br[0],self.br[1] + self.fm.v * self.thickness],
                          [self.bl[0],self.bl[1] + self.fm.v * self.thickness]]
        else:
            self.s_pts = [self.bl,
                          self.br,
                          [self.br[0],self.br[1] + self.fm.v * (self.h + 1)],
                          [self.bl[0],self.bl[1] + self.fm.v * (self.h + 1)]]


    def GetEdges(self):
        self.e_pts = []
        n,e,s,w = False,False,False,False
        if self.x == 0:
            self.e_pts.append([[self.tl[0] + 1,self.tl[1]],
                               [self.bl[0] + 1,self.bl[1]]])
        #    w = True
        elif self.h - self.fm.tiles[self.y][self.x - 1].h > 0: #>= 1:
            self.e_pts.append([[self.tl[0] + 1,self.tl[1]],
                               [self.bl[0] + 1,self.bl[1]]])
        elif self.h == self.fm.tiles[self.y][self.x - 1].h:
            w = True
        if self.x == self.fm.d[0] - 1:
            self.e_pts.append([[self.tr[0] - 1,self.tr[1]],
                               [self.br[0] - 1,self.br[1]]])
        #    e = True
        elif self.h - self.fm.tiles[self.y][self.x + 1].h > 0:
            self.e_pts.append([[self.tr[0] - 1,self.tr[1]],
                               [self.br[0] - 1,self.br[1]]])
        elif self.h == self.fm.tiles[self.y][self.x + 1].h:
            e = True
        if self.y == 0:
            self.e_pts.append([[self.tl[0],self.tl[1] + 1],
                               [self.tr[0],self.tr[1] + 1]])
        #    n = True
        elif self.h - self.fm.tiles[self.y - 1][self.x].h > 0:
            self.e_pts.append([[self.tl[0],self.tl[1] + 1],
                               [self.tr[0],self.tr[1] + 1]])
        elif self.h == self.fm.tiles[self.y - 1][self.x].h:    
            n = True
        if self.y == self.fm.d[1] - 1:
            self.e_pts.append([[self.bl[0],self.bl[1] - 1],
                               [self.br[0],self.br[1] - 1]])
        #    s = True
        elif self.h - self.fm.tiles[self.y + 1][self.x].h > 0:
            self.e_pts.append([[self.bl[0],self.bl[1] - 1],
                               [self.br[0],self.br[1] - 1]])
        elif self.h == self.fm.tiles[self.y + 1][self.x].h > 0:
            s = True

        if self.x != 0 and self.y != 0:
            if (n or w) and self.h - self.fm.tiles[self.y - 1][self.x - 1].h > 0:
                self.e_pts.append([[self.tl[0] + 1,self.tl[1]],
                                   [self.tl[0] + 1,self.tl[1] + 2]])
        if self.x != self.fm.d[0] - 1 and self.y != 0:
            if (n or e) and self.h - self.fm.tiles[self.y - 1][self.x + 1].h > 0:
                self.e_pts.append([[self.tr[0] - 1,self.tr[1]],
                                   [self.tr[0] - 1,self.tr[1] + 2]])
        if self.x != self.fm.d[0] - 1 and self.y != self.fm.d[1] - 1:
            if (s or e) and self.h - self.fm.tiles[self.y + 1][self.x + 1].h > 0:
                self.e_pts.append([[self.br[0] - 1,self.br[1] - 2],
                                   [self.br[0] - 1,self.br[1]]])
        if self.x != 0 and self.y != self.fm.d[1] - 1:
            if (s or w) and self.h - self.fm.tiles[self.y + 1][self.x - 1].h > 0:
                self.e_pts.append([[self.bl[0] + 1,self.bl[1] - 2],
                                   [self.bl[0] + 1,self.bl[1]]])
    
    def DrawSurface(self):
        pygame.draw.polygon(game_window,self.t_clr,self.t_pts)
##        text = stat_font18.render(str(self.x)+","+str(self.y),True,(255,255,255))
##        textRect = text.get_rect()
##        textRect.center = (self.centerx,self.centery)
##        game_window.blit(text,textRect)

    def DrawHighlight(self):
        hcs = self.fm.highlights[self.y][self.x]
        if len(hcs) > 0:
            clrs = [self.t_clr]
            for i in hcs:
                clrs.append(highlight_clrs[i])
            pygame.draw.polygon(game_window, MergeClrs(clrs), self.t_pts)

    def DrawSide(self):
        if len(self.s_pts) > 0:
            pygame.draw.polygon(game_window, self.s_clr, self.s_pts)

    def DrawEdges(self):
        for i in self.e_pts:
            pygame.draw.line(game_window, self.e_clr, i[0], i[1], width = 3)

def CheckifWaters(a,b):
    return a.water and b.water


class Waters(Tile):
    def __init__(self,x,y,h):
        Tile.__init__(self,x,y,h)
        self.water = True
        self.marking = True
        self.r = 0
        self.s_lp = randint(0,4)
        self.f_lp = 0

    def DrawSide(self):
        self.f_lp = (self.f_lp + 0.15)%6
        if len(self.s_pts) > 0:
            self.s_lp = (self.s_lp + 0.1)%5
            s = abs(2 - self.s_lp)
            pygame.draw.polygon(game_window, self.s_clr, self.s_pts)
            c = self.fm.v/self.fm.cv
            w = (self.br[0] - self.bl[0])/6
            h = (self.fm.v)/4
            
            if self.fm.v > 0:
                for i in range(int((self.s_pts[2][1] - self.s_pts[1][1] - int(self.f_lp))//h)):
                    pygame.draw.line(game_window, self.f_clr, [self.bl[0],self.bl[1] + int(self.f_lp) + h * i], [self.br[0],self.br[1] + int(self.f_lp) + h * i])
            
            pts = [[self.s_pts[2][0], self.s_pts[2][1] - (1 + s) * c],
                   self.s_pts[2],
                   self.s_pts[3]]
            for i in range(3):
                for j in range(5):
                    pts.append([self.s_pts[3][0] + w * (i * 2 + 1) - cos(radians(j * 45)) * w, self.s_pts[3][1] - (1 + s) * c - abs(sin(radians(j * 45))) * 4 * c])
            pygame.draw.polygon(game_window, (255,255,255), pts) 

    def DrawMarking(self):
        self.r = (self.r + 1)%180
        r = 5 * sin(radians(self.r))
        d = [False,False,False,False] #N E S W
        c = [False,False,False,False] #NE SE SW NW
        clr = Brighten(self.t_clr,20 * abs(5 - r))

        if self.x > 0:
            tw = self.fm.tiles[self.y][self.x - 1]
            if (not CheckifWaters(tw,self) or tw.h < self.h) and tw.type_id not in pits_values:
                d[3] = True
            if CheckifWaters(tw,self) and tw.h < self.h:
                d[3] = False
        if self.x < self.fm.d[0] - 1:
            te = self.fm.tiles[self.y][self.x + 1]
            if (not CheckifWaters(te,self) or te.h < self.h) and te.type_id not in pits_values:
                d[1] = True
            if CheckifWaters(te,self) and te.h < self.h:
                d[1] = False
        if self.y > 0:
            tn = self.fm.tiles[self.y - 1][self.x]
            if (not CheckifWaters(tn,self) or tn.h < self.h) and tn.type_id not in pits_values:
                d[0] = True
            if CheckifWaters(tn,self) and tn.h < self.h:
                d[0] = False
        if self.y < self.fm.d[1] - 1:
            ts = self.fm.tiles[self.y + 1][self.x]
            if (not CheckifWaters(ts,self) or ts.h < self.h) and ts.type_id not in pits_values:
                d[2] = True
            if CheckifWaters(ts,self) and ts.h < self.h:
                d[2] = False

        if self.x > 0 and self.y > 0:
            tnw = self.fm.tiles[self.y - 1][self.x - 1]
            if not CheckifWaters(tnw,self) and tnw.type_id not in pits_values:
                if (tn.water or tn.type_id == 0) and (tw.water or tw.type_id == 0):
                    c[3] = True
        if self.x > 0 and self.y < self.fm.d[1] - 1:
            tsw = self.fm.tiles[self.y + 1][self.x - 1]
            if not CheckifWaters(tsw,self) and tsw.type_id not in pits_values:
                if (ts.water or ts.type_id == 0) and (tw.water or tw.type_id == 0):
                    c[2] = True
        if self.x < self.fm.d[0] - 1 and self.y < self.fm.d[1] - 1:
            tse = self.fm.tiles[self.y + 1][self.x + 1]
            if not CheckifWaters(tse,self) and tse.type_id not in pits_values:
                if (ts.water or ts.type_id == 0) and (te.water or te.type_id == 0):
                    c[1] = True
        if self.x < self.fm.d[0] - 1 and self.y > 0:
            tne = self.fm.tiles[self.y - 1][self.x + 1]
            if not CheckifWaters(tne,self) and tne.type_id not in pits_values:
                if (tn.water or tn.type_id == 0) and (te.water or te.type_id == 0):
                    c[0] = True

        if d[0]:
            pts = [[self.tl[0],self.tl[1] + r],[self.tr[0],self.tr[1] + r]]
            if d[1]:
                pts[1] = [self.tr[0] - r,self.tr[1] + r]
            if d[3]:
                pts[0] = [self.tl[0] + r,self.tl[1] + r]
            pygame.draw.lines(game_window,clr,False,pts)
        if d[1]:
            pts = [[self.tr[0] - r,self.tr[1]],[self.br[0] - r,self.br[1]]]
            if d[0]:
                pts[0] = [self.tr[0] - r,self.tr[1] + r]
            if d[2]:
                pts[1] = [self.br[0] - r,self.br[1] - r]
            pygame.draw.lines(game_window,clr,False,pts)
        if d[2]:
            pts = [[self.bl[0],self.bl[1] - r],[self.br[0],self.br[1] - r]]
            if d[1]:
                pts[1] = [self.br[0] - r,self.br[1] - r]
            if d[3]:
                pts[0] = [self.bl[0] + r,self.bl[1] - r]
            pygame.draw.lines(game_window,clr,False,pts)
        if d[3]:
            pts = [[self.tl[0] + r,self.tl[1]],[self.bl[0] + r,self.bl[1]]]
            if d[0]:
                pts[0] = [self.tl[0] + r,self.tl[1] + r]
            if d[2]:
                pts[1] = [self.bl[0] + r,self.bl[1] - r]
            pygame.draw.lines(game_window,clr,False,pts)
    
        if c[0]:
            pts = [[self.tr[0] - r,self.tr[1]],[self.tr[0] - r,self.tr[1] + r],[self.tr[0],self.tr[1] + r]]
            pygame.draw.lines(game_window,clr,False,pts)
        if c[1]:
            pts = [[self.br[0] - r,self.br[1]],[self.br[0] - r,self.br[1] - r],[self.br[0],self.br[1] - r]]
            pygame.draw.lines(game_window,clr,False,pts)
        if c[2]:
            pts = [[self.bl[0] + r,self.bl[1]],[self.bl[0] + r,self.bl[1] - r],[self.bl[0],self.bl[1] - r]]
            pygame.draw.lines(game_window,clr,False,pts)
        if c[3]:
            pts = [[self.tl[0] + r,self.tl[1]],[self.tl[0] + r,self.tl[1] + r],[self.tl[0],self.tl[1] + r]]
            pygame.draw.lines(game_window,clr,False,pts)

icon_path = "./_Symbol/"
cracks = pygame.image.load(icon_path + 'cracks_spritesheet.png').convert_alpha()
         
crack = []
for h in range(7):
    crack.append([])
    for i in range(4):
        crack[h].append(Spritesheet_Img(cracks,i * 40,0,40,40,scale = [40,34 + h]))

class Cover():
    def __init__(self, origin):
        self.origin = origin
        self.x = self.origin.x
        self.y = self.origin.y
        self.centerx = self.origin.centerx
        self.centery = self.origin.centery
        self.passable = False

        self.HP = 1 #Absorb 1 hit per HP
        self.MaxHP = 1
        self.MaxDMG = -99
        self.MinDMG = 0

        self.Pntl_HP = 0
        self.trigger = False

        #self.Property = []        

        self.t_clr = (51,12,90)
        self.s_clr = (47,18,77)
        self.e_clr = (34,13,55)

        self.fm = tile_sprites.sprites()[0]
        self.tl = [self.origin.tl[0] + 1,self.origin.tl[1] - self.fm.v + 1]
        self.bl = [self.origin.bl[0] + 1,self.origin.bl[1] - self.fm.v - 1]
        self.tr = [self.origin.tr[0] - 1,self.origin.tr[1] - self.fm.v + 1]
        self.br = [self.origin.br[0] - 1,self.origin.br[1] - self.fm.v - 1]
        self.t_pts = [self.tl,self.bl,self.br,self.tr]
        self.s_pts = [self.bl,self.br,[self.origin.br[0] - 1,self.origin.br[1] - 1],[self.origin.bl[0] + 1,self.origin.bl[1] - 1]]

    def HPChange(self,change,breach = False):
        if not breach and change < 0:
            if change < self.MaxDMG:
                change = self.MaxDMG
            elif change > self.MinDMG:
                change = 0
        change = CorInt(change)
        self.HP += change
        if change < 0:
            for i in range(4):
                Chip(self,[self.t_clr,self.s_clr,self.e_clr][randint(0,2)])
        if self.HP > self.MaxHP:
            self.HP = self.MaxHP
        elif self.HP < 0:
            self.HP = 0

    def ApplyPntlDMG(self,min_dmg,max_dmg,cvr_dmg,breach = False):
        if not breach and cvr_dmg < 0:
            if cvr_dmg < self.MaxDMG:
                cvr_dmg = self.MaxDMG
            elif cvr_dmg > self.MinDMG:
                cvr_dmg = 0
        self.Pntl_HP += cvr_dmg
        self.PntlBreakage()

    def PntlBreakage(self):
        pass

    def Breakage(self):
        pass

    def CheckifProperty(self,prop):
        return prop in self.Property

    def update(self):
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_v]:
            self.Breakage()
        if not CheckifSteppable(self.x,self.y):
            self.HP = 0
        if self.HP == 0:
            self.Breakage()
            for i in range(10):
                #a = randint(50,120)
                #Chip(self,(a,a,a))
                Chip(self,[self.t_clr,self.s_clr,self.e_clr][randint(0,2)])
            self.fm.objects[self.y][self.x] = None
            del self
        else:
            self.tl = [self.origin.tl[0] + 1,self.origin.tl[1] - self.fm.v + 1]
            self.bl = [self.origin.bl[0] + 1,self.origin.bl[1] - self.fm.v - 1]
            self.tr = [self.origin.tr[0] - 1,self.origin.tr[1] - self.fm.v + 1]
            self.br = [self.origin.br[0] - 1,self.origin.br[1] - self.fm.v - 1]
            self.t_pts = [self.tl,self.bl,self.br,self.tr]
            self.s_pts = [self.bl,self.br,[self.origin.br[0] - 1,self.origin.br[1] - 1],[self.origin.bl[0] + 1,self.origin.bl[1] - 1]]
            self.centerx = self.origin.centerx
            self.centery = (self.tl[1] + self.bl[1])/2

    def Draw(self):
        pygame.draw.polygon(game_window, self.t_clr, self.t_pts)
        if self.HP < self.MaxHP:
            if self.HP/self.MaxHP <= 0.25:
                pts = [[0,0,0.18,80,4],[0.18,95,0.23,120,3],[0.18,95,0.24,60,2],
                       [0,0,0.15,210,3],[0.15,210,0.2,230,3],[0.2,230,0.3,220,2],
                       [0,0,0.15,300,4],[0.15,300,0.22,330,3],[0.22,330,0.33,315,2],[0.22,330,0.28,340,2],
                       [0.5,30,0.4,25,3],[0.4,25,0.35,10,2],[0.4,25,0.35,40,1],
                       [0.5,150,0.35,165,3],[0.35,165,0.28,160,2],
                       [0.45,260,0.36,270,3]]
            elif self.HP/self.MaxHP <= 0.5:
                pts = [[0,0,0.18,80,3],[0.18,95,0.23,120,2],[0.18,95,0.24,60,2],
                       [0,0,0.15,210,3],[0.15,210,0.2,230,2],[0.2,230,0.26,220,2],
                       [0,0,0.15,300,3],[0.15,300,0.22,330,2],[0.22,330,0.31,315,2],[0.22,330,0.25,340,2],
                       [0.5,30,0.4,25,2],[0.4,25,0.35,10,1],
                       [0.5,150,0.35,165,2],
                       [0.45,260,0.36,270,2]]
            elif self.HP/self.MaxHP <= 0.75:
                pts = [[0,0,0.18,80,3],[0.18,95,0.23,120,2],[0.18,95,0.22,60,1],
                       [0,0,0.15,210,3],[0.15,210,0.2,230,2],[0.2,230,0.26,220,1],
                       [0,0,0.15,300,3],[0.15,300,0.22,330,2],[0.22,330,0.31,315,1],[0.22,330,0.22,340,1]]
            elif self.HP/self.MaxHP < 1:
                pts = [[0,0,0.18,80,2],
                       [0,0,0.15,210,2],
                       [0,0,0.15,300,2],[0.15,300,0.22,330,1]]
            for i in pts:
                pygame.draw.line(game_window,self.c_clr,
                                 [self.centerx + self.fm.w * i[0] * cos(radians(i[1] - self.fm.dir)),
                                  self.centery - self.fm.h * i[0] * sin(radians(i[1] - self.fm.dir))],
                                 [self.centerx + self.fm.w * i[2] * cos(radians(i[3] - self.fm.dir)),
                                  self.centery - self.fm.h * i[2] * sin(radians(i[3] - self.fm.dir))],
                                 width = i[4])
##            i = self.fm.ch - self.fm.w + int(self.fm.h)
##            if self.HP/self.MaxHP <= 0.25:
##                img = crack[i][3]
##            elif self.HP/self.MaxHP <= 0.5:
##                img = crack[i][2]
##            elif self.HP/self.MaxHP <= 0.75:
##                img = crack[i][1]
##            elif self.HP/self.MaxHP < 1:
##                img = crack[i][0]
##            rect = img.get_rect() 
##            rect.centerx = self.centerx
##            rect.centery = (self.tl[1] + self.bl[1])/2
##            game_window.blit(img,rect)
        pygame.draw.lines(game_window, self.e_clr, True, self.t_pts, width = 3)
        pygame.draw.polygon(game_window, self.s_clr, self.s_pts)  
        pygame.draw.lines(game_window, self.e_clr, True, self.s_pts, width = 3)

class Pit_Tile(Tile):
    '''Bottomless pit'''
    def __init__(self, x = 0, y = 0, h = 0):
        Tile.__init__(self,x,y,-1)
        self.t_clr = (0,0,0)
        self.s_clr = (0,0,0)
        self.e_clr = (0,0,0)

        self.empty = True

        self.name = "Pit Tile"
        self.type_id = tile_values.get(self.name)

    def GetEdges(self):
        pass
    
    def DrawSurface(self):
        pass

    def DrawSide(self):
        pass

    def DrawEdges(self):
        pass

class Grassy_Tile(Tile):
    def __init__(self, x = 0, y = 0, h = 0):
        Tile.__init__(self,x,y,h)

    def DrawSide(self):
        if len(self.s_pts) > 0:
            pygame.draw.polygon(game_window, self.s_clr, self.s_pts)
            pts = [[self.br[0],self.br[1] + 3 * self.fm.v/self.fm.cv],
                   self.br,self.bl,
                   [self.bl[0],self.bl[1] + 3 * self.fm.v/self.fm.cv]
                   ]
            c = self.fm.v/self.fm.cv
            w = (self.br[0] - self.bl[0])/3
            m = CorInt(w/2)
            for i in range(3):
                pts.append([self.bl[0] + w * i + m, self.bl[1] + 6 * c])
                pts.append([self.bl[0] + w * (i + 1), self.bl[1] + 3 * c])
            pygame.draw.polygon(game_window, self.e_clr, pts)

class Grass_Tile(Grassy_Tile):
    '''A tile of grassland'''
    def __init__(self, x = 0, y = 0, h = 0):
        Grassy_Tile.__init__(self,x,y,h)
        self.t_clr = (126,200,80)
        self.s_clr = (112,84,62)
        self.e_clr = Darken(self.t_clr,30)

        self.name = "Grass Tile"
        self.type_id = tile_values.get(self.name)

class Sand_Tile(Tile):
    '''A tile of sand and desert'''
    def __init__(self, x = 0, y = 0, h = 0):
        Tile.__init__(self,x,y,h)
        self.t_clr = (239,221,111)
        self.s_clr = Darken(self.t_clr,20)
        self.e_clr = Darken(self.t_clr,25)

        self.name = "Sand Tile"
        self.type_id = tile_values.get(self.name)


class Stone_Grass_Tile(Grassy_Tile):
    '''A tile of stone with a patch of grass'''
    def __init__(self, x = 0, y = 0, h = 0):
        Grassy_Tile.__init__(self,x,y,h)
        self.t_clr = (126,200,80)
        self.s_clr = (205,214,217)
        self.e_clr = Darken(self.t_clr,30)

        self.name = "Stone Grass Tile"
        self.type_id = tile_values.get(self.name)

class Water_Tile(Waters):
    '''A tile of shallow water, can eb stepped in but reduces movement'''
    def __init__(self, x = 0, y = 0, h = 0):
        Waters.__init__(self,x,y,h - 0.25)
        self.t_clr = (128,197,222)
        self.s_clr = (114,160,199)
        self.e_clr = Darken(self.t_clr,10)
        self.f_clr = Brighten(self.s_clr,20)

        self.name = "Water Tile"
        self.type_id = tile_values.get(self.name)

        self.marking = True

        self.r = 0   

class Unbreakable_Cover(Cover):
    def __init__(self, origin = None):
        '''Created from darkness, impossible to break with normal weapons & magic ATKs'''
        Cover.__init__(self, origin)

        self.t_clr = (51,12,90)
        self.s_clr = (47,18,77)
        self.e_clr = (34,13,55)
        self.c_clr = self.e_clr

        self.name = "Unbreakable Cover"
        self.type_id = object_values.get(self.name)

        self.HP = 1
        self.MaxHP = 1
        self.MaxDMG = 0
        self.MinDMG = 0
   
class Breakable_Cover(Cover):
    def __init__(self, origin = None):
        '''Created from stone, dirt or sand, prune to crack & shatter upon DMG from weapons & magic ATKs'''
        Cover.__init__(self, origin)

        self.t_clr = (150,150,150)
        self.s_clr = (100,100,100)
        self.e_clr = (80,80,80)
        self.c_clr = self.e_clr

        self.name = "Breakable Cover"
        self.type_id = object_values.get(self.name)

        self.HP = 1
        self.MaxHP = 4

class Fragile_Cover(Cover):
    def __init__(self, origin = None):
        '''Created from ice, prone to crack & shatter upon DMG from weapons & magic ATKs'''
        Cover.__init__(self, origin)

        self.t_clr = (140,225,255)#(180,240,255)
        self.s_clr = (110,200,235)#(140,225,255)
        self.e_clr = (160,235,255)#(25,195,255)
        self.c_clr = self.e_clr

        self.name = "Fragile Cover"
        self.type_id = object_values.get(self.name)

        self.HP = 1
        self.MaxHP = 1
        self.MaxDMG = -1
        self.MinDMG = 0

class Dark_Sludge():
    def __init__(self,origin = None):
        self.origin = origin
        self.x = self.origin.x
        self.y = self.origin.y
        self.centerx = self.origin.centerx
        self.centery = self.origin.centery
        self.passable = False

        self.HP = 1
        self.MaxHP = 1
        self.MaxDMG = 0
        self.MinDMG = 0

        self.Pntl_HP = 0
        self.trigger = False       

        self.t_clr = (55,23,101)
        self.g_clr = (115,47,151)
        self.s_clr = (44,19,80)

        self.fm = tile_sprites.sprites()[0]
        self.loop = randint(0,180)
        self.s = 0
        self.tl = self.origin.tl
        self.bl = self.origin.bl
        self.tr = self.origin.tr
        self.br = self.origin.br
        self.t_pts = [self.tl,self.bl,self.br,self.tr]
        self.s_pts = [self.bl,self.br,[self.origin.br[0] - 1,self.origin.br[1] - 1],[self.origin.bl[0] + 1,self.origin.bl[1] - 1]]

        self.name = "Dark Sludge"
        self.type_id = object_values.get(self.name)

    def update(self):
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_b]:
            self.HP = 0
        if not CheckifSteppable(self.x,self.y):
            self.HP = 0
        if self.HP == 0:
            if self.loop < 180:
                self.loop += 2
                if self.loop > 180:
                    self.loop = 180
            elif self.s < 0.5:
                self.s += 0.02
            else:
                self.fm.objects[self.y][self.x] = None
                del self
                return
        else:
            self.loop = (self.loop + 1)%180
        if self.loop == 0 or self.loop == 90:
            DropFlash(self.origin,offx = randint(0,15) * GenPN(),offy = randint(0,10) * GenPN(),r = randint(5,8),flatten = 0.2,spd = 1.5,a_clr = (98,41,171),b_clr = (132,42,180))
        if self.s == 0:
            s = sin(radians(self.loop)) * 10 * self.fm.v/self.fm.cv
            self.tl = [self.origin.tl[0],self.origin.tl[1] - s]
            self.bl = [self.origin.bl[0],self.origin.bl[1] - s]
            self.tr = [self.origin.tr[0],self.origin.tr[1] - s]
            self.br = [self.origin.br[0],self.origin.br[1] - s]
            self.t_pts = [self.tl,self.bl,self.br,self.tr]
            self.s_pts = [self.bl,self.br,self.origin.br,self.origin.bl]
            self.centerx = self.origin.centerx
            self.centery = (self.tl[1] + self.bl[1])/2
        else:
            w = self.fm.w * self.s
            h = self.fm.h * self.s
            s = sin(radians(self.loop)) * 10 * self.fm.v/self.fm.cv
            self.tl = [self.origin.tl[0] + w,self.origin.tl[1] - s + h]
            self.bl = [self.origin.bl[0] + w,self.origin.bl[1] - s - h]
            self.tr = [self.origin.tr[0] - w,self.origin.tr[1] - s + h]
            self.br = [self.origin.br[0] - w,self.origin.br[1] - s - h]
            self.t_pts = [self.tl,self.bl,self.br,self.tr]
            self.centerx = self.origin.centerx
            self.centery = (self.tl[1] + self.bl[1])/2

    def Draw(self):
        s = sin(radians(self.loop))
        pygame.draw.polygon(game_window, GradientClrs(self.t_clr,self.g_clr,1-s,s), self.t_pts)
        if self.s == 0:
            pygame.draw.polygon(game_window, self.s_clr, self.s_pts)

object_values = {"Unbreakable Cover": 1,
                 "Breakable Cover": 2,
                 "Fragile Cover": 3,
                 "Invisible Cover": 4,
                 "Effect Cover": 5,
                 "Dark Sludge": 6}

tile_values = {"Pit Tile": 0,
               "Grass Tile": 1,
               "Sand Tile": 2,
               "Water Tile": 3,
               "Deep Water Tile": 4,
               "Snow Tile": 5,
               "Ice Tile": 6,
               "Stone Grass Tile": 7,
               "Lava Tile": 8,
               "Withered Tile": 10,
               "Dark Sand Tile": 11,
               "Tainted Water Tile": 12,
               "Ooze Tile": 12,
               "Burn Tile": 20,
               "Freeze Tile": 21,
               "Shock Tile": 22,
               "Splash Tile": 23,
               "Poison Tile": 24,
               "Drain Tile": 25,
               "Cursed Tile": 26,
               "Invisible Tile": 27,
               "Invincible Tile": 28,}

tile_spawn = {0: Pit_Tile,
              1: Grass_Tile,
              2: Sand_Tile,
              3: Water_Tile,
              4: Stone_Grass_Tile}
