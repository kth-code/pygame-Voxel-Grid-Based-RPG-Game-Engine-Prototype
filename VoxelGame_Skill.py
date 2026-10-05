import pygame
from random import *
from math import *
from VoxelGame_BaseVars import *
from VoxelGame_Visuals import *
from VoxelGame_ATKProjectiles import *

from VoxelGame_Icons import *

font = game_font18
class Skill():
    def __init__(self):
        self.use_cd = 20
        self.draw_lp = 200
        self.desc_lp = 0
        self.no_tar_msg = "! NO TARGETS IN RANGE !"

    def Text_Sort(self):
        w = window_width * 8/15
        r = 0
        txt = []
        self.desc_w = []
        for i in range(len(self.desc)):
            c_t,t = "",""
            d = self.desc[i].split()
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
                self.desc_w.append(font.size(c_t)[0] + img_w)
                r += 1
        self.desc = list(txt)

    def Set_Instructions(self):
        y = window_height - 10
        text = title_font20.render("Back",True,(255,255,255))
        textRect = text.get_rect()
        i_rect = key_icon_0.get_rect()
        textRect.bottom = y
        i_rect.left = 10
        i_rect.centery = textRect.centery
        textRect.left = i_rect.right + 5
        self.back_instructions = [text,textRect,key_icon_0,i_rect]
        y -= textRect[3] + 10

        self.instructions = []
        
        text = title_font20.render("Confirm",True,(255,255,255))
        textRect = text.get_rect()
        i_rect = key_icon_0.get_rect()
        textRect.bottom = y
        i_rect.left = 10
        i_rect.centery = textRect.centery
        textRect.left = i_rect.right + 5
        self.instructions.append([text,textRect,key_icon_z,i_rect])
        y -= textRect[3] + 10

    def Unload_Instructions(self):
        self.fm.RemoveInstructions(self.back_instructions)
        for i in self.instructions:
            self.fm.RemoveInstructions(i)

    def DrawOptions(self, lp = True):
        if lp and self.draw_lp > 0:
            self.draw_lp -= 10
    
        if len(self.p_tar) > 0:
            self.DrawDesc()
        else:
            self.DrawNoTarget()

    def DrawDesc(self):  
        rect = pygame.Rect(0,0,window_width * 8/15, window_height * 3/20)
        rect.centerx = window_width/2
        rect.bottom = window_height - 30 + self.draw_lp

        f_clr = (35,39,94)
        clr = (53,57,106)

        pygame.draw.rect(game_window,f_clr,(rect.left,rect.top - 10,rect[2],rect[3] + 20))
        pygame.draw.circle(game_window,f_clr,[rect.left,rect.centery],rect[3]/2+10)
        pygame.draw.circle(game_window,f_clr,[rect.right,rect.centery],rect[3]/2+10)

        pygame.draw.rect(game_window,clr,rect)
        pygame.draw.circle(game_window,clr,[rect.left,rect.centery],rect[3]/2)
        pygame.draw.circle(game_window,clr,[rect.right,rect.centery],rect[3]/2)
        
        y = rect.top + 10
        text = title_font30.render(self.name,True,(255,255,255))
        textRect = text.get_rect()
        textRect.centerx = rect.centerx
        textRect.top = y
        game_window.blit(text,textRect)
        y += textRect[3] + 5

        if self.use_cd > 1:
            img = cd_symbol
            i_rect = img.get_rect()

            if self.use_cd > 1:
                text = stat_font20.render(str(self.use_cd)+" Turns",True,(255,255,255))
            else:
                text = stat_font20.render(str(self.use_cd)+" Turn",True,(255,255,255))
            textRect = text.get_rect()
            
            m_rect = pygame.Rect(0,0,textRect[2] + i_rect[2] + 5,30)
            m_rect.left = rect.left
            m_rect.bottom = rect.top - 20
            
            textRect.right = m_rect.right
            textRect.centery = m_rect.centery
            i_rect.right = textRect.left - 5
            i_rect.centery = m_rect.centery

            DrawRoundFrame(m_rect,clr)
            game_window.blit(text,textRect)
            game_window.blit(img,i_rect)
        
        d_clr = (255,255,255)
        y += textRect[3] + 5

        for i in range(len(self.desc)):
            x = rect.centerx - self.desc_w[i]/2
            for j in self.desc[i]:
                if "#" in j:
                    text = font.render("",True,(0,0,0))
                    textRect = text.get_rect()
                    textRect.left = x
                    textRect.top = y
                    image = self.imgs[int(j[1:])]
                    i_rect = image.get_rect()
                    i_rect.left = x
                    i_rect.centery = textRect.centery
                    game_window.blit(image,i_rect)
                    x += i_rect[2]
                elif "@" in j:
                    if 48 <= ord(j[1:2]) <= 57:
                        text = font.render(j[2:],True,self.colour[int(j[1:2])])
                    else:
                        text = font.render(j[2:],True,self.colour[ord(j[1:2])-87])
                else:
                    text = font.render(j,True,(255,255,255))
                textRect = text.get_rect()
                textRect.left = x
                textRect.top = y
                game_window.blit(text,textRect)
                x += textRect[2]
            y += textRect[3] + 5

        text = game_font16.render("1 Action Pt",True,(255,255,255))
        textRect = text.get_rect()
        m_rect = pygame.Rect((0,0,150,textRect[3]))
        m_rect.right = window_width - 30 + self.draw_lp
        m_rect.bottom = window_height - 30
        DrawSmoothFrame(m_rect,(53,57,106), sn = False)
        textRect.left = m_rect.left + 10
        textRect.bottom = m_rect.bottom
        game_window.blit(text,textRect)
            
        text = stat_font18.render("Cost",True,(255,255,255))
        textRect = text.get_rect()
        textRect.bottom = m_rect.top
        textRect.centerx = m_rect.centerx

        m_rect = pygame.Rect((0,0,m_rect[2],textRect[3]))
        m_rect.centerx = textRect.centerx
        m_rect.bottom = textRect.bottom
        DrawSmoothFrame(m_rect,(35,39,94), ss = False)
        game_window.blit(text,textRect)

    def DrawNoTarget(self):
        rect = pygame.Rect(0,0,window_width * 8/15, window_height * 3/20)
        rect.centerx = window_width/2
        rect.bottom = window_height - 30 + self.draw_lp

        f_clr = (35,39,94)#(203,26,26)
        clr = (53,57,106)#(239,55,55)

        pygame.draw.rect(game_window,f_clr,(rect.left,rect.top - 10,rect[2],rect[3] + 20))
        pygame.draw.circle(game_window,f_clr,[rect.left,rect.centery],rect[3]/2+10)
        pygame.draw.circle(game_window,f_clr,[rect.right,rect.centery],rect[3]/2+10)

        pygame.draw.rect(game_window,clr,rect)
        pygame.draw.circle(game_window,clr,[rect.left,rect.centery],rect[3]/2)
        pygame.draw.circle(game_window,clr,[rect.right,rect.centery],rect[3]/2)

        text = title_font30.render(self.name,True,(203,26,26))
        textRect = text.get_rect()
        textRect.centerx = rect.centerx
        textRect.bottom = rect.centery
        game_window.blit(text,textRect)

        text = title_font30.render(self.no_tar_msg,True,(255,255,255))
        textRect = text.get_rect()
        textRect.centerx = rect.centerx
        textRect.top = rect.centery
        DrawRoundFrame(textRect,(239,55,55))
        game_window.blit(text,textRect)

