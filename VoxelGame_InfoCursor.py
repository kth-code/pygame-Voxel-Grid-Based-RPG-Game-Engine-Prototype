import pygame
from math import *
from VoxelGame_BaseVars import *
from VoxelGame_Visuals import *

from VoxelGame_Icons import *

HP_Frame = pygame.Surface((156,16))
HP_Frame.fill((205,235,240))
HP_f_rect = HP_Frame.get_rect()
HP_Bckgd = pygame.Surface((150,10))
HP_Bckgd.fill((75,85,85))
HP_b_rect = HP_Bckgd.get_rect()

edge = pygame.Surface((15,15))
edge.fill((2,2,2))
edge.set_colorkey((1,1,1))
pygame.draw.circle(edge,(1,1,1),[15,15],15)
edges = []
for i in range(4):
    edges.append(pygame.transform.rotate(edge,-90 * i))

def RoundCorner(surface,rect):
    surface.set_colorkey((2,2,2))
    surface.blit(edges[0],[0,0])
    surface.blit(edges[1],[rect[2] - 15,0])
    surface.blit(edges[2],[rect[2] - 15,rect[3] - 15])
    surface.blit(edges[3],[0,rect[3] - 15])
    return surface

info_clr = (45,45,65)#(35,40,75)#(65,70,70)

