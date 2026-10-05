import pygame
from random import *
from math import *
from VoxelGame_BaseVars import *
from VoxelGame_Visuals import *

class Shots_Manager():
    def __init__(self,origin = None,target = None,projectile = None,collide = None,effect = "Magic",prop = [],prop_val = [],func = None):
        self.fm = tile_sprites.sprites()[0]
        self.origin = origin
        self.target = target
        self.func = func
        if projectile:
            self.projectile = projectile
        else:
            self.projectile = Base_Projectile
        self.SE = effect
        self.prop = prop
        self.prop_val = prop_val
        self.collide = collide

        self.fm.projectile_count += 1

        self.loop = -1

        self.c = 0
        
        self.fm.visual_sprites.append(self)

    def update(self):
        self.loop = (self.loop + 1)%15
        if len(self.target) == 0:
            self.fm.visual_sprites.remove(self)
            self.fm.projectile_count -= 1
            del self
        elif self.loop == 0:
            #[Magic_Projectile,Burn_Projectile,Freeze_Projectile,Splash_Projectile,Poison_Projectile,Drain_Projectile][self.c](self.origin,self.target[0],self.collide[0],func = self.func)
            self.projectile(self.origin,self.target[0],self.collide[0],effect = self.SE,prop = self.prop,prop_val = self.prop_val,func = self.func)
            self.target.pop(0)
            self.collide.pop(0)
            self.c += 1

    def draw(self):
        pass

Projectiles_Clrs = {"Magic": [(150,150,255),
                              (171,150,255),
                              (191,150,255)],
                    "Burn": [(255,63,63),
                             (255,146,63),
                             (255,203,134)],
                    "Freeze": [(180,238,255),
                               (193,240,254),
                               (224,246,253)],
                    "Shock": [(122,234,233),
                              (150,240,237),
                              (174,240,237)],
                    "Splash": [(139,179,255),
                               (146,194,255),
                               (155,210,255)],
                    "Poison": [(30,91,20),
                               (36,113,24),
                               (65,148,15)],
                    "Drain": [(206,124,241),
                              (209,136,241),
                              (214,152,240)],
                    "Blind": [(25,39,97),
                              (42,52,112),
                              (58,66,127)],
                    "Corruption": [(120,25,180),
                                   (130,20,185),
                                   (150,15,190)],
##                    "Corruption": [(59,18,130),
##                                   (69,22,138),
##                                   (79,26,146)],
                    "Ether": [(177,233,216),
                              (158,233,228),
                              (138,233,239)]}

