import pygame
from random import *
from math import *
from VoxelGame_BaseVars import *

def DrawTextFrame(rect,colour,ltx = 10,lbx = 5,rtx = 10,rbx = 5,lty = 5,lby = 5,rty = 10,rby = 10, surface = game_window):
    pygame.draw.polygon(surface,colour,[(rect.left - ltx,rect.top - lby),
                                              (rect.left - lbx,rect.bottom + lby),
                                              (rect.right + rbx,rect.bottom + rby),
                                              (rect.right + rtx,rect.top - rty)])

def DrawDoubleFrame(rect,colour1,colour2 = None,ltx = 10,lbx = 5,rtx = 10,rbx = 5,lty = 5,lby = 5,rty = 10,rby = 10,offx = 5,offy = 5, surface = game_window):
    if not colour2:
        colour2 = Darken(colour1,30)
    pygame.draw.polygon(surface,colour2,[(rect.left + offx - ltx,rect.top + offy - lby),
                                              (rect.left + offx - lbx,rect.bottom + offy + lby),
                                              (rect.right + offx + rbx,rect.bottom + offy + rby),
                                              (rect.right + offx + rtx,rect.top + offy - rty)])
    pygame.draw.polygon(surface,colour1,[(rect.left - ltx,rect.top - lby),
                                              (rect.left - lbx,rect.bottom + lby),
                                              (rect.right + rbx,rect.bottom + rby),
                                              (rect.right + rtx,rect.top - rty)])

def DrawHexFrame(rect,colour, offl = 0, offr = 0, surface = game_window):
    pygame.draw.polygon(surface,colour,[(rect.left-5-offl,rect.top),
                                              (rect.left-5-offl-(rect.centery-rect.top),rect.centery),
                                              (rect.left-5-offl,rect.bottom),
                                              (rect.right+offr+5,rect.bottom),
                                              (rect.right+offr+5+(rect.centery-rect.top),rect.centery),
                                              (rect.right+offr+5,rect.top)])

def DrawDoubleHexFrame(rect,colour,colour2, offl = 0, offr = 0,w = 3, surface = game_window):
    pygame.draw.polygon(surface,colour2,[(rect.left-5-offl-w,rect.top-w),
                                             (rect.left-5-offl-w*2-(rect.centery-rect.top),rect.centery),
                                             (rect.left-5-offl-w,rect.bottom+w),
                                             (rect.right+offr+5+w,rect.bottom+w),
                                             (rect.right+offr+5+w*2+(rect.centery-rect.top),rect.centery),
                                             (rect.right+offr+5+w,rect.top-w)])

    pygame.draw.polygon(surface,colour,[(rect.left-5-offl,rect.top),
                                            (rect.left-5-offl-(rect.centery-rect.top),rect.centery),
                                            (rect.left-5-offl,rect.bottom),
                                            (rect.right+offr+5,rect.bottom),
                                            (rect.right+offr+5+(rect.centery-rect.top),rect.centery),
                                            (rect.right+offr+5,rect.top)])

def DrawHexFlash(rect,colour,progress,offl = 0, offr = 0):
    dis = (rect[2]/2 + 5)*progress/100
    w = 5 if progress > 5 else progress
    pygame.draw.polygon(game_window,colour,[[rect.left - 5 - offl + dis,rect.top],
                                            [rect.left - 5 - offl + dis - rect[3]/2,rect.centery],
                                            [rect.left - 5 - offl + dis,rect.bottom],
                                            [rect.left - 5 - offl + dis - w,rect.bottom],
                                            [rect.left - 5 - offl + dis - rect[3]/2 - w,rect.centery],
                                            [rect.left - 5 - offl + dis - w,rect.top]])
    pygame.draw.polygon(game_window,colour,[[rect.right + 5 + offr - dis,rect.top],
                                            [rect.right + 5 + offr - dis + rect[3]/2,rect.centery],
                                            [rect.right + 5 + offr - dis,rect.bottom],
                                            [rect.right + 5 + offr - dis + w,rect.bottom],
                                            [rect.right + 5 + offr - dis + rect[3]/2 + w,rect.centery],
                                            [rect.right + 5 + offr - dis + w,rect.top]])

def DrawRoundFrame(rect,colour, offl = 0, offr = 0, surface = game_window):
    pygame.draw.polygon(surface,colour,[(rect.left-5-offl,rect.top),
                                            (rect.left-5-offl,rect.bottom),
                                            (rect.right+offr+5,rect.bottom),
                                            (rect.right+offr+5,rect.top)])
    pygame.draw.circle(surface,colour,[rect.left-5-offl,rect.centery],rect[3]/2)
    pygame.draw.circle(surface,colour,[rect.right+offr+5,rect.centery],rect[3]/2)

def DrawSmoothFrame(rect,colour, w = 5, h = 3,sn = True,se = True,ss = True,sw = True):
    if w > h:
        xrect = pygame.Rect(0,0,w,rect[3])
        yrect = pygame.Rect(0,0,rect[2] + (w-h)*2,h)
        r = h
    else:
        xrect = pygame.Rect(0,0,w,rect[3] + (h-w)*2)
        yrect = pygame.Rect(0,0,rect[2],h)
        r = w
    
    xrect.centery = rect.centery
    if se:
        xrect.left = rect.right
        pygame.draw.rect(game_window,colour,xrect)
    if sw:
        xrect.right = rect.left
        pygame.draw.rect(game_window,colour,xrect)

    yrect.centerx = rect.centerx
    if sn:
        yrect.bottom = rect.top
        pygame.draw.rect(game_window,colour,yrect)
    if ss:
        yrect.top = rect.bottom
        pygame.draw.rect(game_window,colour,yrect)
    
    pygame.draw.rect(game_window,colour,rect)
    if sn and sw:
        pygame.draw.circle(game_window,colour,[yrect.left,xrect.top],r)
    if ss and sw:    
        pygame.draw.circle(game_window,colour,[yrect.left,xrect.bottom],r)
    if ss and se:
        pygame.draw.circle(game_window,colour,[yrect.right,xrect.bottom],r)
    if sn and se:
        pygame.draw.circle(game_window,colour,[yrect.right,xrect.top],r)

def DrawOctFrame(rect,colour, w = 5, h = 3):
    pygame.draw.polygon(game_window,colour,[[rect.left - w,rect.top],
                                            [rect.left,rect.top - h],
                                            [rect.right,rect.top - h],
                                            [rect.right + w,rect.top],
                                            [rect.right + w,rect.bottom],
                                            [rect.right,rect.bottom + h],
                                            [rect.left,rect.bottom + h],
                                            [rect.left - w,rect.bottom]])

def DrawDiamondFrame(rect,colour,w):
    pygame.draw.polygon(game_window,colour,[(rect.centerx - w,rect.centery),
                                              (rect.centerx,rect.centery - w),
                                              (rect.centerx + w,rect.centery),
                                              (rect.centerx,rect.centery + w)])


def DrawHexBar(rect,value,max_value,clr,f_clr = (205,235,240),b_clr = (75,85,85),f_width = 3):
    r_rect = pygame.Rect(0,0,rect[2] - rect[3],rect[3])
    f_rect = pygame.Rect(0,0,rect[2] - rect[3] + f_width * 2 - 2,rect[3] + f_width * 2)
    
    r_rect.center = rect.center
    f_rect.center = rect.center

    if value == max_value:
        DrawDoubleHexFrame(r_rect,clr,f_clr,-5,-5,w = f_width)
    elif value <= 0:
        DrawDoubleHexFrame(r_rect,clr,b_clr,-5,-5,w = f_width)
    else:
        e_val = (rect[3]/2)/rect[2]
        p_val = value/max_value
        DrawDoubleHexFrame(r_rect,b_clr,f_clr,-5,-5,w = f_width)
        if p_val < e_val:
            p = rect[2] * p_val
            pygame.draw.polygon(game_window,clr,[[r_rect.left - rect[3]/2,r_rect.centery],
                                                 [r_rect.left - rect[3]/2 + p,r_rect.centery - p],
                                                 [r_rect.left - rect[3]/2 + p,r_rect.centery + p]])
                
                
        elif p_val < 1 - e_val:
            v_rect = pygame.Rect(0,0,RoundUp(rect[2] * (p_val - e_val)),rect[3])
            v_rect.left = r_rect.left
            v_rect.centery = r_rect.centery
            pygame.draw.polygon(game_window,clr,[[r_rect.left,rect.top],
                                                 [r_rect.left - rect[3]/2,rect.centery],
                                                 [r_rect.left,rect.bottom],
                                                 [v_rect.right,v_rect.bottom],
                                                 [v_rect.right,v_rect.top],])
        else:
            p = rect[2] * (p_val + e_val - 1)
            pygame.draw.polygon(game_window,clr,[[r_rect.left,rect.top],
                                                 [r_rect.left - rect[3]/2,rect.centery],
                                                 [r_rect.left,rect.bottom],
                                                 [r_rect.right,r_rect.bottom],
                                                 [r_rect.right + p,r_rect.bottom - p],
                                                 [r_rect.right + p,r_rect.top + p],
                                                 [r_rect.right,r_rect.top],])

def DrawBar(rect,value,max_value,clr,f_clr = (205,235,240),b_clr = (75,85,85),f_width = 3,segment = 1,surface = game_window):
    r_rect = pygame.Rect(0,0,rect[2],rect[3])
    f_rect = pygame.Rect(0,0,rect[2] - rect[3],rect[3] + f_width * 2)
    
    r_rect.center = rect.center
    f_rect.center = rect.center
    
    pygame.draw.rect(surface,f_clr,f_rect)
    pygame.draw.circle(surface,f_clr,[f_rect.left,f_rect.centery],rect[3]/2 + f_width)
    pygame.draw.circle(surface,f_clr,[f_rect.right,f_rect.centery],rect[3]/2 + f_width)

    bar = pygame.Surface((rect[2],rect[3]))
    bar.set_colorkey((0,0,0))
    bar.fill(b_clr)
    v_rect = pygame.Rect(0,0,RoundUp(rect[2] * value/max_value),rect[3])
    pygame.draw.rect(bar,clr,v_rect)

    if segment > 1:
        for i in range(1,segment):
            pygame.draw.line(bar,f_clr,[rect[2]*i/segment,0],[rect[2]*i/segment,rect[3]],width = 2)

    side = pygame.Surface((rect[3]/2,rect[3]))
    side.set_colorkey((1,1,1))
    pygame.draw.circle(side,(1,1,1),[rect[3]/2,rect[3]/2],rect[3]/2)
    bar.blit(side,[0,0])
    side = pygame.transform.rotate(side,180)
    bar.blit(side,[rect[2] - rect[3]/2,0])
    surface.blit(bar,r_rect)

def DrawPlaneVortex(center,w,h,d,clr = (59,0,126), frame_clr = (), swirl_clr = [], swirl = False,edge = 18):
    pts = []
    for i in range(18):
        pts.append([center[0] + cos(radians(d+i*20)) * w,center[1] + sin(radians(d+i*20)) * h])
    pygame.draw.polygon(game_window,clr,pts)
    if swirl:
        for j in range(3):
            pts = []
            for i in range(20):
                pts.append([center[0] + cos(radians(d+i*20+120*j)) * w * i/20,center[1] + sin(radians(d+i*20+120*j)) * h * i/20])
                if len(pts) >= 2:
                    pygame.draw.lines(game_window,swirl_clr[j],False,pts,2)
    for i in range(18):
        pts = []
        pts.append([center[0] + cos(radians(d+i*20)) * w,center[1] + sin(radians(d+i*20)) * h])
        pts.append([center[0] + cos(radians(d+i*20+5)) * 1.1 * w,center[1] + sin(radians(d+i*20+5)) * 1.1 * h])
        pts.append([center[0] + cos(radians(d+i*20+10)) * 1.2 * w,center[1] + sin(radians(d+i*20+10)) * 1.2 * h])
        pts.append([center[0] + cos(radians(d+i*20+20)) * 1.25 * w,center[1] + sin(radians(d+i*20+20)) * 1.25 * h])
        pts.append([center[0] + cos(radians(d+i*20+25)) * 1.3 * w,center[1] + sin(radians(d+i*20+25)) * 1.3 * h])
        pts.append([center[0] + cos(radians(d+i*20+19)) * 1.2 * w,center[1] + sin(radians(d+i*20+19)) * 1.2 * h])
        pts.append([center[0] + cos(radians(d+i*20+18)) * 1.1 * w,center[1] + sin(radians(d+i*20+18)) * 1.1 * h])
        pts.append([center[0] + cos(radians(d+(i+1)*20)) * w,center[1] + sin(radians(d+(i+1)*20)) * h])
        pygame.draw.polygon(game_window,clr,pts)
        pygame.draw.lines(game_window,frame_clr,False,pts,1)

def DrawVortex(center,r,d,clr = (59,0,126), frame_clr = (), swirl_clr = None,edge = 18):
    for i in range(5):
        pygame.draw.circle(game_window,Darken(clr,i * 10),center,(r+2)*(1-i/5))
    if swirl_clr:
        for j in range(3):
            pts = []
            for i in range(int(r)-1):
                p1 = [center[0] + cos(radians(d+i*20+120*j)) * i,center[1] + sin(radians(d+i*20+120*j)) * i]
                p2 = [center[0] + cos(radians(d+(i+1)*20+120*j)) * i,center[1] + sin(radians(d+(i+1)*20+120*j)) * i]
                pygame.draw.line(game_window,Darken(swirl_clr,10+65*(1-i/(int(r)-1))),p1,p2,2)

    for i in range(8):
        pts = []
        for j in [[0,1],[11,1.1],[22,1.2],[33,1.23],[45,1.25],[56,1.3],[43,1.2],[40,1.1],[45,1]]:
            pts.append([center[0] + cos(radians(d + i*45 + j[0])) * j[1] * r,center[1] + sin(radians(d + i*45 + j[0])) * j[1] * r])
        pygame.draw.polygon(game_window,clr,pts)

def DrawDiamond(x,y,r,clr = (255,255,255),surface = game_window):
    pygame.draw.polygon(surface,clr,[[x + r,y],
                                     [x,y + r],
                                     [x - r,y],
                                     [x,y - r]])

def DrawStar(x,y,r,sr,d = 0,clr = (255,255,255),surface = game_window):
    pts = []
    for i in range(4):
        pts.append([x + cos(radians(d + i * 90)) * r,y - sin(radians(d + i * 90)) * r])
        pts.append([x + cos(radians(d + i * 90 + 45)) * sr,y - sin(radians(d + i * 90 + 45)) * sr])
    pygame.draw.polygon(surface,clr,pts)
    
class PopUpText():
    def __init__(self,txt = "Lorum Ipsum",x = window_width/2,y = window_height/2,clr = (255,255,255),font = stat_font20, img = None):
        self.font = font
        self.loop = 300
        self.text = self.font.render(txt,True,clr).convert_alpha()
        self.textRect = self.text.get_rect()
        self.textRect.centerx = x
        self.textRect.centery = y
        tile_sprites.sprites()[0].visual_sprites.append(self)

        if img:
            self.img = img.copy()
            self.rect = self.img.get_rect()
        else:
            self.img = None

    def update(self):
        if self.loop <= 0:
            tile_sprites.sprites()[0].visual_sprites.remove(self)
            del self.img
            del self
            return
        self.textRect.centerx -= 0.1
        self.textRect.centery -= 2
        if self.loop < 255:
            self.text.set_alpha(self.loop)
        if self.img:
            if self.loop < 255:
                self.img.set_alpha(self.loop)
                
            self.rect.left = self.textRect.right + 5
            self.rect.centery = self.textRect.centery
        self.loop -= 3

    def draw(self):
        game_window.blit(self.text,self.textRect)

        if self.img:
            game_window.blit(self.img,self.rect)

class CentralDisplay():
    def __init__(self,txt = "Lorum Ipsum",clr = (70,110,255),t_clr = (255,255,255),y = 100,width = None,wait = 1,font = title_font25):
        self.font = font
        h = self.font.size(txt)[1] + 10

        self.clr = clr
        self.y = y
        
        self.t_box = pygame.Surface((7,h),pygame.SRCALPHA,32).convert_alpha()
        self.t_box.fill(self.clr)
        self.t_rect = self.t_box.get_rect()
        self.t_rect.centery = y

        self.text = self.font.render(txt,True,t_clr)
        self.textRect = self.text.get_rect()

        if width:
            if self.textRect[2] > width:
                self.m_lp = self.textRect[2]
            else:
                self.m_lp = width
        else:
            self.m_lp = self.textRect[2]
        self.loop = 0
        self.wait = 0
        self.wait_time = fps * wait
        self.spd = -4

        tile_sprites.sprites()[0].visual_sprites.append(self) 

    def update(self):
        if self.loop < self.m_lp:
            self.loop += 10
            if self.loop > self.m_lp:
                self.m_lp = self.loop
        elif self.wait < self.wait_time:
            self.wait += 1
        elif self.y > -self.t_rect[3]:
            self.y -= self.spd
            self.spd += 0.5
        else:
            tile_sprites.sprites()[0].visual_sprites.remove(self)
            del self

    def draw(self):
        rect = pygame.Rect((0,0,self.loop,self.t_rect[3]))
        rect.centerx = window_width/2
        rect.centery = self.y
        pygame.draw.rect(game_window,self.clr,rect)
        
        if self.loop < self.textRect[2]:
            text = pygame.Surface((self.loop,self.textRect[3]))
            text.fill(self.clr)
            text.blit(self.text,(0,0),(CorInt(self.textRect[2] - self.loop)/2,0,self.loop,self.textRect[3]))
            textRect = text.get_rect()
            textRect.center = rect.center
            game_window.blit(text,textRect)
        else:
            self.textRect.center = rect.center
            game_window.blit(self.text,self.textRect)

        for i in range(10):
            self.t_rect.centery = rect.centery
            self.t_rect.right = rect.left - 7 * i
            self.t_box.set_alpha((10 - i) * 25)
            game_window.blit(self.t_box,self.t_rect)
            self.t_rect.left = rect.right + 7 * i
            game_window.blit(self.t_box,self.t_rect)