class Info_Cursor():
    def __init__(self, x = 7, y = 3):
        pygame.sprite.Sprite.__init__(self)
        self.fm = tile_sprites.sprites()[0]
        self.x = x
        self.y = y

        self.offx,self.offy,self.offh = 0,0,0
        self.offx_list,self.offy_list,self.offh_list = [],[],[] #[0.04,25]
        self.dir = 0 #N1 E2 S3 W4
        self.h_mv = 0 #-1 Down 0 No 1 Up
        
        self.name = "Info Cursor"
        self.name_id = -1
        self.cd = 0
        self.lp = 0

        self.mode = 0

        self.font = game_font16
        self.t_font = title_font25
        self.st_font = title_font20
        self.hp_font = stat_font18

        self.f_h = self.font.size(" ")[1]
        self.hp_h = self.hp_font.size(" ")[1]
        
        self.unit = None
        self.u_count = 0
        self.highlighted = False

        self.clr,self.p_clr,self.n_clr = (70,215,255),(70,215,255),(70,215,255)
        self.c_lp = 0
        self.a_lp = 0

        self.rw_rect = pygame.Rect(0,0,100,self.hp_h)
        
        y = window_height - 10
        text = title_font20.render("Lock & Show More Info",True,(255,255,255))
        textRect = text.get_rect()
        textRect.right = window_width - 10
        textRect.bottom = y
        i_rect = key_icon_z.get_rect()
        i_rect.right = textRect.left - 5
        i_rect.centery = textRect.centery
        self.show = [text,textRect,key_icon_z,i_rect]
        
        y = window_height - 10
        text = title_font20.render("Unlock & Hide Info",True,(255,255,255))
        textRect = text.get_rect()
        textRect.right = window_width - 10
        textRect.bottom = y
        i_rect = key_icon_z.get_rect()
        i_rect.right = textRect.left - 5
        i_rect.centery = textRect.centery
        self.hide = [text,textRect,key_icon_z,i_rect]

        self.desc_txt = pygame.Surface((0,0))
        self.se_txt = pygame.Surface((0,0))
        self.info_txt = pygame.Surface((0,0))
        self.desc_bgd = pygame.Surface((0,0))
        self.se_bgd = pygame.Surface((0,0))
        self.info_bgd = pygame.Surface((0,0))
        self.desc_rect = self.desc_txt.get_rect()
        self.se_rect = self.se_txt.get_rect()
        self.info_rect = self.info_txt.get_rect()
        
    def Draw(self):
        t = self.fm.tiles[self.y][self.x]
        ox = self.offx * self.fm.w
        oy = self.offy * self.fm.h
        oh = self.offh * self.fm.v
        if self.n_clr != self.p_clr:
            self.c_lp += 0.04
            self.clr = GradientClrs(self.n_clr,self.p_clr,self.c_lp,1-self.c_lp)
            if self.c_lp >= 1:
                self.c_lp = 0
                self.clr = self.n_clr
                self.p_clr = self.n_clr
        link = False
        if self.dir == 4 and self.offh != 0:
            if self.offh > 0: #NOTE if set to x -= 1 when offx = 0, t/br in x_pos > t/bl and vice versa
                pts = [[t.tr[0] - 1,t.tl[1] + 1 - oy - oh],
                       [t.tl[0] + 1 + ox ,t.tr[1] + 1 - oy - oh],
                       [t.bl[0] + 1 + ox,t.bl[1] - 1 - oy - oh],
                       [t.br[0] - 1,t.br[1] - 1 - oy - oh]]
            else:
                pts = [[t.tr[0] - 1,t.tr[1] + 1 - oy - oh],
                       [t.tr[0] - 1 + ox,t.tl[1] + 1 - oy - oh],
                       [t.br[0] - 1 + ox,t.bl[1] - 1 - oy - oh],
                       [t.br[0] - 1,t.br[1] - 1 - oy - oh],
                       ]
        elif self.dir == 2 and self.offh != 0:
            if self.offh > 0:
                pts = [[t.tr[0] - 1,t.tr[1] + 1 - oy - oh],
                       [t.tl[0] + 1 + ox,t.tl[1] + 1 - oy - oh],
                       [t.bl[0] + 1 + ox,t.bl[1] - 1 - oy - oh],
                       [t.br[0] - 1,t.br[1] - 1 - oy - oh]]
            else:
                pts = [[t.tr[0] - 1,t.tr[1] + 1 - oy - oh],
                       [t.tr[0] - 1 + ox ,t.tr[1] + 1 - oy - oh],
                       [t.br[0] - 1 + ox,t.br[1] - 1 - oy - oh],
                       [t.br[0] - 1 ,t.bl[1] - 1 - oy - oh],]
        elif self.dir == 1 and self.h_mv != 0:
            if self.h_mv == 1:
                c = (t.bl[1] - t.tl[1]) * self.offy_list[0][1] / 20
                pts = [[t.tl[0] + 1 + ox,t.bl[1] - 1 - oy - oh - c],
                       [t.bl[0] + 1 + ox,t.bl[1] - 1 - oy - oh],
                       [t.br[0] - 1 + ox,t.br[1] - 1 - oy - oh],
                       [t.tr[0] - 1 + ox,t.br[1] - 1 - oy - oh - c]]
            else:
                c = (t.bl[1] - t.tl[1]) * (1 - self.offy_list[0][1] / 20)
                pts = [[t.tl[0] + 1 + ox,t.tl[1] + 1 - oy - oh + c],
                       [t.tl[0] + 1 + ox,t.tl[1] + 1 - oy - oh],
                       [t.tr[0] - 1 + ox,t.tr[1] + 1 - oy - oh],
                       [t.tr[0] - 1 + ox,t.tr[1] + 1 - oy - oh + c]]
        elif self.dir == 3 and self.h_mv == -1:
            c = (t.bl[1] - t.tl[1]) * (1 - self.offy_list[0][1] / 20)
            pts = [[t.tl[0] + 1 + ox,t.bl[1] + 1 - oy - oh - c],
                   [t.bl[0] + 1 + ox,t.bl[1] + 1 - oy - oh],
                   [t.br[0] - 1 + ox,t.br[1] + 1 - oy - oh],
                   [t.tr[0] - 1 + ox,t.br[1] + 1 - oy - oh - c]]
        else:
            link = True
            pts = [[t.bl[0] + 1 + ox,t.bl[1] - 1 - oy - oh],
                   [t.tl[0] + 1 + ox,t.tl[1] + 1 - oy - oh],
                   [t.tr[0] - 1 + ox,t.tr[1] + 1 - oy - oh],
                   [t.br[0] - 1 + ox,t.br[1] - 1 - oy - oh]]
        x = cos(radians(self.lp)) * 10
        y = sin(radians(self.lp)) * 10
        cy = (t.bl[1] + t.tl[1])/2 - oy - oh
        a_pts = [[t.centerx + ox, cy - 70 - y],
                 [t.centerx + ox - x, cy - 90 - y],
                 [t.centerx + ox + x, cy - 90 - y]]
        if CheckifBlock(self.x,self.y):
            for i in range(4):
                pts[i][1] -= self.fm.v
            for i in range(3):
                a_pts[i][1] -= self.fm.v      
        pygame.draw.lines(game_window,self.clr,link,pts,width = 3)
        pygame.draw.polygon(game_window,self.clr,a_pts)
        pygame.draw.lines(game_window,(255,255,255),True,a_pts,width = 3)
        self.lp = (self.lp + 2)%360

    def ShiftW(self):
        #self.x -= 1
        self.offx,self.dir,self.h_mv = 0,0,0

    def ShiftE(self):
        self.x += 1
        self.offx,self.dir,self.h_mv = 0,0,0

    def ShiftN_P(self):
        self.y -= 1
        self.offy,self.dir,self.h_mv = 0,0,0

    def ShiftN_H(self):
        #self.y -= 1
        self.offy,self.dir,self.h_mv = 0,0,0    
        
    def ShiftS_P(self):
        self.offy,self.dir,self.h_mv = 0,0,0

    def ShiftS_H(self):
        self.y += 1
        self.offy,self.dir,self.h_mv = 0,0,0

    def ShiftH(self):
        self.offh = 0

    def CheckSpace(self,x = 0,y = 0):
        if CheckifUnit(self.x,self.y):
            self.p_clr = faction_clrs[self.fm.GetUnit(self.x,self.y).faction]
        elif CheckifBlock(self.x,self.y):
            self.p_clr = (70,255,165)
        else:
            self.p_clr = (70,215,255)
        if CheckifUnit(self.x + x,self.y + y):
            self.n_clr = faction_clrs[self.fm.GetUnit(self.x + x,self.y + y).faction]
        elif CheckifBlock(self.x + x,self.y + y):
            self.n_clr = (70,255,165)
        else:
            self.n_clr = (70,215,255)
        if x == 0 and y == 0:
            self.clr = self.n_clr
        if self.unit:
            if len(self.unit.move_type) > 0:
                ClearAllTiles()
                #ClearHighlightTiles(self.unit.x,self.unit.y, self.unit.Get_Range(n = self.u_count), c = self.unit.move_range[self.u_count][1])
        if CheckifUnit(self.x + x,self.y + y):
            self.u_count = 0
            self.unit = self.fm.GetUnit(self.x + x,self.y + y)
            self.highlighted = False
            self.fm.AddInstructions(self.show)
            self.LoadDesc()
        elif self.unit:
            self.mode = 0
            if len(self.unit.move_type) > 0:
                ClearAllTiles()
                #ClearHighlightTiles(self.unit.x,self.unit.y, self.unit.Get_Range(n = self.u_count), c = self.unit.move_range[self.u_count][1])
            self.unit = None
            self.fm.RemoveInstructions(self.show)
        
    def CheckMove(self):
        if self.cd == 0:
            keystate = pygame.key.get_pressed()
            if keystate[pygame.K_SPACE]:
                self.fm.desc = not self.fm.desc
                self.cd = 20
            elif keystate[pygame.K_a]:
                self.fm.RotateAnticlockwise()
                self.cd = 20
            elif keystate[pygame.K_d]:
                self.fm.RotateClockwise()
                self.cd = 20
        if self.cd == 0 and self.mode == 0:
            if keystate[pygame.K_m]:
                self.fm.mode = 1
                self.fm.acting_unit.cd = 10
                self.fm.focus = self.fm.acting_unit
                self.fm.RemoveInstructions(self.show)
            elif keystate[pygame.K_z] and CheckifUnit(self.x,self.y):
                self.mode = 1
                self.u_count = 0
                self.unit = self.fm.GetUnit(self.x,self.y)
                self.highlighted = False
                self.cd = 20
                self.fm.AddInstructions(self.hide)
                self.fm.RemoveInstructions(self.show)
                self.LoadInfo()
            elif keystate[pygame.K_UP] and self.y != 0:
                self.CheckSpace(x = 0,y = -1)
                self.dir = 1
                d = self.fm.tiles[self.y - 1][self.x].h - self.fm.tiles[self.y][self.x].h
                if CheckifBlock(self.x,self.y - 1):
                    d += 1
                if CheckifBlock(self.x,self.y):
                    d -= 1
                self.offh_list.append([0.05 * d,20,self.ShiftH])
                if d >= 0:
                    self.offy_list.append([0.05,20,self.ShiftN_P])
                    if d > 0:
                        self.h_mv = 1
                else:
                    self.offy = -1
                    self.offh -= d
                    self.offy_list.append([0.05,20,self.ShiftN_H])
                    self.y -= 1
                    self.h_mv = -1
                self.cd = 20
            elif keystate[pygame.K_RIGHT] and self.x != self.fm.d[0] - 1:
                self.CheckSpace(x = 1,y = 0)
                self.dir = 2
                self.offx_list.append([0.05,20,self.ShiftE])
                d = self.fm.tiles[self.y][self.x + 1].h - self.fm.tiles[self.y][self.x].h
                if CheckifBlock(self.x + 1,self.y):
                    d += 1
                if CheckifBlock(self.x,self.y):
                    d -= 1
                if d != 0:
                    if d < 0:
                        self.h_mv = -1
                    elif d > 0:
                        self.h_mv = 1
                    self.offh_list.append([0.05 * d,20,self.ShiftH])
                self.cd = 20
            elif keystate[pygame.K_DOWN] and self.y != self.fm.d[1] - 1:
                self.CheckSpace(x = 0,y = 1)
                self.dir = 3
                d = self.fm.tiles[self.y + 1][self.x].h - self.fm.tiles[self.y][self.x].h
                if CheckifBlock(self.x,self.y + 1):
                    d += 1
                if CheckifBlock(self.x,self.y):
                    d -= 1
                self.offh_list.append([0.05 * d,20,self.ShiftH])
                if d > 0:
                    self.offy_list.append([-0.05,20,self.ShiftS_H])
                    self.h_mv = 1
                else:
                    self.offy = 1
                    self.offh -= d
                    self.offy_list.append([-0.05,20,self.ShiftS_P])
                    self.y += 1
                    if d < 0:
                        self.h_mv = -1
                self.cd = 20
            elif keystate[pygame.K_LEFT] and self.x != 0:
                self.CheckSpace(x = -1,y = 0)
                self.dir = 4
                self.offx_list.append([-0.05,20,self.ShiftW])
                d = self.fm.tiles[self.y][self.x - 1].h - self.fm.tiles[self.y][self.x].h
                if CheckifBlock(self.x - 1,self.y):
                    d += 1
                if CheckifBlock(self.x,self.y):
                    d -= 1
                if d != 0:
                    if d < 0:
                        self.h_mv = -1
                    elif d > 0:
                        self.h_mv = 1
                    self.offh_list.append([0.05 * d,20,self.ShiftH])
                self.offh -= d
                self.cd = 20
                self.offx = 1
                self.x -= 1
        elif self.cd == 0 and self.mode == 1:
            keystate = pygame.key.get_pressed()
            if keystate[pygame.K_z]:
                if len(self.unit.move_type) > 0:
                    ClearAllTiles()
                    #ClearHighlightTiles(self.unit.x,self.unit.y, self.unit.Get_Range(n = self.u_count), c = self.unit.move_range[self.u_count][1])
                self.mode = 0
##                self.unit = None
                self.fm.RemoveInstructions(self.hide)
                self.fm.AddInstructions(self.show)
                self.cd = 20
        
    def update(self):
        if self.cd > 0:
            self.cd -= 1
        if len(self.offx_list) > 0:
            self.offx += self.offx_list[0][0]
            self.offx_list[0][1] -= 1
            if self.offx_list[0][1] == 0:
                self.offx_list[0][2]()
                self.offx_list.pop(0)
        if len(self.offy_list) > 0:
            self.offy += self.offy_list[0][0]
            self.offy_list[0][1] -= 1
            if self.offy_list[0][1] == 0:
                self.offy_list[0][2]()
                self.offy_list.pop(0)
        if len(self.offh_list) > 0:
            self.offh += self.offh_list[0][0]
            self.offh_list[0][1] -= 1
            if self.offh_list[0][1] == 0:
                self.offh_list[0][2]()
                self.offh_list.pop(0)
        self.CheckMove()