#Flat Trajectory============================================================================================================================
class Base_Projectile():
    def __init__(self,origin = None,target = None,collide = [],effect = "Magic",prop = [],prop_val = [],func = None):
        self.fm = tile_sprites.sprites()[0]
        self.origin = origin
        self.initial = self.origin
        self.target = target
        self.func = func
        self.collide = collide

        self.visual_sprites = []
        self.lp = 1020

        if effect:
            self.SE = effect
        else:
            self.SE = "Magic"
        self.prop = prop
        self.prop_val = prop_val

        if self.SE == "Shock":
            self.s_pos = []

        if "Chain" in self.prop:
            self.targeted = []
            n = self.prop_val[self.prop.index("Chain")]
            self.max_chain = n[0]
            self.chain_range = n[1]

        self.phase = "Phase" in self.prop
        if self.phase and self.SE == "Magic":
            self.SE = "Ether"
            self.clrs = [(177,233,216),
                         (158,233,228),
                         (138,233,239)]
        
        self.clrs = Projectiles_Clrs.get(self.SE)
        if self.clrs == None or self.clrs == []:
            self.clrs = [(150, 150, 255),
                         (171, 150, 255),
                         (191, 150, 255)]


        self.start = [self.initial.rect.centerx, self.initial.rect.bottom - self.initial.ra * self.fm.w]
        self.end = [self.target.rect.centerx, self.target.rect.bottom - self.target.rh * self.fm.w]
        self.f_threshold = int(Distance_Pt(self.start, self.end))
        
        self.threshold = self.f_threshold

        self.d = degrees(Direction_Pt(self.start,self.end))

        self.end_pt = [self.target.x,self.target.y]
                        
        if len(self.collide) > 0 and not self.phase:
            fm_desc, fm_v, fm_h = self.fm.desc, self.fm.v, self.fm.h
            self.fm.QuickSetTopView()

            o = self.fm.tiles[self.initial.y][self.initial.x]
            t = self.fm.tiles[self.target.y][self.target.x]
            self.threshold = int(self.f_threshold * Distance_Pt([o.centerx,o.centery],self.collide[0][0])/Distance_Pt([o.centerx,o.centery],[t.centerx,t.centery]) )
            self.end_pt = [self.collide[0][1],self.collide[0][2]]

            self.fm.QuickSetView(fm_desc,fm_v,fm_h)
            
        self.fm.projectile_count += 1

        self.loop = 0
        self.hit = False
        
        self.centerx = self.start[0]
        self.centery = self.start[1]

        self.fm.visual_sprites.append(self)

    def update(self):
        for i in self.visual_sprites:
            i.update()
        if self.hit:
            if len(self.visual_sprites) == 0:
                self.fm.visual_sprites.remove(self)
                self.fm.projectile_count -= 1
                del self
        elif self.loop == self.threshold:
            self.hit = True
            if len(self.collide) > 0 and not self.phase:
                self.func(self.end_pt[0],self.end_pt[1],self.collide[0][3])
            else:
                self.func(self.end_pt[0],self.end_pt[1],None)
            SetMagicSplash(self,self.d,effect = self.SE)
            x,y = randint(1,4) * GenPN(),randint(1,4) * GenPN()
            HitSpark(self.fm,self.centerx + x,self.centery + y)
            for i in range(6):
                BurstTrail(self,d = i * 60,spd = randint(15,25)/10, clr = (255,255,255), base = 4,w = 2,h = 5,offx = x,offy = y)
            if "Chain" in self.prop:
                self.Chain()
        else:
            if len(self.collide) > 0 and not self.phase:
                if self.collide[0][3] > 1:
                    if not CheckifBlock(self.end_pt[0],self.end_pt[1]):
                        self.collide.pop(0)
                        if len(self.collide) > 0:
                            fm_desc, fm_v, fm_h = self.fm.desc, self.fm.v, self.fm.h
                            self.fm.QuickSetTopView()

                            o = self.fm.tiles[self.origin.y][self.origin.x]
                            t = self.fm.tiles[self.target.y][self.target.x]
                            self.threshold = int(self.f_threshold * Distance_Pt([o.centerx,o.centery],self.collide[0][0])/Distance_Pt([o.centerx,o.centery],[t.centerx,t.centery]) )
                            self.end_pt = [self.collide[0][1],self.collide[0][2]]

                            self.fm.QuickSetView(fm_desc,fm_v,fm_h)
                        else:
                            self.threshold = self.f_threshold
                            self.end_pt = [self.target.x,self.target.y]
            self.loop += 8
            if self.loop >= self.threshold:
                self.loop = self.threshold

            self.centerx = self.start[0] + (self.end[0] - self.start[0]) * self.loop/self.f_threshold
            self.centery = self.start[1] + (self.end[1] - self.start[1]) * self.loop/self.f_threshold
            self.Trail()

    def Chain(self):
        self.targeted.append(self.target)
        if len(self.targeted) < self.max_chain and self.end_pt == [self.target.x,self.target.y]:
            a = GetClosestUnitInRange(self.end_pt[0],self.end_pt[1],self.chain_range,[self.origin.faction],self.targeted)
            if a:
                self.initial = self.target
                self.target = a

                self.start = [self.initial.rect.centerx, self.initial.rect.bottom - self.initial.rh * self.fm.w]
                self.end = [self.target.rect.centerx, self.target.rect.bottom - self.target.rh * self.fm.w]
                    
                self.f_threshold = int(Distance_Pt(self.start, self.end))
                self.threshold = self.f_threshold

                self.loop = 0

                self.hit = False

                self.d = degrees(Direction_Pt(self.start,self.end))

                self.end_pt = [self.target.x,self.target.y]

                self.collide = CheckLineofSight(self.initial,self.target)

                if len(self.collide) > 0 and not self.phase:
                    o = self.fm.tiles[self.initial.y][self.initial.x]
                    t = self.fm.tiles[self.target.y][self.target.x]

                    fm_desc, fm_v, fm_h = self.fm.desc, self.fm.v, self.fm.h
                    self.fm.QuickSetTopView()
                        
                    self.threshold = int(self.f_threshold * Distance_Pt([o.centerx,o.centery],self.collide[0][0])/Distance_Pt([o.centerx,o.centery],[t.centerx,t.centery]) )
                    self.end_pt = [self.collide[0][1],self.collide[0][2]]
                    self.fm.QuickSetView(fm_desc,fm_v,fm_h)

    def Trail(self):
        eval("self."+self.SE+"Trail()")

    def MagicTrail(self):
        MagicTrail(self, self.centerx + cos(radians(self.d + 90 + randint(0,180))) * randint(0,4),self.centery - sin(radians(self.d + 90 + randint(0,180))) * randint(0,4), randint(5,10), self.lp)
        a = randint(0,10) * GenPN()
        StarTrail(self, self.centerx + a,self.centery + a, randint(5,10), Get_RClr(self.lp - 100 + randint(0,200),150),spd = 0.5)

    def EtherTrail(self):
        DropTrail(self, self.centerx + cos(radians(self.d + 90 + randint(0,180))) * randint(0,5),self.centery - sin(radians(self.d + 90 + randint(0,180))) * randint(0,5), randint(7,10), GetEtherClr(), 20)
        a = randint(0,10) * GenPN()
        StarTrail(self, self.centerx + a,self.centery + a, randint(5,10), GetEtherClr(),spd = 0.5)
        
    def BurnTrail(self):
        for i in range(2):
            DropTrail(self, self.centerx + cos(radians(self.d + 90 + randint(0,180))) * randint(0,5),self.centery - sin(radians(self.d + 90 + randint(0,180))) * randint(0,5), randint(5,10), GetBurnClr(), 20,spd = 0.75)

    def FreezeTrail(self):
        for i in range(2):
            DropTrail(self, self.centerx + cos(radians(self.d + 90 + randint(0,180))) * randint(0,5),self.centery - sin(radians(self.d + 90 + randint(0,180))) * randint(0,5), randint(5,10), GetFreezeClr(),spd = 0.75)
        SnowflakeTrail(self, self.centerx + cos(radians(self.d + 90 + randint(0,180))) * randint(0,5),self.centery - sin(radians(self.d + 90 + randint(0,180))) * randint(0,5), randint(5,10), GetFreezeClr(),spd = 0.5)

    def ShockTrail(self):
        pass
            
    def SplashTrail(self):
        for i in range(2):
            DropTrail(self, self.centerx + cos(radians(self.d + 90 + randint(0,180))) * randint(0,5),self.centery - sin(radians(self.d + 90 + randint(0,180))) * randint(0,5), randint(5,10), GetSplashClr(), 20,spd = 0.75)  

    def PoisonTrail(self):
        for i in range(2):
            DropTrail(self, self.centerx + cos(radians(self.d + 90 + randint(0,180))) * randint(0,5),self.centery - sin(radians(self.d + 90 + randint(0,180))) * randint(0,5), randint(5,10), GetPoisonClr(),spd = 0.75)

    def DrainTrail(self):
        for i in range(2):
            DropTrail(self, self.centerx + cos(radians(self.d + 90 + randint(0,180))) * randint(0,5),self.centery - sin(radians(self.d + 90 + randint(0,180))) * randint(0,5), randint(5,10), GetDrainClr(),spd = 0.75)
        for i in range(1):
            Explosion(self,randint(10,20),self.d + 90 + randint(0,180),GetDrainClr(),spd = randint(1,2),grow = randint(15,20)/10,start = randint(1,10), a = 40)

    def BlindTrail(self):
        for i in range(2):
            DropTrail(self, self.centerx + cos(radians(self.d + 90 + randint(0,180))) * randint(0,5),self.centery - sin(radians(self.d + 90 + randint(0,180))) * randint(0,5), randint(5,10), GetBlindClr(),spd = 0.75)

    def CorruptionTrail(self):
        for i in range(2):
            DarkTrail(self, self.centerx + cos(radians(self.d + 90 + randint(0,180))) * randint(0,5),self.centery - sin(radians(self.d + 90 + randint(0,180))) * randint(0,5), randint(5,10), GetCorruptionClr(),spd = 0.5)

    def draw(self):
        for i in self.visual_sprites:
            i.draw()
        if not self.hit: #(144,196,244)
            if self.SE == "Shock":
                if len(self.s_pos) > 1:
                    y_pts = []
                    b_pts = []
                    for i in range(len(self.s_pos)):
                        c = i/len(self.s_pos)
                        y_pts.append([self.s_pos[i][0][0] + cos(radians(self.s_pos[i][1])) * self.s_pos[i][2] * c,
                                      self.s_pos[i][0][1] - sin(radians(self.s_pos[i][1])) * self.s_pos[i][2] * c])
                        b_pts.append([self.s_pos[i][0][0] + cos(radians(self.s_pos[i][1] + 180)) * self.s_pos[i][3] * c,
                                      self.s_pos[i][0][1] - sin(radians(self.s_pos[i][1] + 180)) * self.s_pos[i][3] * c])
                    y_pts.append([self.centerx,self.centery])
                    b_pts.append([self.centerx,self.centery])
                    pygame.draw.lines(game_window,(255,247,0),False,y_pts,width = 3)
                    pygame.draw.lines(game_window,(150,240,237),False,b_pts,width = 3)
                    pygame.draw.lines(game_window,(255,255,255),False,y_pts,width = 1)
                    pygame.draw.lines(game_window,(255,255,255),False,b_pts,width = 1)
                self.s_pos.append([[self.centerx,self.centery],self.d + 90,randint(0,12) * GenPN(),randint(0,12) * GenPN()])
                if len(self.s_pos) > 12:
                    self.s_pos.pop(0)

                DrawStar(self.centerx,self.centery,12,6,self.d,clr = (150,240,237))
                DrawStar(self.centerx,self.centery,8,4,self.d,clr = (255,255,255))
            elif self.SE == "Magic":
                DrawStar(self.centerx,self.centery,12,6,self.d,clr = self.clrs[0])
                DrawStar(self.centerx,self.centery,9,4.5,self.d,clr = self.clrs[1])
                DrawStar(self.centerx,self.centery,6,3,self.d,clr = self.clrs[2])
                DrawStar(self.centerx,self.centery,3,2.5,self.d,clr = (255,255,255))
            elif self.SE == "Corruption":
                pygame.draw.circle(game_window,self.clrs[0],[self.centerx,self.centery],12)
                pygame.draw.circle(game_window,self.clrs[1],[self.centerx,self.centery],9)
                pygame.draw.circle(game_window,self.clrs[2],[self.centerx,self.centery],6)
                DrawStar(self.centerx,self.centery,9,5,self.d,clr = (125,30,180))
                DrawStar(self.centerx,self.centery,6,3,self.d,clr = (195,125,235))
            else:
                pygame.draw.circle(game_window,self.clrs[0],[self.centerx,self.centery],12)
                pygame.draw.circle(game_window,self.clrs[1],[self.centerx,self.centery],9)
                pygame.draw.circle(game_window,self.clrs[2],[self.centerx,self.centery],6)

