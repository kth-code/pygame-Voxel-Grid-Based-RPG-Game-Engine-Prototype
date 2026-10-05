import pygame
from random import *
from math import *
from VoxelGame_BaseVars import *
from VoxelGame_Visuals import *
from VoxelGame_ATKProjectiles import *

from VoxelGame_Icons import *

font = game_font18
class Attack():
    def __init__(self):
        self.SE = None
        self.prop = []
        self.prop_val = []
        self.timer = 0
        self.charge_cd = 2
        self.charge_cost = 1
        self.cover_dmg = 1
        self.use_cd = 20
        self.move_cost = True
        self.draw_lp = 200
        self.desc_lp = 0

        self.charge_lp = 0

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
        if self.tar_count > 1:
            text = title_font20.render("Unselect Target",True,(255,255,255))
            textRect = text.get_rect()
            i_rect = key_icon_z.get_rect()
            textRect.bottom = y
            i_rect.left = 10
            i_rect.centery = textRect.centery
            textRect.left = i_rect.right + 5
            self.instructions.append([text,textRect,key_icon_x,i_rect])
            y -= textRect[3] + 10
        
        text = title_font20.render("Select Target",True,(255,255,255))
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

        if self.SE:
            c_rect = pygame.Rect(0,0,180,25)
            c_rect.right = window_width - 25
            c_rect.top = 20 - self.draw_lp/2
            pygame.draw.line(game_window,(255,255,255),[c_rect.left,c_rect.top],[c_rect.left,c_rect.top - 20],width = 3)
            pygame.draw.line(game_window,(255,255,255),[c_rect.right,c_rect.top],[c_rect.right,c_rect.top - 20],width = 3)
            if self.origin.action_pts < self.charge_cost + 1:
                clr = (80,80,80)
                t_clr = (180,180,180)
                DrawHexFrame(c_rect,clr)

                text = stat_font18.render("Insufficient Action Pts",True,t_clr)
                textRect = text.get_rect()
            elif self.timer > 0:
                clr = (80,80,80)
                t_clr = (180,180,180)
                DrawHexFrame(c_rect,clr)

                text = stat_font18.render(self.SE,True,t_clr)
                textRect = text.get_rect()

                img = SE_Gray_Symbols.get(self.SE)
                i_rect = img.get_rect()
            else:
                clr = SE_Dcolour_set.get(self.SE)
                t_clr = (255,255,255)
                DrawHexFrame(c_rect,clr)

                text = stat_font18.render(self.SE,True,t_clr)
                textRect = text.get_rect()

                img = SE_Symbols.get(self.SE)
                i_rect = img.get_rect()

            if self.charge_lp > 0:
                self.charge_lp -= 4

            if 0 < self.charge_lp:
                g_clr = SE_colour_set.get(self.SE)
                DrawHexFlash(c_rect,g_clr,self.charge_lp)

            if self.origin.action_pts < self.charge_cost + 1:
                textRect.center = c_rect.center
                game_window.blit(text,textRect)
            else:
                textRect.right = c_rect.centerx + textRect[2]/2 + i_rect[2]/2 + 2
                textRect.centery = c_rect.centery
                i_rect.right = textRect.left - 5
                i_rect.centery = textRect.centery

                game_window.blit(text,textRect)
                game_window.blit(img,i_rect)

                m_rect = pygame.Rect(0,0,100,25)
                m_rect.right = c_rect.right
                m_rect.top = c_rect.bottom + 10

                if self.timer > 0:
                    text = stat_font18.render("In Cooldown",True,t_clr)
                    img = None
                elif self.charge:
                    text = stat_font18.render("Discharge",True,t_clr)
                    img = key_icon_c
                    i_rect = img.get_rect()
                else:
                    text = stat_font18.render("Charge",True,t_clr)
                    img = key_icon_c
                    i_rect = img.get_rect()
                textRect = text.get_rect()
                if img:
                    textRect.right = m_rect.centerx + textRect[2]/2 + i_rect[2]/2 + 2.5
                    textRect.centery = m_rect.centery
                else:
                    textRect.center = m_rect.center

                pygame.draw.line(game_window,(255,255,255),[m_rect.left,m_rect.top],[m_rect.left,m_rect.top - 9],width = 3)
                pygame.draw.line(game_window,(255,255,255),[m_rect.right,m_rect.top],[m_rect.right,m_rect.top - 9],width = 3)
                DrawHexFrame(m_rect,clr)
                game_window.blit(text,textRect)

                if img:
                    i_rect.right = textRect.left - 5
                    i_rect.centery = textRect.centery
                    game_window.blit(img,i_rect)

                img = cd_symbol
                i_rect = img.get_rect()
                if self.timer > 0:
                    text = stat_font18.render(str(self.timer),True,(255,255,255))
                else:
                    text = stat_font18.render(str(self.charge_cd),True,(255,255,255))
                textRect = text.get_rect()

                m_rect = pygame.Rect(0,0,textRect[2] + i_rect[2] + 5,25)
                m_rect.left = c_rect.left
                m_rect.top = c_rect.bottom + 10

                textRect.right = m_rect.right#m_rect.centerx + textRect[2]/2 + i_rect[2]/2 + 2
                textRect.centery = m_rect.centery
                i_rect.right = textRect.left - 5
                i_rect.centery = m_rect.centery

                pygame.draw.line(game_window,(255,255,255),[m_rect.left,m_rect.top],[m_rect.left,m_rect.top - 9],width = 3)
                pygame.draw.line(game_window,(255,255,255),[m_rect.right,m_rect.top],[m_rect.right,m_rect.top - 9],width = 3)
                DrawHexFrame(m_rect,clr)
                game_window.blit(text,textRect)
                game_window.blit(img,i_rect)
                
        u = self.p_tar[self.tar_no]
        
        d_clr = (255,255,255)
        
        crit = self.origin.Get_Crit(self.ID)

        if u.Pntl_MinHP > 0:
            self.desc_lp = (self.desc_lp + 1)%81
            c = abs(40 - self.desc_lp)/40
            if self.charge:
                img = SE_Symbols.get(self.charge)
                i_rect = img.get_rect()
            
            text = stat_font20.render("Restore "+str(abs(u.Pntl_MinHP))+" - "+str(abs(u.Pntl_MaxHP))+" HP",True,GradientClrs(d_clr,(140,255,150),c,1-c))
            textRect = text.get_rect()

            if self.charge:
                i_rect.left = rect.centerx - textRect[2]/2 - i_rect[2]/2 - 2
                textRect.left = i_rect.right + 5
            else:
                textRect.left = rect.centerx - textRect[2]/2

            textRect.top = y
            if self.charge:
                i_rect.centery = textRect.centery
                game_window.blit(img,i_rect)
        elif self.charge:
            self.desc_lp = (self.desc_lp + 1)%81
            e_clr = SE_colour_set.get(self.charge)
            c = abs(40 - self.desc_lp)/40
            text = stat_font20.render(str(abs(u.Pntl_MinHP))+" - "+str(abs(u.Pntl_MaxHP))+" "+self.charge+" DMG",True,GradientClrs(d_clr,e_clr,c,1-c))
            textRect = text.get_rect()

            img = SE_Symbols.get(self.charge)
            i_rect = img.get_rect()
            
            i_rect.left = rect.centerx - textRect[2]/2 - i_rect[2]/2 - 2
            textRect.left = i_rect.right + 5
            textRect.top = y
            i_rect.centery = textRect.centery
            
            game_window.blit(img,i_rect)
        else:
            text = stat_font20.render(str(abs(u.Pntl_MinHP))+" - "+str(abs(u.Pntl_MaxHP))+" DMG",True,d_clr)
            textRect = text.get_rect()
                
            textRect.left = rect.centerx - textRect[2]/2
            textRect.top = y
            
        game_window.blit(text,textRect)
        y += textRect[3] + 5

        if crit > 0:
            if u.Pntl_MinHP > 0:
                ctext = stat_font20.render(str(crit)+"% - Restore "+str(abs(u.Pntl_CritHP))+" HP",True,GradientClrs(d_clr,(140,255,150),c,1-c))
            elif self.charge:
                ctext = stat_font20.render(str(crit)+"% - "+str(abs(u.Pntl_CritHP))+" "+self.charge+" DMG",True,GradientClrs(d_clr,e_clr,c,1-c))
            else:
                ctext = stat_font20.render(str(crit)+"% - "+str(abs(u.Pntl_CritHP))+" DMG",True,d_clr)
            ctextRect = ctext.get_rect()
            ci_rect = crit_symbol.get_rect()
            ctextRect.right = rect.right
            ci_rect.right = ctextRect.left - 5

            crect = pygame.Rect(0,ctextRect.top,ctextRect[2] + ci_rect[2] + 5,30)#ctextRect[3])
            crect.right = ctextRect.right
            
            crect.bottom = rect.top - 20
            ctextRect.centery = crect.centery
            ci_rect.centery = ctextRect.centery
            
            DrawHexFrame(crect,(53,57,106))#faction_clrs[0])
            #DrawRoundFrame(crect,(53,57,106))
            game_window.blit(ctext,ctextRect)
            game_window.blit(crit_symbol,ci_rect)
            

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

        cost,rect,w = [],[],[]
        a = 1
        if self.charge:
            a += self.charge_cost
        if a == 1:
            text = game_font16.render("1 Action Pt",True,(255,255,255))
        else:
            text = game_font16.render(str(1+self.charge_cost)+" Action Pts",True,(250,200,5))
        cost.append(text)
        textRect = text.get_rect()
        rect.append(textRect)
        if self.move_cost:
            text = game_font16.render("Movement",True,(255,255,255))
            cost.append(text)
            textRect = text.get_rect()
            rect.append(textRect)
        m_rect = pygame.Rect((0,0,150,textRect[3] * len(cost)))
        m_rect.right = window_width - 30 + self.draw_lp
        m_rect.bottom = window_height - 30
        DrawSmoothFrame(m_rect,(53,57,106), sn = False)
        y = m_rect.bottom
        for i in range(len(cost)):
            rect[i].bottom = y
            rect[i].left = m_rect.left + 10
            game_window.blit(cost[i],rect[i])
            y -= rect[i][3]

        text = stat_font18.render("Cost",True,(255,255,255))
        textRect = text.get_rect()
        textRect.bottom = y
        textRect.centerx = m_rect.centerx


        m_rect = pygame.Rect((0,0,m_rect[2],textRect[3]))
        m_rect.centerx = textRect.centerx
        m_rect.bottom = y
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

        text = title_font30.render("! NO TARGET IN RANGE !",True,(255,255,255))
        textRect = text.get_rect()
        textRect.centerx = rect.centerx
        textRect.top = rect.centery
        DrawRoundFrame(textRect,(239,55,55))
        game_window.blit(text,textRect)

