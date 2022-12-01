import pygame
from pygame.locals import *
import math
import random
import gamedata
from gamedata import*
from gametext import*
from character import*

def arrangestore(order):
    global storelen
    minorder = 0
    makeway = False
    for i in range(storelen):#reanrrange the pos from 0 to max
        for item in store:
            if item.order == i:
                item.order = minorder
                item.refresh()
                minorder +=1
    if order > -1:#-1 for no new member
        for item in store:
            if item.order == order:
                makeway = True
        if makeway == True:
            for item in store:
                if item.order >= order:
                    item.order +=1
                    item.refresh()

def checktouch(i,pos):
    if i.rect.collidepoint(pos) and draged.has(i) is False:
        i.touched = True
        return True
    else:
        i.touched = False
        
def release(item):
    global draged
    exist = True
    center = item.rect.center
    if center[1] > Height*5/6:
        exist = trybuy(item)
    if center[1] < Height*4/6 and center[1] > Height*2/6:
        exist = tryplace(item)
    if center[1] < Height*1/6:
        exist = trysell(item)
    if exist:#the draged item still exists
        item.refresh()
    updatemoney()
    draged.empty()

def trybuy(item):
    handitems = hand.sprites()
    if len(handitems) >= handlen or item.type != 'storeitem':
        return True
    elif gamedata.money < item.price:
        return True
    else:#enoughmoney and space
        gamedata.money -= item.price
        item.addtohand()
        arrangestore(-1)
        return True
    
def trysell(item):
    if item.type == 'character':
        sell_effect(item)
        if gamedata.money < gamedata.MAX_MAX_money:
            price = item.price
            if item.lv >=3:
                for i in gamedata.ally:
                    if 'special' in i.effects:
                        if 'beetle0' in i.effects['special']:
                            price+=1
                        if 'beetle1' in i.effects['special']:
                            price+=2
            if 'sell' in item.effects:
                if 'chicken2' in item.effects['sell']:
                    name = generate_lv_item(5)
                    new_item = storecharacter(name,0,0,0)
                    new_item.attack +=3
                    new_item.price = basic_character_prize
                    handitems = hand.sprites()
                    new_item.order = len(handitems)+1
                    new_item.pos = handposition(new_item.order)
                    new_item.type = 'handitem'
                    hand.add(new_item)
                    store.remove(new_item)
                    new_item.refresh()
                            
            gamedata.money += price
        pygame.sprite.Sprite.kill(item)
        return False
    else:
        for i in hand:
            if i.order> item.order:
                i.order-=1
        return True
        
    

def show_place(item):
    order = 0
    allys = ally.sprites()
    if gamedata.ally.has(item) is False and len(allys)>= characterlen:#no space won't show place
        return
    center = item.rect.center
    if center[1] < Height*4/6 and center[1] > Height*2/6:
        order =  order_interval(item.x)
        arrangeally(order)
        item.placing = True
    else:
        arrangeally(-1)
                
def tryplace(item):
    allally = ally.sprites()
    allygroup = ally
    allynum = len(allally)
    
    if allynum >= characterlen and allygroup.has(item) is False:
        return True
    else:
        x = item.x
        order = order_interval(x)
        data = {'lv':item.lv,'hp':item.hp,'atk':item.atk,'spd':item.spd,'range':item.range,'tar':item.tar,
                'effects':item.effects}
        if item.type =='handitem':
            if item.star > 0:#star item summon with new ability
                item.new_effects()
                pygame.sprite.Sprite.kill(item)
                #summon(item.name,order,item.star,item.data,0)
                arrangeally(-1)
            else:
                pygame.sprite.Sprite.kill(item)
                summon(item.name,order,0,data,0)
                arrangeally(-1)
            for i in hand:
                if i.order> item.order:
                    i.order-=1
        if item.type == 'storeitem':
            if gamedata.money < item.price:
                return True
            pygame.sprite.Sprite.kill(item)
            summon(item.name,order,item.star,data,0)
            gamedata.money -= item.price
            arrangestore(-1)
            arrangeally(-1)
            item.refresh()
            
        if item.type == 'character':
            item.order = order
            item.refresh()
            arrangeally(order)
            arrangeally(-1)
            item.refresh()
            
        
def updatemoney():
    for i in texts:
        if i.type is 'money' :
            i.clear()
    text = ''
    text += str(gamedata.money)
    for i in buttons:
        if i.name == 'pouch':
            generate_digit_text(text,i,'m')

def freeze_store():
    froze_any = False
    for i in store:
        if i.froze == True:
            froze_any = True
            break

    if froze_any:
        for i in store:
            i.froze = False
        #tip ('store is unfrozen',(1/2*Width -150,1/2*Height),20)
    else:
        for i in store:
            i.froze = True
        #tip ('store is frozen',(1/2*Width -150,1/2*Height),20)