class Healing_Orb():
    def __init__(self,origin = None,target = None,change = 0):
        self.fm = tile_sprites.sprites()[0]
        self.origin = origin
        self.target = target

        self.visual_sprites = []
        self.lp = 1020

        self.change = change
        
        self.clrs = [(176,90,225),
                     (184,120,222),
                     (188,144,213)]

        self.start = [self.origin.rect.centerx, self.origin.rect.bottom - self.origin.rh * self.fm.w]
        self.end = [self.target.rect.centerx, self.target.rect.bottom - self.target.rh * self.fm.w]
        self.f_threshold = int(Distance_Pt(self.start, self.end))
        
        self.threshold = self.f_threshold

        self.d = degrees(Direction_Pt(self.start,self.end))

        self.end_pt = [self.target.x,self.target.y]
            
        self.fm.projectile_count += 1

        self.loop = 0
        self.hit = False
        
        self.centerx = self.start[0]
        self.centery = self.start[1]

        self.fm.visual_sprites.append(self)

    def update(self):
        for i in self.visual_sprites:
            i.update()
        if self.hit:
            if len(self.visual_sprites) == 0:
                self.fm.visual_sprites.remove(self)
                self.fm.projectile_count -= 1
                del self
        elif self.loop == self.threshold:
            self.hit = True
            self.target.HPChange(self.change)
        else:
            self.loop += 6
            if self.loop >= self.threshold:
                self.loop = self.threshold

            self.centerx = self.start[0] + (self.end[0] - self.start[0]) * self.loop/self.f_threshold
            self.centery = self.start[1] + (self.end[1] - self.start[1]) * self.loop/self.f_threshold
            LightTrail(self, self.centerx,self.centery, 6, self.clrs[0],spd = 0.5)

    def draw(self):
        for i in self.visual_sprites:
            i.draw()
        if not self.hit:
            pygame.draw.circle(game_window,self.clrs[0],[self.centerx,self.centery],6)
            pygame.draw.circle(game_window,self.clrs[1],[self.centerx,self.centery],4)
            pygame.draw.circle(game_window,self.clrs[2],[self.centerx,self.centery],2)