class LoS_Weapon(Attack): #LoS: Line of Sight
    def __init__(self,origin):
        Attack.__init__(self)
        self.fm = tile_sprites.sprites()[0]
        self.origin = origin
        self.mlt = [1,1.5]
        
        self.range = 50
        self.crit = 200
        self.cover_dmg = 1
        self.tar_count = 1
        self.target = []
        self.dmg_freq = []
        self.dmg_threshold = []

        self.dmgd = []
        
        self.target_path = []
        #self.tar_cld = []
        self.total_cld = []
        self.current_path = None
        
        self.p_tar = []
        self.tar_no = 0

        self.charge = False
        self.MinDMG = 0
        self.MaxDMG = 0
        self.CritDMG = 0

        self.cd = 0

    def Get_Target(self):
        self.draw_lp = 200
        x = self.origin.x
        y = self.origin.y
        r = self.origin.Get_Range(self.ID)
        self.p_tar = GetUnitsInRange(x,y,r,f = [1,2],IgnoreInvisible = False)
        self.tar_no = 0
        self.target = []
        self.dmg_freq = []
        self.dmg_rdct = []
        self.dmg_threshold = []
        self.target_path = []
        self.all_cld = []

        self.dmgd = []

        SetBoundaryTiles(x,y,r,c = 1,exclude = 0)

        self.charge = None
        for i in range(len(self.p_tar)):
            if "Phase" in self.prop:
                self.all_cld.append([])
            else:
                self.all_cld.append(CheckLineofSight(self.origin,self.p_tar[i]))
            self.dmg_freq.append(0)
            self.dmg_rdct.append(0)
            self.dmg_threshold.append([])
            self.target_path.append(None)
            
            for j in self.all_cld[i]:
                if j[3] >= 2:
                    #self.dmg_threshold[i].append(self.fm.objects[j[2]][j[1]].HP + self.dmg_rdct[i])
                    #self.dmg_rdct[i] += self.fm.objects[j[2]][j[1]].HP
                    self.dmg_threshold[i].append(RoundUp(self.fm.objects[j[2]][j[1]].HP/self.cover_dmg) + self.dmg_rdct[i])
                    self.dmg_rdct[i] += RoundUp(self.fm.objects[j[2]][j[1]].HP/self.cover_dmg)#self.fm.objects[j[2]][j[1]].HP
                else:
                    self.dmg_threshold[i].append(999 + self.dmg_rdct[i])
                    self.dmg_rdct[i] += 999
            
        self.fm.AddInstructions(self.back_instructions)
        
        if len(self.p_tar) > 0:
            stat = self.origin.Get_DMG(m = self.ID, t = 1)
            self.MinDMG,self.MaxDMG,self.CritDMG = stat[0],stat[1],stat[2]
            #self.tar_cld = self.all_cld[self.tar_no] #CheckLineofSight(self.origin,self.p_tar[self.tar_no])
            SetTargetTile(self.p_tar[self.tar_no],5)
            self.ApplyDR()
            self.SetTP()

            for i in self.instructions:
                self.fm.AddInstructions(i)

    def CalcPntlDMG(self):
        ClearAllHighlightTiles()
        for i in self.fm.units_list:#self.p_tar:
            i.ResetPntl()
            i.Pntl_SE = self.charge
        for y in self.fm.objects:
            for x in y:
                if x:
                    x.trigger = False
                    x.Pntl_HP = 0
        for i in range(len(self.p_tar)):
            if self.dmg_rdct[i] < self.dmg_freq[i]:
                self.p_tar[i].Pntl_MinHP += self.p_tar[i].Get_ActualDMG(self.MinDMG, effect = self.p_tar[i].Pntl_SE,source_type = 1, hit_no = self.dmg_freq[i] - self.dmg_rdct[i])
                self.p_tar[i].Pntl_MaxHP += self.p_tar[i].Get_ActualDMG(self.MaxDMG, effect = self.p_tar[i].Pntl_SE,source_type = 1, hit_no = self.dmg_freq[i] - self.dmg_rdct[i])
                self.p_tar[i].Pntl_CritHP += self.p_tar[i].Get_ActualDMG(self.CritDMG, effect = self.p_tar[i].Pntl_SE,source_type = 1, hit_no = self.dmg_freq[i] - self.dmg_rdct[i])
                self.p_tar[i].Pntl_Hit += self.dmg_freq[i] - self.dmg_rdct[i]

    def SetDMG(self):
        self.dmg_freq[self.tar_no] += 1
        self.CalcPntlDMG()

    def UnsetDMG(self):
        self.dmg_freq[self.tar_no] -= 1
    
    def UnapplyDR(self):
        t = self.p_tar[self.tar_no]
        self.UnsetDMG()

    def ApplyDR(self):
        t = self.p_tar[self.tar_no]

        self.SetDMG()
        self.CalcPntlDMG()

    def SetTP(self):
        fm_desc, fm_v, fm_h = self.fm.desc, self.fm.v, self.fm.h
        self.fm.QuickSetTopView()
    
        for i in range(len(self.p_tar)):
            if self.target_path[i]:
                self.fm.visual_sprites.remove(self.target_path[i])
            self.target_path[i] = None
            t = self.p_tar[i]
            tt = [self.fm.s_x + t.x * self.fm.w,self.fm.s_y + t.y * self.fm.h]#self.fm.tiles[t.y][t.x] #[tt.centerx, tt.centery]
            ot = self.fm.tiles[self.origin.y][self.origin.x]

            if self.dmg_freq[i] > 0:
                if self.dmg_rdct[i] == 0:#> self.dmg_rdct[i]:
                    line = SightLine(self.fm,ot,tt,clr = (160,255,155))
                else:
                    mark = []
                    end = []
                    if self.dmg_freq[i] > self.dmg_rdct[i]:
                        clr = (160,255,155)
                    elif self.dmg_rdct[i] < 999:
                        clr = (255,155,155)
                    else:
                        clr = (200,155,255)
                    for j in range(len(self.dmg_threshold[i])):
                        end = self.all_cld[i][j][0]
                        x,y = self.all_cld[i][j][1],self.all_cld[i][j][2]
                        if self.dmg_freq[i] >= self.dmg_threshold[i][j]:
                            mark.append([1,self.all_cld[i][j][0]]) #Type, Collision Pt
                            mark.append([2,x,y])
                            if self.all_cld[i][j][3] >= 1:
                                self.fm.objects[y][x].ApplyPntlDMG(self.MinDMG,self.MaxDMG,-self.cover_dmg)
                            if self.dmg_freq[i] == self.dmg_threshold[i][j]:
                                break
                        else:
                            mark.append([0,self.all_cld[i][j][0]])
                            mark.append([2,self.all_cld[i][j][1],self.all_cld[i][j][2]])
                            break
                    if self.dmg_freq[i] > self.dmg_rdct[i]:
                        end = tt
                    line = SightLine(self.fm,ot,end,clr = clr,marking = mark)
                            
                self.target_path[i] = line

        self.fm.QuickSetView(fm_desc,fm_v,fm_h)
 
    def Select_Target(self):
        keystate = pygame.key.get_pressed()
        if len(self.p_tar) > 0:
            if self.cd == 0:
                if keystate[pygame.K_LEFT]:
                    ClearTargetTile(self.p_tar[self.tar_no])
                    self.UnapplyDR()
                    if self.p_tar[self.tar_no] in self.target:
                        SetTargetTile(self.p_tar[self.tar_no],1)
                    self.tar_no = (self.tar_no - 1)%len(self.p_tar)
                    SetTargetTile(self.p_tar[self.tar_no],5)
                    self.ApplyDR()
                    self.SetTP()
                    self.cd = 20
                elif keystate[pygame.K_RIGHT]:
                    ClearTargetTile(self.p_tar[self.tar_no])
                    self.UnapplyDR()
                    if self.p_tar[self.tar_no] in self.target:
                        SetTargetTile(self.p_tar[self.tar_no],1)
                    self.tar_no = (self.tar_no + 1)%len(self.p_tar)
                    SetTargetTile(self.p_tar[self.tar_no],5)
                    self.ApplyDR()
                    self.SetTP()
                    self.cd = 20
                elif keystate[pygame.K_z]:
                    self.target.append(self.p_tar[self.tar_no])
                    self.SetTP()
                    self.cd = 20
                    self.SetDMG()
                    if len(self.target) == self.tar_count:
                        self.Start()
                    else:
                        self.SetTP()
                elif keystate[pygame.K_x] and len(self.target) > 0:
                    if self.dmg_freq[self.p_tar.index(self.target[0])] == 1:#self.p_tar[self.tar_no] != self.target[0]:
                        ClearTargetTile(self.target[0])
                    self.dmg_freq[self.p_tar.index(self.target[0])] -= 1
                    self.CalcPntlDMG()
                    self.target.pop(0)
                    self.SetTP()
                    self.cd = 20
                elif self.SE and keystate[pygame.K_c] and self.timer == 0 and self.origin.action_pts >= self.charge_cost + 1:
                    self.desc_lp = 0
                    if self.charge:
                        self.charge = None
                    else:
                        self.charge = self.SE
                        SetChargeBurst(self.origin,self.charge)
                    self.CalcPntlDMG()
                    self.cd = 20
                    self.charge_lp = 100
                elif keystate[pygame.K_0]:
                    self.Unload_Instructions()
                    self.origin.mode = 0
                    for i in self.target_path:
                        if i:
                            self.fm.visual_sprites.remove(i)
                    for i in self.p_tar:
                        i.Pntl_MinHP = 0
                        i.Pntl_MaxHP = 0
                        i.Pntl_CritHP = 0
                        i.Pntl_SE = None
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

        self.fm.show_hp = False
        ClearAllHighlightTiles()
        ClearAllBoundaryTiles()
        ClearAllTargetTiles()
        
        for i in self.target_path:
            if i:
                self.fm.visual_sprites.remove(i)   
        self.target_path = []
        
        MoveDisplay(self.name,clr = faction_clrs[0])

        collides = []
        for i in self.target:
            n = self.p_tar.index(i)
            collides.append(self.all_cld[n])

        Shots_Manager(self.origin,target = self.target, projectile = Base_Projectile, collide = collides,effect = self.charge,prop = self.prop,prop_val = self.prop_val,func = self.Strike)

        self.origin.act_record[self.ID] = False
        if self.origin.moveset[1-self.ID]:
            self.origin.act_record[1-self.ID] = False
        if self.move_cost:
            self.origin.act_record[-1] = False
        self.origin.act_CD[self.ID] = self.use_cd
        self.origin.Set_ActPts(-1)
        self.Unload_Instructions()
        self.origin.mode = 0

        if self.charge:
            self.timer = self.charge_cd
            self.origin.Set_ActPts(-self.charge_cost)

        if len(self.fm.acting_units) == 0:
            self.fm.a_cd = fps * 1.5

    def Strike(self,x,y,hit_type):
        fm = tile_sprites.sprites()[0]
        t = fm.tiles[y][x]
        #SetMagicShockwave(t.centerx,t.centery, effect = self.charge,r = 2)
        if CheckifUnit(x,y,faction = [1,2]):
            stat = self.origin.Get_DMG(m = self.ID, t = 0)
            u = fm.GetUnit(x,y)
            if SE_Default_Stack.get(self.charge) == 0:
                u.HPChange(change = stat[0], effect = self.charge,timer = 2,attacker = self.origin,crit = stat[1],impact_pt = [x,y])
            elif u in self.dmgd:
                u.HPChange(change = stat[0], effect = self.charge,timer = 0,attacker = self.origin,crit = stat[1],impact_pt = [x,y])
            else:
                u.HPChange(change = stat[0], effect = self.charge,timer = 2,attacker = self.origin,crit = stat[1],impact_pt = [x,y])
            self.dmgd.append(u)
        elif hit_type != None and hit_type >= 1:#CheckifBlock(x,y):
            fm.objects[y][x].HPChange(change = -self.cover_dmg)