class Heal_Skill(Skill):
    def __init__(self,origin):
        Skill.__init__(self)
        self.fm = tile_sprites.sprites()[0]
        self.origin = origin
        
        self.heal_rate = 0.3
        self.range = 15
        
        self.p_tar = []
        self.no_tar_msg = "! MAX HEALTH ALREADY !"

        self.cd = 0

    def Get_Target(self):
        self.fm.show_hp = True
        x = self.origin.x
        y = self.origin.y
        r = self.origin.Get_Range(self.ID)

        self.p_tar = GetUnitsInRange(x,y,r,f = [0])

        for i in self.p_tar:
            if i.HP == i.MaxHP:
                self.p_tar.remove(i)
        
        SetBoundaryTiles(x,y,r,c = 4,exclude = [1,2])
        
        self.fm.AddInstructions(self.back_instructions)
        
        if len(self.p_tar) > 0:
            for i in self.p_tar:
                SetTargetTile(i,4)
            self.CalcPntlHeal()
            for i in self.instructions:
                self.fm.AddInstructions(i)

    def CalcPntlHeal(self):
        for i in self.p_tar:
            i.ResetPntl()
        for i in range(len(self.p_tar)):
            self.p_tar[i].Pntl_MinHP += self.p_tar[i].Get_ActualDMG(self.p_tar[i].MaxHP * self.heal_rate, hit_no = 1)
            self.p_tar[i].Pntl_MaxHP += self.p_tar[i].Get_ActualDMG(self.p_tar[i].MaxHP * self.heal_rate, hit_no = 1)
            self.p_tar[i].Pntl_CritHP += self.p_tar[i].Get_ActualDMG(self.p_tar[i].MaxHP * self.heal_rate, hit_no = 1)
  
    def Select_Target(self):
        keystate = pygame.key.get_pressed()
        if len(self.p_tar) > 0:
            if self.cd == 0:
                if keystate[pygame.K_z]:
                    self.cd = 20
                    self.Start()
                elif keystate[pygame.K_0]:
                    self.Unload_Instructions()
                    self.origin.mode = 0
                    ClearAllHighlightTiles()
                    ClearAllBoundaryTiles()
                    ClearAllTargetTiles()
                    self.fm.desc = False
                    self.fm.show_hp = False
            else:
                self.cd -= 1
        elif keystate[pygame.K_0]:
            self.Unload_Instructions()
            self.origin.mode = 0
            ClearAllHighlightTiles()
            ClearAllBoundaryTiles()
            ClearAllTargetTiles()
            self.fm.desc = False
            self.fm.show_hp = False

    def Start(self):
        for i in self.p_tar:
            i.Pntl_MinHP = 0
            i.Pntl_MaxHP = 0
            i.Pntl_CritHP = 0
            i.Pntl_SE = None
            
        ClearAllHighlightTiles()
        ClearAllBoundaryTiles()
        ClearAllTargetTiles()
        MoveDisplay(self.name,clr = faction_clrs[0])

        t = self.fm.tiles[self.origin.y][self.origin.x]
        for i in range(10):
            MagicSpiral(self.fm,t.centerx,t.centery,randint(1,360),colour = Brighten((140,255,150),randint(0,5)*10),spd = 1.5,s_range = self.range * 40 + 20,start = 10,delay = i * -2,flat = True)
            
        for i in self.p_tar:
            i.HPChange(i.MaxHP * self.heal_rate)

        self.fm.show_hp = False
        #self.fm.desc = False

        self.origin.act_record[self.ID] = False
        self.origin.act_CD[self.ID] = self.use_cd
        self.origin.Set_ActPts(-1)
        self.Unload_Instructions()
        self.origin.mode = 0
        
        self.target = []

        if len(self.fm.acting_units) == 0:
            self.fm.a_cd = fps * 1.5