class Reflect_Orb():
    def __init__(self,origin = None,target = None,change = 0):
        self.fm = tile_sprites.sprites()[0]
        self.origin = origin
        self.target = target

        self.visual_sprites = []
        self.lp = 1020

        self.change = change
        
        self.clrs = [(131,248,254),
                     (155,250,255),
                     (177,251,255)]

        self.start = [self.origin.rect.centerx, self.origin.rect.bottom - self.origin.rh * self.fm.w]
        self.end = [self.target.rect.centerx, self.target.rect.bottom - self.target.rh * self.fm.w]
        self.f_threshold = int(Distance_Pt(self.start, self.end))
        
        self.threshold = self.f_threshold

        self.d = degrees(Direction_Pt(self.start,self.end))

        self.end_pt = [self.target.x,self.target.y]
            
        self.fm.projectile_count += 1

        self.loop = 0
        self.hit = False
        
        self.centerx = self.start[0]
        self.centery = self.start[1]

        self.fm.visual_sprites.append(self)

    def update(self):
        for i in self.visual_sprites:
            i.update()
        if self.hit:
            if len(self.visual_sprites) == 0:
                self.fm.visual_sprites.remove(self)
                self.fm.projectile_count -= 1
                del self
        elif self.loop == self.threshold:
            self.hit = True
            self.target.HPChange(self.change)
        else:
            self.loop += 6
            if self.loop >= self.threshold:
                self.loop = self.threshold

            self.centerx = self.start[0] + (self.end[0] - self.start[0]) * self.loop/self.f_threshold
            self.centery = self.start[1] + (self.end[1] - self.start[1]) * self.loop/self.f_threshold
            LightTrail(self, self.centerx,self.centery, 6, self.clrs[0],spd = 0.5)

    def draw(self):
        for i in self.visual_sprites:
            i.draw()
        if not self.hit:
            pygame.draw.circle(game_window,self.clrs[0],[self.centerx,self.centery],6)
            pygame.draw.circle(game_window,self.clrs[1],[self.centerx,self.centery],4)
            pygame.draw.circle(game_window,self.clrs[2],[self.centerx,self.centery],2)