class Dropdown_Weapon(Attack):
    def __init__(self,origin):
        Attack.__init__(self)
        self.fm = tile_sprites.sprites()[0]
        self.origin = origin
        
        self.mlt = [1.25,1.75]
        self.range = 15
        self.crit = 20
        self.tar_count = 2#3
        self.target = []
        self.dmg_freq = []
        
        self.p_tar = []
        self.tar_no = 0

        self.charge = None
        self.MinDMG = 0
        self.MaxDMG = 0

        self.cd = 0

    def Get_Target(self):
        x = self.origin.x
        y = self.origin.y
        r = self.origin.Get_Range(self.ID)

        self.p_tar = GetUnitsInRange(x,y,r,f = [1,2],IgnoreInvisible = False)
        self.tar_no = 0
        self.target = []
        self.dmg_freq = []

        self.charge = None
        for i in self.p_tar:
            self.dmg_freq.append(0)
        
        SetBoundaryTiles(x,y,r,c = 1,exclude = 0)
        
        self.fm.AddInstructions(self.back_instructions)
        
        if len(self.p_tar) > 0:
            stat = self.origin.Get_DMG(m = self.ID, t = 1)
            self.MinDMG,self.MaxDMG,self.CritDMG = stat[0],stat[1],stat[2]
            
            SetTargetTile(self.p_tar[self.tar_no],5)
            self.ApplyDR()

            for i in self.instructions:
                self.fm.AddInstructions(i)

    def CalcPntlDMG(self):
        for i in self.fm.units_list:#self.p_tar:
            i.ResetPntl()
            i.Pntl_SE = self.charge
        