class Heal_30(Heal_Skill):
    def __init__(self,origin,ID = 2):
        Heal_Skill.__init__(self,origin = origin)
        self.name = "Heal"
        self.ID = ID

        self.icon = heal_icon#pygame.transform.scale(SE_Symbols.get("Regeneration"),[35,35])
        self.i_rect = self.icon.get_rect()

        self.range = 4
        self.use_cd = 2
        
        self.desc = ["Restore @030% @0HP to all allies within range."]
        self.short_desc = ["+30% HP"]

        self.imgs = []
        self.colour = [(152,247,160)]

        self.origin.move_type.append("Skill")
        self.origin.move_label.append(self.name)
        self.origin.move_stat.append(False)
        self.origin.move_mlt.append(None)
        self.origin.move_SE.append(None)
        self.origin.move_cd.append(self.use_cd)
        self.origin.move_crit.append(0)
        self.origin.move_range.append([self.range,4])
        self.origin.move_get_tile.append(None)
        self.origin.move_icon.append(self.icon)

        d = list(self.desc)
        for i in range(len(self.imgs)):
            for j in range(len(d)):
                n = len(self.imgs) - 1 - i
                d[j] = d[j].replace("#"+str(n),"#"+str(len(self.origin.imgs)+n))
        for i in range(len(self.colour)):
            for j in range(len(d)):
                n = len(self.colour) - 1 - i
                if n > 9:
                    n = chr(n + 87)
                d[j] = d[j].replace("@"+str(n),"@"+str(len(self.origin.colour)+n))
        self.origin.move_info.append(d)

        self.origin.colour += self.colour
        self.origin.imgs += self.imgs

        self.Text_Sort()
        self.Set_Instructions()

