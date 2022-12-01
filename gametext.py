import pygame
from pygame.locals import *
import math
import random
import gamedata
from gamedata import*

texts = []
tips = []
tip_images = []
choices = []
infotexts = []

def refresh_texts():
    for i in texts:
        if i.type is 'info' and i.belonging.touched == False:
            i.clear()
            
class proj(pygame.sprite.Sprite):
    def __init__(self,name,start,end):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.imagename = "images/icon/"+self.name+".png"
        self.image = pygame.image.load(self.imagename).convert_alpha()
        self.original_image = self.image
        startx = start.x
        endx = end.x
        self.x = startx
        self.y = Height/2-50
        self.pos = (self.x,self.y)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.duration = gamedata.projectile_time
        self.spd = (endx-startx)/self.duration
        self.clock = 0
        projs.add(self)
        
    def update(self):
        if self.duration < 0:
            pygame.sprite.Sprite.kill(self)
            return
        else:
            self.duration -= 1
            self.clock+=1
        self.x += self.spd
        if self.duration < gamedata.projectile_time/2:
            self.y += 20
        else:
            self.y -= 20
        self.pos = (self.x,self.y)
        self.image = pygame.transform.rotate(self.original_image,
                                                     -36* self.clock)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
    
    
class icon(pygame.sprite.Sprite):
    def __init__(self,name,belonging):
        global allyheight
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.belonging = belonging
        self.imagename = "images/icon/"+self.name+".png"
        self.image = pygame.image.load(self.imagename).convert_alpha()
        bpos = self.belonging.pos
        x = bpos[0]
        y = bpos[1]
        if name is 'hp':
            x -= 65
            y += 10
        if name is 'atk':
            x -= 0
            y += 10
        if name is 'spd':
            x += 65
            y += 10
        if name is 'range':
            x += 60
            y -= 150
        if name is 'star':
            x -= 60
            y -= 150
        if name is 'star2':
            x -= 30
            y -= 150
        if name is 'freeze':
            y -= 70
        if name is 'place':
            character_order = order_interval(bpos[0])
            character_pos = allyposition(character_order)
            x = character_pos[0]
            y = character_pos[1]-70
        self.pos = (x,y)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        icons.add(self)


class digit(icon):
    def __init__(self,text,adjustx,adjusty,belonging,dtype):
        name = ''
        if dtype != 'w':
            name += dtype
        name += str(text)
        super(digit, self).__init__(name,belonging)
        x = self.pos[0]+adjustx
        y = self.pos[1]+adjusty
        self.pos = (x,y)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        #digits.add(self)
        
def generate_digits(number,belonging,dtype):
    number = int(max(number,0))
    number = str(number)
    length = len(number)
    for i in range(length):
        adjustx = (i-length/2)*20+10
        adjusty = 0
        digit(number[i],adjustx,adjusty,belonging,dtype)

def generate_damage_digits(number,belonging,y):
    number = max(number,0)
    number = str(number)
    length = len(number)
    for i in range(length):
        adjustx = (i-length/2)*80+40
        adjusty = y
        digit(number[i],adjustx,adjusty,belonging,'d')
        
def generate_digit_text(text,belonging,dtype):
    #! is / for '/' could not appear in image name
    length = len(text)
    if dtype == 'm':
        width = 60
    else:
        width = 20
    for i in range(length):
        adjustx = (i-length/2)*width+width/2
        adjusty = 70
        digit(text[i],adjustx,adjusty,belonging,dtype)
            
class speffect(pygame.sprite.Sprite):
    def __init__(self,animation,belonging):
        global allyheight
        pygame.sprite.Sprite.__init__(self)
        self.belonging = belonging
        self.imagename = "images/animation/"+animation+".png"
        self.image = pygame.image.load(self.imagename).convert_alpha()
        self.name = animation
        bpos = self.belonging.pos
        x = bpos[0] 
        y = bpos[1] -60
        self.pos = (x,y)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        icons.add(self)   
        