##        for i in range(len(self.p_tar)):
##            units = GetUnitsInRange(self.p_tar[i].x,self.p_tar[i].y,2,f = [1,2])
        for i in range(len(self.p_tar)):
            if self.dmg_freq[i] > 0:
                units = GetUnitsInRange(self.p_tar[i].x,self.p_tar[i].y,2,f = [1,2])    
                for j in units:
                    j.Pntl_MinHP += j.Get_ActualDMG(self.MinDMG, effect = j.Pntl_SE,source_type = 1, hit_no = self.dmg_freq[i])
                    j.Pntl_MaxHP += j.Get_ActualDMG(self.MaxDMG, effect = j.Pntl_SE,source_type = 1, hit_no = self.dmg_freq[i])
                    j.Pntl_CritHP += j.Get_ActualDMG(self.CritDMG, effect = j.Pntl_SE,source_type = 1, hit_no = self.dmg_freq[i])
                    j.Pntl_Hit += self.dmg_freq[i]

    def SetDMG(self):
        t = self.p_tar[self.tar_no]
        self.dmg_freq[self.p_tar.index(t)] += 1
        self.CalcPntlDMG()

    def UnsetDMG(self):
        t = self.p_tar[self.tar_no]
        self.dmg_freq[self.p_tar.index(t)] -= 1
    
    def UnapplyDR(self):
        t = self.p_tar[self.tar_no]
        self.UnsetDMG()
        ClearAllHighlightTiles()

    def ApplyDR(self):
        t = self.p_tar[self.tar_no]
        SetHighlightTiles(t.x,t.y,2,1)
        self.SetDMG()
        self.CalcPntlDMG()
        
    def Select_Target(self):
        keystate = pygame.key.get_pressed()
        if len(self.p_tar) > 0:
            if self.cd == 0:
                if keystate[pygame.K_LEFT]:
                    ClearTargetTile(self.p_tar[self.tar_no])
                    self.UnapplyDR()
                    if self.p_tar[self.tar_no] in self.target:
                        SetTargetTile(self.p_tar[self.tar_no],1)
                    self.tar_no = (self.tar_no - 1)%len(self.p_tar)
                    SetTargetTile(self.p_tar[self.tar_no],5)
                    self.ApplyDR()
                    self.cd = 20
                elif keystate[pygame.K_RIGHT]:
                    ClearTargetTile(self.p_tar[self.tar_no])
                    self.UnapplyDR()
                    if self.p_tar[self.tar_no] in self.target:
                        SetTargetTile(self.p_tar[self.tar_no],1)
                    self.tar_no = (self.tar_no + 1)%len(self.p_tar)
                    SetTargetTile(self.p_tar[self.tar_no],5)
                    self.ApplyDR()
                    self.cd = 20
                elif keystate[pygame.K_z]:
                    self.target.append(self.p_tar[self.tar_no])
                    self.cd = 20
                    self.SetDMG()
                    if len(self.target) == self.tar_count:
                        self.Start()
                elif keystate[pygame.K_x] and len(self.target) > 0:
                    self.UnapplyDR()
                    for i in self.target:
                        ClearTargetTile(i)
                    self.target.pop(0)
                    for i in range(len(self.p_tar)):
                        self.dmg_freq[i] = 0
                    for i in self.target:
                        if i == self.p_tar[self.tar_no]:
                            SetTargetTile(i,5)
                        else:
                            SetTargetTile(i,1)
                        for j in GetUnitsInRange(i.x,i.y,2,f = [1,2]):
                            self.dmg_freq[self.p_tar.index(j)] += 1
                    SetTargetTile(self.p_tar[self.tar_no],5)
                    self.ApplyDR()
                    self.CalcPntlDMG()
                    self.cd = 20
                elif self.SE and keystate[pygame.K_c] and self.timer == 0 and self.origin.action_pts >= self.charge_cost + 1:
                    if self.charge:
                        self.charge = None
                    else:
                        self.charge = self.SE
                        SetChargeBurst(self.origin,self.charge)
                    self.CalcPntlDMG()
                    self.cd = 20
                    self.charge_lp = 100
                elif keystate[pygame.K_0]:
                    self.Unload_Instructions()
                    self.origin.mode = 0
                    for i in self.p_tar:
                        i.Pntl_MinHP = 0
                        i.Pntl_MaxHP = 0
                        i.Pntl_CritHP = 0
                        i.Pntl_SE = None
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
        Mlt_Skyrain(self.origin,target = self.target, effect = self.charge, func = self.Strike)