class Apply_Effect(Skill):
    def __init__(self,origin):
        Skill.__init__(self)
        self.fm = tile_sprites.sprites()[0]
        self.origin = origin
        
        self.SE = None
        self.timer = 0
        self.value = None
        self.stack_threshold = None
        
        self.highlight = 5
        self.tar_ally = True
        self.range = 15
        
        self.p_tar = []

        self.cd = 0

    def Get_Target(self):
        x = self.origin.x
        y = self.origin.y
        r = self.origin.Get_Range(self.ID)

        if self.tar_ally:
            self.p_tar = GetUnitsInRange(x,y,r,f = [0])
            SetBoundaryTiles(x,y,r,c = self.highlight,exclude = [1,2])
        else:
            self.p_tar = GetUnitsInRange(x,y,r,f = [1])
            SetBoundaryTiles(x,y,r,c = self.highlight,exclude = [0,2])
        
        self.fm.AddInstructions(self.back_instructions)
        
        if len(self.p_tar) > 0:
            for i in self.p_tar:
                SetTargetTile(i,self.highlight)
            for i in self.instructions:
                self.fm.AddInstructions(i)
  
    def Select_Target(self):
        keystate = pygame.key.get_pressed()
        if len(self.p_tar) > 0:
            if self.cd == 0:
                if keystate[pygame.K_z]:
                    self.cd = 20
                    self.Start()
                elif keystate[pygame.K_0]:
                    self.Unload_Instructions()
                    self.origin.mode = 0
                    ClearAllHighlightTiles()
                    ClearAllBoundaryTiles()
                    ClearAllTargetTiles()
                    self.fm.desc = False
            else:
                self.cd -= 1
        elif keystate[pygame.K_0]:
            self.Unload_Instructions()
            self.origin.mode = 0
            ClearAllHighlightTiles()
            ClearAllBoundaryTiles()
            ClearAllTargetTiles()
            self.fm.desc = False

    def Start(self):
        for i in self.p_tar:
            i.Pntl_MinHP = 0
            i.Pntl_MaxHP = 0
            i.Pntl_CritHP = 0
            i.Pntl_SE = None
            
        ClearAllHighlightTiles()
        ClearAllBoundaryTiles()
        ClearAllTargetTiles()
        MoveDisplay(self.name,clr = faction_clrs[0])

        for i in self.p_tar:
            i.ApplyStatusEffect(effect = self.SE,turn = self.timer,value = self.value,stack_threshold = self.stack_threshold)
            if self.tar_ally:
                UpwardLines(i,SE_colour_set.get(self.SE))

        #self.fm.desc = False

        self.origin.act_record[self.ID] = False
        self.origin.act_CD[self.ID] = self.use_cd
        self.origin.Set_ActPts(-1)
        self.Unload_Instructions()
        self.origin.mode = 0
        
        self.target = []

        if len(self.fm.acting_units) == 0:
            self.fm.a_cd = fps * 1.5

class Apply_Quicken(Apply_Effect):
    def __init__(self,origin,ID = 2):
        Apply_Effect.__init__(self,origin = origin)
        self.name = "Quicken"
        self.ID = ID

        self.icon = quicken_icon#pygame.transform.scale(SE_Symbols.get("Quicken"),[35,35])
        self.i_rect = self.icon.get_rect()

        self.range = 4
        self.use_cd = 2

        self.SE = "Quicken"
        self.timer = 1
        self.value = None
        self.stack_threshold = None

        self.highlight = 6
        self.tar_ally = True
        
        self.desc = ["Enable unit and allies within range to move further."]
        self.short_desc = ["Apply Quicken."]

        self.imgs = [quicken_symbol, duration_symbol]
        self.colour = [SE_colour_set.get("Quicken")]

        self.origin.move_type.append("Skill")
        self.origin.move_label.append(self.name)
        self.origin.move_stat.append(False)
        self.origin.move_mlt.append(None)
        self.origin.move_SE.append(None)
        self.origin.move_cd.append(self.use_cd)
        self.origin.move_crit.append(0)
        self.origin.move_range.append([self.range,4])
        self.origin.move_get_tile.append(None)
        self.origin.move_icon.append(self.icon)

        d = list(self.desc)
        for i in range(len(self.imgs)):
            for j in range(len(d)):
                n = len(self.imgs) - 1 - i
                d[j] = d[j].replace("#"+str(n),"#"+str(len(self.origin.imgs)+n))
        for i in range(len(self.colour)):
            for j in range(len(d)):
                n = len(self.colour) - 1 - i
                if n > 9:
                    n = chr(n + 87)
                d[j] = d[j].replace("@"+str(n),"@"+str(len(self.origin.colour)+n))
        self.origin.move_info.append(d)

        self.origin.colour += self.colour
        self.origin.imgs += self.imgs

        self.Text_Sort()
        self.Set_Instructions()