class ChainCentralDisplay():
    def __init__(self,txt = ["Lorum Ipsum"],clr = [(70,110,255)],y = [100],width = [None],wait = [1]):
        self.font = title_font25

        self.txts = txt
        self.clrs = clr
        self.ys = y
        self.ws = width
        self.waits = wait

        self.count = -1

        self.Next()
        tile_sprites.sprites()[0].visual_sprites.append(self) 

    def Next(self):
        self.count += 1
        if self.count == len(self.txts):
            tile_sprites.sprites()[0].visual_sprites.remove(self)
            del self
            return

        h = self.font.size(self.txts[self.count])[1] + 10
        
        self.clr = self.clrs[self.count % len(self.clrs)]
        self.y = self.ys[self.count % len(self.ys)]
        
        self.t_box = pygame.Surface((7,h),pygame.SRCALPHA,32).convert_alpha()
        self.t_box.fill(self.clr)
        self.t_rect = self.t_box.get_rect()
        self.t_rect.centery = self.y

        self.text = self.font.render(self.txts[self.count],True,(255,255,255))
        self.textRect = self.text.get_rect()

        if self.ws[self.count % len(self.ws)]:
            if self.textRect[2] > self.ws[self.count % len(self.ws)]:
                self.m_lp = self.textRect[2]
            else:
                self.m_lp = self.ws[self.count % len(self.ws)]
        else:
            self.m_lp = self.textRect[2]
        self.loop = 0
        self.wait = self.waits[self.count % len(self.waits)]
        self.wait_time = fps * self.wait
        self.spd = -4

    def update(self):
        if self.loop < self.m_lp:
            self.loop += 10
            if self.loop > self.m_lp:
                self.m_lp = self.loop
        elif self.wait < self.wait_time:
            self.wait += 1
        elif self.y > -self.t_rect[3]:
            self.y -= self.spd
            self.spd += 0.5
        else:
            self.Next()

    def draw(self):
        rect = pygame.Rect((0,0,self.loop,self.t_rect[3]))
        rect.centerx = window_width/2
        rect.centery = self.y
        pygame.draw.rect(game_window,self.clr,rect)
        
        if self.loop < self.textRect[2]:
            text = pygame.Surface((self.loop,self.textRect[3]))
            text.fill(self.clr)
            text.blit(self.text,(0,0),(CorInt(self.textRect[2] - self.loop)/2,0,self.loop,self.textRect[3]))
            textRect = text.get_rect()
            textRect.center = rect.center
            game_window.blit(text,textRect)
        else:
            self.textRect.center = rect.center
            game_window.blit(self.text,self.textRect)

        for i in range(10):
            self.t_rect.centery = rect.centery
            self.t_rect.right = rect.left - 7 * i
            self.t_box.set_alpha((10 - i) * 25)
            game_window.blit(self.t_box,self.t_rect)
            self.t_rect.left = rect.right + 7 * i
            game_window.blit(self.t_box,self.t_rect)

class MoveDisplay():
    def __init__(self,txt = "Lorum Ipsum",clr = (70,110,255),y = 100):
        self.font = title_font25
        self.l = self.font.size(txt)[0] + 80
        h = self.font.size(txt)[1] + 10
        self.offx = self.l
        self.loop = 0
        self.clr = clr
        self.m_box = pygame.Surface((self.l - 50,h),pygame.SRCALPHA,32).convert_alpha()
        self.m_rect = self.m_box.get_rect()
        self.m_rect.centery = y
##        self.m_box.fill(clr)
        self.m_box.set_alpha(240)

        self.t_box = pygame.Surface((5,h),pygame.SRCALPHA,32).convert_alpha()
        self.t_rect = self.t_box.get_rect()
        self.t_rect.centery = y
##        self.t_box.fill(clr)

        self.text = self.font.render(txt,True,(255,255,255))
        self.textRect = self.text.get_rect()
        self.textRect.centery = y

        tile_sprites.sprites()[0].visual_sprites.append(self)

    def update(self):
        if self.offx > 0 and self.loop == 0:
            self.offx -= 8
            if self.offx < 0:
                self.offx = 0
            self.m_box.fill(Brighten(self.clr,self.offx*100/self.l))
            self.t_box.fill(Brighten(self.clr,self.offx*100/self.l))
        elif self.loop <= fps:
            self.loop += 1
        elif self.offx < self.l:
            self.offx += 5
        else:
            tile_sprites.sprites()[0].visual_sprites.remove(self)
            del self

    def draw(self):
        for i in range(10):
            self.t_rect.left = window_width - self.l + self.offx + 5 * i
            self.t_box.set_alpha(i * 25)
            game_window.blit(self.t_box,self.t_rect)
        self.m_rect.left = self.t_rect.right
        game_window.blit(self.m_box,self.m_rect)
        self.textRect.left = self.t_rect.right + 20
        game_window.blit(self.text,self.textRect)

class TurnDisplay():
    def __init__(self,txt = "Lorum Ipsum",clr = (70,110,255),y = window_height/2, d = 1):
        self.font = stat_font75
        self.d = d
        self.l = self.font.size(txt)[0] + 80 + 20 * 10
        h = self.font.size(txt)[1] + 50
        self.offx = self.l
        self.loop = 0
        self.m_box = pygame.Surface((self.l - 50,h),pygame.SRCALPHA,32).convert_alpha()
        self.m_rect = self.m_box.get_rect()
        self.m_rect.centery = y
        self.m_box.fill(clr)
        self.m_box.set_alpha(140)

        self.t_box = pygame.Surface((10,h),pygame.SRCALPHA,32).convert_alpha()
        self.t_rect = self.t_box.get_rect()
        self.t_rect.centery = y
        self.t_box.fill(clr)

        self.cd = 0

        self.text = self.font.render(txt,True,(255,255,255))
        self.textRect = self.text.get_rect()
        self.textRect.centery = y

        tile_sprites.sprites()[0].visual_sprites.append(self)

    def update(self):
        self.loop += 16
        if self.loop <= self.l:
            self.offx -= 16
        elif self.cd <= fps:
            self.cd += 1
            self.loop -= 16
        elif self.loop <= self.l * 2:
            self.offx += 20
        else:#if -self.l == self.loop:
            tile_sprites.sprites()[0].visual_sprites.remove(self)
            del self

    def draw(self):
        for i in range(20):
            if self.d == 1:
                self.t_rect.right = self.l - self.offx - 10 * i
            else:
                self.t_rect.left = window_width - self.l + self.offx + 10 * i
            self.t_box.set_alpha((i * 1) * 7)
            game_window.blit(self.t_box,self.t_rect)
        if self.d == 1:
            self.m_rect.right = self.t_rect.left
            self.textRect.right = self.t_rect.left - 40
        else:
            self.m_rect.left = self.t_rect.right
            self.textRect.left = self.t_rect.right + 40
        game_window.blit(self.m_box,self.m_rect)
        game_window.blit(self.text,self.textRect)

class SightLine():
    def __init__(self,original,unit,pt,clr = (255,255,255),marking = []):
        self.origin = original
        self.unit = unit
        self.pt = pt
        self.clr = clr
        self.m_clr = Brighten(clr,30)#(255,255,255)#Darken(clr,20)
        self.t_clr = Brighten(clr,60)
        self.origin.visual_sprites.append(self)

        self.w_lp = 0
        self.m_lp = 0
        #self.a_lp = 0
        self.marking = []
        self.moving = []
        #0: X, 1 8-Pt Star, 2: Square
        for i in marking:
            if i[0] == 0:
                m = 7
                w = 3
                s = m - w
                pts = [[i[1][0] - m,i[1][1] - s],[i[1][0] - m,i[1][1] - m],[i[1][0] - s,i[1][1] - m],[i[1][0],i[1][1] - w],
                       [i[1][0] + s,i[1][1] - m],[i[1][0] + m,i[1][1] - m],[i[1][0] + m,i[1][1] - s],[i[1][0] + w,i[1][1]],
                       [i[1][0] + m,i[1][1] + s],[i[1][0] + m,i[1][1] + m],[i[1][0] + s,i[1][1] + m],[i[1][0],i[1][1] + w],
                       [i[1][0] - s,i[1][1] + m],[i[1][0] - m,i[1][1] + m],[i[1][0] - m,i[1][1] + s],[i[1][0] - w,i[1][1]]]
                self.marking.append(pts)
            elif i[0] == 1:
                pts = []
                for j in range(4):
                    pts.append([i[1][0] + cos(radians(j * 90)) * 10,i[1][1] - sin(radians(j * 90)) * 10])
                self.marking.append(pts)
                pts = []
                for j in range(4):
                    pts.append([i[1][0] + cos(radians(j * 90 + 45)) * 9,i[1][1] - sin(radians(j * 90 + 45)) * 9])
                self.marking.append(pts)
            elif i[0] == 2:
                self.moving.append(i)

    def update(self):
        self.w_lp = (self.w_lp + 2)%180
        self.m_lp = (self.m_lp + 0.5)%19
        #self.a_lp = (self.a_lp + 0.5)%21

    def draw(self):
        if self.origin.v == 0:
            c = self.m_lp#sin(radians(self.m_lp)) * (self.origin.w)/2
            for i in self.moving:
                if i[0] == 2:
                    t = self.origin.tiles[i[2]][i[1]]
                    cx = (t.bl[0] + t.br[0])/2
                    cy = (t.bl[1] + t.tl[1])/2
                    pygame.draw.lines(game_window,self.m_clr,True,[[cx - c,cy - c],
                                                                   [cx + c,cy - c],
                                                                   [cx + c,cy + c],
                                                                   [cx - c,cy + c]],width = 1)
                    
                    #pygame.draw.lines(game_window,self.t_clr,True,t.t_pts,width = 3)
                    pygame.draw.lines(game_window,self.t_clr,True,[[t.bl[0] + 1,t.bl[1] - 1],
                                                                   [t.br[0] - 1,t.br[1] - 1],
                                                                   [t.tr[0] - 1,t.tr[1] + 1],
                                                                   [t.tl[0] + 1,t.tl[1] + 1],],width = 3)
            c = sin(radians(self.w_lp))
            cx,cy = self.unit.centerx, self.unit.centery 
            pygame.draw.circle(game_window,self.clr,[cx,cy],CorInt(c * 2 + 2))
            pygame.draw.circle(game_window,self.clr,self.pt,CorInt(c * 2 + 2))
            pygame.draw.line(game_window,self.clr,[cx,cy],self.pt,width = 3)

            #pygame.draw.circle(game_window,self.clr,[cx + (self.pt[0] - cx) * self.a_lp/20 ,cy + (self.pt[1] - cy) * self.a_lp/20],5)
            
            for i in self.marking:
                pygame.draw.polygon(game_window,self.m_clr,i)

class ImpactSpikes():
    def __init__(self,original,clr = (255,255,255),start = 0,ph = 30,sh = 20,spd = 3):
        self.origin = original
        self.loop = start
        self.clr = clr
        self.fm = tile_sprites.sprites()[0]
        self.ph = ph
        self.sh = sh
        self.spd = spd
        self.origin.visual_sprites.append(self)

    def update(self):
        self.loop += self.spd
        if self.loop >= 180:
            self.origin.visual_sprites.remove(self)#self.kill()
            del self
            return

    def draw_b(self):
        if self.loop < 0:
            return
        pts = [self.origin.tl]
        c = sin(radians(self.loop))
        w = (self.origin.br[0] - self.origin.bl[0])/5
        m = CorInt(w/2)
        for i in range(5):
            h = self.ph if i % 2 == 0 else self.sh
            pts.append([self.origin.tl[0] + w * i + m, self.origin.tl[1] - h * c])
            pts.append([self.origin.tl[0] + w * (i + 1), self.origin.tl[1]])
        pygame.draw.polygon(game_window,self.clr,pts)
        w = self.fm.h/10
        pygame.draw.lines(game_window,self.clr,False,[self.origin.bl,self.origin.tl,[self.origin.tl[0],self.origin.tl[1] + w - self.ph * c]])
        pygame.draw.lines(game_window,self.clr,False,[self.origin.br,self.origin.tr,[self.origin.tr[0],self.origin.tl[1] + w - self.ph * c]])

    def draw_f(self):
        if self.loop < 0:
            return
        pts = [self.origin.bl]
        c = sin(radians(self.loop))
        w = (self.origin.br[0] - self.origin.bl[0])/5
        m = CorInt(w/2)
        for i in range(5):
            h = self.ph if i % 2 == 0 else self.sh
            pts.append([self.origin.bl[0] + w * i + m, self.origin.bl[1] - h * c])
            pts.append([self.origin.bl[0] + w * (i + 1), self.origin.bl[1]])
        pygame.draw.polygon(game_window,self.clr,pts)   

class SquareCoil():
    def __init__(self,original,h = 50,clr = (255,255,255),start = 0,spd = 3):
        self.origin = original
        self.loop = start
        self.clr = clr
        self.l_clr = Brighten(clr,50)
        self.h = h
        self.fm = tile_sprites.sprites()[0]
        self.spd = spd
        self.origin.visual_sprites.append(self)

    def update(self):
        self.loop += self.spd
        if self.loop >= self.h:
            self.origin.visual_sprites.remove(self)#self.kill()
            del self
            return

    def draw_b(self):
        if self.loop < 0:
            return
        pts = [[self.origin.bl[0],self.origin.bl[1] - self.loop],
               [self.origin.tl[0],self.origin.tl[1] - self.loop],
               [self.origin.tr[0],self.origin.tr[1] - self.loop],
               [self.origin.br[0],self.origin.br[1] - self.loop]]
        pygame.draw.lines(game_window,self.clr,False,pts,width = 3)
        pygame.draw.lines(game_window,self.l_clr,False,pts,width = 1)
        

    def draw_f(self):
        if self.loop < 0:
            return
        pts = [[self.origin.bl[0],self.origin.bl[1] - self.loop],[self.origin.br[0],self.origin.br[1] - self.loop]]
        pygame.draw.lines(game_window,self.clr,False,pts,width = 3)
        pygame.draw.lines(game_window,self.l_clr,False,pts,width = 1)

class ShockBurst():
    def __init__(self,original,start = 0, d = None, l = 20, w = 7, ox = None, oy = None,follow = True):
        self.origin = original
        self.loop = start
        self.fm = tile_sprites.sprites()[0]
        if ox != None:
            self.ox = ox
        else:
            self.ox = - 15 + randint(0,30)
        if oy != None:
            self.oy = oy
        else:
            self.oy = randint(0,10)
        self.l = l
        self.pts = [[0,0]]
        if d:
            self.d = d
        else:
            self.d = randint(45,135)
        self.w = w
        self.follow = follow
        self.ocx,self.ocy = self.origin.centerx,self.origin.centery
        self.origin.visual_sprites.append(self)

    def update(self):
        if self.loop % 3 == 0 and self.loop >= 0:
            if len(self.pts) < self.w: 
                self.pts.append([cos(radians(self.d)) * self.l * len(self.pts) - 10 + randint(0,20),
                                 sin(radians(self.d)) * self.l * len(self.pts) - 10 + randint(0,20)])
            elif self.w > 0:
                self.w -= 1
        if self.w == 0:
            self.origin.visual_sprites.remove(self)#self.kill()
            del self
            return
        self.loop += 1
        if self.follow:
            self.ocx,self.ocy = self.origin.centerx,self.origin.centery

    def draw_b(self):
        pass

    def draw_f(self):
        if len(self.pts) > 1:
            for i in range(len(self.pts) - 2):
                if len(self.pts) - i - 1 < self.w:
                    pygame.draw.line(game_window,(144,196,244),
                                     [self.ocx + self.ox + self.pts[i][0],self.ocy + self.oy - self.pts[i][1]],
                                     [self.ocx + self.ox + self.pts[i+1][0],self.ocy + self.oy - self.pts[i+1][1]],
                                     width = len(self.pts) - i + 1)
                else:
                    pygame.draw.line(game_window,(144,196,244),
                                     [self.ocx + self.ox + self.pts[i][0],self.ocy + self.oy - self.pts[i][1]],
                                     [self.ocx + self.ox + self.pts[i+1][0],self.ocy + self.oy - self.pts[i+1][1]],
                                     width = self.w)
            for i in range(len(self.pts) - 2):
                if len(self.pts) - i - 1 < self.w:
                    pygame.draw.line(game_window,(255,255,255),
                                     [self.ocx + self.ox + self.pts[i][0],self.ocy + self.oy - self.pts[i][1]],
                                     [self.ocx + self.ox + self.pts[i+1][0],self.ocy + self.oy - self.pts[i+1][1]],
                                     width = len(self.pts) - i - 1)
                else:
                    pygame.draw.line(game_window,(255,255,255),
                                     [self.ocx + self.ox + self.pts[i][0],self.ocy + self.oy - self.pts[i][1]],
                                     [self.ocx + self.ox + self.pts[i+1][0],self.ocy + self.oy - self.pts[i+1][1]],
                                     width = self.w)

    def draw(self):
        self.draw_f()