##        self.desc_txt = pygame.Surface((0,0))
##        self.se_txt = pygame.Surface((0,0))
##        self.info_txt = pygame.Surface((0,0))
##        self.desc_bgd = pygame.Surface((0,0))
##        self.se_bgd = pygame.Surface((0,0))
##        self.info_bgd = pygame.Surface((0,0))
##        self.desc_rect = self.desc_txt.get_rect()
##        self.se_rect = self.se_txt.get_rect()
##        self.info_rect = self.info_txt.get_rect()
        
    def LoadDesc(self):
        self.desc_bgd = pygame.Surface((0,0))
        rw,eh = 0,0
        if len(self.unit.Resistance) > 0 and len(self.unit.Weakness) > 0:
            rw += 2 + max(len(self.unit.Resistance),len(self.unit.Weakness))
        elif len(self.unit.Resistance) > 0:
            rw += 2 + len(self.unit.Resistance)//2 + len(self.unit.Resistance)%2
        elif len(self.unit.Weakness)  > 0:
            rw += 2 + len(self.unit.Weakness)//2 + len(self.unit.Weakness)%2
        if rw > 0:
            eh = (self.hp_h + 5) * 2 + (self.f_h + 5) * (rw - 2)
        
        self.desc_txt = pygame.Surface((450,100 + len(self.unit.info) * (self.f_h + 5) + eh))
        self.desc_bgd = self.desc_txt.copy()
        self.desc_txt.fill(info_clr)
        self.desc_txt.set_colorkey(info_clr)
        self.desc_rect = self.desc_txt.get_rect()
        
        self.desc_bgd.fill(info_clr)
        self.desc_bgd.set_alpha(220)
        RoundCorner(self.desc_bgd,self.desc_rect)

        x = 25
        y = 75
        for i in self.unit.info:
            for j in i:
                if "#" in j:
                    text = self.font.render("",True,(0,0,0))
                    textRect = text.get_rect()
                    textRect.left = x
                    textRect.top = y
                    image = self.unit.imgs[int(j[1:])]
                    rect = image.get_rect()
                    rect.left = x
                    rect.centery = textRect.centery
                    self.desc_txt.blit(image,rect)
                    x += rect[2]
                elif "@" in j:
                    if 48 <= ord(j[1:2]) <= 57:
                        text = self.font.render(j[2:],True,self.unit.colour[int(j[1:2])])
                    else:
                        text = self.font.render(j[2:],True,self.unit.colour[ord(j[1:2])-87])
                else:
                    text = self.font.render(j,True,(255,255,255))
                textRect = text.get_rect()
                textRect.left = x
                textRect.top = y
                self.desc_txt.blit(text,textRect)
                x += textRect[2]
            x = 25
            y += textRect[3] + 5
        if rw > 0:
            y += textRect[3] + 5

        text = self.hp_font.render("HP   "+str(self.unit.HP)+"/"+str(self.unit.MaxHP),True,(255,255,255))
        textRect = text.get_rect()
        textRect.left = self.desc_rect.centerx - (166 + textRect[2])/2
        textRect.centery = 50
        self.desc_txt.blit(text,textRect)

        HP_b_rect.left = textRect.right + 13
        HP_b_rect.centery = textRect.centery
        if self.unit.HP > 0:
            if self.unit.HP/self.unit.MaxHP <= 0.3:
                DrawBar(HP_b_rect,self.unit.HP,self.unit.MaxHP,(255,115,115),segment = self.unit.HP_Segment,surface = self.desc_txt)
            else:
                DrawBar(HP_b_rect,self.unit.HP,self.unit.MaxHP,faction_bar_clrs[self.unit.faction],segment = self.unit.HP_Segment,surface = self.desc_txt)  

        if len(self.unit.Resistance) > 0 and len(self.unit.Weakness) > 0:
            cy = y
            text = self.hp_font.render("Resistance",True,(255,255,255))
            textRect = text.get_rect()
            textRect.centerx = self.desc_rect[2]/4
            textRect.top = cy
            self.rw_rect.center = textRect.center
            DrawHexFrame(self.rw_rect,(50,123,180),surface = self.desc_txt)
            self.desc_txt.blit(text,textRect)

##            img = resistance_icon
##            rect = img.get_rect()
##            rect.center = self.rw_rect.left-10,self.rw_rect.centery
##            pygame.draw.circle(self.desc_txt,(50,123,180),rect.center,17)
##            pygame.draw.circle(self.desc_txt,(10,80,150),rect.center,13)
##            self.desc_txt.blit(img,rect)

            cy += textRect[3] + 5

            w = []
            for i in self.unit.Resistance:
                w.append(self.font.size(i)[0])
            w,s = max(w)+5,ES_width
            for i in self.unit.Resistance:
                img = Element_Symbols.get(i)
                rect = img.get_rect()
                rect.centerx = self.rw_rect.centerx - w/2
                text = self.font.render(i,True,(255,255,255))
                textRect = text.get_rect()
                textRect.top = cy
                rect.centery = textRect.centery
                textRect.left = rect.centerx + s/2 + 5
                self.desc_txt.blit(img,rect)
                self.desc_txt.blit(text,textRect)
                cy += textRect[3] + 5
            my = cy
            
            cy = y
            text = self.hp_font.render("Weakness",True,(255,255,255))
            textRect = text.get_rect()
            textRect.centerx = self.desc_rect[2]*3/4
            textRect.top = cy
            self.rw_rect.center = textRect.center
            DrawHexFrame(self.rw_rect,(180,50,50),surface = self.desc_txt)

            self.desc_txt.blit(text,textRect)