##        if self.charge:
##            Mlt_Hail(self.origin,target = self.target, func = self.Strike)
##        else:
##            Mlt_Magic_Comet(self.origin,target = self.target, func = self.Strike)

        self.fm.show_hp = False
        self.fm.desc = False

        self.origin.act_record[self.ID] = False
        if self.origin.moveset[1-self.ID]:
            self.origin.act_record[1-self.ID] = False
        if self.move_cost:
            self.origin.act_record[-1] = False
        self.origin.act_CD[self.ID] = self.use_cd
        self.origin.Set_ActPts(-1)
        self.Unload_Instructions()
        self.origin.mode = 0
        
        self.target = []
        self.dmg_freq = []

        if self.charge:
            self.timer = self.charge_cd
            self.origin.Set_ActPts(-self.charge_cost)

        if len(self.fm.acting_units) == 0:
            self.fm.a_cd = fps * 1.5

    def Strike(self,x,y):
        fm = tile_sprites.sprites()[0]
        SetShockwave(x,y,2)
        for i in GetTilesInRange(x,y,2):
            stat = self.origin.Get_DMG(m = self.ID, t = 0)
            if CheckifUnit(i.x,i.y,faction = [1,2]):
                fm.GetUnit(i.x,i.y).HPChange(change = stat[0], effect = self.charge,timer = 2,attacker = self.origin,crit = stat[1],impact_pt = [x,y])
            elif CheckifBlock(i.x,i.y):
                fm.objects[i.y][i.x].HPChange(change = -self.cover_dmg)