class Chip():
    def __init__(self,original,colour,vx = None,vy = None,offx = None,offy = None):
        self.fm = tile_sprites.sprites()[0]
        
        self.origin = original
        self.size = randint(5,10)
        self.rect = pygame.Rect(0,0,self.size,self.size)
        if offx == None:
            self.x = self.origin.bl[0] + randint(0,int(self.fm.h)+10)
        else:
            self.x = self.origin.bl[0] + offx
        if offy == None:
            self.y = self.origin.bl[1] - randint(0,int(self.fm.h)+10)
        else:
            self.y = self.origin.bl[1] + offy
        if vx == None:
            self.vx = randint(1,2) * GenPN()
        else:
            self.vx = vx
        if vy == None:
            self.vy = randint(1,3)
        else:
            self.vy = vy
        self.ry = 0
        self.rect.centerx = self.x
        self.rect.centery = self.y
        self.colour = colour
        self.loop = 0

        self.fm.visual_sprites.append(self)

    def update(self):
        if self.loop >= 30:
            self.fm.visual_sprites.remove(self)
            del self

    def draw(self):
        a = RoundUp(self.size*(30-self.loop)/30)
        self.loop += 1
        self.rect.centerx = self.x + self.vx * self.loop
        self.rect.centery = self.y + self.ry
        self.ry -= self.vy
        self.vy -= 0.25
        pygame.draw.circle(game_window,self.colour,self.rect.center,a)

class RingBurst():
    def __init__(self,origin,x,y,clr,r,spd = 1,delay = 0):
        self.origin = origin
        self.x = x
        self.y = y
        self.clr = clr
        self.r = r
        self.w = 3
        self.spd = spd
        self.loop = delay
        self.origin.visual_sprites.append(self)

    def update(self):
        if self.loop < 0:
            self.loop += 1
        else:
            self.loop += self.spd
            if self.loop > 90:
                self.loop = 90
            self.w = RoundUp(3 * cos(radians(self.loop)))
            if self.loop == 90:
                self.origin.visual_sprites.remove(self)

    def draw(self):
        if self.w > 0 and self.loop >= 0:
            pygame.draw.circle(game_window,self.clr,[self.x,self.y],self.r * self.loop/90,width = self.w)

class StarBurst():
    def __init__(self,origin,x,y,clr,d,dis = 3,spd = 2,r = None):
        self.origin = origin
        self.x = x
        self.y = y
        if r:
            self.r = r
        else:
            self.r = randint(10,15)
        self.loop = 90
        self.dx = dis * cos(radians(d))
        self.dy = -dis * sin(radians(d))
        self.d = randint(0,360)
        self.spd = spd
        self.clr = clr
        self.origin.visual_sprites.append(self)

    def update(self):
        self.d += 1
        self.x += self.dx * sin(radians(self.loop))
        self.y += self.dy * sin(radians(self.loop))
        self.loop -= self.spd
        if self.loop == 0:
            self.origin.visual_sprites.remove(self)

    def draw(self):
        pts = []
        for i in range(5):
            pts.append([self.x + cos(radians(self.d + i * 72)) * self.r * sin(radians(self.loop)),self.y - sin(radians(self.d + i * 72)) * self.r * sin(radians(self.loop))])
            pts.append([self.x + cos(radians(self.d + i * 72 + 36)) * self.r * 1.5 * sin(radians(self.loop)),self.y - sin(radians(self.d + i * 72 + 36)) * self.r * 1.5 * sin(radians(self.loop))])
        pygame.draw.polygon(game_window,self.clr,pts)

    def draw_b(self):
        pass

    def draw_f(self):
        self.draw()

class CircleBurst():
    def __init__(self,origin,x,y,clr,d,dis = 3,spd = 2):
        self.origin = origin
        self.x = x
        self.y = y
        if r:
            self.r = r
        else:
            self.r = randint(10,15)
        self.loop = 90
        self.dx = dis * cos(radians(d))
        self.dy = -dis * sin(radians(d))
        self.spd = spd
        self.clr = clr
        self.origin.visual_sprites.append(self)

    def update(self):
        self.x += self.dx * sin(radians(self.loop))
        self.y += self.dy * sin(radians(self.loop))
        self.loop -= self.spd
        if self.loop == 0:
            self.origin.visual_sprites.remove(self)

    def draw(self):
        pygame.draw.circle(game_window,self.clr,[self.x,self.y],self.r * sin(radians(self.loop)))

    def draw_b(self):
        pass

    def draw_f(self):
        self.draw()

class MagicShockwave():
    def __init__(self,origin,x,y,r,clr = (174,98,255),spd = 2,a = 175,sparkle = True,delay = 0):
        self.origin = origin
        self.clr = clr
        self.r = r
        #self.w = 3
        self.spd = spd
        self.loop = delay
        self.origin.visual_sprites.append(self)
        self.a = a
        self.sparkle = sparkle
        
        self.surface = pygame.Surface((r * 2,r * 2))
        self.rect = self.surface.get_rect()
        self.rect.center = x,y
        self.surface.set_colorkey((0,0,0))
        self.surface.set_alpha(self.a)

    def update(self):
        self.loop += self.spd
        if self.sparkle:
            for i in range(3):
                d = randint(0,360)
                StarTrail(self.origin,self.rect.centerx + cos(radians(d)) * self.r * (self.loop - i)/90,self.rect.centery - sin(radians(d)) * self.r * (self.loop - i)/90, randint(5,10), GetMagicClr(),spd = 0.5)
        if self.loop >= 90:
            self.origin.visual_sprites.remove(self)

    def draw(self):
        if self.loop >= 0:
            self.surface.fill((0,0,0))
            pygame.draw.circle(self.surface,self.clr,[self.r,self.r],self.r * self.loop/90,width = 5)
            if self.loop >= 65:
                self.surface.set_alpha(self.a*(90-self.loop)/25)
            game_window.blit(self.surface,self.rect)

class FireShockwave():
    def __init__(self,origin,x,y,r,spd = 2.5):
        self.origin = origin
        self.x = x
        self.y = y
        self.w = 3
        self.spd = spd
        self.loop = 0
        self.origin.visual_sprites.append(self)

        self.r = r

    def update(self):
        self.loop += self.spd
        a = int(self.r * self.loop * 0.25/90)
        for i in range(a):
            d = i * 360/a + randint(0,10)
            DropTrail(self.origin,self.x + cos(radians(d)) * self.r * self.loop/90,self.y - sin(radians(d)) * self.r * self.loop/90, randint(10,15), GetBurnClr(),spd = 0.5)
        if self.loop >= 90:
            self.origin.visual_sprites.remove(self)

    def draw(self):
        pass

class ElectricShockwave():
    def __init__(self,origin,x,y,r,spd = 2):
        self.origin = origin
        self.x = x
        self.y = y
        self.w = 3
        self.spd = spd
        self.loop = 0
        self.lp = 0
        self.origin.visual_sprites.append(self)

        self.r = r

        self.surface = pygame.Surface((r * 2 + 8,r * 2 + 8))
        self.rect = self.surface.get_rect()
        self.rect.center = x,y
        self.surface.set_colorkey((0,0,0))
        self.surface.set_alpha(250)
        self.pts = [[],[],[]]
        self.clrs = [(255,247,0),(210,155,255),(0,228,255)]

    def update(self):
        self.loop += self.spd
        if self.lp == 0:
            self.pts = [[],[],[]]
            for j in range(3):
                for i in range(18):
                    self.pts[j].append([randint(2,6) * GenPN(),randint(2,6) * GenPN()])
        self.lp = (self.lp + 1)%2
        self.surface.fill((0,0,0))
        for j in range(3):
            pts = []
            for i in range(18):
                pts.append([self.r + 4 + cos(radians(i * 20)) * self.r * self.loop/90 + self.pts[j][i][0],
                            self.r + 4 - sin(radians(i * 20)) * self.r * self.loop/90 + self.pts[j][i][1]])
            pygame.draw.lines(self.surface,self.clrs[j],True,pts,width = 3)
            pygame.draw.lines(self.surface,(255,255,255),True,pts,width = 1)
        if self.loop >= 65:
            self.surface.set_alpha((90-self.loop)*10)
        if self.loop >= 90:
            self.origin.visual_sprites.remove(self)

    def draw(self):
        game_window.blit(self.surface,self.rect)
            
class LiquidShockwave():
    def __init__(self,origin,x,y,r,clr = (135,165,255),spd = 2):
        self.origin = origin
        self.clr = clr
        self.r = r
        self.spd = spd
        self.loop = 0
        self.origin.visual_sprites.append(self)
        
        self.surface = pygame.Surface((r * 2.1,r * 2.1))
        self.rect = self.surface.get_rect()
        self.rect.center = x,y
        self.surface.set_colorkey((0,0,0))
        self.surface.set_alpha(150)

        self.sr = r * 0.05
        self.cr = r + self.sr

    def update(self):
        self.loop += self.spd
        if self.loop >= 90:
            self.origin.visual_sprites.remove(self)

    def draw(self):
        c = sin(radians(self.loop))
        self.surface.fill((0,0,0))
        pts = []
        for i in range(60):
            r = (self.r + self.sr * sin(radians(i * 60)) * sin(radians(self.loop)) ) * c
            pts.append([self.cr + cos(radians(i * 6)) * r,self.cr - sin(radians(i * 6)) * r])
        pygame.draw.polygon(self.surface,self.clr,pts)
        pygame.draw.lines(self.surface,(255,255,255),True,pts,width = 2)
        pygame.draw.circle(self.surface,(0,0,0),[self.cr,self.cr],(self.r * 0.85) * c)
        if self.loop >= 60:
            self.surface.set_alpha((90-self.loop)*5)            
        game_window.blit(self.surface,self.rect)

def SetMagicShockwave(x,y,effect = None,r = 2):
    fm = tile_sprites.sprites()[0]
    if effect in ["Burn"]:
        FireShockwave(fm,x,y,fm.w * (r + 0.5))
    elif effect in ["Shock"]:
        ElectricShockwave(fm,x,y,fm.w * (r + 0.5))   
    elif effect in ["Splash","Poison"]:
        LiquidShockwave(fm,x,y,fm.w * (r + 0.5),clr = SE_colour_set.get(effect))
    elif effect in ["Drain"]:
        for i in range(3):
            for j in range(5):
                MagicSpiral(fm,x,y,j * 72 + randint(0,20),colour = GetDrainClr(),spd = 3,s_range = fm.w * (r + 0.5) + randint(0,5),start = 10,delay = i * -2 - randint(0,2))
    else:
        MagicShockwave(fm,x,y,fm.w * (r + 0.5),(174,98,255))
        for i in range(1,7):
            MagicShockwave(fm,x,y,fm.w * (r + 0.5),GradientClrs((174,98,255),(98,218,255),1-i/6,i/6),a = 175 - i * 25,delay = -2 * i,sparkle = False)

def SetMagicBurst(x,y,effect = None,r = 2):
    fm = tile_sprites.sprites()[0]
    if effect in ["Burn","Poison","Blind","Corruption"]:
        for j in range(7):
            Explosion(fm.tiles[y][x],randint(r * 10,r * 15),j * 30,GetEffectClr(effect),dark = 50,spd = r * randint(1,2)/2,grow = randint(2,4),start = randint(1,5))
    elif effect in ["Splash","Drain"]:
        for j in range(7):
            Explosion(fm.tiles[y][x],randint(r * 10,r * 15),j * 30,GetEffectClr(effect),bright = 35,spd = r * randint(1,2)/2,grow = randint(2,4),start = randint(1,5))
    elif effect in ["Freeze"]:
        for j in range(7):
            Explosion(fm.tiles[y][x],randint(r * 10,r * 15),j * 30,GetEffectClr(effect),bright = 35,spd = r * randint(1,2)/2,grow = randint(2,4),start = randint(1,5))
    elif effect in ["Shock"]:
        for j in range(3):
            ShockBurst(fm.tiles[y][x],start = -randint(0,4) * 2, l = 10, d = (j + 1)*36)
    else:
        for j in range(7):
            Explosion(fm.tiles[y][x],randint(r * 10,r * 15),j * 30,GetMagicClr(),bright = 35,spd = r * randint(1,2)/2,grow = randint(2,4),start = randint(1,5))

def SetMagicSplash(unit,d = 0,effect = None):
    if effect in ["Burn","Poison","Blind"]:
        for j in range(11):
            Explosion(unit,randint(15,25),d + (j - 5) * 5,GetEffectClr(effect),dark = 50,spd = randint(2,3),grow = randint(15,20)/10,start = randint(1,10),a = 120)
        Explosion(unit,randint(15,25),d - 70,GetEffectClr(effect),dark = 50,spd = randint(1,3),grow = randint(15,20)/10,start = randint(1,10),a = 120)
        Explosion(unit,randint(15,25),d + 70,GetEffectClr(effect),dark = 50,spd = randint(1,3),grow = randint(15,20)/10,start = randint(1,10),a = 120)
    elif effect in ["Splash","Drain","Ether"]:
        for j in range(11):
            Explosion(unit,randint(15,25),d + (j - 5) * 5,GetEffectClr(effect),spd = randint(2,3),grow = randint(15,20)/10,start = randint(1,10),a = 120)
        Explosion(unit,randint(15,25),d - 70,GetEffectClr(effect),bright = 35,spd = randint(1,3),grow = randint(15,20)/10,start = randint(1,10),a = 120)
        Explosion(unit,randint(15,25),d + 70,GetEffectClr(effect),bright = 35,spd = randint(1,3),grow = randint(15,20)/10,start = randint(1,10),a = 120)
    elif effect in ["Freeze"]:
        for j in range(11):
            CrystalShard(unit, d = d + (j - 5) * 5,spd = randint(4,6), clr = GetFreezeClr())
            if j % 2 == 0:
                BurstTrail(unit, d = d + (j - 5) * 5,spd = randint(4,6), clr = GetFreezeClr())
        CrystalShard(unit, d = d - 70,spd = randint(4,6), clr = GetFreezeClr())
        CrystalShard(unit, d = d + 70,spd = randint(4,6), clr = GetFreezeClr())
    elif effect in ["Shock"]:
        for j in range(5):
            ShockBurst(unit,start = -randint(0,4) * 2, l = 20, d = d + (j - 2) * 8,follow = False)
        ShockBurst(unit,start = -randint(0,4) * 2, l = 10, d = d - 70,follow = False)
        ShockBurst(unit,start = -randint(0,4) * 2, l = 10, d = d + 70,follow = False)
    else:
        for j in range(11):
            #Explosion(unit,randint(15,25),d + (j - 5) * 5,GetEffectClr(effect),spd = randint(3,4),grow = randint(15,20)/10,start = randint(1,10),a = 120)
            Stardust(unit, d = d + (j - 5) * 5,spd = randint(4,6), clr = GetMagicClr())
        Explosion(unit,randint(15,25),d - 70,GetEffectClr(effect),bright = 35,spd = randint(1,3),grow = randint(15,20)/10,start = randint(1,10),a = 120)
        Explosion(unit,randint(15,25),d + 70,GetEffectClr(effect),bright = 35,spd = randint(1,3),grow = randint(15,20)/10,start = randint(1,10),a = 120)

def SetChargeBurst(unit,effect):
    fm = tile_sprites.sprites()[0]
    t = fm.tiles[unit.y][unit.x]
    if effect in ["Burn","Drain"]:
        for i in range(6):
            MagicSwirl(unit,i * 60,h = randint(40,80),colour = GetEffectClr(effect),w = 15,grow = randint(2,3)/10,l = randint(10,30),slant = randint(1,3)/10)
    elif effect in ["Splash","Poison","Blind","Ether"]:
        for i in range(6):
            BubbleSwirl(unit,5,i * 60,GetEffectClr(effect),max_h = int(unit.rect[3] * 0.75),grow = 2,spd = 0.4,charge_swirl = 20)
    elif effect in ["Freeze"]:
        for j in range(5):
            CrystalShard(t, d = 90 + (j - 2) * 30,spd = randint(2,3), clr = GetFreezeClr(),min_s = 10,max_s = 15)
        for j in range(7):
            BurstTrail(t, d = 90 - (j - 3) * 2,spd = randint(3,4), clr = GetFreezeClr(),offx = (j - 3) * 3,offy = randint(0,8),w = randint(2,4),h = randint(5,10))
    elif effect in ["Shock"]:
        for j in range(3):
            ShockBurst(t,start = -randint(0,4) * 2, l = 15, d = 90 + (j - 1) * 20,ox = (j - 1) * 5,oy = 18)
    else:
        for j in range(11):
            #Explosion(unit,randint(15,25),d + (j - 5) * 5,GetEffectClr(effect),spd = randint(3,4),grow = randint(15,20)/10,start = randint(1,10),a = 120)
            Stardust(unit, d = 90 + (j - 5) * 5,spd = randint(4,6), clr = GetMagicClr())
        Explosion(unit,randint(15,25),20,GetMagicClr(),bright = 35,spd = randint(1,3),grow = randint(15,20)/10,start = randint(1,10),a = 120)
        Explosion(unit,randint(15,25),160,GetMagicClr(),bright = 35,spd = randint(1,3),grow = randint(15,20)/10,start = randint(1,10),a = 120)

class HitSpark():
    def __init__(self,origin,x,y,clr = (255,255,255)):
        self.origin = origin
        self.x = x
        self.y = y
        self.loop = 0
        self.d = randint(1,360)

        self.clr = clr
        self.origin.visual_sprites.append(self)

    def update(self):
        self.loop += 8
        if self.loop >= 90:
            self.origin.visual_sprites.remove(self)
            del self

    def draw(self):
        c = cos(radians(self.loop))
        s = sin(radians(self.loop))
        pts = []
        w1 = 8 * c
        w2 = 10 + s * 5
        for i in range(6):
            pts.append([self.x + cos(radians(self.d + i * 60)) * w1,self.y - sin(radians(self.d + i * 60)) * w1])
            pts.append([self.x + cos(radians(self.d + i * 60 + 30)) * w2,self.y - sin(radians(self.d + i * 60 + 30)) * w2])
        pygame.draw.polygon(game_window,self.clr,pts)
        pygame.draw.circle(game_window,self.clr,[self.x,self.y],20 * s,width = RoundUp(3 * c))

