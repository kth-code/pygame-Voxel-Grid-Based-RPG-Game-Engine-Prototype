import pygame
from VoxelGame_BaseVars import *
from VoxelGame_Visuals import *
from VoxelGame_Icons import *

class Dialogue_Box(pygame.sprite.Sprite):
    def __init__(self,origin,name_txt,txt,clr,extra_clr = [],imgs = []): #Displayer Mode: 0 - Within Boundary Box, 1 - Full
        pygame.sprite.Sprite.__init__(self)
        self.width = window_width * 11/15
        self.bottom = window_height + 50
        self.name_font = title_font30
        self.word_font = game_font18
        self.title_font = stat_font20
        self.name_txt = name_txt
        self.txt = txt
        self.txts = []
        self.clr = clr
        self.extra_clr = extra_clr
        self.imgs = imgs

        self.origin = origin
        self.prev_mode = self.origin.mode
        self.origin.mode = -2
        self.origin.visual_sprites.append(self)

        self.CD = 0
        self.loop = 0
        self.deloop = 0
        self.new = False
        self.up = False
        self.spd = 24

        self.rect = pygame.Rect((0,0,self.width,200))
        self.rect.centerx = window_width/2
        self.rect.bottom = self.bottom

        self.load_page(0)
            
    def load_page(self,p):
        self.page = p
        self.name = self.name_font.render(self.name_txt[p],True,self.clr[p][0])
        self.name_rect = self.name.get_rect()
        self.name_rect.left = self.rect.left + 10
        
        self.word_lp = 0
        
        self.count = 0
        self.max_count = len(self.txt[p])

    def set_text(self,text):
        self.txts = []
        c_t = ""
        t = ""
        d = text.split()
        c = 0
        r = 0
        img_w = 0
        while c < len(d):
            c_t = ""
            img_w = 0
            self.txts.append([])
            while self.word_font.size(c_t)[0] < self.width - 20 and c < len(d):
                if self.word_font.size(c_t + d[c])[0] < self.width - 20:
                    self.txts[r].append(d[c] + " ")
                    if "#" in d[c]:
                        img_w += self.imgs[int(d[c][1:])].get_width()
                        if c + 1 < len(d):
                            if d[c+1] not in [".",",","!"]:
                                self.txts[r].append(" ")
                                c_t += " "
                    elif "@" in d[c]:
                        c_t += d[c][2:] + " "
                    else:
                        c_t += d[c] + " "
                    c += 1
                else:
                    break
            r += 1

    def update(self):
        pass

    def draw(self):
        if not self.new:
            if self.spd > -5:
                self.rect.bottom = self.bottom + (200 - self.loop)
        else:
            enact = True
            if self.page + 1 < len(self.name_txt):
                if self.name_txt[self.page] == self.name_txt[self.page + 1]:
                    self.deloop = 0
                    self.load_page(self.page+1)
                    self.new = False
                    enact = False
            if enact:
                self.rect.bottom = self.bottom + (200 - self.deloop)
                if self.deloop > 0:
                    self.deloop -= self.spd
                    self.spd += 1
                else:
                    self.origin.mode = self.prev_mode
                    self.origin.visual_sprites.remove(self)
                    self.kill()
                    del self
                    return
        self.name_rect.centery = self.rect.top - 2
        DrawRoundFrame(self.rect,(85,84,88))
        if len(self.name_txt[self.page]) > 0:
            DrawTextFrame(self.name_rect,self.clr[self.page][1])
            game_window.blit(self.name,self.name_rect)
        x = 0
        y = 0
        keystate = pygame.key.get_pressed()
        if self.CD > 0:
            self.CD -= 1
        elif keystate[pygame.K_z] and self.up:
            if self.count < self.max_count:
                self.count = self.max_count
                self.set_text(self.txt[self.page])
            else:
                self.new = True
                self.CD += 10
                if self.page + 1 < len(self.name_txt):
                    self.load_page(self.page+1)
                    self.new = False
                else:
                    self.deloop = self.loop
            self.CD += 10
        if self.count < self.max_count:
            text = self.title_font.render("Skip",True,(255,255,255))
        elif self.page + 1 == len(self.name_txt):
            text = self.title_font.render("Close",True,(255,255,255))
        else:
            text = self.title_font.render("Next",True,(255,255,255))
        textRect = text.get_rect()
        textRect.right = self.rect.right - 8
        textRect.bottom = self.rect.bottom - 5
        game_window.blit(text,textRect)
        img = key_icon_z
        rect = img.get_rect()
        rect.right = textRect.left - 5
        rect.centery = textRect.centery
        game_window.blit(img,rect)
        if not self.new:
            if self.up:
                if self.count < self.max_count and self.word_lp == 0:
                    self.count += 1
                    if self.txt[self.page][self.count-1:self.count] == "#":
                        while self.txt[self.page][self.count-1:self.count] != " ":
                            self.count += 1
                    elif self.txt[self.page][self.count-1:self.count] == "@":
                        self.count += 2
                    self.set_text(self.txt[self.page][0:self.count])
                self.word_lp = (self.word_lp + 1) % 3
                for i in self.txts:
                    for j in i:
                        if "#" in j:
                            text = self.word_font.render("",True,(0,0,0))
                            textRect = text.get_rect()
                            textRect.left = self.rect.left + 10 + x
                            textRect.top = self.rect.top + 30 + y
                            img = self.imgs[int(j[1:])]
                            rect = img.get_rect()
                            rect.left = self.rect.left + 10 + x
                            rect.centery = textRect.centery
                            game_window.blit(img,rect)
                            x += rect[2]
                            text = self.word_font.render("",True,(255,255,255))
                        elif "@" in j:
                            text = self.word_font.render(j[2:],True,self.extra_clr[int(j[1:2])])
                        else:
                            text = self.word_font.render(j,True,(255,255,255))
                        textRect = text.get_rect()
                        textRect.left = self.rect.left + 10 + x
                        textRect.top = self.rect.top + 30 + y
                        game_window.blit(text,textRect)
                        x += textRect[2]
                    x = 0
                    y += 30
            elif self.spd > -5:
                self.spd -= 1
                self.loop += self.spd
                if self.spd == -5:
                    self.up = True