class Thorns_Orb():
    def __init__(self,origin = None,target = None,change = 0):
        self.fm = tile_sprites.sprites()[0]
        self.origin = origin
        self.target = target

        self.visual_sprites = []
        self.lp = 1020

        self.change = change
        
        self.clrs = [( 139, 56, 217 ),
                     ( 125, 62, 185 ),
                     ( 118, 71, 162 )]

        self.start = [self.origin.rect.centerx, self.origin.rect.bottom - self.origin.rh * self.fm.w]
        self.end = [self.target.rect.centerx, self.target.rect.bottom - self.target.rh * self.fm.w]
        self.f_threshold = int(Distance_Pt(self.start, self.end))
        
        self.threshold = self.f_threshold

        self.d = degrees(Direction_Pt(self.start,self.end))

        self.end_pt = [self.target.x,self.target.y]
            
        self.fm.projectile_count += 1

        self.loop = 0
        self.hit = False
        
        self.centerx = self.start[0]
        self.centery = self.start[1]

        self.fm.visual_sprites.append(self)

    def update(self):
        for i in self.visual_sprites:
            i.update()
        if self.hit:
            if len(self.visual_sprites) == 0:
                self.fm.visual_sprites.remove(self)
                self.fm.projectile_count -= 1
                del self
        elif self.loop == self.threshold:
            self.hit = True
            self.target.HPChange(self.change)
        else:
            self.loop += 6
            if self.loop >= self.threshold:
                self.loop = self.threshold

            self.centerx = self.start[0] + (self.end[0] - self.start[0]) * self.loop/self.f_threshold
            self.centery = self.start[1] + (self.end[1] - self.start[1]) * self.loop/self.f_threshold
            DarkTrail(self, self.centerx,self.centery, 6, self.clrs[0],spd = 0.5)

    def draw(self):
        for i in self.visual_sprites:
            i.draw()
        if not self.hit:
            pygame.draw.circle(game_window,self.clrs[0],[self.centerx,self.centery],6)
            pygame.draw.circle(game_window,self.clrs[1],[self.centerx,self.centery],4)
            pygame.draw.circle(game_window,self.clrs[2],[self.centerx,self.centery],2)

#Skyrains===================================================================================================================================
skyrain_spd = {"Magic": 10,
               "Burn": 10,
               "Freeze": 8,
               "Shock": 1,
               "Splash": 10,
               "Poison": 8,
               "Drain": 10,
               "Blind": 8,
               "Corruption": 8}