class BubbleSwirl():
    def __init__(self,origin,r,d,clr,max_h = 50,grow = 1,spd = 0.2,charge_swirl = 0):
        self.origin = origin
        self.x = self.origin.rect.centerx
        self.y = self.origin.rect.bottom
        self.offy = 0
        self.r = r
        self.d = d
        self.max_h = max_h
        self.w = 10
        self.spd = spd
        self.grow = grow

        self.clr = clr

        self.d_lp = 0

        self.loop = 0
        self.lp = charge_swirl

        self.b_pts,self.f_pts = [],[]
        
        self.origin.visual_sprites.append(self)

    def update(self):
        if self.lp == 0:
            if self.loop >= 90:
                self.loop += self.grow#1
                self.r -= 0.5
                self.d = (self.d + 5)%360
            else:
                self.loop += self.grow
                self.w += self.spd
                self.d = (self.d + 5)%360

            self.offy = self.max_h * self.loop/90

            self.b_pts,self.f_pts = [],[]
            for i in range(int(self.r * 2)):
                if self.loop - i * 5 > 0:
                    d = self.d - 5 * (i + 1)
                    y = self.max_h * (self.loop - i * 5)/90
                    if 0 <= d < 180:
                        self.b_pts.append([[self.x + cos(radians(d)) * self.w,self.y - y - sin(radians(d)) * 5],self.r - i/2])
                    else:
                        self.f_pts.append([[self.x + cos(radians(d)) * self.w,self.y - y - sin(radians(d)) * 5],self.r - i/2])


            if self.loop >= 90 and self.r == 0:
                self.origin.visual_sprites.remove(self)
                del self
        else:
            self.lp -= 1
            self.b_pts,self.f_pts = [],[]
            self.d = (self.d + 5)%360
            self.w += self.spd
            if 0 <= self.d < 180:
                self.b_pts.append([[self.x + cos(radians(self.d)) * self.w,self.y - self.offy - sin(radians(self.d)) * 5],self.r])
            else:
                self.f_pts.append([[self.x + cos(radians(self.d)) * self.w,self.y - self.offy - sin(radians(self.d)) * 5],self.r])

    def draw_b(self):
        for i in self.b_pts:
            pygame.draw.circle(game_window,self.clr,i[0],i[1])
            
    def draw_f(self):
        for i in self.f_pts:
            pygame.draw.circle(game_window,self.clr,i[0],i[1])

##    def draw_b(self):
##        if 0 <= self.d < 180:
##            pygame.draw.circle(game_window,self.clr,[self.x + cos(radians(self.d)) * self.w,self.y - self.offy - sin(radians(self.d)) * 5],self.r)
##            
##    def draw_f(self):
##        if 180 <= self.d < 360:
##            pygame.draw.circle(game_window,self.clr,[self.x + cos(radians(self.d)) * self.w,self.y - self.offy - sin(radians(self.d)) * 5],self.r)

class Explosion():
    def __init__(self,origin,s,d,clr,dark = 0,bright = 0,spd = 3,grow = 3,start = 0,a = 240,x = None,y = None):
        self.origin = origin
        self.loop = start
        self.s = s
        self.offx = cos(radians(d)) * spd
        self.offy = -sin(radians(d)) * spd
        if x:
            self.ox = x
        else:
            self.ox = self.origin.centerx
        if y:
            self.oy = y
        else:
            self.oy = self.origin.centery
        
        self.clr = clr
        self.t_clr = clr
        self.td = dark
        self.d = 0
        self.tb = bright
        self.b = 0
        self.a = a
        
        self.spd = spd
        self.grow = grow
        
        self.rect = pygame.Rect(0,0,s,s)
        self.rect.centerx = self.ox + self.offx * self.loop
        self.rect.centery = self.oy + self.offy * self.loop
        
        self.origin.visual_sprites.append(self)

    def update(self):
        if self.a > 120:
            self.rect = pygame.Rect(0,0,self.s,self.s)
            self.rect.centerx = self.ox + self.offx * self.loop
            self.rect.centery = self.oy + self.offy * self.loop
            
            self.s += self.grow
            self.a -= 10
            self.loop += 1
            
        elif self.s > 0:
            self.rect = pygame.Rect(0,0,self.s,self.s)
            self.rect.centerx = self.ox + self.offx * self.loop
            self.rect.centery = self.oy + self.offy * self.loop

            self.s -= self.grow
            self.a -= 10
            self.loop += 1.5

        if self.d > 0:
            self.t_clr = Darken(self.clr,self.d)
        elif self.b > 0:
            self.t_clr = Brighten(self.clr,self.b)
        if self.d < self.td and self.a > 0:
            self.d = self.td * (1 - self.a/240)
        elif self.b < self.tb and self.a > 0:
            self.b = self.tb * (1 - self.a/240)
        if self.s <= 0:
            self.origin.visual_sprites.remove(self)
            del self

    def draw(self):
        self.draw_f()

    def draw_b(self):
        pass

    def draw_f(self):
        pygame.draw.circle(game_window,self.t_clr,self.rect.center,self.rect[2]/2)

class CrystalShard():
    def __init__(self,origin,spd = 5,d = 0, clr = (255,255,255),min_s = 10,max_s = 15):
        self.origin = origin
        self.ox = self.origin.centerx
        self.oy = self.origin.centery

        self.offx = cos(radians(d)) * spd
        self.offy = -sin(radians(d)) * spd
        self.centerx,self.centery = self.ox,self.oy
        
        self.d = d
        
        self.ls = []
        for i in range(3):
            self.ls.append(randint(min_s,max_s))
        self.loop = 0
        self.d_lp = 0

        self.clr = clr
        
        self.origin.visual_sprites.append(self)

    def update(self):
        self.loop += 1
        self.d_lp += 5
        self.centerx = self.ox + self.offx * self.loop
        self.centery = self.oy + self.offy * self.loop
        if self.d_lp == 90:
            self.origin.visual_sprites.remove(self)
            del self
        
    def draw(self):
        self.draw_f()

    def draw_b(self):
        pass

    def draw_f(self):
        pts = []
        c = cos(radians(self.d_lp))
        for i in range(3):
            pts.append([self.centerx + cos(radians(self.d + i * 120)) * self.ls[i] * c,self.centery - sin(radians(self.d + i * 120)) * self.ls[i] * c])
        pygame.draw.polygon(game_window,self.clr,pts)

class Stardust():
    def __init__(self,origin,spd = 5,d = 0, clr = (255,255,255)):
        self.origin = origin
        self.ox = self.origin.centerx
        self.oy = self.origin.centery

        self.offx = cos(radians(d)) * spd
        self.offy = -sin(radians(d)) * spd
        self.centerx,self.centery = self.ox,self.oy
        
        self.d = d
        
        self.loop = 0
        self.d_lp = 0

        self.clr = clr
        
        self.origin.visual_sprites.append(self)

    def update(self):
        self.loop += 1
        self.d_lp += 5
        self.centerx = self.ox + self.offx * self.loop
        self.centery = self.oy + self.offy * self.loop
        if self.d_lp >= 90:
            self.origin.visual_sprites.remove(self)
            del self
        
    def draw(self):
        self.draw_f()

    def draw_b(self):
        pass

    def draw_f(self):
        pts = []
        c = cos(radians(self.d_lp))
        s = sin(radians(self.d_lp)) * 3
        DrawStar(self.centerx,self.centery,(8 + s) * c,6 * c,self.d,self.clr)
##        for i in range(4):
##            pts.append([self.centerx + cos(radians(self.d + i * 90)) * (8 + s) * c,self.centery - sin(radians(self.d + i * 90)) * (8 + s) * c])
##            pts.append([self.centerx + cos(radians(self.d + i * 90 + 45)) * 6 * c,self.centery - sin(radians(self.d + i * 90 + 45)) * 6 * c])
##        pygame.draw.polygon(game_window,self.clr,pts)

class BurstTrail():
    def __init__(self,origin,spd = 5,d = 0, clr = (255,255,255), base = 0, w = 6, h = 10,x = None,y = None,offx = 0,offy = 0):
        self.origin = origin
        if x:
            self.ox = x + offx
        else:
            self.ox = self.origin.centerx + offx
        if y:
            self.oy = y + offy
        else:
            self.oy = self.origin.centery + offy

        self.offx = cos(radians(d)) * spd
        self.offy = -sin(radians(d)) * spd
        self.centerx,self.centery = self.ox,self.oy
        
        self.d = d
        
        self.loop = base
        self.d_lp = 0

        self.clr = clr

        self.w = w
        self.h = h
        
        self.origin.visual_sprites.append(self)

    def update(self):
        self.loop += 1
        if self.loop >= 0:
            self.d_lp += 5
        self.centerx = self.ox + self.offx * self.loop
        self.centery = self.oy + self.offy * self.loop
        if self.d_lp >= 90:
            self.origin.visual_sprites.remove(self)
            del self
        
    def draw(self):
        self.draw_f()

    def draw_b(self):
        pass

    def draw_f(self):
        if self.loop >= 0:
            c = cos(radians(self.d_lp))
            s = sin(radians(self.d_lp)) * 10
            pts = [[self.centerx + cos(radians(self.d)) * (self.h + s),self.centery - sin(radians(self.d)) * (self.h + s)],
                   [self.centerx + cos(radians(self.d + 90)) * self.w * c,self.centery - sin(radians(self.d + 90)) * self.w * c],
                   [self.centerx + cos(radians(self.d + 180)) * (self.h + s),self.centery - sin(radians(self.d + 180)) * (self.h + s)],
                   [self.centerx + cos(radians(self.d + 270)) * self.w * c,self.centery - sin(radians(self.d + 270)) * self.w * c]]

            pygame.draw.polygon(game_window,self.clr,pts)

class DropTrail():
    def __init__(self,origin,x,y,r,clr,bright = 0,spd = 1):
        self.origin = origin
        self.x = x
        self.y = y
        self.r = r
        self.clr = clr
        self.b = bright
        self.spd = spd
        self.origin.visual_sprites.append(self)

    def update(self):
        self.r -= self.spd
        if self.b > 0:
            self.b -= 2
        if self.r <= 0:
            self.origin.visual_sprites.remove(self)
            del self

    def draw(self):
        if self.b > 0:
            pygame.draw.circle(game_window,Brighten(self.clr,self.b),[self.x,self.y],self.r)
        else:
            pygame.draw.circle(game_window,self.clr,[self.x,self.y],self.r)

    def draw_b(self):
        self.draw()

    def draw_f(self):
        pass

class LightTrail():
    def __init__(self,origin,x,y,r,clr,bright = 0,spd = 1):
        self.origin = origin
        self.x = x
        self.y = y
        self.r = r
        self.clr = clr
        self.b = bright
        self.spd = spd
        self.origin.visual_sprites.append(self)

    def update(self):
        self.r -= self.spd
        if self.b < 100:
            self.b += 4
            if self.b > 100:
                self.b = 100
        if self.r <= 0:
            self.origin.visual_sprites.remove(self)
            del self

    def draw(self):
        pygame.draw.circle(game_window,Brighten(self.clr,self.b),[self.x,self.y],self.r)

    def draw_b(self):
        self.draw()

    def draw_f(self):
        pass

class DarkTrail():
    def __init__(self,origin,x,y,r,clr,dark = 0,spd = 1):
        self.origin = origin
        self.x = x
        self.y = y
        self.r = r
        self.clr = clr
        self.d = dark
        self.spd = spd
        self.origin.visual_sprites.append(self)

    def update(self):
        self.r -= self.spd
        if self.d < 100:
            self.d += 4
            if self.d > 100:
                self.d = 100
        if self.r <= 0:
            self.origin.visual_sprites.remove(self)
            del self

    def draw(self):
        pygame.draw.circle(game_window,Darken(self.clr,self.d),[self.x,self.y],self.r)

    def draw_b(self):
        self.draw()

    def draw_f(self):
        pass

class MagicTrail():
    def __init__(self,origin,x,y,r,lp,bright = 150,spd = 1):
        self.origin = origin
        self.x = x
        self.y = y
        self.r = r
        self.lp = lp
        self.b = bright
        self.spd = spd
        self.origin.visual_sprites.append(self)

    def update(self):
        self.r -= self.spd
        self.lp = (self.lp - 20)%1530
        if self.b > 150:
            self.b -= 2
        if self.r <= 0:
            self.origin.visual_sprites.remove(self)
            del self

    def draw(self):
        pygame.draw.circle(game_window,Get_RClr(self.lp,self.b),[self.x,self.y],self.r)

    def draw_b(self):
        pygame.draw.circle(game_window,Get_RClr(self.lp,self.b),[self.x,self.y],self.r)

    def draw_f(self):
        pass

class CrystalTrail():
    def __init__(self,origin,x,y,r,clr,bright = 0,spd = 1):
        self.origin = origin
        self.x = x
        self.y = y
        self.r = r
        self.clr = clr
        self.b = bright
        self.spd = spd
        self.d = randint(1,360)
        self.origin.visual_sprites.append(self)

    def update(self):
        self.d = (self.d + 1)%360
        self.r -= self.spd
        if self.b > 0:
            self.b -= 2
        if self.r <= 0:
            self.origin.visual_sprites.remove(self)
            del self

    def draw(self):
        pts = []
        for i in range(4):
            pts.append([self.x + cos(radians(self.d + i * 90)) * self.r,
                        self.y - sin(radians(self.d + i * 90)) * self.r])
        if self.b > 0:
            pygame.draw.polygon(game_window,Brighten(self.clr,self.b),[self.x,self.y],pts)
        else:
            pygame.draw.polygon(game_window,self.clr,pts)

    def draw_b(self):
        pts = []
        for i in range(4):
            pts.append([self.x + cos(radians(self.d + i * 90)) * self.r,
                        self.y - sin(radians(self.d + i * 90)) * self.r])
        if self.b > 0:
            pygame.draw.polygon(game_window,Brighten(self.clr,self.b),[self.x,self.y],pts)
        else:
            pygame.draw.polygon(game_window,self.clr,pts)

    def draw_f(self):
        pass