def check_max_refresh():
    max_ref = gamedata.max_refresh_basic
    for i in gamedata.ally:
        if 'special' in i.effects:
            if 'beetle2' in i.effects['special']:
                max+=10
    gamedata.max_refresh = max_ref
                
#type 0 for auto refresh, 1 for player refresh
def refreshstore(refresh_type):
    global draged
    if refresh_type == 1 and gamedata.money < gamedata.refresh_cost:
        return
    elif gamedata.refresh_time > gamedata.max_refresh:
        return
    else:
        store.empty()
        draged.empty()
        texts.clear()
        filled = 0#already filled place
        if refresh_type == 1:#only auto refresh will remember the froze items
            pygame.mixer.Sound.play(refresh_sound)
            gamedata.refresh_time +=1
            gamedata.money -= gamedata.refresh_cost
            for i in gamedata.ally:
                if 'special' in i.effects:
                    if 'beetle2' in i.effects['special']:
                        gamedata.money +=1
            gamedata.frozestore.empty()
        else:
            for i in gamedata.frozestore:
                store.add(i)
                filled +=1
            gamedata.frozestore.empty()
        #add new items
        for i in range (storelen-filled):
            name = generate_store_item(gamedata.storelv)
            star = 0
            addstore(name,star,i)
        updatemoney()
    
def addstore(name,star,order):
    global price
    arrangestore(order)
    storecharacter(name,star,order,price)

def store_levelup():
    global storelen
    if gamedata.money < gamedata.store_level_cost:
        return
    elif gamedata.storelv < max_storelv:
        gamedata.money -= gamedata.store_level_cost
        gamedata.storelv+=1
        storelen +=1
        storelen = min(storelen,6)
        gamedata.store_level_cost = gamedata.storelv*2+3
        
def print_team_info():
    f = open('team_info.txt','a')
    f.write('[')
    f.write(str(gamedata.stage))
    for item in ally:
        f.write(',[')
        data =  {'name':item.name,'star':item.star,'order':item.order}
        f.write(str(data))
        f.write(',')
        data =  {'lv':item.lv,'hp':item.hp,'atk':item.atk,'spd':item.spd,'range':item.range,'tar':item.tar,
                'effects':item.effects}
        f.write(str(data))
        f.write(']')
    f.write('],\n')
    f.close()
    
class storecharacter(pygame.sprite.Sprite):
    def __init__(self,name,star,order,price):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.type = 'storeitem'
        self.data = character_data(name)
        self.lv = self.data['lv']
        self.hp = self.data['hp']
        self.atk = self.data['atk']
        self.spd = self.data['spd']
        self.range = self.data['range']
        self.tar = self.data['tar']
        self.effects = self.data['effects']
        self.star = star
        self.price = price#buy or sell price
        self.froze = False#whether froze
        self.touched = False#whether touched
        self.placing = False#whether is being placing
        store_amount = store
        self.imagename = "images/animals/"+self.name+".png"
        self.image = pygame.image.load(self.imagename).convert_alpha()
        self.order = order
        self.pos = storeposition(self.order)
        self.x = self.pos[0]
        self.y = self.pos[1]
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.pos
        self.generate_text()
        store.add(self)
        
    def generate_text(self):

        pri ='$'
        pri += str(self.price)
        hp_icon = icon('hp',self)
        atk_icon = icon('atk',self)
        spd_icon = icon('spd',self)
        ran_icon = icon('range',self)
        
        dtype ='w'
        generate_digits(self.atk,atk_icon,dtype)
        generate_digits(self.spd,spd_icon,dtype)
        generate_digits(self.range,ran_icon,dtype)
        generate_digits(self.hp,hp_icon,dtype)
        
        #price_text(pri,self)
        
        if self.star >=1:
            icon('star',self)
        if self.star >=2:
            icon('star2',self)
        if self.froze:
            icon('freeze',self)
            
    def addtohand(self):
        global store,hand
        self.price = basic_character_prize
        handitems = hand.sprites()
        self.order = len(handitems)+1
        self.pos = handposition(self.order)
        self.type = 'handitem'
        self.froze = False
        hand.add(self)
        store.remove(self)
        self.refresh()
        test_triple(self)
    
    def touch(self):#when touched by mouse but not draged
        x = self.pos[0]
        y = self.pos[1]
        pos = pos = (x - 50 ,y)
        infotext(self.name,self.lv,self.effects,pos,self)
        
    def drag(self,pos):#when draged
        self.pos = pos
        self.x = self.pos[0]
        self.y = self.pos[1]
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.generate_text()
                    
    def refresh(self):
        if self.type == 'storeitem':
            self.pos = storeposition(self.order)
        else:
            self.pos = handposition(self.order)
        self.x = self.pos[0]
        self.y = self.pos[1]
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.pos
        self.generate_text()
        
    def remove(self):
        pygame.sprite.Sprite.kill(self)
        
        