class Test_Wand(LoS_Weapon):
    def __init__(self,origin,ID = 1):
        LoS_Weapon.__init__(self,origin = origin)
        self.name = "Magic Spell"
        self.SE = "Burn"
        self.ID = ID

        self.icon = Projectile_Icons.get(self.SE)
        self.i_rect = self.icon.get_rect()

        self.charge_cd = 0#2
        self.use_cd = 0
        self.cover_dmg = 2

        self.tar_count = 1

        self.desc = ["A medium-ranged blast of magic."]
        self.prop = []
        self.prop_val = []

        self.imgs = []
        
        self.colour = [(76,204,255)]
        self.mlt = [3,4]
        self.crit = 100

        self.origin.move_type.append("Attack")
        self.origin.move_label.append(self.name)
        self.origin.move_stat.append(True)
        self.origin.move_mlt.append(self.mlt)
        self.origin.move_SE.append(None)
        self.origin.move_cd.append(self.use_cd)
        self.origin.move_crit.append(self.crit)
        self.origin.move_range.append([self.range,1])
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
                d[j] = d[j].replace("#"+str(n),"#"+str(len(self.origin.colour)+n))
        self.origin.move_info.append(d)

        self.origin.colour += self.colour
        self.origin.imgs += self.imgs

        self.Text_Sort()
        self.Set_Instructions()

        self.ID = 0
            
class Test_Launcher(Dropdown_Weapon):
    def __init__(self,origin,ID = 1):
        Dropdown_Weapon.__init__(self,origin = origin)
        self.name = "Blast Strike"
        self.SE = "Shock"
        self.ID = ID

        self.icon = Projectile_Icons.get(self.SE)
        self.i_rect = self.icon.get_rect()

        self.charge_cd = 4
        self.use_cd = 2
        self.cover_dmg = 2
        self.crit = 100

        self.desc = ["Launch 2 projects that falls on the target(s)."]

        self.imgs = [aoe_range_symbol]
        self.colour = []

        self.origin.move_type.append("Attack")
        self.origin.move_label.append(self.name)
        self.origin.move_stat.append(True)
        self.origin.move_mlt.append(self.mlt)
        self.origin.move_SE.append(None)
        self.origin.move_cd.append(self.use_cd)
        self.origin.move_crit.append(self.crit)
        self.origin.move_range.append([self.range,1])
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