##            img = weakness_icon
##            rect = img.get_rect()
##            rect.center = self.rw_rect.left-10,self.rw_rect.centery
##            pygame.draw.circle(self.desc_txt,(180,50,50),rect.center,17)
##            pygame.draw.circle(self.desc_txt,(150,10,10),rect.center,13)
##            self.desc_txt.blit(img,rect)
            
            cy += textRect[3] + 5
            w = []
            for i in self.unit.Weakness:
                w.append(self.font.size(i)[0])
            w,s = max(w)+5,ES_width
            for i in self.unit.Weakness:
                img = Element_Symbols.get(i)
                rect = img.get_rect()
                rect.centerx = self.rw_rect.centerx - w/2
                text = self.font.render(i,True,(255,255,255))
                textRect = text.get_rect()
                textRect.top = cy
                rect.centery = textRect.centery
                textRect.left = rect.centerx + s/2 + 5
                self.desc_txt.blit(img,rect)
                self.desc_txt.blit(text,textRect)
                cy += textRect[3] + 5
            if cy > my:
                my = cy
            pygame.draw.line(self.desc_txt,(255,255,255),[self.desc_rect.centerx,y + 10],[self.desc_rect.centerx,my - 10],width = 1)
            DrawDiamond(self.desc_rect.centerx,y + 6,2,surface = self.desc_txt)
            DrawDiamond(self.desc_rect.centerx,my - 6,2,surface = self.desc_txt)
            DrawDiamond(self.desc_rect.centerx,y,3,surface = self.desc_txt)
            DrawDiamond(self.desc_rect.centerx,my,3,surface = self.desc_txt)
   
        elif len(self.unit.Resistance) > 0:
            text = self.hp_font.render("Resistance",True,(255,255,255))
            textRect = text.get_rect()
            textRect.centerx = self.desc_rect.centerx
            textRect.top = y
            self.rw_rect.center = textRect.center
            DrawHexFrame(self.rw_rect,(50,123,180),surface = self.desc_txt)
            self.desc_txt.blit(text,textRect)
            y += textRect[3] + 5

            w = [[],[],[]]
            for i in range(len(self.unit.Resistance)):
                if len(self.unit.Resistance) % 2 == 1 and i == len(self.unit.Resistance) - 1:
                    w[0].append(self.font.size(self.unit.Resistance[i])[0])
                elif i % 2 == 0:
                    w[1].append(self.font.size(self.unit.Resistance[i])[0])
                else:
                    w[2].append(self.font.size(self.unit.Resistance[i])[0])
            for i in range(3):
                if len(w[i]) > 0:
                    w[i] = max(w[i])+5
            for i in range(len(self.unit.Resistance)):
                if len(self.unit.Resistance) % 2 == 1 and i == len(self.unit.Resistance) - 1:
                    x,a = self.desc_rect.centerx - w[0]/2, 0
                elif i % 2 == 0:
                    x,a = self.desc_rect[2]/4 - w[1]/2, 1
                else:
                    x,a = self.desc_rect[2]*3/4 - w[2]/2, 2
                img = Element_Symbols.get(self.unit.Resistance[i])
                rect = img.get_rect()
                rect.centerx = x
                text = self.font.render(self.unit.Resistance[i],True,(255,255,255))
                textRect = text.get_rect()
                textRect.top = y
                rect.centery = textRect.centery
                textRect.left = rect.centerx + ES_width/2 + 5
                self.desc_txt.blit(img,rect)
                self.desc_txt.blit(text,textRect)
                if i % 2 == 1:
                    y += textRect[3] + 5
        elif len(self.unit.Weakness)  > 0:
            text = self.hp_font.render("Weakness",True,(255,255,255))
            textRect = text.get_rect()
            textRect.centerx = self.desc_rect.centerx
            textRect.top = y
            self.rw_rect.center = textRect.center
            DrawHexFrame(self.rw_rect,(180,50,50),surface = self.desc_txt)
            self.desc_txt.blit(text,textRect)
            y += textRect[3] + 5
            
            w = [[],[],[]]
            for i in range(len(self.unit.Weakness)):
                if len(self.unit.Weakness) % 2 == 1 and i == len(self.unit.Weakness) - 1:
                    w[0].append(self.font.size(self.unit.Weakness[i])[0])
                elif i % 2 == 0:
                    w[1].append(self.font.size(self.unit.Weakness[i])[0])
                else:
                    w[2].append(self.font.size(self.unit.Weakness[i])[0])
            for i in range(3):
                if len(w[i]) > 0:
                    w[i] = max(w[i])+5
            for i in range(len(self.unit.Weakness)):
                if len(self.unit.Weakness) % 2 == 1 and i == len(self.unit.Weakness) - 1:
                    x,a = self.desc_rect.centerx - w[0]/2, 0
                elif i % 2 == 0:
                    x,a = self.desc_rect[2]/4 - w[1]/2, 1
                else:
                    x,a = self.desc_rect[2]*3/4 - w[2]/2, 2
                img = Element_Symbols.get(self.unit.Weakness[i])
                rect = img.get_rect()
                rect.centerx = x
                text = self.font.render(self.unit.Weakness[i],True,(255,255,255))
                textRect = text.get_rect()
                textRect.top = y
                rect.centery = textRect.centery
                textRect.left = rect.centerx + ES_width/2 + 5
                self.desc_txt.blit(img,rect)
                self.desc_txt.blit(text,textRect)
                if i % 2 == 1:
                    y += textRect[3] + 5

        self.desc_rect.right = window_width - 20
        self.desc_rect.top = 30
        
        self.LoadSE()
        self.LoadInfo()

    def LoadSE(self):
        if len(self.unit.EffectTimer) > 0:

            n_w,t_w,i_w = [],[],[]
            for i in range(len(self.unit.EffectTimer)):
                n_w.append(self.font.size(self.unit.StatusEffect[i])[0])
                t_w.append(self.font.size(str(self.unit.EffectTimer[i]))[0])
            self.se_txt = pygame.Surface((70 + SE_width + max(n_w) + max(t_w),25 + len(self.unit.EffectTimer) * (self.f_h + 5)))
            self.se_bgd = self.se_txt.copy()
            
            i_w = SE_width/2
            self.se_rect = self.se_txt.get_rect()
            self.se_txt.fill(info_clr)
            self.se_txt.set_colorkey(info_clr)

            self.se_bgd.fill(info_clr)
            self.se_bgd.set_colorkey(info_clr)
            self.se_bgd.set_alpha(220)
            RoundCorner(self.se_bgd,self.se_rect)

            y = 15
            for i in range(len(self.unit.EffectTimer)):
                text = self.font.render("",True,(0,0,0))
                textRect = text.get_rect()
                textRect.top = y
                image = SE_Symbols.get(self.unit.StatusEffect[i],missing_icon)
                rect = image.get_rect()
                rect.centerx = 15 + i_w
                rect.centery = textRect.centery
                self.se_txt.blit(image,rect)

                x = 25 + i_w * 2
                    
                text = self.font.render(self.unit.StatusEffect[i],True,SE_colour_set.get(self.unit.StatusEffect[i],(255,255,255)))
                textRect = text.get_rect()
                textRect.left = x
                textRect.top = y
                self.se_txt.blit(text,textRect)
                x += textRect[2] + 10
                    
                text = self.font.render(str(self.unit.EffectTimer[i]),True,(255,255,255))
                textRect = text.get_rect()
                textRect.right = self.se_rect[2] - 25
                textRect.top = y
                self.se_txt.blit(text,textRect)
                y += self.f_h + 5

            self.se_rect.top = self.desc_rect.bottom + 20
            self.se_rect.right = window_width - 20

    def LoadInfo(self):
        if len(self.unit.move_info[self.u_count]) > 0:
            h = 35
            i_w = 30 #Shift Box Right (+)
            
            temp_txt = pygame.Surface((450,25 + self.t_font.size("")[1] + len(self.unit.move_info[self.u_count]) * (self.f_h + 5) + (self.hp_h + 5 if self.unit.move_stat[self.u_count] else 0)))
            temp_bgd = temp_txt.copy()
            temp_rect = temp_bgd.get_rect()
            
            self.info_txt = pygame.Surface((450 + i_w,25 + self.t_font.size("")[1] + len(self.unit.move_info[self.u_count]) * (self.f_h + 5) + h + (self.hp_h + 5 if self.unit.move_stat[self.u_count] else 0)))
            self.info_bgd = self.info_txt.copy()
            self.info_rect = self.info_txt.get_rect()

            temp_txt.fill(info_clr)
            temp_bgd.fill(info_clr)
            RoundCorner(temp_bgd,temp_rect)
            
            self.info_txt.fill(info_clr)
            self.info_txt.set_colorkey(info_clr)
            self.info_bgd.set_colorkey((0,0,0))
            
            #self.info_bgd.fill(info_clr)
            #self.info_bgd.fill(temp_bgd.get_colorkey())
            self.info_bgd.set_alpha(220)
            
            x = 25
            y = 10
            self.info_bgd.blit(temp_bgd,[i_w,h])            
            text = self.t_font.render(self.unit.move_label[self.u_count],True,(255,255,255))
            textRect = text.get_rect()
            textRect.left, textRect.top = x,y  
            
            temp_txt.blit(text,textRect)
            y = textRect.bottom + 5

            lrect = textRect
    
            if self.unit.move_stat[self.u_count]:
                if self.unit.move_SE[self.u_count]:
                    text = self.hp_font.render(self.unit.Get_DMG(m = self.u_count,t = 2),True,SE_colour_set.get(self.unit.move_SE[self.u_count]))
                    textRect = text.get_rect()
                    textRect.left, textRect.top = x + 5 + SE_width,y
                    image = SE_Symbols.get(self.unit.move_SE[self.u_count])
                    rect = image.get_rect()
                    rect.left = x
                    rect.centery = textRect.centery
                    temp_txt.blit(image,rect)
                else:
                    text = self.hp_font.render(self.unit.Get_DMG(m = self.u_count,t = 2),True,(255,255,255))
                    textRect = text.get_rect()
                    textRect.left, textRect.top = x,y
                temp_txt.blit(text,textRect)
                y += textRect[3] + 5
                
                if self.unit.Get_Crit(self.u_count) > 0:
                    text = self.hp_font.render(str(self.unit.Get_Crit(self.u_count))+"% - "+self.unit.Get_DMG(m = self.u_count,t = 2,crit = True),True,(255,255,255))
                    textRect = text.get_rect()
                    textRect.right = temp_rect[2] - 5 - (textRect.centery - textRect.top) - 1 + i_w
                    textRect.bottom = h - 10#frame_rect.top - 10
                    DrawHexFrame(textRect,faction_clrs[self.unit.faction],offl = 15,surface = self.info_txt)
                    self.info_txt.blit(text,textRect)
                    image = crit_symbol
                    rect = image.get_rect()
                    rect.right = textRect.left - 5
                    rect.centery = textRect.centery
                    self.info_txt.blit(image,rect)
                
            if self.unit.move_cd[self.u_count] > 0:
                if self.unit.move_cd[self.u_count] > 1:
                    text = self.hp_font.render(str(self.unit.move_cd[self.u_count])+" Turns",True,(255,255,255))
                else:
                    text = self.hp_font.render(str(self.unit.move_cd[self.u_count])+" Turn",True,(255,255,255))
                textRect = text.get_rect()
                image = cd_symbol
                rect = image.get_rect()
                rect.left = textRect.centery - textRect.top + i_w
                textRect.left = rect.right + 5
                textRect.bottom = h - 10
                rect.centery = textRect.centery
                DrawHexFrame(textRect,faction_clrs[self.unit.faction],offl = 15,surface = self.info_txt)
                self.info_txt.blit(text,textRect)
                self.info_txt.blit(image,rect)

            for i in self.unit.move_info[self.u_count]:
                for j in i:
                    if "#" in j:
                        text = self.font.render("",True,(0,0,0))
                        textRect = text.get_rect()
                        textRect.left, textRect.top = x,y
                        image = self.unit.imgs[int(j[1:])]
                        rect = image.get_rect()
                        rect.left = x
                        rect.centery = textRect.centery
                        temp_txt.blit(image,rect)
                        x += rect[2]
                    elif "@" in j:
                        if 48 <= ord(j[1:2]) <= 57:
                            text = self.font.render(j[2:],True,self.unit.colour[int(j[1:2])])
                        else:
                            text = self.font.render(j[2:],True,self.unit.colour[ord(j[1:2])-87])
                    else:
                        text = self.font.render(j,True,(255,255,255))
                    textRect = text.get_rect()
                    textRect.left,textRect.top = x,y
                    temp_txt.blit(text,textRect)
                    x += textRect[2]
                x = 25
                y += textRect[3] + 5

            self.info_txt.blit(temp_txt,[i_w,h])

            if len(self.unit.move_icon) > self.u_count and self.unit.move_icon[self.u_count]:#len(self.unit.imgs) > 0:
                image = self.unit.move_icon[self.u_count]
                rect = image.get_rect()
                rect.centerx = i_w
                rect.centery = lrect.centery + h
                self.info_txt.blit(image,rect)