class Mlt_Skyrain():
    def __init__(self,origin,target = [],effect = "Magic",func = None,skip = False):
        if effect == "Shock":
            Mlt_Lightning_Strike(origin = origin,target = target,func = func,skip = skip)
            del self
            return
        self.fm = tile_sprites.sprites()[0]
        self.origin = origin
        self.target = target
        self.func = func

        self.hit = False

        self.strike = False
        self.spd = 10
        self.visual_sprites = []

        if effect:
            self.SE = effect
        else:
            self.SE = "Magic"

        self.clrs = Projectiles_Clrs.get(self.SE)
        if self.clrs == None or self.clrs == []:
            self.clrs = [(150, 150, 255),
                         (171, 150, 255),
                         (191, 150, 255)]

        self.Trail = eval("self."+self.SE+"Trail")
        if self.SE == "Magic":
            self.Draw = self.MagicDraw
        else:
            self.Draw = self.DefaultDraw

        self.r_lp = 0
        self.lp = 1020

        self.loop = 0
        self.fm.tiles[self.origin.y][self.origin.x].visual_sprites.append(self)
        if skip:
            self.c = 0
        else:
            self.centerx = self.fm.tiles[self.origin.y][self.origin.x].centerx
            self.centery = self.fm.tiles[self.origin.y][self.origin.x].centery
            self.c = self.centery/self.spd

        self.fm.projectile_count += 1

    def update(self):
        for i in self.visual_sprites:
            i.update()
        if self.strike:
            self.loop = (self.loop + 1)%8
            if self.loop == 0:
                Skyrain(origin = self.origin,target = self.target[0],effect = self.SE,func = self.func, skip = True)
                self.target.pop(0)
            if len(self.target) == 0:
                self.fm.tiles[self.origin.y][self.origin.x].visual_sprites.remove(self)
                self.fm.projectile_count -= 1
                del self
        else:
            self.Trail()
            if self.loop < self.c:
                self.loop += 1
                self.centery -= self.spd
                if self.loop > self.c:
                    self.loop = self.c
            elif self.loop == self.c:
                self.strike = True
                self.loop = 0

    def MagicTrail(self):
        for i in range(2):
            MagicTrail(self, self.centerx + randint(0,5) * GenPN(),self.centery, randint(8,12), self.lp)
        StarTrail(self, self.centerx + randint(0,10) * GenPN(),self.centery, randint(5,10), Get_RClr(self.lp - 100 + randint(0,200),150),spd = 0.5)
        
    def BurnTrail(self):
        for i in range(2):
            DropTrail(self, self.centerx + randint(0,5) * GenPN(),self.centery, randint(5,15), GetBurnClr(), 20)

    def FreezeTrail(self):
        for i in range(2):
            DropTrail(self, self.centerx + randint(0,5) * GenPN(),self.centery, randint(5,15), GetFreezeClr(),spd = 0.75)
            SnowflakeTrail(self, self.centerx + randint(0,10) * GenPN(),self.centery, randint(5,10), GetFreezeClr(),spd = 0.5)

    def SplashTrail(self):
        for i in range(2):
            DropTrail(self, self.centerx + randint(0,5) * GenPN(),self.centery, randint(10,15), GetSplashClr(), 20) 

    def PoisonTrail(self):
        for i in range(2):
            DropTrail(self, self.centerx + randint(0,5) * GenPN(),self.centery, randint(5,15), GetPoisonClr(),spd = 0.75)

    def DrainTrail(self):
        for j in range(2):
            Explosion(self,randint(20,30),randint(45,135),GetDrainClr(),spd = randint(1,2),grow = randint(15,20)/10,start = randint(1,10), a = 40)

    def BlindTrail(self):
        for i in range(2):
            DropTrail(self, self.centerx + randint(0,5) * GenPN(),self.centery, randint(10,15), GetBlindClr())

    def CorruptionTrail(self):
        for i in range(2):
            DropTrail(self, self.centerx + randint(0,5) * GenPN(),self.centery, randint(10,15), GetCorruptionClr())

    def DefaultDraw(self):
        pygame.draw.circle(game_window,self.clrs[0],[self.centerx,self.centery],16)
        pygame.draw.circle(game_window,self.clrs[1],[self.centerx,self.centery],13)
        pygame.draw.circle(game_window,self.clrs[2],[self.centerx,self.centery],10)
    
    def MagicDraw(self):
        self.r_lp = (self.r_lp + 10)%360
        DrawStar(self.centerx,self.centery,16,7,self.r_lp,clr = self.clrs[0])
        DrawStar(self.centerx,self.centery,13,6,self.r_lp,clr = self.clrs[1])
        DrawStar(self.centerx,self.centery,10,5,self.r_lp,clr = self.clrs[2])
        DrawStar(self.centerx,self.centery,8,3,self.r_lp,clr = (255,255,255))

    def draw_b(self):
        pass

    def draw_f(self):
        for i in self.visual_sprites:
            i.draw()
        if not self.strike:
            if self.SE == "Magic":
                self.r_lp = (self.r_lp + 10)%360
                DrawStar(self.centerx,self.centery,16,7,self.r_lp,clr = self.clrs[0])
                DrawStar(self.centerx,self.centery,13,6,self.r_lp,clr = self.clrs[1])
                DrawStar(self.centerx,self.centery,10,5,self.r_lp,clr = self.clrs[2])
                DrawStar(self.centerx,self.centery,8,3,self.r_lp,clr = (255,255,255))
            else:
                pygame.draw.circle(game_window,self.clrs[0],[self.centerx,self.centery],16)
                pygame.draw.circle(game_window,self.clrs[1],[self.centerx,self.centery],13)
                pygame.draw.circle(game_window,self.clrs[2],[self.centerx,self.centery],10)