class SnowflakeTrail():
    def __init__(self,origin,x,y,r,clr,spd = 1):
        self.origin = origin
        self.x = x
        self.y = y
        self.r = r
        self.clr = clr
        self.spd = spd
        self.d = randint(1,360)
        self.origin.visual_sprites.append(self)

    def update(self):
        self.d = (self.d + 1)%360
        self.r -= self.spd
        if self.r <= 0:
            self.origin.visual_sprites.remove(self)
            del self

    def draw(self):
        for i in range(3):
            pygame.draw.line(game_window,self.clr,
                             [self.x + cos(radians(self.d + i * 60)) * self.r,self.y - sin(radians(self.d + i * 60)) * self.r],
                             [self.x + cos(radians(self.d + i * 60 + 180)) * self.r,self.y - sin(radians(self.d + i * 60 + 180)) * self.r],width = int(self.r//2))

    def draw_b(self):
        for i in range(3):
            pygame.draw.line(game_window,self.clr,
                             [self.x + cos(radians(self.d + i * 60)) * self.r,self.y - sin(radians(self.d + i * 60)) * self.r],
                             [self.x + cos(radians(self.d + i * 60 + 180)) * self.r,self.y - sin(radians(self.d + i * 60 + 180)) * self.r],width = int(self.r//2))

    def draw_f(self):
        pass

class SparkTrail():
    def __init__(self,origin,x,y,r,clr,spd = 1):
        self.origin = origin
        self.x = x
        self.y = y
        self.r = r
        self.clr = clr
        self.spd = spd
        self.d = 0#randint(1,360)
        self.origin.visual_sprites.append(self)

    def update(self):
        self.d = (self.d + 1)%360
        self.r -= self.spd
        if self.r <= 0:
            self.origin.visual_sprites.remove(self)
            del self

    def draw(self):
        pts = []
        for i in range(8):
            pts.append([self.x + cos(radians(self.d + i * 45)) * self.r,self.y - sin(radians(self.d + i * 45)) * self.r])
            pts.append([self.x + cos(radians(self.d + i * 45 + 22.5)) * self.r * 0.75,self.y - sin(radians(self.d + i * 45 + 22.5)) * self.r * 0.75])
        pygame.draw.polygon(game_window,self.clr,pts)

    def draw_b(self):
        self.draw()

    def draw_f(self):
        pass

class StarTrail():
    def __init__(self,origin,x,y,r,clr,spd = 1):
        self.origin = origin
        self.x = x
        self.y = y
        self.r = r
        self.clr = clr
        self.spd = spd
        self.d = 0#randint(1,360)
        self.origin.visual_sprites.append(self)

    def update(self):
        #self.d = (self.d + 1)%360
        self.r -= self.spd
        if self.r <= 0:
            self.origin.visual_sprites.remove(self)
            del self

    def draw(self):
        DrawStar(self.x,self.y,self.r,self.r * 0.5,self.d,self.clr)

    def draw_b(self):
        self.draw()

    def draw_f(self):
        pass

class SwingTrail():
    def __init__(self,origin,offx,r,clr,bright = 0,spd = 1,d = 0):
        self.origin = origin
        self.x = self.origin.centerx
        self.y = self.origin.centery
        self.offx = offx
        self.r = r
        self.clr = clr
        self.b = bright
        self.spd = spd
        self.d = d
        self.origin.visual_sprites.append(self)

    def update(self):
        #self.d = (self.d + 60)%360
        if self.offx < 0:
            self.offx += 0.25
        else:
            self.offx -= 0.25
        self.r -= self.spd
        if self.b > 0:
            self.b -= 2
        if self.r <= 0:
            self.origin.visual_sprites.remove(self)
            del self

    def draw(self):
        #print(cos(radians(self.d)) * self.offx)
        if self.b > 0:
            pygame.draw.circle(game_window,Brighten(self.clr,self.b),[self.x + cos(radians(self.d)) * self.offx,self.y - sin(radians(self.d)) * 5],self.r)
        else:
            pygame.draw.circle(game_window,self.clr,[self.x + cos(radians(self.d)) * self.offx,self.y - sin(radians(self.d)) * 5],self.r)

    def draw_b(self):
        if self.b > 0:
            pygame.draw.circle(game_window,Brighten(self.clr,self.b),[self.x + cos(radians(self.d)) * self.offx,self.y - sin(radians(self.d)) * 5],self.r)
        else:
            pygame.draw.circle(game_window,self.clr,[self.x + cos(radians(self.d)) * self.offx,self.y - sin(radians(self.d)) * 5],self.r)

    def draw_f(self):
        pass

class BeamBurst():
    def __init__(self,x,y,d = 0,w = 10,rotate = 0.5,clr = (65,32,112),e_clr = (238,226,255)):#88,26,177
        self.fm = tile_sprites.sprites()[0]
        #self.tile = self.fm.tiles[y][x]
        tile = self.fm.tiles[y][x]
        self.cx = tile.centerx
        self.cy = tile.centery
        self.d = d
        self.w = w
        self.wd = 0
        self.clr = clr
        self.e_clr = e_clr
        self.r = rotate#rotate/180
        self.bw = 200#1500
        self.fm.visual_sprites.append(self)

    def update(self):
        self.d += self.r *  (1 + cos(radians(self.wd - 90)))
        self.wd += 4
        if self.wd >= 180:
            self.fm.visual_sprites.remove(self)

    def draw(self):
        c = 1-abs(90-self.wd)/90
        w = (self.w + 2) * c#sin(radians(self.wd))
        pygame.draw.polygon(game_window,self.e_clr,[[self.cx,self.cy],
                                                    [self.cx + cos(radians(self.d - w)) * self.bw,self.cy - sin(radians(self.d - w)) * self.bw],
                                                    [self.cx + cos(radians(self.d + w)) * self.bw,self.cy - sin(radians(self.d + w)) * self.bw],])
        w = self.w * c#sin(radians(self.wd))
        pygame.draw.polygon(game_window,self.clr,[[self.cx,self.cy],
                                                  [self.cx + cos(radians(self.d - w)) * self.bw,self.cy - sin(radians(self.d - w)) * self.bw],
                                                  [self.cx + cos(radians(self.d + w)) * self.bw,self.cy - sin(radians(self.d + w)) * self.bw],])
##        pygame.draw.polygon(game_window,self.e_clr,[[self.tile.centerx,self.tile.centery],
##                                                    [self.tile.centerx + cos(radians(self.d - w)) * self.bw,self.tile.centery - sin(radians(self.d - w)) * self.bw],
##                                                    [self.tile.centerx + cos(radians(self.d + w)) * self.bw,self.tile.centery - sin(radians(self.d + w)) * self.bw],])
##        w = self.w * c#sin(radians(self.wd))
##        pygame.draw.polygon(game_window,self.clr,[[self.tile.centerx,self.tile.centery],
##                                                  [self.tile.centerx + cos(radians(self.d - w)) * self.bw,self.tile.centery - sin(radians(self.d - w)) * self.bw],
##                                                  [self.tile.centerx + cos(radians(self.d + w)) * self.bw,self.tile.centery - sin(radians(self.d + w)) * self.bw],])
class ElectricSwirl():
    def __init__(self,origin):
        self.loop = 0
        self.origin = origin
        self.oy = randint(0,self.origin.rect[3])
        self.dy = -0.2 + randint(0,4)/10
        self.w = self.origin.rect[2]/2 + randint(5,10)
        self.h = -self.origin.rect[3]/2 + randint(0,self.origin.rect[3])
        self.d = randint(1,72) * 5
        self.l = randint(10,15)
        self.td = (self.l + randint(8,15)) * 5

        self.clr = [(255,247,0),(0,228,255)][randint(0,1)]
        self.d_clr = Darken(self.clr, 10)

        self.b_pts = []
        self.f_pts = []
        
        self.offy = []

        self.origin.visual_sprites.append(self)

    def update(self):
        if self.loop <= self.td + (self.l - 1) * 5:
            self.loop += 2.5
            if self.loop % 5 == 0:
                if self.loop <= self.td:
                    self.h += self.dy
                    self.offy.append(-2 + randint(0,4))
                    if len(self.offy) >= self.l:
                        self.offy.pop(0)
                else:
                    if len(self.offy) > 0:
                        self.offy.pop(0)
            self.b_pts = []
            self.f_pts = []
            for i in range(len(self.offy)):
                d = self.d + self.loop + i * 5
                if d % 180 == 0:
                    self.b_pts.append([self.origin.rect.centerx + cos(radians(d)) * self.w, self.origin.rect.centery - self.h - sin(radians(d)) * 3 + self.offy[i] + self.dy * i])
                    self.f_pts.append([self.origin.rect.centerx + cos(radians(d)) * self.w, self.origin.rect.centery - self.h - sin(radians(d)) * 3 + self.offy[i] + self.dy * i])
                elif 0 < d % 360 < 180:
                    self.b_pts.append([self.origin.rect.centerx + cos(radians(d)) * self.w, self.origin.rect.centery - self.h - sin(radians(d)) * 3 + self.offy[i] + self.dy * i])
                else:
                    self.f_pts.append([self.origin.rect.centerx + cos(radians(d)) * self.w, self.origin.rect.centery - self.h - sin(radians(d)) * 3 + self.offy[i] + self.dy * i])
                
        else:
            if self.origin.HP > 0:
                self.loop = 0
                self.oy = randint(0,self.origin.rect[3])
                self.dy = -0.2 + randint(0,4)/10
                self.w = self.origin.rect[2]/2 + randint(5,10)
                self.h = -self.origin.rect[3]/2 + randint(0,self.origin.rect[3])
                self.d = randint(1,72) * 5
                self.l = randint(10,15)
                self.td = (self.l + randint(8,15)) * 5

                self.clr = [(255,247,0),(0,228,255)][randint(0,1)]
                self.d_clr = Darken(self.clr, 10)

                self.b_pts = []
                self.f_pts = []
                
                self.offy = []
            else:
                self.origin.visual_sprites.remove(self)
                del self

    def draw_b(self):
        if len(self.b_pts) > 1:
            pygame.draw.lines(game_window,self.d_clr,False,self.b_pts, width = 2)

    def draw_f(self):
        if len(self.f_pts) > 1:
            pygame.draw.lines(game_window,self.clr,False,self.f_pts, width = 2)

class DropFlash():
    def __init__(self,origin,offx = 0,offy = 0,r = 5,flatten = 0.1,spd = 1,a_clr = (0,0,255),b_clr = (0,0,255)):
        self.origin = origin
        self.offx = offx
        self.offy = offy
        self.r = 0
        self.mr = r
        self.w = 0
        self.h = 0
        self.a_clr = a_clr
        self.b_clr = b_clr
        self.clr = a_clr
        self.loop = 0
        self.flatten = flatten
        self.spd = spd
        self.origin.visual_sprites.append(self)

    def update(self):
        if self.r < self.mr:
            self.r += self.flatten
            self.w,self.h = self.r,self.r
        else:
            self.w -= self.flatten
            self.h += self.flatten
            self.clr = GradientClrs(self.a_clr,self.b_clr,self.w/self.r,1-self.w/self.r)
        self.loop += self.spd
        if self.w <= 0:
            self.origin.visual_sprites.remove(self)
            del self

    def draw(self):
        pts = []
        for i in range(10):
            pts.append([self.origin.centerx + self.offx + cos(radians(i * 36)) * self.w,
                        self.origin.centery + self.offy - self.loop - sin(radians(i * 36)) * self.h])
        pygame.draw.polygon(game_window,self.clr,pts)

    def draw_b(self):
        pass
    
    def draw_f(self):
        self.draw()

def UpwardLines(unit,clr):
    fm = tile_sprites.sprites()[0]
    w = unit.rect[2]//5 + 2
    a,b = (w-1)/2,(w+1)/2
    for j in range(w):
        UpwardLine(fm.tiles[unit.y][unit.x],
                   spd = 0.05 * (unit.rect[3] + 35) - 0.25 - randint(0,1),
                   clr = clr,
                   l = randint(int(unit.rect[3]*2/3),unit.rect[3]),
                   h = randint(unit.rect[3] + 20,unit.rect[3] + 50),
                   offx = unit.rect[2] * (j - a)/b,
                   offy = randint(int(unit.rect[3]*0.1),int(unit.rect[3]*0.3)),
                   delay = randint(0,3) * 10)

class UpwardLine():
    def __init__(self,origin,spd = 2, clr = (255,255,255),l = 20,h = 50,offx = 0,offy = 0,delay = 0):
        self.origin = origin
        self.sx = offx
        self.sy = offy
        self.ex = self.sx
        self.ey = self.sy
        self.l = l
        self.h = h
        self.w = 0
        self.clr = clr
        self.spd = spd
        self.loop = -delay
        self.origin.visual_sprites.append(self)

    def update(self):
        self.loop += self.spd
        if self.loop >= self.l + self.h:
            self.origin.visual_sprites.remove(self)
            del self
        elif self.loop >= 0:
            if self.loop < self.l:
                self.ey -= self.spd
            elif self.loop < self.h:
                self.ey -= self.spd
                self.sy -= self.spd
            else:
                self.sy -= self.spd

    def draw(self):
        if self.loop >= 0:
            pygame.draw.polygon(game_window,self.clr,[[self.origin.centerx + self.sx - 1,self.origin.centery + self.sy],
                                                      [self.origin.centerx + self.sx,self.origin.centery + self.sy + 1],
                                                      [self.origin.centerx + self.sx + 1,self.origin.centery + self.sy],
                                                      [self.origin.centerx + self.ex + 1,self.origin.centery + self.ey],
                                                      [self.origin.centerx + self.ex,self.origin.centery + self.ey - 1],
                                                      [self.origin.centerx + self.ex - 1,self.origin.centery + self.ey]])
            #pygame.draw.line(game_window,self.clr,[self.sx,self.sy],[self.ex,self.ey],width = 5)
        
    def draw_b(self):
        pass

    def draw_f(self):
        self.draw()

class EnchantedGlow():
    def __init__(self,w = 300,h = 200,loop = 4):
        self.fm = tile_sprites.sprites()[0]
        self.w, self.h = w,h
        self.s = 0
        self.surface = pygame.Surface((w * 2,h * 2))
        self.surface.fill((0,0,0))
        self.surface.set_colorkey((0,0,0))
        self.surface.set_alpha(0)
        self.rect = self.surface.get_rect()
        self.c_lp = 0
        self.d = 0

        self.loop = 0
        self.m_loop = loop * fps

        self.fm.visual_sprites.append(self)

    def update(self):
        self.c_lp = (self.c_lp + 5)%1530
        self.d = (self.d + 1)%360

        if self.loop < self.m_loop:
            if self.s < 1:
                self.s += 0.02
                self.surface.set_alpha(self.s * 100)
            self.loop += 1
        else:
            if self.s > 0:
                self.s -= 0.02
                self.surface.set_alpha(self.s * 100)
            else:
                self.fm.visual_sprites.remove(self)
                del self
                return

    def draw(self):
        self.surface.fill((0,0,0))
        pts = []
        for i in range(40):
            c = (1 - sin(radians(i * 54))) * 20
            pts.append([self.w + cos(radians(self.d + i * 9)) * (self.w - c) * self.s,
                        self.h - sin(radians(self.d + i * 9)) * (self.h - c) * self.s])
        pygame.draw.polygon(self.surface,Get_RClr(self.c_lp,150),pts)
        for i in [[0,0],[window_width,0],[window_width,window_height],[0,window_height]]:
            self.rect.center = i
            game_window.blit(self.surface,self.rect)

class MagicSpiral():
    def __init__(self,original,x,y,angle,colour = (90,191,238),spd = 1,s_range = 40,start = 10,delay = 0,flat = False):
        self.fm = tile_sprites.sprites()[0]
        self.origin = original
        self.ox = x
        self.oy = y
        self.d = angle
        self.clr = colour
        self.spd = spd
        self.start = start
        self.r = start
        self.max_r = s_range
        self.shift = 0.5
        self.rb = self.r
        self.loop = delay
        self.flat = flat

        self.surface = pygame.Surface((s_range * 2,s_range * 2)).convert_alpha()
        self.surface.fill((0,0,0))
        self.surface.set_colorkey((0,0,0))
        self.rect = self.surface.get_rect()
        
        
        self.origin.visual_sprites.append(self)

    def update(self):
        self.d = (self.d + 5)%360
        if self.loop < 0:
            self.loop += 1
        else:
            if self.r < self.max_r:
                self.r += self.spd
                self.shift = 0.5 * (1 - self.r/self.max_r)
                self.rb = self.r
                #self.ra = self.rb - (self.rb - self.start) * self.shift
            else:
                self.origin.visual_sprites.remove(self)
                del self
                return

    def draw(self):
        pts = []
##        if self.flat:
##            c = self.fm.h/self.fm.w
##        else:
##            c = 1
##        for i in range(7):
##            pts.append([self.ox + cos(radians(self.d + i * 30)) * self.rb,
##                            self.oy - sin(radians(self.d + i * 30)) * self.rb * c])
##        pts.reverse()
##        for i in range(5):
##            pts.append([self.ox + cos(radians(self.d + (i+1) * 30)) * self.ra,
##                            self.oy - sin(radians(self.d + (i+1) * 30)) * self.ra * c])
##        pygame.draw.polygon(game_window,self.clr,pts)
        self.surface.fill((0,0,0))
        self.surface.set_alpha(160)
        if self.flat:
            c = self.fm.h/self.fm.w
        else:
            c = 1
        for i in range(7):
            pts.append([self.max_r + cos(radians(self.d + i * 30)) * self.rb,
                        self.max_r - sin(radians(self.d + i * 30)) * self.rb * c])
        pts.reverse()
        for i in range(5):
            r = self.rb - sin(radians((i + 1)*15)) * ((self.rb - self.start) * self.shift)
            pts.append([self.max_r + cos(radians(self.d + (i+1) * 30)) * r,
                        self.max_r - sin(radians(self.d + (i+1) * 30)) * r * c])
        pygame.draw.polygon(self.surface,self.clr,pts)
        self.rect.center = [self.ox,self.oy]
        game_window.blit(self.surface,self.rect)

    def draw_b(self):
        pass

    def draw_f(self):
        self.draw()

class MagicSwirl():
    def __init__(self,original,angle,colour = (90,191,238),spd = 1,grow = 0.1,b_colour = None,l = None,w = None,h = None,slant = 1,Follow = True,clockwise = False,reverse = False):
        self.origin = original
        self.d = angle
        self.follow = Follow
        self.rect = pygame.Rect(0,0,1,1)
        self.reverse = reverse
        if not self.follow:
            self.ox = self.origin.rect.centerx
            if self.reverse:
                self.oyb = self.origin.rect.top
                self.oyt = self.origin.rect.bottom
            else:
                self.oyb = self.origin.rect.bottom
                self.oyt = self.origin.rect.top
        self.rect.centerx = self.origin.rect.centerx
        self.rect.centery = self.origin.rect.bottom - 5
        if w:
            self.w = w
        else:
            self.w = self.origin.rect[2]/2 + randint(0,5)
        if h:
            self.max_h = h
        else:
            self.max_h = self.origin.rect[3]
        if l:
            self.length = l
        else:
            self.length = CorInt(self.origin.rect[3]*0.75)
        if self.length > self.max_h:
            self.length = self.max_h
        self.spd = spd
        self.grow = grow
        self.offy = -self.length
        self.slant = slant
        self.lp = 0
        self.f_pts = []
        self.b_pts = []
        self.colour = colour
        if clockwise:
            self.w *= -1
            self.grow *= -1
        if b_colour:
            self.b_colour = b_colour
        else:
            self.b_colour = Darken(self.colour,30)
        self.origin.visual_sprites.append(self)

    def update(self):
        if self.lp >= self.max_h + self.length:
            self.origin.visual_sprites.remove(self)#self.kill()
            del self
            return
        self.lp += 1
        self.offy += self.spd
        self.w += self.grow
        if self.follow:
            self.rect.centerx = self.origin.rect.centerx
            if self.reverse:
                if self.offy > self.max_h:
                    self.rect.centery = self.origin.rect.bottom
                elif self.offy >= 0:
                    self.rect.centery = self.origin.rect.top - 5 + self.offy
                    self.d = (self.d + 5) % 360
                else:
                    self.rect.centery = self.origin.rect.top - 5
                    self.d = (self.d + 5) % 360
            else:
                if self.offy > self.max_h:
                    self.rect.centery = self.origin.rect.top
                elif self.offy >= 0:
                    self.rect.centery = self.origin.rect.bottom - 5 - self.offy
                    self.d = (self.d + 5) % 360
                else:
                    self.rect.centery = self.origin.rect.bottom - 5
                    self.d = (self.d + 5) % 360
        else:
            if self.offy > self.max_h:
                self.rect.centery = self.oyt
            elif self.offy >= 0:
                if self.reverse:
                    self.rect.centery = self.oyb - 5 + self.offy
                else:
                    self.rect.centery = self.oyb - 5 - self.offy
                self.d = (self.d + 5) % 360
            else:
                self.rect.centery = self.oyb - 5
                self.d = (self.d + 5) % 360
        if self.offy < 0:
            l = self.length-abs(self.offy)
        elif self.offy + self.length >= self.max_h:
            l = self.max_h - self.offy
        else:
            l = self.length
        f_a_pts = []
        f_b_pts = []
        b_a_pts = []
        b_b_pts = []
        for i in range(l):
            h = l/8 - abs(l/2 - i)/4
            x = self.rect.centerx + cos(radians(self.d + i*3)) * self.w
            if self.reverse:
                y = self.rect.centery + i * self.slant - sin(radians(self.d + i*3)) * 5
            else:
                y = self.rect.centery - i * self.slant - sin(radians(self.d + i*3)) * 5
            if (self.d + i * 3) % 180 == 0:
                b_a_pts.append([x,y - h])
                b_b_pts.append([x,y + h])
                f_a_pts.append([x,y - h])
                f_b_pts.append([x,y + h])
            elif 0 < (self.d + i * 3)%360 < 180:
                b_a_pts.append([x,y - h])
                b_b_pts.append([x,y + h])
            else:
                f_a_pts.append([x,y - h])
                f_b_pts.append([x,y + h]) 
        f_b_pts.reverse()
        b_b_pts.reverse()
        self.f_pts = f_a_pts + f_b_pts
        self.b_pts = b_a_pts + b_b_pts

    def draw_b(self):
        if len(self.b_pts) > 2:
            pygame.draw.polygon(game_window,self.b_colour,self.b_pts)
        elif len(self.b_pts) > 1:
            pygame.draw.lines(game_window,self.b_colour,False,self.b_pts)

    def draw_f(self):
        if len(self.f_pts) > 2:
            pygame.draw.polygon(game_window,self.colour,self.f_pts)
        elif len(self.f_pts) > 1:
            pygame.draw.lines(game_window,self.colour,False,self.f_pts)

##class ElectricLeakage()
##    def __init__(self,x,y):
##        self.fm = tile_sprites.sprites()[0]
##        self.loop = 0
##        self.t = self.fm.tiles[y][x]
##        self.t.visual_sprites.append(self)
##
##    def update(self):
##        #if self.loop % 20 == 0:
##            d = randint(180,360)
##            BurstTrail(self.t], d = d,spd = 3 + sin(radians(d)) * 2, clr = (255,233,94),offy = 0)
##        #self.loop = (self.loop + 1)%20

#Unit Status Effects
def ApplyUnitSEV(unit,effect,turn):
    if effect in unit.StatusEffect:
        unit.EffectTimer[unit.StatusEffect.index(effect)] += turn
    else:
        unit.StatusEffect.append(effect)
        unit.EffectTimer.append(turn)
        unit.SEVisual.append(False)

glow_spot = pygame.image.load("./_Symbol/Glow.png")
##glow_spot = pygame.Surface((25,25))
##glow_spot.set_colorkey((0,0,0))
##pygame.draw.circle(glow_spot,(255,255,255),[12,12],12)

class StatusEffectVisual():
    def __init__(self,original,effect, SCD = None):
        self.Effect = effect
        self.origin = original
        self.loop = 0
        self.Delete = False
        self.fm = tile_sprites.sprites()[0]

        self.origin.visual_sprites.append(self)
        if SCD:
            eval("self."+self.Effect.replace(" ","")+"_Assign(SCD)")
        else:
            eval("self."+self.Effect.replace(" ","")+"_Assign()")

    def update(self):
        eval("self."+self.Effect.replace(" ","")+"_Update()")

    def draw_b(self):
        eval("self."+self.Effect+"_Back()")

    def draw_f(self):
        eval("self."+self.Effect+"_Front()")

    def remove(self):
        self.origin.visual_sprites.remove(self)
        del self

    def Burn_Assign(self, SCD = 0):
        self.h = self.origin.rect[3] - 10 + randint(0,20)
        self.loop = -5 * SCD
        self.clr = (randint(235,255),randint(0,120),0)
        self.ox = -self.origin.rect[2]/2 - 3 + randint(0,self.origin.rect[2] + 6)
        self.r = RoundUp(self.origin.rect[2] * randint(2,3)/10)#randint(4,7)
        self.max_r = self.r
    
    def Burn_Update(self):
        if self.loop < 25:
            self.loop += 1
            if self.loop > 15:
                self.r = self.max_r * (25 - self.loop)/10
        else:
            if self.origin.Burn:
                self.Burn_Assign()
            else:
                self.remove()

    def Burn_Back(self):
        pass

    def Burn_Front(self):
        if self.loop >= 0:
            pygame.draw.circle(game_window,self.clr,[self.origin.rect.centerx + self.ox, self.origin.rect.bottom - self.h * self.loop/25],self.r)

    def Freeze_Assign(self):
        w = self.origin.rect[2]/2
        h = w * 0.15
        c = w//5
        self.pts = []
        self.w = []
        self.d = []
        self.clrs = []
        self.s = 0
        for i in range(11):
            self.pts.append([cos(radians(180 + 18 * i)) * w,-sin(radians(180 + 18 * i)) * h])
            self.w.append(self.origin.rect[2]/4 + randint(1,2))
            self.d.append(randint(0,360))
            self.clrs.append(GetFreezeClr())

    def Freeze_Update(self):
        if self.origin.Freeze:
            if self.s < 1:
                self.s += 0.02
        elif self.s > 0:
            self.s -= 0.02
        else:
            self.remove()

    def Freeze_Back(self):
        pass

    def Freeze_Front(self):
        for i in range(len(self.d)):
            pts = []
            for j in range(4):
                pts.append([self.origin.rect.centerx + self.pts[i][0] + cos(radians(self.d[i] + j * 90)) * self.w[i] * self.s,self.origin.rect.bottom + self.pts[i][1] - sin(radians(self.d[i] + j * 90)) * self.w[i] * self.s])
            pygame.draw.polygon(game_window,self.clrs[i],pts)

    def Shock_Assign(self):
        self.loop = 0
        self.oy = randint(0,self.origin.rect[3])
        self.dy = -0.2 + randint(0,4)/10
        self.w = self.origin.rect[2]/2 + randint(5,10)
        self.h = -self.origin.rect[3]/2 + randint(0,self.origin.rect[3])
        self.d = randint(1,72) * 5
        self.l = randint(10,15)
        self.td = (self.l + randint(8,15)) * 5

        self.clr = [(255,247,0),(0,228,255)][randint(0,1)]
        self.d_clr = Darken(self.clr, 10)

        self.b_pts = []
        self.f_pts = []
        
        self.offy = []

    def Shock_Update(self):
        #print(self.offy)
        if self.loop <= self.td + (self.l - 1) * 5:
            self.loop += 2.5
            if self.loop % 5 == 0:
                if self.loop <= self.td:
                    self.h += self.dy
                    self.offy.append(-2 + randint(0,4))
                    if len(self.offy) >= self.l:
                        self.offy.pop(0)
                else:
                    if len(self.offy) > 0:
                        self.offy.pop(0)
            self.b_pts = []
            self.f_pts = []
            for i in range(len(self.offy)):
                d = self.d + self.loop + i * 5
                if d % 180 == 0:
                    self.b_pts.append([self.origin.rect.centerx + cos(radians(d)) * self.w, self.origin.rect.centery - self.h - sin(radians(d)) * 3 + self.offy[i] + self.dy * i])
                    self.f_pts.append([self.origin.rect.centerx + cos(radians(d)) * self.w, self.origin.rect.centery - self.h - sin(radians(d)) * 3 + self.offy[i] + self.dy * i])
                elif 0 < d % 360 < 180:
                    self.b_pts.append([self.origin.rect.centerx + cos(radians(d)) * self.w, self.origin.rect.centery - self.h - sin(radians(d)) * 3 + self.offy[i] + self.dy * i])
                else:
                    self.f_pts.append([self.origin.rect.centerx + cos(radians(d)) * self.w, self.origin.rect.centery - self.h - sin(radians(d)) * 3 + self.offy[i] + self.dy * i])
                
        else:
            if self.origin.Shock:
                self.Shock_Assign()
            else:
                self.remove()

    def Shock_Back(self):
        if len(self.b_pts) > 1:
            pygame.draw.lines(game_window,self.d_clr,False,self.b_pts, width = 2)

    def Shock_Front(self):
        if len(self.f_pts) > 1:
            pygame.draw.lines(game_window,self.clr,False,self.f_pts, width = 2)

    def Splash_Assign(self, SCD = 0):
        self.loop = -10 * SCD #int(-self.origin.rect[3] * SCD/4)
        self.clr = (130,randint(195,250),255)
        self.ox = -self.origin.rect[2]/2 - 3 + randint(0,self.origin.rect[2] + 6)
        self.oy = randint(0,10)
        self.r = 0
        self.max_r = self.origin.rect[3] // 10 + randint(0,1)
        self.h = self.origin.rect[3] - 10 + randint(0,20)

    def Splash_Update(self):
        if self.loop < 40:#self.h:
            self.loop += 1
            if self.loop < 5:
                self.r = self.max_r * self.loop/5
            elif self.loop >= 35:
                self.r = self.max_r * (40 - self.loop)/5
        elif self.loop == 40:#self.h:
            if self.Effect in self.origin.StatusEffect:
                self.Splash_Assign()
            else:
                self.remove()

    def Splash_Back(self):
        pass

    def Splash_Front(self):
        if self.loop >= 0:
            pygame.draw.circle(game_window,self.clr,[self.origin.rect.centerx + self.ox, self.origin.rect.top - self.oy + self.h * self.loop/40],self.r)
        
    def Poison_Assign(self, SCD = 0):
        self.loop = -10 * SCD
        self.clr = GetPoisonClr()#(95,185,90)
        self.ox = -self.origin.rect[2]/2 - 3 + randint(0,self.origin.rect[2] + 6)
        self.oy = randint(0,10)
        self.r = 0
        self.max_r = 2 + self.origin.rect[3] // 10 + randint(0,1)#randint(3,5)
        self.h = self.origin.rect[3] - 10 + randint(0,20)
    
    def Poison_Update(self):
        if self.loop < 40:#self.h:
            self.loop += 1
            if self.loop < 5:
                self.r = self.max_r * self.loop/5
            elif self.loop >= 35:
                self.r = self.max_r * (40 - self.loop)/5
        elif self.loop == 40:
            if self.origin.Poison:
                self.Poison_Assign()
            else:
                self.remove()

    def Poison_Back(self):
        pass

    def Poison_Front(self):
        if self.loop >= 0:
            pygame.draw.circle(game_window,self.clr,[self.origin.rect.centerx + self.ox, self.origin.rect.bottom + self.oy - self.h * self.loop/40],self.r)

    def Blind_Assign(self, SCD = 0):
        self.h = self.origin.rect[3] * randint(10,12)/10#- 10 + randint(0,20)
        self.loop = -10 * SCD#50 + 10 * SCD#-10 * SCD
        self.clr = GetBlindClr()
        self.ox = -self.origin.rect[2]/2 - 2 + randint(0,self.origin.rect[2] + 4)
        self.max_r = RoundUp(self.origin.rect[2] * randint(4,6)/10)
        self.r = self.max_r
    
    def Blind_Update(self):
##        if self.loop > 0:
##            self.loop -= 1
##            if self.loop > 30:
##                self.r = self.max_r * (50 - self.loop)/20
##        else:
##            if self.origin.Blind:
##                self.Blind_Assign()
##            else:
##                self.remove()
        if self.loop < 50:
            self.loop += 1
            if self.loop > 30:
                self.r = self.max_r * (50 - self.loop)/20
        else:
            if self.origin.Blind:
                self.Blind_Assign()
            else:
                self.remove()

    def Blind_Back(self):
        if self.loop >= 0:
            pygame.draw.circle(game_window,self.clr,[self.origin.rect.centerx + self.ox, self.origin.rect.bottom - self.h * self.loop/25],self.r)
            
    def Blind_Front(self):
        pass

    def Curse_Assign(self):
        self.f_pts, self.b_pts = [],[]
        self.f_d, self.b_d = [],[]
        self.c = 10
        self.v = 0
        self.w = self.origin.rect[2]/2 + 5 + self.c
        self.h = self.w#self.origin.rect[3]/2 + 5
        self.i_clr = (128,70,230)
        self.clr = self.i_clr
        self.d_clr = Darken(self.clr,10)

    def Curse_Update(self):
        self.loop = (self.loop + 2)%360
        self.f_pts, self.b_pts = [],[]
        self.f_d, self.b_d = [],[]
        
        for i in range(4):
            for j in range(5):
                d = self.loop + i * 90 + j * 15
                d %= 360
                if i % 2 == 0:
                    pts = [self.origin.rect.centerx + sin(radians(d)) * self.w,
                           self.origin.rect.centery - sin(radians(d)) * self.h]
                    if 90 < d < 270:
                        self.f_pts.append(pts)
                        if j % 2 == 0:
                            self.f_d.append(0)
                        else:
                            self.f_d.append([[self.origin.rect.centerx + sin(radians(d-self.v * 2)) * self.w,
                                              self.origin.rect.centery - sin(radians(d-self.v * 2)) * self.h],
                                             [self.origin.rect.centerx + sin(radians(d+self.v * 2)) * self.w,
                                              self.origin.rect.centery - sin(radians(d+self.v * 2)) * self.h]])
                    else:
                        self.b_pts.append(pts)
                        if j % 2 == 0:
                            self.b_d.append(0)
                        else:
                            self.b_d.append([[self.origin.rect.centerx + sin(radians(d-self.v * 2)) * self.w,
                                              self.origin.rect.centery - sin(radians(d-self.v * 2)) * self.h],
                                             [self.origin.rect.centerx + sin(radians(d+self.v * 2)) * self.w,
                                              self.origin.rect.centery - sin(radians(d+self.v * 2)) * self.h]])
                else:
                    pts = [self.origin.rect.centerx + sin(radians(d)) * self.w,
                           self.origin.rect.centery + sin(radians(d)) * self.h]
                    if 90 < d < 270:
                        self.f_pts.append(pts)
                        if j % 2 == 0:
                            self.f_d.append(0)
                        else:
                            self.f_d.append([[self.origin.rect.centerx + sin(radians(d-self.v * 2)) * self.w,
                                              self.origin.rect.centery + sin(radians(d-self.v * 2)) * self.h],
                                             [self.origin.rect.centerx + sin(radians(d+self.v * 2)) * self.w,
                                              self.origin.rect.centery + sin(radians(d+self.v * 2)) * self.h]])
                    else:
                        self.b_pts.append(pts)
                        if j % 2 == 0:
                            self.b_d.append(0)
                        else:
                            self.b_d.append([[self.origin.rect.centerx + sin(radians(d-self.v * 2)) * self.w,
                                              self.origin.rect.centery + sin(radians(d-self.v * 2)) * self.h],
                                             [self.origin.rect.centerx + sin(radians(d+self.v * 2)) * self.w,
                                              self.origin.rect.centery + sin(radians(d+self.v * 2)) * self.h]])
        if self.origin.Curse:
            if self.c > 0:
                self.c -= 0.5
                self.w -= 0.5
                self.h = self.w
                self.clr = GradientClrs((255,255,255),self.i_clr,self.c/10,1-self.c/10)
                self.d_clr = Darken(self.clr,10)
                self.v += 0.25
        elif self.c < 10:
            self.c += 0.5
            self.v -= 0.25
            self.w += 0.5
            self.h = self.w
            self.clr = GradientClrs((255,255,255),self.i_clr,self.c/15,1-self.c/15)
            self.d_clr = Darken(self.clr,10)
        else:
            self.remove()

    def Curse_Back(self):
        for i in range(len(self.b_pts)):
            if self.b_d[i] == 0:
                pygame.draw.circle(game_window,self.d_clr,self.b_pts[i],self.v,width = 3)
            else:
                pygame.draw.line(game_window,self.d_clr,self.b_d[i][0],self.b_d[i][1],width = 3)

    def Curse_Front(self):
        for i in range(len(self.f_pts)):
            if self.f_d[i] == 0:
                pygame.draw.circle(game_window,self.clr,self.f_pts[i],self.v,width = 3)
            else:
                pygame.draw.line(game_window,self.clr,self.f_d[i][0],self.f_d[i][1],width = 3)

    def Strengthen_Assign(self,SCD = 0):
        self.clr = SE_colour_set.get(self.Effect)
        self.w = self.origin.rect[2] * 0.7
        self.h = self.w * 0.15
        self.max_h = self.origin.rect[3] + randint(10,15)
        self.loop = randint(0,360)
        self.offy = 0
        self.d = SCD * 30#15
        self.spd = self.max_h/60

        self.l = 5

        self.centerx = self.origin.rect.centerx + cos(radians(self.loop)) * self.w
        self.centery = self.origin.rect.bottom - self.offy - sin(radians(self.loop)) * self.h

    def Strengthen_Update(self):
        if self.d > 0:
            self.d -= 1
            if self.d < 0:
                self.d = 0
            return
        self.loop = (self.loop + 5)%360

        self.offy += self.spd
        self.w += 0.1
        self.centerx = self.origin.rect.centerx + cos(radians(self.loop)) * self.w
        self.centery = self.origin.rect.bottom - self.offy - sin(radians(self.loop)) * self.h

        if self.max_h - self.offy < 10 and self.l > 0:
            self.l -= 0.5

        if self.offy >= self.max_h:
            if self.origin.Strengthen:
                self.Strengthen_Assign()
            else:
                self.remove()

    def Strengthen_Back(self):
        if self.d == 0 and self.loop < 180:
            DrawStar(self.centerx,self.centery,self.l,self.l * 0.4,self.loop,self.clr)

    def Strengthen_Front(self):
        if self.d == 0 and self.loop > 180:
            DrawStar(self.centerx,self.centery,self.l,self.l * 0.4,self.loop,self.clr)

    def Weaken_Assign(self, SCD = 0):
        self.loop = int(-self.origin.rect[3] * SCD/4)
        self.clr = [(216,99,228),(216,99,228),(113,99,228)][randint(0,2)]#SE_colour_set.get(self.Effect)
        self.ox = -self.origin.rect[2]/2 - 3 + randint(0,self.origin.rect[2] + 6)
        self.oy = randint(0,10)
        self.mr = self.origin.rect[3] // 10 + randint(2,4)#randint(4,7)
        self.r = 0
        self.h = self.origin.rect[3] - 10 + randint(0,20)
        self.d = randint(1,360)
        self.pd = []
        for i in range(3):
            self.pd.append(randint(0,20) * GenPN())

    def Weaken_Update(self):
        self.d = (self.d + 1)%360
        if self.loop < self.h:
            if self.r < self.mr:
                self.r += 0.5
                if self.r > self.mr:
                   self.r = self.mr
            self.loop += 0.5
        elif self.loop == self.h:
            if self.r > 0:
                self.r -= 0.5
            elif self.origin.Weaken:
                self.Weaken_Assign()
            else:
                self.remove()

    def Weaken_Back(self):
        pass

    def Weaken_Front(self):
        if self.loop >= 0:
            pts = []
            for i in range(3):
                pts.append([self.origin.rect.centerx + self.ox + cos(radians(self.d + i * 120 + self.pd[i])) * self.r, self.origin.rect.top - self.oy + self.loop - sin(radians(self.d + i * 120 + self.pd[i])) * self.r])
            pygame.draw.polygon(game_window,self.clr,pts,width = 2)

    def Reinforce_Assign(self,SCD = 0):
        self.centerx = self.origin.rect.centerx
        self.centery = self.origin.rect.centery
        self.loop = 0
        self.w = self.origin.rect[2]/2 + 10
        self.h = self.w * 0.3
        self.d = SCD * 72
        self.f_pts = []
        self.b_pts = []
        self.colour = (215,231,235)
        self.b_colour = Darken(self.colour,30)
        self.s = 0

    def Reinforce_Update(self):
        def R_CheckFB(d,c):
            if d % 180 == 0:
                self.f_pts.append(c)
                self.b_pts.append(c)
            elif 0 < d % 360 < 180:
                self.b_pts.append(c)
            else:
                self.f_pts.append(c)
            
        if self.s == 1:
            self.d = (self.d + 2)%360
        self.centerx = self.origin.rect.centerx
        self.centery = self.origin.rect.centery - 5
        self.f_pts = []
        self.b_pts = []

        for i in [[-20,-1],[-10,-1.2],[0,-1.5],[10,-1.2],[20,-1],[18,-0.5],[10,0.6],[0,1],[-10,0.6],[-18,-0.5]]:
            x = self.centerx + cos(radians(self.d + i[0] * self.s)) * self.w
            y = self.centery + 5 - sin(radians(self.d + i[0] * self.s)) * 5 + self.h * i[1] * (2-self.s)
            R_CheckFB(self.d + i[0],[x,y])
        if not self.origin.Reinforce:#self.Effect not in self.origin.StatusEffect:
            self.s -= 0.1
            if self.s < 0:
                self.remove()
        elif self.s < 1:
            self.s += 0.1
            if self.s >= 1:
                self.s = 1
                
    def Reinforce_Back(self):
        if len(self.b_pts) > 2:
            pygame.draw.polygon(game_window,self.b_colour,self.b_pts)
        elif len(self.b_pts) > 1:
            pygame.draw.lines(game_window,self.b_colour,False,self.b_pts)

    def Reinforce_Front(self):
        if len(self.f_pts) > 2:
            pygame.draw.polygon(game_window,self.colour,self.f_pts)
        elif len(self.f_pts) > 1:
            pygame.draw.lines(game_window,self.colour,False,self.f_pts)

    def Vulnerable_Assign(self,SCD = 0):#[0,0]):        
        self.img = glow_spot.copy()
        x = pygame.Surface((25,25)).convert_alpha()
        clr = (randint(86,195),randint(86,98),255)
        x.fill((255 - clr[0],255 - clr[1],255 - clr[2],0))
        self.img.blit(x,(0,0),special_flags=pygame.BLEND_RGBA_SUB)

        self.img = pygame.transform.scale(self.img,[CorInt(self.origin.rect[2] * 0.3),CorInt(self.origin.rect[3]*(10 + randint(2,5))/10)])
        self.img.set_alpha(0)

        self.rect = self.img.get_rect()
        self.offx = self.origin.rect[2] * randint(0,5)/10 * GenPN()
        self.offy = -self.origin.rect[3] * randint(0,5)/10

        self.loop = -SCD * 130

    def Vulnerable_Update(self):
        self.offy += 0.15
        self.loop += 5
        if self.loop == 520:
            if self.origin.Vulnerable:
                del self.img
                self.Vulnerable_Assign()
            else:
                self.remove()
        else:
            self.img.set_alpha(255 - abs(255 - self.loop))

    def Vulnerable_Back(self):
        pass

    def Vulnerable_Front(self):
        self.rect.centerx = self.origin.rect.centerx + self.offx
        self.rect.centery = self.origin.rect.centery + self.offy
        game_window.blit(self.img,self.rect)

    def Quicken_Assign(self):
        self.w = self.origin.rect[2]
        self.h = self.origin.rect[2] * 0.3
        self.clr = Brighten(SE_colour_set.get(self.Effect),40)
        self.d = 0
        self.r = 0
        self.l = 3

    def Quicken_Update(self):
        self.d = (self.d + 2)%360

        if self.origin.Quicken:
            if self.r < 1:
                self.r += 0.05
                if self.r > 1:
                    self.r = 1
        else:
            if self.r <= 0:
                self.remove()
            else:
                self.r -= 0.05

    def Quicken_Back(self):
        pts = []
        for i in range(5):
            pts.append([self.origin.rect.centerx + cos(radians(self.d + i * 72)) * self.w * self.r,
                        self.origin.rect.bottom + sin(radians(self.d + i * 72)) * self.h * self.r])
            pts.append([self.origin.rect.centerx + cos(radians(self.d + i * 72 + 36)) * self.w * 0.6 * self.r,
                        self.origin.rect.bottom + sin(radians(self.d + i * 72 + 36)) * self.h * 0.6 * self.r])
        pygame.draw.polygon(game_window,self.clr,pts,width = self.l)

    def Quicken_Front(self):
        pass

    def Regeneration_Assign(self,SCD = 0):
        self.centerx = self.origin.rect.centerx
        self.centery = self.origin.rect.centery
        self.loop = 0
        self.w = self.origin.rect[2]
        self.h = self.w * 0.3
        self.d = SCD * 72
        self.f_pts = []
        self.b_pts = []
        self.clr = (167,255,163)#(245,163,255)

    def Regeneration_Update(self):
        def R_CheckFB(d,c):
            d = d % 360
            if 0 < d < 180:
                self.b_pts.append(c)
            else:
                self.f_pts.append(c)

        if self.origin.Regeneration:
                
            self.d = (self.d + 2)%360
            self.centerx = self.origin.rect.centerx
            self.centery = self.origin.rect.top
            self.f_pts = []
            self.b_pts = []

            self.n = self.origin.GetSETimer(self.Effect)
            self.a = 360/self.n
            rect = pygame.Rect(0,0,3,3)
            for h in range(self.n):
                rect.center = self.centerx + cos(radians(self.d + h * self.a)) * self.w,self.centery - sin(radians(self.d + h * self.a)) * self.h
                pts = [[rect.left - 3,rect.bottom],[rect.left,rect.bottom],[rect.left,rect.bottom + 3],
                       [rect.right,rect.bottom + 3],[rect.right,rect.bottom],[rect.right + 3,rect.bottom],
                       [rect.right + 3,rect.top],[rect.right,rect.top],[rect.right,rect.top - 3],
                       [rect.left,rect.top - 3],[rect.left,rect.top],[rect.left - 3,rect.top],]
                R_CheckFB(self.d + h * self.a,pts)
        else:
            self.remove()

    def Regeneration_Back(self):
        for i in self.b_pts:
            #if len(i) > 2:
            pygame.draw.polygon(game_window,self.clr,i)

    def Regeneration_Front(self):
        for i in self.f_pts:
            #if len(i) > 2:
            pygame.draw.polygon(game_window,self.clr,i)

    def Invincible_Assign(self,SCD = 0):
        self.centerx = self.origin.rect.centerx
        self.centery = self.origin.rect.centery
        self.loop = 0
        self.w = self.origin.rect[2]/2 + 15
        self.s = 0
        self.d = SCD * 72
        self.f_pts = []
        self.b_pts = []
        self.colour = (136,241,219)
        self.b_colour = Darken(self.colour,5)
        self.n = self.origin.GetSEValue(self.Effect)

    def Invincible_Update(self):
        def R_CheckFB(d,c,n):
            if d % 180 == 0:
                self.f_pts[n].append(c)
                self.b_pts[n].append(c)
            elif 0 < d % 360 < 180:
                self.b_pts[n].append(c)
            else:
                self.f_pts[n].append(c)

        self.d = (self.d + 2)%360
        self.centerx = self.origin.rect.centerx
        self.centery = self.origin.rect.centery - 5
        self.f_pts = []
        self.b_pts = []
        self.h = self.w * 0.3

        self.a = 360/self.n
        for h in range(self.n):
            self.f_pts.append([])
            self.b_pts.append([])
            for i in range(4): 
                x = self.centerx + cos(radians(self.d + h * self.a)) * self.w + cos(radians(i * 90 + self.d)) * 7 * self.s
                y = self.centery + 5 - sin(radians(self.d + h * self.a)) * 5 + sin(radians(i * 90 + self.d)) * 7 * self.s# + self.h * i[1]
                R_CheckFB(self.d + h * self.a,[x,y],h)
                x = self.centerx + cos(radians(self.d + h * self.a)) * self.w + cos(radians(i * 90 + 45 + self.d)) * 3 * self.s
                y = self.centery + 5 - sin(radians(self.d + h * self.a)) * 5 + sin(radians(i * 90 + 45 + self.d)) * 3 * self.s# + self.h * i[1]
                R_CheckFB(self.d + h * self.a,[x,y],h)
            
        if self.origin.Invincible:
            self.n = self.origin.GetSEValue(self.Effect)
            if self.s < 1:#self.mw > self.w:
                self.s += 0.05
                if self.s >= 1:
                    self.s == 1
        else:
            if self.s > 0:
                self.s -= 0.05
            else:
                self.remove()

    def Invincible_Back(self):
        for i in self.b_pts:
            if len(i) > 2:
                pygame.draw.polygon(game_window,self.b_colour,i)
            elif len(i) > 1:
                pygame.draw.lines(game_window,self.b_colour,False,i)

    def Invincible_Front(self):
        for i in self.f_pts:
            if len(i) > 2:
                pygame.draw.polygon(game_window,self.colour,i)
            elif len(i) > 1:
                pygame.draw.lines(game_window,self.colour,False,i)

    def Invisible_Assign(self, SCD = 0):
        self.loop = -SCD * 25
        self.shrink = False
        self.clr = GetEtherClr()
        self.r = RoundUp(self.origin.rect[2] * randint(20,30)/100)
        self.offx = self.origin.rect[2] * randint(0,6)/10 * GenPN()
        self.offy = self.origin.rect[3] * randint(3,6)/10

    def Invisible_Update(self):
        if self.loop < 0:
            self.loop += 1
        elif self.shrink:
            self.loop -= 1
            self.offy -= 0.5
            if self.loop == 0:
                if self.origin.Invisible:
                    self.Invisible_Assign()
                else:
                    self.remove()
        else:
            self.loop += 2
            self.offy -= 0.2
            if self.loop == 100:
                self.shrink = True

    def Invisible_Back(self):
        pass

    def Invisible_Front(self):
        if self.loop > 0:
            r = self.r * self.loop/100
            pygame.draw.circle(game_window,self.clr,[self.origin.rect.centerx + self.offx,self.origin.rect.centery + self.offy],r)
            if r > 2:
                pygame.draw.circle(game_window,(255,255,255),[self.origin.rect.centerx + self.offx,self.origin.rect.centery + self.offy],r - 2)
                
    def Reflect_Assign(self):
        self.centerx = self.origin.rect.centerx
        self.centery = self.origin.rect.centery
        self.loop = 0
        self.w = self.origin.rect[2] * 0.8
        self.h = self.w
        self.colour = (162,231,255)
        self.b_colour = Darken(self.colour,30)
        self.d = 0
        self.s = 0

    def Reflect_Update(self):
        self.centerx = self.origin.rect.centerx
        self.centery = self.origin.rect.centery# - 5

        self.d = (self.d + 1)%90
        if not self.origin.Reflect:#self.Effect not in self.origin.StatusEffect:
            self.s -= 0.1
            if self.s <= 0:
                self.remove()
        elif self.s <= 1:
            self.s += 0.1
            if self.s >= 1:
                self.s = 1
                
    def Reflect_Back(self):
        pass

    def Reflect_Front(self):
        pts,m_pts = [],[]
        for i in [[-1,0.7],[-0.5,0.8],[0,1],[0.5,0.8],[1,0.7],[0.8,-0.3],[0.6,-0.7],[0.3,-0.9],[0,-1],[-0.3,-0.9],[-0.6,-0.7],[-0.8,-0.3]]:    
            x = self.w * i[0] * self.s
            y = -self.h * i[1] * (2 - self.s)
            pts.append([self.centerx + x,self.centery + y])
            m_pts.append([self.centerx + x * sin(radians(self.d)),self.centery + y * sin(radians(self.d))])
        pygame.draw.polygon(game_window,self.colour,m_pts,width = 1)
        pygame.draw.polygon(game_window,self.colour,pts,width = 3)

    def Thorns_Assign(self):
        self.centerx = self.origin.rect.left
        self.centery = self.origin.rect.bottom + 2
        self.loop = 0
        self.w = self.origin.rect[2] * 0.2
        self.colour = SE_colour_set.get(self.Effect)
        self.s = 0
##        for i in range(5):
##            t = self.fm.tiles[self.origin.y][self.origin.x]
##            Explosion(t,randint(10,15),30 + i * 30,[t.t_clr,t.s_clr,t.e_clr][randint(0,2)],spd = randint(1,2),grow = randint(2,4),start = randint(1,5),a = 160)

    def Thorns_Update(self):
        self.centerx = self.origin.rect.left
        self.centery = self.origin.rect.bottom + 2

        self.loop = (self.loop + 1)%180
        if not self.origin.Thorns:#self.Effect not in self.origin.StatusEffect:
            self.s -= 0.05
            if self.s <= 0:
                self.remove()
        elif self.s <= 1:
            self.s += 0.05
            if self.s >= 1:
                self.s = 1
                
    def Thorns_Back(self):
        pass

    def Thorns_Front(self):
        pos = [self.origin.rect.left,self.origin.rect.centerx,self.origin.rect.right]
        for j in range(3):
            pts = []
            for i in [[-1,0],[-0.5,0.2],[-0.75,0.4],[0.3,0.6],[0.2,0.4],[0.8,0.2],[0.4,0]]:    
                if j % 2 == 0:
                    x = pos[j] + self.w * i[0]
                    y = -self.origin.rect[3] * i[1] * (1 + sin(radians(self.loop)) * 0.4) * self.s
                else:
                    x = pos[j] - self.w * i[0]
                    y = 3-self.origin.rect[3] * i[1] * (1 + (1 - sin(radians(self.loop))) * 0.4) * self.s
                pts.append([x,self.centery + y])
            pygame.draw.polygon(game_window,self.colour,pts)

#Tile Status Effects
def ApplyTileSEV(tile,effect,turn):
    if effect in tile.StatusEffect:
        tile.EffectTimer[tile.StatusEffect.index(effect)] += turn
    else:
        tile.StatusEffect.append(effect)
        tile.EffectTimer.append(turn)
        tile.SEVisual.append(False)

class TileStatusEffectVisual():
    def __init__(self,original,effect, SCD = None):
        self.Effect = effect
        self.origin = original
        self.loop = 0
        self.Delete = False
        self.fm = tile_sprites.sprites()[0]

        self.origin.visual_sprites.append(self)
        if SCD:
            eval("self."+self.Effect.replace(" ","")+"_Assign(SCD)")
        else:
            eval("self."+self.Effect.replace(" ","")+"_Assign()")
    
    def update(self):
        eval("self."+self.Effect.replace(" ","")+"_Update()")

    def draw_b(self):
        eval("self."+self.Effect+"_Back()")

    def draw_f(self):
        eval("self."+self.Effect+"_Front()")

    def remove(self):
        self.origin.visual_sprites.remove(self)
        del self

    def GetAdjacents(self, xh = False):
        adjs = [self.GetTop(xh),self.GetRight(xh),self.GetBottom(xh),self.GetLeft(xh)]
        return adjs

    def GetTop(self, xh = False):
        if self.origin.y > 0:
            t = self.fm.tiles[self.origin.y - 1][self.origin.x]
            if (xh or self.origin.h <= t.h) and self.Effect in t.StatusEffect:
                return False
        return True

    def GetBottom(self, xh = False):
        if self.origin.y < self.fm.d[1] - 1:
            t = self.fm.tiles[self.origin.y + 1][self.origin.x]
            if (xh or self.origin.h <= t.h) and self.Effect in t.StatusEffect:
                return False
        return True

    def GetLeft(self, xh = False):
        if self.origin.x > 0:
            t = self.fm.tiles[self.origin.y][self.origin.x - 1]
            if (xh or self.origin.h <= t.h) and self.Effect in t.StatusEffect:
                return False
        return True

    def GetRight(self, xh = False):
        if self.origin.x < self.fm.d[0] - 1:
            t = self.fm.tiles[self.origin.y][self.origin.x + 1]
            if (xh or self.origin.h <= t.h) and self.Effect in t.StatusEffect:
                return False
        return True

    def GetAdjacents_AH(self): #ACCOUNTS ALL HEIGHTS
        adjs = [self.GetTop_AH(),self.GetRight_AH(),self.GetBottom_AH(),self.GetLeft_AH()]
        return adjs

    def GetTop_AH(self):
        if self.origin.y > 0:
            t = self.fm.tiles[self.origin.y - 1][self.origin.x]
            if self.origin.h == t.h and self.Effect in t.StatusEffect:
                return False
        return True

    def GetBottom_AH(self):
        if self.origin.y < self.fm.d[1] - 1:
            t = self.fm.tiles[self.origin.y + 1][self.origin.x]
            if self.origin.h == t.h and self.Effect in t.StatusEffect:
                return False
        return True

    def GetLeft_AH(self):
        if self.origin.x > 0:
            t = self.fm.tiles[self.origin.y][self.origin.x - 1]
            if self.origin.h == t.h and self.Effect in t.StatusEffect:
                return False
        return True

    def GetRight_AH(self):
        if self.origin.x < self.fm.d[0] - 1:
            t = self.fm.tiles[self.origin.y][self.origin.x + 1]
            if self.origin.h == t.h and self.Effect in t.StatusEffect:
                return False
        return True

    def Burn_Assign(self, SCD = 0):
        self.h = randint(30,70)#self.origin.rect[3] - 10 + randint(0,20)
        self.by = -randint(0,4)
        self.loop = -5 * SCD
        self.clr = (randint(235,255),randint(0,120),0)
        self.ox = -5 + randint(0,30)#-self.origin.rect[2]/2 - 3 + randint(0,self.origin.rect[2] + 6)
        self.r = 0
        self.max_r = randint(6,8)
        self.lp = self.max_r

    def Burn_Update(self):
        if self.loop < 0:
            self.loop += 1
        elif self.lp > 0:
            self.by += 1
            self.lp -= 1
            self.r = self.max_r - self.lp
        elif self.loop < 20:
            self.loop += 1
            if self.loop > 10:
                self.r = self.max_r * (20 - self.loop)/10
        else:
            if self.origin.Burn:
                self.Burn_Assign()
            else:
                self.remove()

    def Burn_Back(self):
        pass

    def Burn_Front(self):
        if self.loop >= 0:
            pygame.draw.circle(game_window,self.clr,[self.origin.rect.centerx + self.ox, self.origin.rect.bottom - self.by - self.h * self.loop/20],self.r)
##    def Burn_Assign(self):
##        self.aph = 20
##        self.ash = 15
##        self.bph = 8
##        self.bsh = 6
##        self.base = 0
##        self.a_clr = (252,100,0)
##        self.b_clr = (250,192,0)
##
##    def Burn_Update(self):
##        if self.Delete:
##            if self.base > 0:
##                self.base -= 0.25
##                self.loop += 1
##            else:
##                self.remove()
##        else:
##            self.loop += 2
##            if self.base < 4:
##                self.base += 0.5
##            if self.loop >= 160:
##                if self.Effect in self.origin.StatusEffect:
##                    self.loop = 20
##                else:
##                    self.Delete = True
##
##    def Burn_Back(self):
##        c = sin(radians(self.loop))
##        w = (self.origin.br[0] - self.origin.bl[0])/5
##        m = CorInt(w/2)
##        a_pts = [self.origin.tr,self.origin.tl]
##        b_pts = [self.origin.tr,self.origin.tl]
##        for i in range(5):
##            h = self.aph if i % 2 == 0 else self.ash
##            a_pts.append([self.origin.tl[0] + w * i + m, self.origin.tl[1] - self.base - h * c])
##            a_pts.append([self.origin.tl[0] + w * (i + 1), self.origin.tl[1] - self.base])
##            h = self.bph if i % 2 == 0 else self.bsh
##            b_pts.append([self.origin.tl[0] + w * i + m, self.origin.tl[1] - self.base - h * c])
##            b_pts.append([self.origin.tl[0] + w * (i + 1), self.origin.tl[1] - self.base])
##        pygame.draw.polygon(game_window,self.a_clr,a_pts)
##        pygame.draw.polygon(game_window,self.b_clr,b_pts)
##        w = self.fm.h/10
##        pygame.draw.lines(game_window,self.a_clr,False,[self.origin.bl,[self.origin.tl[0],self.origin.tl[1] - self.base],[self.origin.tl[0],self.origin.tl[1] + w - self.aph * c - self.base]])
##        pygame.draw.lines(game_window,self.a_clr,False,[self.origin.br,[self.origin.tr[0],self.origin.tr[1] - self.base],[self.origin.tr[0],self.origin.tl[1] + w - self.aph * c - self.base]])
##
##    def Burn_Front(self):
##        if self.GetBottom():
##            a_pts = [self.origin.br,self.origin.bl]
##            b_pts = [self.origin.br,self.origin.bl]
##            c = sin(radians(self.loop))
##            w = (self.origin.br[0] - self.origin.bl[0])/5
##            m = CorInt(w/2)
##            for i in range(5):
##                h = self.aph if i % 2 == 0 else self.ash
##                a_pts.append([self.origin.bl[0] + w * i + m, self.origin.bl[1] - self.base - h * c])
##                a_pts.append([self.origin.bl[0] + w * (i + 1), self.origin.bl[1] - self.base])
##                h = self.bph if i % 2 == 0 else self.bsh
##                b_pts.append([self.origin.bl[0] + w * i + m, self.origin.bl[1] - self.base - h * c])
##                b_pts.append([self.origin.bl[0] + w * (i + 1), self.origin.bl[1] - self.base])
##            pygame.draw.polygon(game_window,self.a_clr,a_pts)
##            pygame.draw.polygon(game_window,self.b_clr,b_pts)

    def Freeze_Assign(self, SCD = 0):
        self.clr = (randint(190,230),randint(230,245),255)
        self.ox = -10 + randint(0,20)
        self.oy = randint(0,10)
        self.r = randint(3,5)
        self.h = randint(25,40)
        self.d = randint(1,360)

        self.s = randint(3,4)
        self.a = 360/(self.s*2)

        self.loop = self.h + 15 * SCD
        
        self.adjs = [False,False,False,False]

    def Freeze_Update(self):
        self.d = (self.d + 1)%360
        if self.loop > 0:
            self.loop -= 0.75
        else:
            if self.r > 0:
                self.r -= 0.5
            elif self.Effect in self.origin.StatusEffect:
                self.Freeze_Assign()
            else:
                self.remove()

    def Freeze_Back(self):
        pass

    def Freeze_Front(self):
        if self.loop <= self.h:
            for i in range(self.s):
                pygame.draw.line(game_window,self.clr,
                                 [self.origin.centerx + self.ox + cos(radians(self.d + i * self.a)) * self.r,
                                  self.origin.centery + self.oy - self.loop - sin(radians(self.d + i * self.a)) * self.r],
                                 [self.origin.centerx + self.ox + cos(radians(self.d + i * self.a + 180)) * self.r,
                                  self.origin.centery + self.oy - self.loop - sin(radians(self.d + i * self.a + 180)) * self.r],width = 1)

    def Shock_Assign(self):
        self.base = 0
        self.loop = -1
        self.y_clr = (255,247,0)
        self.b_clr = (0,228,255)
        self.ty_pts = []
        self.tb_pts = []
        self.ry_pts = []
        self.rb_pts = []
        self.by_pts = []
        self.bb_pts = []
        self.ly_pts = []
        self.lb_pts = []
        
        self.adjs = [False,False,False,False]

    def Shock_Update(self):
        if self.Delete:
            if self.base > 0:
                self.base -= 0.1
                self.loop = (self.loop + 1)%90
            else:
                self.remove()
        else:
            if self.base < 3:
                self.base += 0.2
            if self.Effect in self.origin.StatusEffect:
                self.loop = (self.loop + 1)%90
                self.adjs = self.GetAdjacents()#_AH()
            else:
                self.Delete = True

    def Shock_Back(self):
        if self.loop % 5 == 0:
            if self.adjs[0]:
                self.ty_pts = []
                self.tb_pts = []
                for i in range(1,int((self.fm.w)//4)):
                    self.ty_pts.append(-self.base + randint(0,int(self.base * 2)))
                    self.tb_pts.append(-self.base + randint(0,int(self.base * 2)))
            if self.adjs[1]:
                self.ry_pts = []
                self.rb_pts = []
                for i in range(1,int(self.fm.w//4)):
                    self.ry_pts.append(-self.base + randint(0,int(self.base * 2)))
                    self.rb_pts.append(-self.base + randint(0,int(self.base * 2)))
            if self.adjs[2]:
                self.by_pts = []
                self.bb_pts = []
                for i in range(1,int(self.fm.w//4)):
                    self.by_pts.append(-self.base + randint(0,int(self.base * 2)))
                    self.bb_pts.append(-self.base + randint(0,int(self.base * 2)))
            if self.adjs[3]:
                self.ly_pts = []
                self.lb_pts = []
                for i in range(1,int(self.fm.w//4)):
                    self.ly_pts.append(-self.base + randint(0,int(self.base * 2)))
                    self.lb_pts.append(-self.base + randint(0,int(self.base * 2)))
                
        if self.adjs[0]:
            a_pts = [self.origin.tl]
            b_pts = [self.origin.tl]
            for i in range(1,len(self.ty_pts)):
                a_pts.append([self.origin.tl[0] + i * 4,self.origin.tl[1] + self.ty_pts[i-1]])
                b_pts.append([self.origin.tl[0] + i * 4,self.origin.tl[1] + self.tb_pts[i-1]])
            a_pts.append(self.origin.tr)
            b_pts.append(self.origin.tr) 
            pygame.draw.lines(game_window,self.y_clr,False,a_pts,width = 2)
            pygame.draw.lines(game_window,self.b_clr,False,b_pts,width = 2)
        if self.adjs[1]:
            c = self.fm.h/self.fm.w
            a_pts = [self.origin.tr]
            b_pts = [self.origin.tr]
            for i in range(1,len(self.ry_pts)):
                a_pts.append([self.origin.tr[0] + self.ry_pts[i-1],self.origin.tr[1] + i * 4 * c])
                b_pts.append([self.origin.tr[0] + self.rb_pts[i-1],self.origin.tr[1] + i * 4 * c])
            a_pts.append(self.origin.br)
            b_pts.append(self.origin.br) 
            pygame.draw.lines(game_window,self.y_clr,False,a_pts,width = 2)
            pygame.draw.lines(game_window,self.b_clr,False,b_pts,width = 2)
        if self.adjs[2]:
            a_pts = [self.origin.bl]
            b_pts = [self.origin.bl]
            for i in range(1,len(self.by_pts)):
                a_pts.append([self.origin.bl[0] + i * 4,self.origin.bl[1] + self.by_pts[i-1]])
                b_pts.append([self.origin.bl[0] + i * 4,self.origin.bl[1] + self.bb_pts[i-1]])
            a_pts.append(self.origin.br)
            b_pts.append(self.origin.br) 
            pygame.draw.lines(game_window,self.y_clr,False,a_pts,width = 2)
            pygame.draw.lines(game_window,self.b_clr,False,b_pts,width = 2)
        if self.adjs[3]:
            c = self.fm.h/self.fm.w
            a_pts = [self.origin.tl]
            b_pts = [self.origin.tl]
            for i in range(1,len(self.ly_pts)):
                a_pts.append([self.origin.tl[0] + self.ly_pts[i-1],self.origin.tl[1] + i * 4 * c])
                b_pts.append([self.origin.tl[0] + self.lb_pts[i-1],self.origin.tl[1] + i * 4 * c])
            a_pts.append(self.origin.bl)
            b_pts.append(self.origin.bl) 
            pygame.draw.lines(game_window,self.y_clr,False,a_pts,width = 2)
            pygame.draw.lines(game_window,self.b_clr,False,b_pts,width = 2)

    def Shock_Front(self):
        pass

    def Splash_Assign(self, SCD = 0):
        self.loop = -7 * SCD
        self.clr = (130,randint(195,250),255)
        self.ox = -self.fm.w/2 - 3 + randint(0,self.fm.w + 6)
        self.oy = randint(0,15)#-self.fm.h/2 - 3 + randint(0,self.fm.h + 6)
        self.r = 0#randint(3,4)
        self.tr = randint(4,6)

    def Splash_Update(self):
        self.loop += 1
        if self.r < self.tr:
            self.r += 0.3
        elif self.Effect in self.origin.StatusEffect:
            self.Splash_Assign()
        else:
            self.remove()

    def Splash_Back(self):
        pass

    def Splash_Front(self):
        if self.loop >= 0:
            if self.tr - self.r < 0.6:
                pygame.draw.circle(game_window,self.clr,[self.origin.centerx + self.ox, self.origin.bl[1] - self.oy - self.loop],self.r,width = 1)
            else:
                pygame.draw.circle(game_window,self.clr,[self.origin.centerx + self.ox, self.origin.bl[1] - self.oy - self.loop],self.r,width = 2)
        
    def Poison_Assign(self, SCD = 0):
        self.loop = -10 * SCD
        self.clr = (95,185,90)
        self.ox = -10 + randint(0,20)
        self.oy = randint(0,10)
        self.r = randint(3,5)
        self.h = randint(25,40)
        
        self.adjs = [False,False,False,False]

    def Poison_Update(self):
        if self.loop < self.h:
            self.loop += 1
        elif self.loop == self.h:
            if self.r > 0:
                self.r -= 0.5
            elif self.Effect in self.origin.StatusEffect:
                self.Poison_Assign()
            else:
                self.remove()

    def Poison_Back(self):
        pass

    def Poison_Front(self):
        if self.loop >= 0:
            pygame.draw.circle(game_window,self.clr,[self.origin.centerx + self.ox, self.origin.centery + self.oy - self.loop],self.r)

    def Drain_Assign(self, SCD = 0):
        self.loop = -35 * SCD
        self.sx = -10 + randint(0,20)
        self.sy = randint(0,10) * GenPN()
        self.ex = self.sx
        self.ey = self.sy
        self.l = randint(4,6) * 5
        self.h = 70 - self.l
        self.clr = SE_colour_set.get("Drain")
        self.spd = 2

    def Drain_Update(self):
        self.loop += self.spd
        if self.loop >= self.l + self.h:
            if self.Effect in self.origin.StatusEffect:
                self.Drain_Assign()
            else:
                self.remove()
        elif self.loop >= 0:
            if self.loop < self.l:
                self.ey -= self.spd
            elif self.loop < self.h:
                self.ey -= self.spd
                self.sy -= self.spd
            else:
                self.sy -= self.spd

    def Drain_Back(self):
        pass

    def Drain_Front(self):
        if self.loop >= 0:
            pygame.draw.polygon(game_window,self.clr,[[self.origin.centerx + self.sx - 1,self.origin.centery + self.sy],
                                                      [self.origin.centerx + self.sx,self.origin.centery + self.sy + 1],
                                                      [self.origin.centerx + self.sx + 1,self.origin.centery + self.sy],
                                                      [self.origin.centerx + self.ex + 1,self.origin.centery + self.ey],
                                                      [self.origin.centerx + self.ex,self.origin.centery + self.ey - 1],
                                                      [self.origin.centerx + self.ex - 1,self.origin.centery + self.ey]])

    def Blind_Assign(self, SCD = 0):
        self.loop = randint(0,180)
        self.clr = SE_colour_set.get("Blind")
        self.base = 0
        self.surface = pygame.Surface((self.origin.br[0] - self.origin.bl[0] + 1,self.origin.bl[1] - self.origin.tl[1] + 1)).convert_alpha()
        self.rect = self.surface.get_rect()
        self.surface.fill(self.clr)
        self.p_w,self.p_h = self.fm.w,self.fm.h
        self.surfaces = [None]
        self.rects = [None]
        self.s = 4
        for i in range(1,self.s + 1):
            self.surfaces.append(pygame.Surface((self.fm.w,i)).convert_alpha())
            self.surfaces[i].fill(self.clr)
            self.rects.append(self.surfaces[i].get_rect())
            

    def Blind_Update(self):
        if self.Effect in self.origin.StatusEffect:
            if self.base == 150:
                self.loop = (self.loop + 2)%180
            else:
                self.base += 5
            if self.p_h != self.fm.h or self.p_w != self.fm.w:
                self.surface = pygame.Surface((self.origin.br[0] - self.origin.bl[0] + 1,self.origin.bl[1] - self.origin.tl[1] + 1)).convert_alpha()
                self.surface.fill(self.clr)
                self.rect = self.surface.get_rect()
        else:
            if self.loop < 180:
                self.loop += 5
                if self.loop > 180:
                    self.loop = 180
            elif self.base > 0:
                self.base -= 5
            else:
                self.remove()

    def Blind_Back(self):
        s = sin(radians(self.loop))
        self.surface.set_alpha(self.base + int(60 * s))
        self.rect.left = self.origin.bl[0] + 1
        self.rect.centery = self.origin.centery - self.s * s
        game_window.blit(self.surface,self.rect)
        n = RoundUp(self.s * s)
        if n > 0:
            self.surfaces[n].set_alpha(self.base + int(60 * s))
            self.rects[n].left = self.rect.left
            self.rects[n].top = self.rect.bottom
            game_window.blit(self.surfaces[n],self.rects[n])
        

    def Blind_Front(self):
        pass