##            image = list(Projectile_Icons.values())[randint(0,9)]#freeze_projectile_icon
##            rect = image.get_rect()
##            rect.right = lrect.left + i_w
##            rect.centery = lrect.centery + h
##            self.info_txt.blit(image,rect)
                
            self.info_rect.left = 100
            self.info_rect.bottom = window_height - 30

    def DrawInfo(self):
        c = (40 - abs(self.a_lp - 40))/8
        self.a_lp = (self.a_lp + 1)%81

        if self.fm.acting_unit.draw_lp < 100:
            self.fm.acting_unit.draw_lp += 4
            self.fm.acting_unit.DrawOptions(lp = False)

        game_window.blit(self.desc_bgd,self.desc_rect)
        game_window.blit(self.desc_txt,self.desc_rect)

        text = self.t_font.render(self.unit.name,True,(255,255,255))
        textRect = text.get_rect()
        textRect.right = self.desc_rect.centerx + (self.unit.i_rect[2] + 5 + textRect[2])/2
        textRect.centery = self.desc_rect.top
        DrawDoubleFrame(textRect, faction_clrs[self.unit.faction], ltx = 15 + self.unit.i_rect[2],lbx = 10 + self.unit.i_rect[2])
        game_window.blit(text,textRect)
        self.unit.i_rect.right = textRect.left - 5
        self.unit.i_rect.centery = textRect.centery
        game_window.blit(self.unit.icon,self.unit.i_rect)

        n = self.fm.units_list.index(self.unit)
        l = len(self.fm.units_list)

        if l > 1 and self.mode == 1:
            pygame.draw.polygon(game_window,(255,255,255),[[self.desc_rect.left + 10 + c,textRect.centery],
                                                           [self.desc_rect.left + 20 + c,textRect.centery - 10],
                                                           [self.desc_rect.left + 20 + c,textRect.centery + 10]])
            pygame.draw.polygon(game_window,(255,255,255),[[self.desc_rect.right - 10 - c,textRect.centery],
                                                           [self.desc_rect.right - 20 - c,textRect.centery - 10],
                                                           [self.desc_rect.right - 20 - c,textRect.centery + 10]])

            u = self.fm.units_list[(n - 1)%l]
            u.i_rect.left = self.desc_rect.left + 30
            u.i_rect.centery = textRect.centery
            game_window.blit(u.icon,u.i_rect)

            u = self.fm.units_list[(n + 1)%l]
            u.i_rect.right = self.desc_rect.right - 30
            u.i_rect.centery = textRect.centery
            game_window.blit(u.icon,u.i_rect)


        if self.mode == 1:
            if len(self.unit.EffectTimer) > 0:
                game_window.blit(self.se_bgd,self.se_rect)
                game_window.blit(self.se_txt,self.se_rect)
            
            keystate = pygame.key.get_pressed()
            if len(self.unit.move_type) > 0:
                if not self.highlighted:
                    self.highlighted = True
                    if self.unit.move_get_tile[self.u_count]:
                        self.unit.move_get_tile[self.u_count](self.unit.x,self.unit.y,self.unit.Get_MvmRange(),c = self.unit.move_range[self.u_count][1])
                    else:
                        SetHighlightTiles(self.unit.x,self.unit.y, self.unit.Get_Range(n = self.u_count), c = self.unit.move_range[self.u_count][1])
                        SetBoundaryTiles(self.unit.x,self.unit.y, self.unit.Get_Range(n = self.u_count), c = self.unit.move_range[self.u_count][1],exclude = -1)
                if self.cd == 0 and self.mode == 1:
                    if keystate[pygame.K_UP]:
                        ClearAllTiles()
                        self.highlighted = False
                        self.u_count = (self.u_count - 1)%len(self.unit.move_type)
                        self.cd = 20
                        self.LoadInfo()
                    elif keystate[pygame.K_DOWN]:
                        ClearAllTiles()
                        self.highlighted = False
                        self.u_count = (self.u_count + 1)%len(self.unit.move_type)
                        self.cd = 20
                        self.LoadInfo()
                    elif keystate[pygame.K_LEFT] and l > 1:
                        ClearAllTiles()
                        self.highlighted = False
                        self.u_count = 0
                        self.unit = self.fm.units_list[(n - 1)%l]
                        self.clr,self.p_clr,self.n_clr = faction_clrs[self.unit.faction],faction_clrs[self.unit.faction],faction_clrs[self.unit.faction]
                        self.x, self.y = self.unit.x, self.unit.y
                        self.cd = 20
                        self.LoadDesc()
                    elif keystate[pygame.K_RIGHT] and l > 1:
                        ClearAllTiles()
                        self.highlighted = False
                        self.u_count = 0
                        self.unit = self.fm.units_list[(n + 1)%l]
                        self.clr,self.p_clr,self.n_clr = faction_clrs[self.unit.faction],faction_clrs[self.unit.faction],faction_clrs[self.unit.faction]
                        self.x, self.y = self.unit.x, self.unit.y
                        self.cd = 20
                        self.LoadDesc()
                y = window_height - 30
                pygame.draw.polygon(game_window,(255,255,255),[[50,window_height - 10 + c],
                                                               [40,window_height - 20 + c],
                                                               [60,window_height - 20 + c],])
                for i in range(len(self.unit.move_type)):
                    n = len(self.unit.move_type) - 1 - i
                    text = self.st_font.render(self.unit.move_type[n],True,(247,225,36) if n == self.u_count else (255,255,255))
                    textRect = text.get_rect()
                    textRect.centerx = 50
                    textRect.bottom = y
                    y -= textRect[3] + 10
                    if n == self.u_count:
                        DrawTextFrame(textRect, (29,90,118),ltx = 8,lbx = 4,rtx = 8,rbx = 4,lty = 3,lby = 3,rty = 6,rby = 6)
                    game_window.blit(text,textRect)
                pygame.draw.polygon(game_window,(255,255,255),[[50,textRect[1] - 20 - c],
                                                               [40,textRect[1] - 10 - c],
                                                               [60,textRect[1] - 10 - c],])

                if len(self.unit.move_info[self.u_count]) > 0:
                    game_window.blit(self.info_bgd,self.info_rect)
                    game_window.blit(self.info_txt,self.info_rect)