class Mlt_Lightning_Strike():
    def __init__(self,origin,target = [],func = None,skip = False):
        self.fm = tile_sprites.sprites()[0]
        self.origin = origin
        self.target = target
        self.func = func

        self.offx = [0]
        
        self.fm.tiles[self.origin.y][self.origin.x].visual_sprites.append(self)
        self.fm.projectile_count += 1

        self.strike = skip

        if skip:
            self.c = 0
        else:
            self.centerx = self.fm.tiles[self.origin.y][self.origin.x].centerx
            self.basey = self.fm.tiles[self.origin.y][self.origin.x].centery
            
            for i in range(int(self.basey//20)):
                self.offx.append(- 7 + randint(0,14))
                self.c = len(self.offx) - 1
        self.loop = 0

    def update(self):
        if self.strike:
            self.loop = (self.loop + 1)%8
            if self.loop == 0:
                Lightning_Strike(origin = self.origin,target = self.target[0],func = self.func, skip = True)
                self.target.pop(0)
            if len(self.target) == 0:
                self.fm.tiles[self.origin.y][self.origin.x].visual_sprites.remove(self)
                self.fm.projectile_count -= 1
                del self
        else:
            if self.loop < self.c:
                self.loop += 0.75
                if self.loop > self.c:
                    self.loop = self.c
            elif self.loop == self.c:
                self.strike = True
                self.loop = 0

    def draw_b(self):
        pass

    def draw_f(self):
        if not self.strike:
            h = self.basey / (len(self.offx) - 1)
            pts = []
            p = (self.c - self.loop)/self.c
            for i in range(int(self.loop),len(self.offx)):
                pts.append([self.centerx + self.offx[i] * p,self.basey - i * h])
            if len(pts) > 1:
                pygame.draw.lines(game_window,(144,196,244),False,pts,width = int(6 * p))
                pygame.draw.lines(game_window,(255,255,255),False,pts,width = int(4 * p))

class Skyrain():
    '''Input a tile or unit as coordination'''
    def __init__(self,origin = None,target = None,effect = "Magic",func = None,skip = False):
        if effect == "Shock":
            Lightning_Strike(origin = origin,target = target,func = func,skip = skip)
            del self
            return
        self.fm = tile_sprites.sprites()[0]
        self.origin = origin
        self.target = target
        self.func = func

        self.hit = False

        self.wait = 5
        self.spd = 10

        self.r_lp = 0
        self.lp = 1020
        
        self.visual_sprites = []

        if effect:
            self.SE = effect
        else:
            self.SE = "Magic"

        self.Trail = eval("self."+self.SE+"Trail")
        if self.SE == "Magic":
            self.Draw = self.MagicDraw
        else:
            self.Draw = self.DefaultDraw

        self.clrs = Projectiles_Clrs.get(self.SE)
        if self.clrs == None or self.clrs == []:
            self.clrs = [(150, 150, 255),
                         (171, 150, 255),
                         (191, 150, 255)]

        if skip:
            self.fm.tiles[self.target.y][self.target.x].visual_sprites.append(self)
            self.centerx = self.fm.tiles[self.target.y][self.target.x].centerx
            self.centery = 0
            self.c = 0
            self.loop = self.wait + 0.5
        else:
            self.fm.tiles[self.origin.y][self.origin.x].visual_sprites.append(self)
            self.centerx = self.fm.tiles[self.origin.y][self.origin.x].centerx
            self.centery = self.fm.tiles[self.origin.y][self.origin.x].centery
            self.c = self.centery/self.spd + 20
            self.loop = 0

        self.fm.projectile_count += 1

    def update(self):
        for i in self.visual_sprites:
            i.update()
        if not self.hit:
            self.Trail()
        if self.loop < self.c:
            self.loop += 1
            self.centery -= self.spd
            if self.loop > self.c:
                self.loop = self.c
        elif self.loop == self.c:
            self.loop += 1
            self.fm.tiles[self.origin.y][self.origin.x].visual_sprites.remove(self)
            self.fm.tiles[self.target.y][self.target.x].visual_sprites.append(self)
            self.centerx = self.fm.tiles[self.target.y][self.target.x].centerx
            self.centery = 0
        elif self.centery < self.fm.tiles[self.target.y][self.target.x].centery:
            self.loop += 1
            self.centery += self.spd
        else:
            if len(self.visual_sprites) == 0:
                self.fm.tiles[self.target.y][self.target.x].visual_sprites.remove(self)
                self.fm.projectile_count -= 1
                del self
            elif not self.hit:
                self.func(self.target.x,self.target.y)
                SetMagicBurst(self.target.x,self.target.y,self.SE)
                self.hit = True

    def MagicTrail(self):
        for i in range(2):
            MagicTrail(self, self.centerx + randint(0,5) * GenPN(),self.centery, randint(8,12), self.lp)
        StarTrail(self, self.centerx + randint(0,10) * GenPN(),self.centery, randint(5,10), Get_RClr(self.lp - 100 + randint(0,200),150),spd = 0.5)
        
    def BurnTrail(self):
        for i in range(2):
            DropTrail(self, self.centerx + randint(0,5) * GenPN(),self.centery, randint(5,15), GetBurnClr(), 20)

    def FreezeTrail(self):
        for i in range(2):
            DropTrail(self, self.centerx + randint(0,5) * GenPN(),self.centery, randint(5,15), GetFreezeClr(),spd = 0.75)
            SnowflakeTrail(self, self.centerx + randint(0,10) * GenPN(),self.centery, randint(5,10), GetFreezeClr(),spd = 0.5)

    def SplashTrail(self):
        for i in range(2):
            DropTrail(self, self.centerx + randint(0,5) * GenPN(),self.centery, randint(10,15), GetSplashClr(), 20) 

    def PoisonTrail(self):
        for i in range(2):
            DropTrail(self, self.centerx + randint(0,5) * GenPN(),self.centery, randint(5,15), GetPoisonClr(),spd = 0.75)

    def DrainTrail(self):
        for j in range(2):
            Explosion(self,randint(20,30),randint(45,135),GetDrainClr(),spd = randint(1,2),grow = randint(15,20)/10,start = randint(1,10), a = 40)

    def BlindTrail(self):
        for i in range(2):
            DropTrail(self, self.centerx + randint(0,5) * GenPN(),self.centery, randint(10,15), GetBlindClr())

    def CorruptionTrail(self):
        for i in range(2):
            DropTrail(self, self.centerx + randint(0,5) * GenPN(),self.centery, randint(10,15), GetCorruptionClr())
    
    def DefaultDraw(self):
        pygame.draw.circle(game_window,self.clrs[0],[self.centerx,self.centery],16)
        pygame.draw.circle(game_window,self.clrs[1],[self.centerx,self.centery],13)
        pygame.draw.circle(game_window,self.clrs[2],[self.centerx,self.centery],10)
    
    def MagicDraw(self):
        self.r_lp = (self.r_lp + 10)%360
        DrawStar(self.centerx,self.centery,16,7,self.r_lp,clr = self.clrs[0])
        DrawStar(self.centerx,self.centery,13,6,self.r_lp,clr = self.clrs[1])
        DrawStar(self.centerx,self.centery,10,5,self.r_lp,clr = self.clrs[2])
        DrawStar(self.centerx,self.centery,8,3,self.r_lp,clr = (255,255,255))

    def draw_b(self):
        pass

    def draw_f(self):
        for i in self.visual_sprites:
            i.draw()
        if not self.hit:
            self.Draw()

class Lightning_Strike():
    '''Input a tile or unit as coordination'''
    def __init__(self,origin = None,target = None,func = None,skip = False):
        self.fm = tile_sprites.sprites()[0]
        self.origin = origin
        self.target = target
        self.func = func

        self.wait = 5

        self.offx = [0]
        if skip:
            self.fm.tiles[self.target.y][self.target.x].visual_sprites.append(self)
            self.centerx = self.fm.tiles[self.target.y][self.target.x].centerx
            self.basey = self.fm.tiles[self.target.y][self.target.x].centery
        else:
            self.fm.tiles[self.origin.y][self.origin.x].visual_sprites.append(self)
            self.centerx = self.fm.tiles[self.origin.y][self.origin.x].centerx
            self.basey = self.fm.tiles[self.origin.y][self.origin.x].centery

        self.fm.projectile_count += 1

        for i in range(int(self.basey//20)):
            self.offx.append(- 7 + randint(0,14))

        if skip:
            self.c = 0
            self.loop = self.wait + 0.5
        else:
            self.c = len(self.offx) - 1
            self.loop = 0

    def update(self):
        if self.loop < self.c:
            self.loop += 0.75
            if self.loop > self.c:
                self.loop = self.c
        elif self.loop == self.c:
            self.loop += 0.5
            self.fm.tiles[self.origin.y][self.origin.x].visual_sprites.remove(self)
            self.fm.tiles[self.target.y][self.target.x].visual_sprites.append(self)
            self.offx = [0]
            self.centerx = self.fm.tiles[self.target.y][self.target.x].centerx
            self.basey = self.fm.tiles[self.target.y][self.target.x].centery
            for i in range(int(self.basey//20)):
                self.offx.append(- 7 + randint(0,14))
        elif self.loop == self.wait + self.c + 0.5:
            self.func(self.target.x,self.target.y)
            SetMagicBurst(self.target.x,self.target.y,"Shock")
            self.loop += 0.5
        elif self.loop < 10 + self.wait + self.c:
            self.loop += 0.5
        elif self.loop >= 10 + self.wait + self.c:
            self.fm.tiles[self.target.y][self.target.x].visual_sprites.remove(self)
            self.fm.projectile_count -= 1
            del self

    def draw_b(self):
        pass

    def draw_f(self):
        h = self.basey / (len(self.offx) - 1)
        pts = []
        if self.loop <= self.c:
            p = (self.c - self.loop)/self.c
            for i in range(int(self.loop),len(self.offx)):
                pts.append([self.centerx + self.offx[i] * p,self.basey - i * h])
            if len(pts) > 1:
                pygame.draw.lines(game_window,(144,196,244),False,pts,width = int(6 * p))
                pygame.draw.lines(game_window,(255,255,255),False,pts,width = int(4 * p))
        elif self.loop >= self.c + self.wait:
            p = (1 - (self.loop - self.c - self.wait)/10)
            for i in range(len(self.offx)):
                pts.append([self.centerx + self.offx[i] * p,self.basey - i * h])
            pygame.draw.lines(game_window,(144,196,244),False,pts,width = int(6 * p))
            pygame.draw.lines(game_window,(255,255,255),False,pts,width = int(4 * p))