class upgrade_choice(): #3line of text,the total number of choice,and the unit
    def __init__(self,stats,new,removed,change,num,order,unit):
        self.stats = stats
        self.unitimage = unit.image
        #set the text into lines
        self.new_properties = []
        new_len = len(new)
        rem_len = len(removed)
        #arrange new properties
        linelength = 20
        newline = ""
        for textcount in range(new_len):
            newline +=str(new[textcount])
            if len(newline)>=17 and new[textcount] == ' ':
               self.new_properties.append(newline)
               newline = ""
        self.new_properties.append(newline) 
        self.num = num
        self.order = order
        
        if self.order == 1:
            self.x = Width*0.26
        else:
            self.x = Width*0.73
        self.y = 0.5*Height
        self.pos = (self.x,self.y)
        
        self.change = change
        self.target = unit
        
        self.image = pygame.image.load("images\icon\choice.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        choices.append(self)
    
    def choose(self):#change the stats and ability(effects) of unit
        stats = self.change[0]
        ability = self.change[1]
        remove = self.change[2]
        self.target.hp += stats[0]
        self.target.atk += stats[1]
        self.target.spd += stats[2]
        self.target.range += stats[3]
        if ability is not None:#if their are new ability, change target corresponding effects
            ability_type = ability[0]
            ability_content = ability[1]
            self.target.effects[ability_type] = ability_content
        if remove is not None:
            self.target.effects.pop(remove)
        self.target.refresh()
        choices.clear()
        gamedata.has_choice = False

class tip_image(pygame.sprite.Sprite):
    def __init__(self,name,pos,time):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.pos = pos
        self.time = time
        self.imagename = "images/icon/"+self.name+".png"
        self.image = pygame.image.load(self.imagename).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        tip_images.append(self)
        
    def refresh(self):
        self.time -= 1
        if self.time<=0:
            tip_images.remove(self)    
class text:
    def __init__(self,words):
        self.words = words
        self.type = None
        
    def changewords(self,words):
        self.words = words
        self.content = f.render(words,True,(0,0,0))
        self.Rect =self.content.get_rect
    
    def clear(self):
        global texts
        texts.remove(self)

class tip(text):
    def __init__(self,words,pos,time):
        super(tip, self).__init__(words)
        self.type = 'tips'
        self.pos = pos
        self.time = time
        self.content = f3.render(words,True,(0,0,0))
        self.Rect = self.content.get_rect()
        self.Rect.center = self.pos
        tips.append(self)
    
    def refresh(self):
        self.time -= 1
        if self.time<=0:
            tips.remove(self)
            
class life_tip(tip):
    def __init__(self,reduction,remaining):
        self.type = 'tips'
        words = 'life - '
        words += str(reduction)
        words += ' , '
        words += str(remaining)
        words += ' remaining'
        pos = (1/2*Width-200,0.3*Height)
        time = 120
        super(life_tip, self).__init__(words,pos,time)
        self.content = f3.render(words,True,(0,0,0))
        self.Rect = self.content.get_rect()
        self.Rect.center = self.pos
        tips.append(self)

class infotext(text):
    def __init__(self,words,lv,effects,pos,belonging):
        super(infotext, self).__init__(words)
        self.type = 'info'
        self.pos = pos
        self.x = pos[0]
        self.y = pos[1]
        self.contents = []
        words = words
        words += ', level '
        words += str(lv)
        content = f2.render(words,True,(0,0,0),(255,255,255))
        self.contents.append(content)
        
        for i in effects:
            effect = [i,effects[i]]
            text = get_intro(effect)
            content = f2.render(text,True,(0,0,0),(255,255,255))
            self.contents.append(content)
            
        self.belonging = belonging
        infotexts.append(self)
        

class commontext(text):
    def __init__(self,words,pos,ttype):
        super(commontext, self).__init__(words)
        self.content = f2.render(words,True,(0,0,0))
        self.type = ttype
        self.pos = pos
        self.Rect = self.content.get_rect()
        self.Rect.center = self.pos
        texts.append(self)

class moneytext(text):
    def __init__(self,words,pos,ttype):
        super(moneytext, self).__init__(words)
        self.content = f5.render(words,True,(0,0,0))
        self.type = ttype
        self.pos = pos
        self.Rect = self.content.get_rect()
        self.Rect.center = self.pos
        texts.append(self)
    
class price_text(text):
    def __init__(self,words,belonging):
        super(price_text, self).__init__(words)
        self.type = 'cinfo'
        self.belonging = belonging
        self.content = f2.render(words,True,(0,0,0))
        bpos = self.belonging.pos
        x = bpos[0]- 10*len(words)
        y = bpos[1]+ 45
        self.pos = (x,y)
        self.Rect =self.content.get_rect()
        self.Rect.center = self.pos
        texts.append(self)

        
class HP_text(text):
    def __init__(self,words,belonging):
        super(HP_text, self).__init__(words)
        self.type = 'cinfo'
        self.belonging = belonging
        bpos = self.belonging.pos
        x = bpos[0]-78
        y = bpos[1]
        self.pos = (x,y)
        self.content = f.render(words,True,(0,0,0))
        self.Rect =self.content.get_rect()
        self.Rect.center = self.pos
        texts.append(self)

class ATK_text(text):
    def __init__(self,words,belonging):
        super(ATK_text, self).__init__(words)
        self.type = 'cinfo'
        self.belonging = belonging
        bpos = self.belonging.pos
        x = bpos[0]-15
        y = bpos[1]
        self.pos = (x,y)
        self.content = f.render(words,True,(0,0,0))
        self.Rect =self.content.get_rect()
        self.Rect.center = self.pos
        texts.append(self)

class SPD_text(text):
    def __init__(self,words,belonging):
        super(SPD_text, self).__init__(words)
        self.type = 'cinfo'
        self.belonging = belonging
        bpos = self.belonging.pos
        x = bpos[0]+50
        y = bpos[1]
        self.pos = (x,y)
        self.content = f.render(words,True,(0,0,0))
        self.Rect =self.content.get_rect()
        self.Rect.center = self.pos
        texts.append(self)

class RAN_text(text):
    def __init__(self,words,belonging):
        super(RAN_text, self).__init__(words)
        self.type = 'cinfo'
        self.belonging = belonging
        bpos = self.belonging.pos
        x = bpos[0]+50
        y = bpos[1]-170
        self.pos = (x,y)
        self.content = f.render(words,True,(0,0,0))
        self.Rect =self.content.get_rect()
        self.Rect.center = self.pos
        texts.append(self)