##    def DrawInfo(self):
##        c = (40 - abs(self.a_lp - 40))/8
##        self.a_lp = (self.a_lp + 1)%81
##
##        if self.fm.acting_unit.draw_lp < 100:
##            self.fm.acting_unit.draw_lp += 4
##            self.fm.acting_unit.DrawOptions(lp = False)
##
##        rw,eh = 0,0
##        if len(self.unit.Resistance) > 0 and len(self.unit.Weakness) > 0:
##            rw += 2 + max(len(self.unit.Resistance),len(self.unit.Weakness))
##        elif len(self.unit.Resistance) > 0:
##            rw += 2 + len(self.unit.Resistance)//2 + len(self.unit.Resistance)%2
##        elif len(self.unit.Weakness)  > 0:
##            rw += 2 + len(self.unit.Weakness)//2 + len(self.unit.Weakness)%2
##        if rw > 0:
##            eh = (self.hp_h + 5) * 2 + (self.f_h + 5) * (rw - 2)
##        frame = pygame.Surface((450,100 + len(self.unit.info) * (self.f_h + 5) + eh))
##        frame_rect = frame.get_rect()
##
##        frame.fill(info_clr)
##        frame.set_alpha(200)
##        frame_rect.right = window_width - 20
##        frame_rect.top = 30
##        x = frame_rect.left + 25
##        y = frame_rect.top + 75
##        RoundCorner(frame,frame_rect)
##        game_window.blit(frame,frame_rect)
##
##        self.text = self.t_font.render(self.unit.name,True,(255,255,255))
##        self.textRect = self.text.get_rect()
##        self.textRect.right = frame_rect.centerx + (self.unit.i_rect[2] + 5 + self.textRect[2])/2
##        self.textRect.centery = frame_rect.top
##        DrawDoubleFrame(self.textRect, faction_clrs[self.unit.faction], ltx = 15 + self.unit.i_rect[2],lbx = 10 + self.unit.i_rect[2])
##        game_window.blit(self.text,self.textRect)
##        self.unit.i_rect.right = self.textRect.left - 5
##        self.unit.i_rect.centery = self.textRect.centery
##        game_window.blit(self.unit.icon,self.unit.i_rect)
##
##        n = self.fm.units_list.index(self.unit)
##        l = len(self.fm.units_list)
##
##        if l > 1 and self.mode == 1:
##            pygame.draw.polygon(game_window,(255,255,255),[[frame_rect.left + 10 + c,self.textRect.centery],
##                                                           [frame_rect.left + 20 + c,self.textRect.centery - 10],
##                                                           [frame_rect.left + 20 + c,self.textRect.centery + 10]])
##            pygame.draw.polygon(game_window,(255,255,255),[[frame_rect.right - 10 - c,self.textRect.centery],
##                                                           [frame_rect.right - 20 - c,self.textRect.centery - 10],
##                                                           [frame_rect.right - 20 - c,self.textRect.centery + 10]])
##
##            u = self.fm.units_list[(n - 1)%l]
##            u.i_rect.left = frame_rect.left + 30
##            u.i_rect.centery = self.textRect.centery
##            game_window.blit(u.icon,u.i_rect)
##
##            u = self.fm.units_list[(n + 1)%l]
##            u.i_rect.right = frame_rect.right - 30
##            u.i_rect.centery = self.textRect.centery
##            game_window.blit(u.icon,u.i_rect)
##
##        self.text = self.hp_font.render("HP   "+str(self.unit.HP)+"/"+str(self.unit.MaxHP),True,(255,255,255))
##        self.textRect = self.text.get_rect()
##        self.textRect.left = frame_rect.centerx - (166 + self.textRect[2])/2
##        self.textRect.centery = frame_rect.top + 50
##        game_window.blit(self.text,self.textRect)
##
##        HP_b_rect.left = self.textRect.right + 13
##        HP_b_rect.centery = self.textRect.centery
##        if self.unit.HP > 0:
##            if self.unit.HP/self.unit.MaxHP <= 0.3:
##                DrawBar(HP_b_rect,self.unit.HP,self.unit.MaxHP,(255,115,115))
##            else:
##                DrawBar(HP_b_rect,self.unit.HP,self.unit.MaxHP,faction_bar_clrs[self.unit.faction])
##
##        for i in self.unit.info:
##            for j in i:
##                if "#" in j:
##                    self.text = self.font.render("",True,(0,0,0))
##                    self.textRect = self.text.get_rect()
##                    self.textRect.left = x
##                    self.textRect.top = y
##                    self.image = self.unit.imgs[int(j[1:])]
##                    self.rect = self.image.get_rect()
##                    self.rect.left = x
##                    self.rect.centery = self.textRect.centery
##                    game_window.blit(self.image,self.rect)
##                    x += self.rect[2]
##                elif "@" in j:
##                    if 48 <= ord(j[1:2]) <= 57:
##                        self.text = self.font.render(j[2:],True,self.unit.colour[int(j[1:2])])
##                    else:
##                        self.text = self.font.render(j[2:],True,self.unit.colour[ord(j[1:2])-87])
##                else:
##                    self.text = self.font.render(j,True,(255,255,255))
##                self.textRect = self.text.get_rect()
##                self.textRect.left = x
##                self.textRect.top = y
##                game_window.blit(self.text,self.textRect)
##                x += self.textRect[2]
##            x = frame_rect.left + 25
##            y += self.textRect[3] + 5
##        if rw > 0:
##            y += self.textRect[3] + 5
##        if len(self.unit.Resistance) > 0 and len(self.unit.Weakness) > 0:
##            cy = y
##            self.text = self.hp_font.render("Resistance",True,(255,255,255))
##            self.textRect = self.text.get_rect()
##            self.textRect.centerx = frame_rect.left + frame_rect[2]/4
##            self.textRect.top = cy
##            self.rw_rect.center = self.textRect.center
##            DrawHexFrame(self.rw_rect,(50,123,180))
##            game_window.blit(self.text,self.textRect)
##            cy += self.textRect[3] + 5
##
##            w,s = [],[]
##            for i in self.unit.Resistance:
##                w.append(self.font.size(i)[0])
##                s.append(ES_Widths.get(i))
##            w,s = max(w)+5,max(s)
##            for i in self.unit.Resistance:
##                self.img = Element_Symbols.get(i)
##                self.rect = self.img.get_rect()
##                self.rect.centerx = self.rw_rect.centerx - w/2
##                self.text = self.font.render(i,True,(255,255,255))
##                self.textRect = self.text.get_rect()
##                self.textRect.top = cy
##                self.rect.centery = self.textRect.centery
##                self.textRect.left = self.rect.centerx + s/2 + 5
##                game_window.blit(self.img,self.rect)
##                game_window.blit(self.text,self.textRect)
##                cy += self.textRect[3] + 5
##            my = cy
##            
##            cy = y
##            self.text = self.hp_font.render("Weakness",True,(255,255,255))
##            self.textRect = self.text.get_rect()
##            self.textRect.centerx = frame_rect.right - frame_rect[2]/4
##            self.textRect.top = cy
##            self.rw_rect.center = self.textRect.center
##            DrawHexFrame(self.rw_rect,(180,50,50))
##            game_window.blit(self.text,self.textRect)
##            cy += self.textRect[3] + 5
##            w,s = [],[]
##            for i in self.unit.Weakness:
##                w.append(self.font.size(i)[0])
##                s.append(ES_Widths.get(i))
##            w,s = max(w)+5,max(s)
##            for i in self.unit.Weakness:
##                self.img = Element_Symbols.get(i)
##                self.rect = self.img.get_rect()
##                self.rect.centerx = self.rw_rect.centerx - w/2
##                self.text = self.font.render(i,True,(255,255,255))
##                self.textRect = self.text.get_rect()
##                self.textRect.top = cy
##                self.rect.centery = self.textRect.centery
##                self.textRect.left = self.rect.centerx + s/2 + 5
##                game_window.blit(self.img,self.rect)
##                game_window.blit(self.text,self.textRect)
##                cy += self.textRect[3] + 5
##            if cy > my:
##                my = cy
##            pygame.draw.line(game_window,(255,255,255),[frame_rect.centerx,y],[frame_rect.centerx,my],width = 3)
##            
##        elif len(self.unit.Resistance) > 0:
##            self.text = self.hp_font.render("Resistance",True,(255,255,255))
##            self.textRect = self.text.get_rect()
##            self.textRect.centerx = frame_rect.centerx
##            self.textRect.top = y
##            self.rw_rect.center = self.textRect.center
##            DrawHexFrame(self.rw_rect,(50,123,180))
##            game_window.blit(self.text,self.textRect)
##            y += self.textRect[3] + 5
##
##            w,s = [[],[],[]],[[],[],[]]
##            for i in range(len(self.unit.Resistance)):
##                if len(self.unit.Resistance) % 2 == 1 and i == len(self.unit.Resistance) - 1:
##                    w[0].append(self.font.size(self.unit.Resistance[i])[0])
##                    s[0].append(ES_Widths.get(self.unit.Resistance[i]))
##                elif i % 2 == 0:
##                    w[1].append(self.font.size(self.unit.Resistance[i])[0])
##                    s[1].append(ES_Widths.get(self.unit.Resistance[i]))
##                else:
##                    w[2].append(self.font.size(self.unit.Resistance[i])[0])
##                    s[2].append(ES_Widths.get(self.unit.Resistance[i]))
##            for i in range(3):
##                if len(w[i]) > 0:
##                    w[i] = max(w[i])+5
##                if len(s[i]) > 0:
##                    s[i] = max(s[i])
##            for i in range(len(self.unit.Resistance)):
##                if len(self.unit.Resistance) % 2 == 1 and i == len(self.unit.Resistance) - 1:
##                    x,a = frame_rect.centerx - w[0]/2, 0
##                elif i % 2 == 0:
##                    x,a = frame_rect.left + frame_rect[2]/4 - w[1]/2, 1
##                else:
##                    x,a = frame_rect.centerx + frame_rect[2]/4 - w[2]/2, 2
##                self.img = Element_Symbols.get(self.unit.Resistance[i])
##                self.rect = self.img.get_rect()
##                self.rect.centerx = x
##                self.text = self.font.render(self.unit.Resistance[i],True,(255,255,255))
##                self.textRect = self.text.get_rect()
##                self.textRect.top = y
##                self.rect.centery = self.textRect.centery
##                self.textRect.left = self.rect.centerx + s[a]/2 + 5
##                game_window.blit(self.img,self.rect)
##                game_window.blit(self.text,self.textRect)
##                if i % 2 == 1:
##                    y += self.textRect[3] + 5
##        elif len(self.unit.Weakness)  > 0:
##            self.text = self.hp_font.render("Weakness",True,(255,255,255))
##            self.textRect = self.text.get_rect()
##            self.textRect.centerx = frame_rect.centerx
##            self.textRect.top = y
##            self.rw_rect.center = self.textRect.center
##            DrawHexFrame(self.rw_rect,(180,50,50))
##            game_window.blit(self.text,self.textRect)
##            y += self.textRect[3] + 5
##            
##            w,s = [[],[],[]],[[],[],[]]
##            for i in range(len(self.unit.Weakness)):
##                if len(self.unit.Weakness) % 2 == 1 and i == len(self.unit.Weakness) - 1:
##                    w[0].append(self.font.size(self.unit.Weakness[i])[0])
##                    s[0].append(ES_Widths.get(self.unit.Weakness[i]))
##                elif i % 2 == 0:
##                    w[1].append(self.font.size(self.unit.Weakness[i])[0])
##                    s[1].append(ES_Widths.get(self.unit.Weakness[i]))
##                else:
##                    w[2].append(self.font.size(self.unit.Weakness[i])[0])
##                    s[2].append(ES_Widths.get(self.unit.Weakness[i]))
##            for i in range(3):
##                if len(w[i]) > 0:
##                    w[i] = max(w[i])+5
##                if len(s[i]) > 0:
##                    s[i] = max(s[i])
##            for i in range(len(self.unit.Weakness)):
##                if len(self.unit.Weakness) % 2 == 1 and i == len(self.unit.Weakness) - 1:
##                    x,a = frame_rect.centerx - w[0]/2, 0
##                elif i % 2 == 0:
##                    x,a = frame_rect.left + frame_rect[2]/4 - w[1]/2, 1
##                else:
##                    x,a = frame_rect.centerx + frame_rect[2]/4 - w[2]/2, 2
##                self.img = Element_Symbols.get(self.unit.Weakness[i])
##                self.rect = self.img.get_rect()
##                self.rect.centerx = x
##                self.text = self.font.render(self.unit.Weakness[i],True,(255,255,255))
##                self.textRect = self.text.get_rect()
##                self.textRect.top = y
##                self.rect.centery = self.textRect.centery
##                self.textRect.left = self.rect.centerx + s[a]/2 + 5
##                game_window.blit(self.img,self.rect)
##                game_window.blit(self.text,self.textRect)
##                if i % 2 == 1:
##                    y += self.textRect[3] + 5
##        if self.mode == 1:
##            if len(self.unit.EffectTimer) > 0:
##                t = frame_rect.bottom + 20
##
##                n_w = []
##                t_w = []
##                i_w = []
##                for i in range(len(self.unit.EffectTimer)):
##                    i_w.append(SE_Widths.get(self.unit.StatusEffect[i]))
##                    n_w.append(self.font.size(self.unit.StatusEffect[i])[0])
##                    t_w.append(self.font.size(str(self.unit.EffectTimer[i]))[0])
##                frame = pygame.Surface((70 + max(i_w) + max(n_w) + max(t_w),25 + len(self.unit.EffectTimer) * (self.f_h + 5)))
##                i_w = max(i_w)/2
##                frame_rect = frame.get_rect()
##                frame.fill(info_clr)
##                frame.set_alpha(200)
##                frame_rect.top = t
##                frame_rect.right = window_width - 20
##                RoundCorner(frame,frame_rect)
##                game_window.blit(frame,frame_rect)
##
##                y = frame_rect.top + 15
##                for i in range(len(self.unit.EffectTimer)):
##                    self.text = self.font.render("",True,(0,0,0))
##                    self.textRect = self.text.get_rect()
##                    self.textRect.top = y
##                    self.image = SE_Symbols.get(self.unit.StatusEffect[i])
##                    self.rect = self.image.get_rect()
##                    self.rect.centerx = frame_rect.left + 15 + i_w
##                    self.rect.centery = self.textRect.centery
##                    game_window.blit(self.image,self.rect)
##
##                    x = frame_rect.left + 25 + i_w * 2
##                    
##                    self.text = self.font.render(self.unit.StatusEffect[i],True,SE_colour_set.get(self.unit.StatusEffect[i]))
##                    self.textRect = self.text.get_rect()
##                    self.textRect.left = x
##                    self.textRect.top = y
##                    game_window.blit(self.text,self.textRect)
##                    x += self.textRect[2] + 10
##                    
##                    self.text = self.font.render(str(self.unit.EffectTimer[i]),True,(255,255,255))
##                    self.textRect = self.text.get_rect()
##                    self.textRect.right = frame_rect.right - 25
##                    self.textRect.top = y
##                    game_window.blit(self.text,self.textRect)
##                    y += self.f_h + 5
##                    
##            
##            keystate = pygame.key.get_pressed()
##            if len(self.unit.move_type) > 0:
##                if not self.highlighted:
##                    self.highlighted = True
##                    if self.unit.move_get_tile[self.u_count]:
##                        self.unit.move_get_tile[self.u_count](self.unit.x,self.unit.y,self.unit.Get_MvmRange(),c = self.unit.move_range[self.u_count][1])
##                    else:
##                        SetHighlightTiles(self.unit.x,self.unit.y, self.unit.Get_Range(n = self.u_count), c = self.unit.move_range[self.u_count][1])
##                        SetBoundaryTiles(self.unit.x,self.unit.y, self.unit.Get_Range(n = self.u_count), c = self.unit.move_range[self.u_count][1],exclude = -1)
##                if self.cd == 0 and self.mode == 1:
##                    if keystate[pygame.K_UP]:
##                        ClearAllTiles()
##                        self.highlighted = False
##                        self.u_count = (self.u_count - 1)%len(self.unit.move_type)
##                        self.cd = 20
##                    elif keystate[pygame.K_DOWN]:
##                        ClearAllTiles()
##                        self.highlighted = False
##                        self.u_count = (self.u_count + 1)%len(self.unit.move_type)
##                        self.cd = 20
##                    elif keystate[pygame.K_LEFT] and l > 1:
##                        ClearAllTiles()
##                        self.highlighted = False
##                        self.u_count = 0
##                        self.unit = self.fm.units_list[(n - 1)%l]
##                        self.clr,self.p_clr,self.n_clr = faction_clrs[self.unit.faction],faction_clrs[self.unit.faction],faction_clrs[self.unit.faction]
##                        self.x, self.y = self.unit.x, self.unit.y
##                        self.cd = 20
##                    elif keystate[pygame.K_RIGHT] and l > 1:
##                        ClearAllTiles()
##                        self.highlighted = False
##                        self.u_count = 0
##                        self.unit = self.fm.units_list[(n + 1)%l]
##                        self.clr,self.p_clr,self.n_clr = faction_clrs[self.unit.faction],faction_clrs[self.unit.faction],faction_clrs[self.unit.faction]
##                        self.x, self.y = self.unit.x, self.unit.y
##                        self.cd = 20
##                y = window_height - 30
##                pygame.draw.polygon(game_window,(255,255,255),[[50,window_height - 10 + c],
##                                                               [40,window_height - 20 + c],
##                                                               [60,window_height - 20 + c],])
##                for i in range(len(self.unit.move_type)):
##                    n = len(self.unit.move_type) - 1 - i
##                    self.text = self.st_font.render(self.unit.move_type[n],True,(247,225,36) if n == self.u_count else (255,255,255))
##                    self.textRect = self.text.get_rect()
##                    self.textRect.centerx = 50
##                    self.textRect.bottom = y
##                    y -= self.textRect[3] + 10
##                    if n == self.u_count:
##                        DrawTextFrame(self.textRect, (29,90,118),ltx = 8,lbx = 4,rtx = 8,rbx = 4,lty = 3,lby = 3,rty = 6,rby = 6)
##                    game_window.blit(self.text,self.textRect)
##
##                pygame.draw.polygon(game_window,(255,255,255),[[50,self.textRect[1] - 20 - c],
##                                                               [40,self.textRect[1] - 10 - c],
##                                                               [60,self.textRect[1] - 10 - c],])
##
##                if len(self.unit.move_info[self.u_count]) > 0:
##                    frame = pygame.Surface((450,25 + self.t_font.size("")[1] + len(self.unit.move_info[self.u_count]) * (self.f_h + 5) + (self.hp_h + 5 if self.unit.move_stat[self.u_count] else 0)))
##                    frame_rect = frame.get_rect()
##                    frame.fill(info_clr)
##                    frame.set_alpha(200)
##                    frame_rect.left = 100
##                    frame_rect.bottom = window_height - 30
##                    x = frame_rect.left + 25
##                    y = frame_rect.top + 10
##                    RoundCorner(frame,frame_rect)
##                    game_window.blit(frame,frame_rect)
##
##                    self.text = self.t_font.render(self.unit.move_label[self.u_count],True,(255,255,255))
##                    self.textRect = self.text.get_rect()
##                    self.textRect.left, self.textRect.top = x,y
##                    game_window.blit(self.text,self.textRect)
##                    y = self.textRect.bottom + 5
##    
##                    if self.unit.move_stat[self.u_count]:
##                        if self.unit.move_SE[self.u_count]:
##                            self.text = self.hp_font.render(self.unit.Get_DMG(m = self.u_count,t = 2),True,SE_colour_set.get(self.unit.move_SE[self.u_count]))
##                            self.textRect = self.text.get_rect()
##                            self.textRect.left, self.textRect.top = x + 5 + SE_Widths.get(self.unit.move_SE[self.u_count]),y
##                            self.image = SE_Symbols.get(self.unit.move_SE[self.u_count])
##                            self.rect = self.image.get_rect()
##                            self.rect.left = x
##                            self.rect.centery = self.textRect.centery
##                            game_window.blit(self.image,self.rect)
##                        else:
##                            self.text = self.hp_font.render(self.unit.Get_DMG(m = self.u_count,t = 2),True,(255,255,255))
##                            self.textRect = self.text.get_rect()
##                            self.textRect.left, self.textRect.top = x,y
##                        game_window.blit(self.text,self.textRect)
##                        y += self.textRect[3] + 5
##                        if self.unit.Get_Crit(self.u_count) > 0:
##                            self.text = self.hp_font.render(str(self.unit.Get_Crit(self.u_count))+"% - "+self.unit.Get_DMG(m = self.u_count,t = 2,crit = True),True,(255,255,255))
##                            self.textRect = self.text.get_rect()
##                            self.textRect.right = frame_rect.right - 5 - (self.textRect.centery - self.textRect.top)
##                            self.textRect.bottom = frame_rect.top - 10
##                            DrawHexFrame(self.textRect,faction_clrs[self.unit.faction],offl = 15)
##                            game_window.blit(self.text,self.textRect)
##                            self.image = crit_symbol
##                            self.rect = self.image.get_rect()
##                            self.rect.right = self.textRect.left - 5
##                            self.rect.centery = self.textRect.centery
##                            game_window.blit(self.image,self.rect)
##                    if self.unit.move_cd[self.u_count] > 0:
##                        if self.unit.move_cd[self.u_count] > 1:
##                            self.text = self.hp_font.render(str(self.unit.move_cd[self.u_count])+" Turns",True,(255,255,255))
##                        else:
##                            self.text = self.hp_font.render(str(self.unit.move_cd[self.u_count])+" Turn",True,(255,255,255))
##                        self.textRect = self.text.get_rect()
##                        self.textRect.left = frame_rect.left + 25 + (self.textRect.centery - self.textRect.top)
##                        self.textRect.bottom = frame_rect.top - 10
##                        DrawHexFrame(self.textRect,faction_clrs[self.unit.faction],offl = 15)
##                        game_window.blit(self.text,self.textRect)
##                        self.image = cd_symbol
##                        self.rect = self.image.get_rect()
##                        self.rect.right = self.textRect.left - 5
##                        self.rect.centery = self.textRect.centery
##                        game_window.blit(self.image,self.rect)
##            
##                    for i in self.unit.move_info[self.u_count]:
##                        for j in i:
##                            if "#" in j:
##                                self.text = self.font.render("",True,(0,0,0))
##                                self.textRect = self.text.get_rect()
##                                self.textRect.left, self.textRect.top = x,y
##                                self.image = self.unit.imgs[int(j[1:])]
##                                self.rect = self.image.get_rect()
##                                self.rect.left = x
##                                self.rect.centery = self.textRect.centery
##                                game_window.blit(self.image,self.rect)
##                                x += self.rect[2]
##                            elif "@" in j:
##                                if 48 <= ord(j[1:2]) <= 57:
##                                    self.text = self.font.render(j[2:],True,self.unit.colour[int(j[1:2])])
##                                else:
##                                    self.text = self.font.render(j[2:],True,self.unit.colour[ord(j[1:2])-87])
##                            else:
##                                self.text = self.font.render(j,True,(255,255,255))
##                            self.textRect = self.text.get_rect()
##                            self.textRect.left,self.textRect.top = x,y
##                            game_window.blit(self.text,self.textRect)
##                            x += self.textRect[2]
##                        x = frame_rect.left + 25
##                        y += self.textRect[3] + 5
