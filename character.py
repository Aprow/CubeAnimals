import pygame
from pygame.locals import *
import math
import random
import gamedata
from gamedata import*
from gametext import*
from upgradetype import*
basic_character_price = 1

def summon(name,order,star,data,group):#summon a new character
     if group == 0:
         team = ally.sprites()
     else:
         team = enemy.sprites()
     if len(team)>= characterlen:
         return
     else:
         arrangeally(order)
         arrangeenemy(order)
         character(name,order,star,data,group)
         arrangeally(-1)
     # just the modified list in gamedata.characterdata
     
def order_interval(x):
    global characterlen
    for i in range(characterlen):
        place =  allyposition(i)
        nextplace =  allyposition(i+1)
        if place[0]-x  < x-nextplace[0] or i == characterlen-1:
            return i
    return characterlen-1

def arrangeally(order):
    global characterlen
    group = []
    group += ally.sprites()
    allys = ally.sprites()
    makeway = False
    countorder = 0
    minorder = 0
    
    for item in group:
        if draged.has(item) is True:
            group.remove(item)
            #print(item.name,item.order)
        
    while len(group)>0:
        for item in group:
            if item.order <= countorder:
                item.order = minorder
                item.refresh()
                group.remove(item)
                minorder+=1
                break
        countorder +=1
                                        
    
    if order > -1:#-1 for no new member
        group = []
        group += ally.sprites()
        for item in group:
        if draged.has(item) is True:
            item.order = order
            group.remove(item)
            
        if len(group)<5:
            for item in group:
                if item.order >= order:
                    item.order +=1
                    item.order = min(item.order,len(group))
                    item.refresh()
        
                
def arrangeenemy(order):
    global characterlen
    group = []
    group += enemy.sprites()
    minorder = 0
    countorder = 0
    makeway = False
    allenemy = enemy.sprites()
    
    while len(group)>0:
        for item in group:
            if item.order <= countorder:
                item.order = minorder
                item.refresh()
                group.remove(item)
                minorder+=1
                break
        countorder +=1
                                        
    group = []
    group += enemy.sprites()
    
    if order > -1:#-1 for no new member
        if len(group)<6:
            for item in group:
                if item.order >= order:
                    item.order +=1
                    item.order = min(item.order,len(group))
                    item.refresh()   
    
class character(pygame.sprite.Sprite):
    def __init__(self,name,order,star,data,group):
        #group0 for ally, 1 for enemy
        pygame.sprite.Sprite.__init__(self)
        #basic data
        self.name = name
        self.id = pygame.time.get_ticks()#the creation time,use to differentiate same character
        self.type = 'character'
        self.data = data
        #the basic data
        self.lv = data['lv']
        self.hp = data['hp']
        self.mhp = data['hp']
        self.atk = data['atk']
        self.spd = data['spd']
        self.range = data['range']
        self.friends = ally
        self.foe = enemy
        #the displayed data
        self.display_hp = self.hp
        self.display_atk = self.atk
        self.display_spd = self.spd
        self.display_range = self.range
        self.tar = data['tar']#target type
        self.effects = data['effects']#effect types
        self.buffs = []#buffs of self
        self.damage = 0#damage current taken
        self.star = star
        self.group = group
        self.price = basic_character_price        
        self.imagename = "images/animals/"+self.name+".png"
        self.image = pygame.image.load(self.imagename).convert_alpha()
        self.rect = self.image.get_rect()
        self.original_image = self.image
        
        #special conditions
        self.max_action = 1#action each round
        self.remained_action = 1#action each round
        self.touched = False#whether touched
        self.placing = False#whether is being placing
        self.tempstat = [0,0,0,0]#special stats for next action
        self.buffing = [0,0,0,0]#special text color for buffed stats
        #special counter
        self.counter = 0
        self.motion = None#whether is in attacking motion
        self.effectanimation = None#effect animation
        self.motionclock = 0#time of animation
        self.motionwait = 0#wait time of animation
        
        #re-arrange order
        if self.group == 0:
            arrangeally(order)
        self.order =order
        self.place(order)
        self.generate_text()
        self.born()
        self.refresh()
    
        
    def born(self):
        if gamedata.summon_trigger == True:#trigger only when in store or during battle
            character_born(self,self.group)
        if self.group == 0:
            ally.add(self)
        else:#for enemy
            if gamedata.window is 'battle':
                enemy.add(self)
                self.friends = enemy
                self.foe = ally
        if gamedata.window is 'store':#only characters summoned in store window will be remained
            test_triple(self)
        
        characters.add(self)
        arrangeally(-1)
        arrangeenemy(-1)
            
    def generate_text(self):
        hp_icon = icon('hp',self)
        atk_icon = icon('atk',self)
        spd_icon = icon('spd',self)
        ran_icon = icon('range',self)
        
        if self.buffing[0] > 0:
            dtype = 'g'
        elif self.hp < self.mhp:
            dtype = 'r'
        else:
            dtype = 'w'
        generate_digits(self.hp,hp_icon,dtype)
        if self.buffing[1] > 0:
            dtype = 'g'
        else:
            dtype = 'w'
        generate_digits(self.display_atk,atk_icon,dtype)
        if self.buffing[2] > 0:
            dtype = 'g'
        else:
            dtype = 'w'
        generate_digits(self.display_spd,spd_icon,dtype)
        if self.buffing[3] > 0:
            dtype = 'g'
        else:
            dtype = 'w'
        generate_digits(self.display_range,ran_icon,dtype)        
        if self.star >=1:
            icon('star',self)
        if self.star >=2:
            icon('star2',self)
        if self.placing:
            icon('place',self)
            
    def place(self,order):
        if self.group == 0:
            self.pos = allyposition(self.order)
            arrangeally(self.order)
        if self.group == 1:
            self.pos = enemyposition(self.order)
            arrangeenemy(self.order)
        
    def touch(self):#when touched by mouse but not draged
        x = self.pos[0]
        y = self.pos[1]
        pos = (x - 50 ,y)
        infotext(self.name,self.lv,self.effects,pos,self)
        
    def drag(self,pos):#when draged
        self.pos = pos
        self.x = self.pos[0]
        self.y = self.pos[1]
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.generate_text()
        
    def refresh(self):
        passiveeffect(self)
        #refresh selfs' stats
        self.hp = min(self.hp,self.mhp)
        self.display_atk = max(self.display_atk,1)
        self.display_spd = max(self.display_spd,1)
        self.display_range = max(self.display_range,1)
        self.atk = max(self.atk,1)
        self.spd = max(self.spd,1)
        self.range = max(self.range,1)
        self.spd = min(self.spd,max_spd)
        self.display_spd = min(self.display_spd,max_spd)
        if self.motion == None and self.effectanimation == None:
            self.image = self.original_image
            if self.group == 0:
                self.pos = allyposition(self.order)
            if self.group == 1:
                self.pos = enemyposition(self.order)
        self.x = self.pos[0]
        self.y = self.pos[1]
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.pos
        self.generate_text()
    
    def round_action(self):#actions per round
        possible = []
        for i in self.foe:
            if self.order+i.order < self.display_range:
                possible.append(i)
        if len(possible) == 0:
            return
        if self.tar == 'rand':#random target
            target = random.choice(possible)
        elif self.tar == 'near':#nearest target
            for i in possible:
                if i.order == 0:
                    target = i
        elif self.tar == 'far':#farthest target
            maxorder = -1
            for i in possible:
                if i.order > maxorder:
                    target = i
                    maxorder =i.order
        #restore the character being attacked
        self.attack(target)
        
    def attack(self,target):#functions when a character attacks an foe
        self.motion = 'attack'
        gamedata.actionlist.add(self)
        self.motionclock = gamedata.attack_time
        self.motionwait = 0
        if 'attack' in self.effects:
            for i in self.effects['attack']:
                attackfunction = eval(i)
                attackfunction(self,target)
        
        target.hurt(self.display_atk)
    
    def hurt(self,damage):#functions when a character receives damage
        pygame.mixer.Sound.play(hit_sound)
        self.motion = 'hurt'
        gamedata.actionlist.add(self)
        self.motionclock = gamedata.hurt_time
        self.motionwait = gamedata.attack_time-1
        
        self.gain_speffect('damage')  
        if 'hurt' in self.effects:
            for i in self.effects['hurt']:
                hurtfunction = eval(i)
                damage = hurtfunction(self,damage)
                damage = max(1,damage) 
        damage = max(1,damage)
        self.damage = damage
        self.hp -= damage
        
    def death(self):
        self.motion = None
        self.effectanimation = None
        pygame.sprite.Sprite.kill(self)
        if 'death' in self.effects:
            for i in self.effects['death']:
                deathfunction = eval(i)
                deathfunction(self)
        data = (self.name,self.star)
        if self.group == 0:#when dead, add to death group
            gamedata.deadally.append(self)
            
        else:
            gamedata.deadenemy.append(self)
        character_death(self,self.group)
        arrangeally(-1)
        arrangeenemy(-1)
        
    def gainstats(self,stats):
        self.buffing = stats
        self.mhp+=stats[0]
        self.hp+=stats[0]
        self.atk+=stats[1]
        self.spd+=stats[2]
        self.range+=stats[3]
        self.gain_speffect('strengthen')
        if 'gain_stats' in self.effects:
            for i in self.effects['gain_stats']:
                function = eval(i)
                function(self,stats)
                
    def addeffect(self,effects):#gain new effect
        for i in effects:
            if i in self.effects:
                for j in effects[i]:
                    if j not in self.effects[i]:
                       self.effects[i].append(j)
            else:
                self.effects.update(effects)
        if 'add_effect' in self.effects:
            for i in self.effects['add_effect']:
                function = eval(i)
                function(self,effect)
    #motions
    def actionmotion(self):
        if self.motion is not None:
            if self.motionwait > 0:
                self.motionwait -=1
            if self.motionwait == 0:
                self.motionclock -=1
                if self.motion == 'attack':
                    self.attackmotion()
                if self.motion == 'hurt':
                    self.hurtmotion()
            if self.motionclock == 0:
                self.motionwait = 0
                self.refresh()
                gamedata.actionlist.remove(self)
                self.motion = None
                    
    def gain_speffect(self,name):
        time = gamedata.effectdata[name]
        effectlist = []
        for i in range(time):
            text = name + str(i)
            effectlist.append(text)
        if self.effectanimation is None:
            self.effectanimation = effectlist
            gamedata.animationlist.add(self)
        else:
            self.effectanimation =  effectlist + self.effectanimation
        
    def sp_animation(self):
        #effectanimation[name,frame]
        
        if len(self.effectanimation) > 0:
            effect = self.effectanimation.pop()
            speffect(effect,self)
        else:
        
             self.effectanimation = None
             gamedata.animationlist.remove(self)
            
        
    def attackmotion(self):
        
        if self.motion:
            if self.group == 0:
                self.image = pygame.transform.rotate(self.original_image,
                                                    -gamedata.attacksequence[self.motionclock])
            else:
                self.image = pygame.transform.rotate(self.original_image,
                                                     gamedata.attacksequence[self.motionclock])
            self.pos = (self.x,self.y)
           
        self.refresh()
        
    def hurtmotion(self):
        generate_damage_digits(self.damage,self, -gamedata.hurtsequence[self.motionclock])
        self.refresh()
        
    def refreshbuffs(self):
        self.damage = 0
        self.buffing = [0,0,0,0]
        self.display_atk = self.atk
        self.display_spd = self.spd
        self.display_range = self.range
        for i in self.buffs:
            #if buff caster is not exist,remove the buff
            if i[1] is 'effect':
                if i[0] not in characters:
                    self.buffs.remove(i)
                    #remove effects haven't updated
                
            if i[0] not in characters:
                self.buffs.remove(i)
            else:#add buffs for user
                if i[1] is 'hp':
                    pass
                if i[1] is 'atk':
                    self.display_atk += i[2]
                if i[1] is 'spd':
                    self.display_spd += i[2]
                if i[1] is 'range':
                    self.display_range += i[2]
        self.display_hp += self.tempstat[0]
        self.display_atk += self.tempstat[1]
        self.display_spd += self.tempstat[2]
        self.display_range += self.tempstat[3]
        self.buffs.clear()
                        
        
class triple_character(pygame.sprite.Sprite):
    def __init__(self,name,star,data):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.data = data
        self.lv = self.data['lv']
        self.hp = self.data['hp']
        self.atk = self.data['atk']
        self.spd = self.data['spd']
        self.range = self.data['range']
        self.tar = self.data['tar']
        self.effects = self.data['effects']
        self.star = star
        self.price = basic_character_prize
        self.touched = False#whether touched
        self.placing = False#whether is being placing
        self.imagename = "images/animals/"+self.name+".png"
        self.image = pygame.image.load(self.imagename).convert_alpha()
        self.price = basic_character_prize
        #when a triple created, add it to hand
        handitems = hand.sprites()
        self.order = len(handitems)+1
        self.pos = handposition(self.order)
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.pos
        self.x = self.pos[0]
        self.y = self.pos[1]
        #self.type = 'handitem'
        self.addtohand()
        self.refresh()
        
    def addtohand(self):
        global store,hand
        self.price = basic_character_prize
        handitems = hand.sprites()
        self.order = len(handitems)+1
        self.pos = handposition(self.order)
        self.type = 'handitem' 
        hand.add(self)
        self.refresh()
        
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
        
        price_text(pri,self)
        if self.star >=1:
            icon('star',self)
        if self.star >=2:
            icon('star2',self)
        if self.placing:
            icon('place',self)
        
    def new_effects(self):
        upgrades = get_upgrades(self.name)
        choice_num = len(upgrades)+1#number of upgradechoice
        order = 0
        for i in upgrades:
            order +=1
            choicedata = upgrade_change(i)
            upgrade_choice(choicedata[0],choicedata[1],choicedata[2],
                           choicedata[3],choice_num,order,self)
        if choice_num > 0:
            gamedata.has_choice = True#stop the game and force to make choice
        self.remove()
    
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
    
    def gainstats(self,stats):
        #self.mhp+=stats[0]
        self.hp+=stats[0]
        self.atk+=stats[1]
        self.spd+=stats[2]
        self.range+=stats[3]
        
    def remove(self):
        pygame.sprite.Sprite.kill(self)
                                               

#effectfunctions:    
#passive
#bufftype: owner,type,amount
def passiveeffect(user):
    passives = []
    if ('passive' in user.effects) is False:
        return
    else:
        passives = user.effects['passive']
    for passive in passives:
        passivefunction = eval(passive)
        passivefunction(user)
        
def addbuff(target,buff):
    for i in target.buffs:
        if i == buff:#if alreadyadded, return
            return
    target.buffs.append(buff)
    
def dog0(user):#character ahead user has +2 attack
    for i in user.friends:
        if i.order == user.order -1:
            buff = (user,'atk',2)
            addbuff(i,buff)
            
def dog1(user):#other friends has +1 attack
    for i in user.friends:
        if i is not user:
            buff = (user,'atk',1)
            addbuff(i,buff)
            
def eagle0(user):#other friends has +1 attack
    for i in user.friends:
        if i.order == user.order +1:
            buff = (user,'range',3)
            addbuff(i,buff)

def eagle1(user):#other friends has +1 attack
    for i in user.friends:
        if i.order == user.order +1:
            buff = (user,'range',3)
            addbuff(i,buff)

def eagle2(user):#other friends has +1 attack
    for i in user.friends:
        if i is not user:
            buff = (user,'range',1)
            addbuff(i,buff)


#battlestarteffect
def lion2(unit,user):
    effect = {'death':'lion_death'}
    for i in user.friends:
        if i is not user:
            i.addeffect(effect)
        
def soldiercrab0(user):
    for i in user.friends:
        if i.order == user.order+1:
            stats=[i.hp,0,0,0]
            proj('candy_hp',i,user)
            user.gainstats(stats)
            
def soldiercrab1(user):
    for i in user.friends:
        if i.order == user.order+1 or i.order == user.order-1:
            stats=[i.hp,0,0,0]
            proj('candy_hp',i,user)
            user.gainstats(stats)

def soldiercrab2(user):
    for i in user.friends:
        if i.order == user.order+1:
            stats=[i.hp,0,0,0]
            proj('candy_ah',i,user)
            user.gainstats(stats)
            user.atk = i.atk

def scorpion0(user):
    maxhp = 0
    target = None
    for i in user.foe:
        if i.hp > maxhp:
            maxhp = i.hp
            target = i
    if target is not None:
        target.hp -= int(target.hp/2)
        target.gain_speffect('weaken')

def scorpion1(user):
    maxhp = 0
    target = None
    for i in user.foe:
        if i.hp > maxhp:
            maxhp = i.hp
            target = i
    if target is not None:
        target.hp -= int(target.hp/2)
        target.gain_speffect('weaken')
    maxhp = 0
    target = None
    for i in user.foe:
        if i.hp > maxhp:
            maxhp = i.hp
            target = i
    if target is not None:
        target.hp -= int(target.hp/2)
        target.gain_speffect('weaken')

def scorpion2(user):
    maxhp = 0
    target = None
    for i in user.foe:
        if i.hp > maxhp:
            maxhp = i.hp
            target = i
    if target is not None:
        target.hp -= int(target.hp/2)
        target.atk -= int(target.atk/2)
        target.gain_speffect('weaken')
    
def marmot0(user):
    stats=[0,2*gamedata.storelv,0,0]
    proj('candy_atk',user,user)
    user.gainstats(stats)

def marmot1(user):
    stats=[0,4*gamedata.storelv,0,0]
    proj('candy_atk',user,user)
    user.gainstats(stats)
    

def marmot2(user):
    friends = user.friends.sprites()
    for i in (friends):
        if i.order == user.order -1:
            stats=[0,gamedata.storelv,0,0]
            proj('candy_atk',user,i)
            i.gainstats(stats)
        if i.order == user.order +1:
            stats=[0,gamedata.storelv,0,0]
            proj('candy_atk',user,i)
            i.gainstats(stats)
    
def frog0(user):
    damage = user.display_atk
    foes = user.foe.sprites()
    if len(foes)>0:
        target = random.choice(foes)
        target.hurt(damage)

def frog1(user):
    damage = user.display_atk
    foes = user.foe.sprites()
    if len(foes)>0:
        target = random.choice(foes)
        target.hurt(damage)
    if len(foes)>0:
        target = random.choice(foes)
        target.hurt(damage)
        
def frog2(user):
    damage = user.display_atk
    damage += int(damage/2)
    foes = user.foe.sprites()
    if len(foes)>0:
        target = random.choice(foes)
        lowest_hp = target.hp
        for i in foes:
            if i.hp < lowest_hp:
                lowest_hp = i.hp
                target = i
        target.hurt(damage)

def narwhal0(user):
    for i in user.foe:
        if i.order == 0:
            effects = {'hurt':['narwhalhurt0']}
            i.addeffect(effects)

def narwhal1(user):
    for i in user.foe:
        if i.order == 0:
            effects = {'hurt':['narwhalhurt1']}
            i.addeffect(effects)
    
#endeffect:
def anglerfish0(user):
    friends = user.friends.sprites()
    friends.remove(user)
    if len(friends)>0:
        i = random.choice(friends)
        gamedata.add_hand.append(i.name)

def anglerfish1(user):
    friends = user.friends.sprites()
    friends.remove(user)
    if len(friends)>0:
        i = random.choice(friends)
        friends.remove(i)
        gamedata.add_hand.append(i.name)
    if len(friends)>0:
        i = random.choice(friends)
        friends.remove(i)
        gamedata.add_hand.append(i.name)

def anglerfish2(user):
     name = generate_lv_item(5)
     gamedata.add_hand.append(name)
     
def orca0(user):
    friends = user.friends.sprites()
    random.shuffle(friends)
    for i in friends:
        for j in gamedata.store:
            if j.range == i.range:
                hp = int(j.hp*0.3)
                atk = int(j.atk*0.3)
                stats=[hp,atk,0,0]
                i.gainstats(stats)
                proj('candy_ah',user,i)
                j.remove()
                break

def orca1(user):
    friends = user.friends.sprites()
    random.shuffle(friends)
    for i in friends:
        for j in gamedata.store:
            if j.range == i.range:
                hp = int(j.hp*0.5)
                atk = int(j.atk*0.5)
                stats=[hp,atk,0,0]
                i.gainstats(stats)
                proj('candy_ah',user,i)
                j.remove()
                break

def orca2(user):
    friends = user.friends.sprites()
    random.shuffle(friends)
    for i in friends:
        for j in gamedata.store:
            hp = int(j.hp*0.4)
            atk = int(j.atk*0.4)
            stats=[hp,atk,0,0]
            i.gainstats(stats)
            proj('candy_ah',user,i)
            j.remove()
            break
            
def shark0(user):
    hp = 0
    atk = 0
    for i in user.friends:
        if i is not user:
            hp += int(i.hp*0.2)
            atk += int(i.atk*0.2)
            i.hp -= int(i.hp*0.2)
            i.atk -= int(i.atk*0.2)
            proj('candy_ah',i,user)
    stats = [hp,atk,0,0]
    user.gainstats(stats)
    

def shark1(user):
    hp = 0
    atk = 0
    for i in user.friends:
        if i is not user:
            hp += int(i.hp*0.3)
            atk += int(i.atk*0.3)
            i.hp -= int(i.hp*0.2)
            i.atk -= int(i.atk*0.2)
            proj('candy_ah',i,user)
    stats = [hp,atk,0,0]
    user.gainstats(stats)

def shark2(user):
    hp = 0
    atk = 0
    for i in user.friends:
        if i.order == user.order -1:
            hp += int(i.hp*0.5)
            atk += int(i.atk*0.5)
            proj('candy_ah',i,user)
            i.death()
            
    stats = [hp,atk,0,0]
    user.gainstats(stats)
    
def rabbit2(user):
    for i in user.friends:
        i.spd +=1

def bee0(user):
    friendunits = user.friends.sprites()
    friendunits.remove(user)
    leng = len(friendunits)
    if len(friendunits)>=1:
        unit = random.choice(friendunits)
        stats = [2,0,0,0]
        proj('candy_hp',user,unit)
        if gamedata.money > 0:
            unit = random.choice(friendunits)
            stats[0] +=2
        unit.gainstats(stats)
        
def bee1(user):
    friendunits = user.friends.sprites()
    friendunits.remove(user)
    if len(friendunits)>=1:
        unit = random.choice(friendunits)
        stats = [4,0,0,0]
        unit.gainstats(stats)
        proj('candy_hp',user,unit)
        if gamedata.money > 0:
            unit = random.choice(friendunits)
            stats[0] +=4
        unit.gainstats(stats)
        
def bee2(user):
    friendunits = user.friends.sprites()
    for i in friendunits:
        if i.order == 0:
            unit = i
        else:
            return
    stats = [2,0,0,0]
    unit.gainstats(stats)
    proj('candy_hp',user,unit)
    for i in range(gamedata.money):
        stats[0] += 3
    unit.gainstats(stats)
            
def fox0(user):
    for i in user.friends:
        if i.star > 0:
            stats = [3,1,0,0]
            user.gainstats(stats)

def fox1(user):
    for i in user.friends:
        if i.star > 0:
            stats = [6,2,0,0]
            user.gainstats(stats)

def fox2(user):
    for i in user.friends:
        if i.star > 0:
            stats = [4,2,0,0]
            i.gainstats(stats)

def sparrow0(user):
    order = 0
    target =user
    for i in user.friends:
        if i.order>order:
            order = i.order
            target = i
    stats = [0,1,0,0]
    target.gainstats(stats)
    proj('candy_atk',user,target)

def sparrow1(user):
    order = 0
    target =user
    for i in user.friends:
        if i.order>order:
            order = i.order
            target = i
    stats = [0,2,0,0]
    target.gainstats(stats)
    proj('candy_atk',user,target)

def sparrow2(user):
    order = 0
    target =user
    for i in user.friends:
        if i.order>user.order:
            stats = [0,1,0,0]
            i.gainstats(stats)
            proj('candy_atk',user,i)
            
def walrus0(user):
    for i in gamedata.store:
        if i.froze is True:
            i.hp+=4
            i.atk+=1

def walrus1(user):
    for i in gamedata.store:
        if i.froze is True:
            i.hp+=8
            i.atk+=2

def walrus2(user):
    frozed = []
    for i in gamedata.store:
        if i.froze is True:
            frozed.append(i)
    if len(frozed)>0:
        i = random.choice(frozed)
        i.hp+=4
        i.atk+=1
        i.addtohand()

def panda0(user):
    friends = user.friends.sprites()
    friends.remove(user)
    random.shuffle(friends)
    for i in range(6):
        for j in friends:
            if j.lv == i:
                stats = [4,1,0,0]
                j.gainstats(stats)
                proj('candy_ah',user,j)

def panda1(user):
    friends = user.friends.sprites()
    friends.remove(user)
    random.shuffle(friends)
    for i in range(6):
        for j in friends:
            if j.lv == i:
                stats = [8,2,0,0]
                j.gainstats(stats)
                proj('candy_ah',user,j)

def panda2(user):
    for j in user.friends:
        stats = [6,2,0,0]
        j.gainstats(stats)
        proj('candy_ah',user,j)
        
#attackeffect
def pheonix0(user,target):
    if user.hp<=18:
        stats = [0,9,0,0]
        user.gainstats(stats)
    else:
        user.hp -=9
        

def pheonix1(user,target):
    if user.hp<=36:
        stats = [0,18,0,0]
        user.gainstats(stats)
    else:
        user.hp -=18

def pheonix2(user,target):
    stats = [0,12,0,0]
    user.gainstats(stats)
    if user.hp <= 12:
        user.hp = 1
    else:
        user.hp -=12
        
def moose0(user,target):
    for i in user.foe:
        if i.order == target.order -1 or i.order == target.order +1:
            damage = int(user.display_atk * 0.7)
            i.hurt(damage)

def moose1(user,target):
    for i in user.foe:
        if i.order == target.order -1 or i.order == target.order +1:
            damage = user.display_atk
            i.hurt(damage)

def tiger0(user,target):
    if user.counter == 0:
        user.counter = user.atk
    stats = [0,user.counter,0,0]
    user.gainstats(stats)

def tiger1(user,target):
    if user.counter == 0:
        user.counter = 2*user.atk
    stats = [0,user.counter,0,0]
    user.gainstats(stats)

def tiger2(user,target):
    user.display_atk += target.atk    
            
def rabbit0(user,target):#friends spd +=1
    for i in user.friends:
        stats = [0,0,1,0]
        i.gainstats(stats)
        proj('candy_spd',user,i)

def rabbit1(user,target):#friends spd +=1
    for i in user.friends:
        stats = [0,0,1,0]
        i.gainstats(stats)
        proj('candy_spd',user,i)
        
def duck0(user,target):#summon a ducck
    data = characterdata['duckling']
    order = user.order
    if user.group == 0:
        arrangeally(order)
    else:
        arrangeenemy(order)
    summon('duckling',order,0,data,user.group)
    
def sloth2(user,target):#gain +4 atk
    stats = [0,5,0,0]
    user.gainstats(stats)
    
def zebra0(user,target):
    for i in user.friends:
        if i.order == user.order +1:
            i.hurt(1)

def zebra1(user,target):
    for i in characters:
        if i is not user:
            i.hurt(1)
            
def pig1(user):
    if user.group is 0:
        gamedata.extra_money +=1

def ostrich0(user,target):#gain +1 atk
    if user.hp > 0.75*user.mhp:
        user.display_atk*=2

def ostrich1(user,target):#gain +1 atk
    if user.hp > 0.75*user.mhp:
        user.display_atk*=3

def ostrich2(user,target):#gain +1 atk
    if user.hp < 0.5*user.mhp:
        user.display_atk*=3

def gorilla1(user,target):#gain +1 atk
    stats = [0,1,0,0]
    user.gainstats(stats)

def narwhal2(user,target):
    effects = {'hurt':['narwhalhurt2']}
    target.addeffect(effects)

def parrot0(user,target):
    effects = []
    friends = user.friends.sprites()
    friends.remove(user)
    for i in friends:
        if 'attack' not in i.effects:
            friends.remove(i)
    if len(friends) == 0:
        return
    i = random.choice(friends)
    if 'attack' in i.effects:
        effects = i.effects['attack']
        for j in effects:
            if j != 'parrot0' and j != 'parrot1' and j != 'parrot2':
                effect = eval(j)
                effect(i,target)

def parrot1(user,target):
    effects = []
    friends = user.friends.sprites()
    friends.remove(user)
    for i in friends:
        if 'attack' not in i.effects:
            friends.remove(i)
    if len(friends) == 0:
        return
    i=random.choice(friends)
    if 'attack' in i.effects:
        effects = i.effects['attack']
        for j in effects:
            if j != 'parrot0' and j != 'parrot1' and j != 'parrot2':
                effect = eval(j)
                effect(i,target)
    i=random.choice(friends)
    if 'attack' in i.effects:
        effects = i.effects['attack']
        for j in effects:
            if j != 'parrot0' and j != 'parrot1' and j != 'parrot2':
                effect = eval(j)
                effect(i,target)

def parrot2(user,target):
    effects = []
    friends = user.friends.sprites()
    friends.remove(user)
    for i in friends:
        if 'attack' not in i.effects:
            friends.remove(i)
    usereffect = set(user.effect.items())
    for j in friends:
        friendeffect = set(j.effect.items())
        if friendeffect.issubset(usereffect):
           friends.remove(j)
    if len(friends) == 0:
        return
    i=random.choice(friends)
    if 'attack' in i.effects:
        effects = i.effects['attack']
        for j in effects:
            user.addeffect(j)
        
def leopard0(user,target):
    damage = 4
    foe = user.foe.sprites()
    if len(foe)>0:
        enemy = random.choice(foe)
        minhp = enemy.hp
    for i in foe:
        if i.hp< minhp:
            enemy = i
            minhp = enemy.hp
    enemy.hurt(damage)

def leopard1(user,target):
    damage = 8
    foe = user.foe.sprites()
    if len(foe)>0:
        enemy = random.choice(foe)
        minhp = enemy.hp
    for i in foe:
        if i.hp<minhp:
            enemy = i
            minhp = enemy.hp
    enemy.hurt(damage)

def leopard2(user,target):
    damage = 12
    foe = user.foe.sprites()
    maxhp = 0
    for i in foe:
        if i.hp>maxhp:
            enemy = i
            maxhp = enemy.hp
    enemy.hurt(damage)

def penguin0(user,target):
    target.spd =1

def penguin1(user,target):
    target.spd =1
    target.atk -=1
    target.atk = max(target.atk,1)

def penguin2(user,target):
    if target.speed < user.speed:
        user.display_damage += 10
    else:
        target.spd =1

def firefly0(user,target):
    friends = user.friends.sprites()
    for i in friends:
        if i.hp >= i.mhp or i is user:
            friends.remove(i)
    if len(friends)>0:
        i= random.choice(friends)
        i.hp+=6
        i.hp = min(i.hp,i.mhp)
        i.gain_speffect('cure')
        
def firefly1(user,target):
    friends = user.friends.sprites()
    for i in friends:
        if i.hp >= i.mhp or i is user:
            friends.remove(i)
    if len(friends)>0:
        i= random.choice(friends)
        i.hp+=12
        i.hp = min(i.hp,i.mhp)
        i.gain_speffect('cure')

def firefly2(user,target):
    for i in user.friends:
        if i is not user:
            i.hp+=6
            i.hp = min(i.hp,i.mhp)
            i.gain_speffect('cure')
    
#hurteffect
def fly2(user,damage):
    if user.lv >1:
        name = generate_lv_item(user.lv-1)
        data = {'lv':0,'hp':0,'atk':0,'spd':0,'range':0,'tar':None,
  'effects':{}}
        data.update(characterdata[name])
        data['hp'] = 1
        order = user.order
        if user.group == 0:
            arrangeally(order)
        else:
            arrangeenemy(order)
        summon(name,order,0,data,user.group)
    return damage

def hippo0(user,damage):
    user.display_atk +=10
    return damage

def hippo1(user,damage):
    user.display_atk +=20
    return damage

def hippo2(user,damage):
    user.display_atk +=10 +user.counter*5
    user.counter+=1
    return damage

def spider0(user,damage):
    for i in user.foe.sprites():
        if i.order == 0:
            reflection = int(damage/2)
            i.hurt(reflection)
    return damage

def spider1(user,damage):
    for i in user.foe.sprites():
        if i.order == 0:
            reflection = int(damage/2)
            i.hurt(reflection)
    return damage

def spider2(user,damage):
    for i in user.foe.sprites():
        if i.order == 0 or i.order == 1:
            reflection = int(damage/2)
            i.hurt(reflection)
    return damage
                    
def badger0(user,damage):
    if damage > user.atk:
        stats = [0,6,0,0]
        user.gainstats(stats)
    return damage

def badger1(user,damage):
    if damage > user.atk:
        stats = [0,12,0,0]
        user.gainstats(stats)
    return damage

def badger2(user,damage):
    if damage > user.atk:
        stats = [0,8,0,0]
        user.gainstats(stats)
    else:
        damage -= int(damage/2)
    return damage

def duck1(user,damage):#summon a ducck
    data = characterdata['duckling']
    order = user.order
    if user.group == 0:
        arrangeally(order)
    else:
        arrangeenemy(order)
    summon('duckling',order,0,data,user.group)
    return damage
    
def sloth0(user,damage):#gain +1 atk
    stats = [0,1,0,0]
    user.gainstats(stats)
    return damage
    
def sloth1(user,damage):#gain +1 atk
    stats = [0,2,0,0]
    user.gainstats(stats)
    return damage
    
def dog2(user,damage):
    for i in user.friends:
        if i.order == user.order +1:
            stats = [0,2,0,0]
            i.gainstats(stats)
            proj('candy_atk',user,i)
    return damage
            
def buffalo0(user,damage):#deal 3 damage
    foes = user.foe.sprites()
    if len(foes)>0:
        i = random.choice(foes)
        i.hurt(3)
    return damage

def buffalo1(user,damage):#deal 3 damage
    foes = user.foe.sprites()
    if len(foes)>0:
        i = random.choice(foes)
        i.hurt(6)
    return damage

def buffalo1(user,damage):#deal 3 damage
    foes = user.foe.sprites()
    amount = 4
    amount += user.counter
    user.counter +=1
    if len(foes)>0:
        i = random.choice(foes)
        i.hurt(amount)
    return damage

def turtle0(user,damage):
    user.gain_speffect('block')
    return damage -3

def turtle1(user,damage):
    user.gain_speffect('block')
    return damage -6

def turtle2(user,damage):
    amount = 4
    amount += user.counter
    user.counter +=1
    user.gain_speffect('block')
    return damage-amount

def narwhalhurt0(user,damage):
    damage+=4
    return damage

def narwhalhurt1(user,damage):
    damage+=int(damage/2)
    return damage

def narwhalhurt2(user,damage):
    damage+=6
    return damage

def koala0(user,damage):
    if user.order > 0:
        damage = int(damage *0.5)
        damage = max(1,damage)
        user.gain_speffect('block')
    return damage

def koala1(user,damage):
    if user.order > 0:
        damage = int(damage *0.3)
        damage = max(1,damage)
        user.gain_speffect('block')
    return damage

def koala2(user,damage):
    friendunits = user.friends.sprites()
    if len(friendunits) == 1:
        damage = int(damage *0.2)
        damage = max(1,damage)
        user.gain_speffect('block')
    return damage

def rhino0(user,damage):
    user.mhp+=1
    for j in gamedata.characterstorage:#the prototype also gain stats
        if j[0]['id'] == user.id:
            j[1]['hp'] +=1
    return damage

def rhino1(user,damage):
    user.mhp+=2
    for j in gamedata.characterstorage:#the prototype also gain stats
        if j[0]['id'] == user.id:
            j[1]['hp'] +=2
    return damage

def alpaca0(user,damage):
    for i in user.friends:
        if i is not user:
            stats = [1,0,0,0]
            i.gainstats(stats)
            proj('candy_hp',user,i)
    return damage

def alpaca1(user,damage):
    for i in user.friends:
        if i is not user:
            stats = [2,0,0,0]
            i.gainstats(stats)
            proj('candy_hp',user,i)
    return damage

def alpaca2(user,damage):
    for i in user.friends:
        if i is not user:
            stats = [1,0,0,0]
            i.gainstats(stats)
            proj('candy_hp',user,i)
            if i.hp<user.hp:
                stats = [0,1,0,0]
                i.gainstats(stats)
    return damage 

#deatheffect
def mole0(user):
    name = generate_lv_item(1)
    data = {'lv':0,'hp':0,'atk':0,'spd':0,'range':0,'tar':None,
  'effects':{}}
    data.update(characterdata[name])
    data['atk']+=1
    order = user.order
    if user.group == 0:
        arrangeally(order)
    else:
        arrangeenemy(order)
    summon(name,order,0,data,user.group)

def mole1(user):
    name = generate_store_item(1)
    data = {'lv':0,'hp':0,'atk':0,'spd':0,'range':0,'tar':None,
  'effects':{}}
    data.update(characterdata[name])
    data['atk']+=1
    order = user.order
    if user.group == 0:
        arrangeally(order)
    else:
        arrangeenemy(order)
    summon(name,order,0,data,user.group)
    
    name = generate_lv_item(1)
    data = characterdata[name]
    data['atk']+=1
    order = user.order
    if user.group == 0:
        arrangeally(order)
    else:
        arrangeenemy(order)
    summon(name,order,0,data,user.group)
    
def mole2(user):
    name = generate_lv_item(2)
    data = {'lv':0,'hp':0,'atk':0,'spd':0,'range':0,'tar':None,
  'effects':{}}
    data.update(characterdata[name])
    data['atk']+=2
    order = user.order
    if user.group == 0:
        arrangeally(order)
    else:
        arrangeenemy(order)
    summon(name,order,0,data,user.group)
    
def fly0(user):
    if user.lv >1:
        name = generate_lv_item(user.lv-1)
        data = {'lv':0,'hp':0,'atk':0,'spd':0,'range':0,'tar':None,
  'effects':{}}
        data.update(characterdata[name])
        data['hp']=1
        effect = {'death':['fly0']}
        if 'death' in data['effects']:
            data['effects']['death'].append('fly0')
        else:
            data['effects'].update(effect)
        order = user.order
        if user.group == 0:
            arrangeally(order)
        else:
            arrangeenemy(order)
        summon(name,order,0,data,user.group)

def fly1(user):
    if user.lv >1:
        name = generate_lv_item(user.lv-1)
        data = {'lv':0,'hp':0,'atk':0,'spd':0,'range':0,'tar':None,
  'effects':{}}
        data.update(characterdata[name])
        effect = {'death':['fly1']}
        if 'death' in data['effects']:
            data['effects']['death'].append('fly1')
        else:
            data['effects'].update(effect)
        order = user.order
        if user.group == 0:
            arrangeally(order)
        else:
            arrangeenemy(order)
        summon(name,order,0,data,user.group)
        
def lion_death(user):
    stats = [0,9,0,0]
    for i in user.friends:
        i.gainstats(stats)
        proj('candy_atk',user,i)
        
def crow0(user):
    if user.group == 0:
        team = gamedata.deadally
    if user.group == 1:
        team = gamedata.deadenemy
    for i in team:
        if i.name == 'crow':
            team.remove(i)
    length = len(team)
    if length >0:
        name = team[0].name
        data = {'lv':0,'hp':0,'atk':0,'spd':0,'range':0,'tar':None,
  'effects':{}}
        data.update(characterdata[name])
        data['hp']=1
        order = user.order
        if user.group == 0:
            arrangeally(order)
        else:
            arrangeenemy(order)
        summon(name,order,0,data,user.group)

def crow1(user):
    if user.group == 0:
        team = gamedata.deadally
    if user.group == 1:
        team = gamedata.deadenemy
    for i in team:
        if i.name == 'crow':
            team.remove(i)
    length = len(team)
    if length >0:
        name = team[0].name
        data = {'lv':0,'hp':0,'atk':0,'spd':0,'range':0,'tar':None,
  'effects':{}}
        data.update(characterdata[name])
        order = user.order
        if user.group == 0:
            arrangeally(order)
        else:
            arrangeenemy(order)
        summon(name,order,0,data,user.group)

def crow2(user):
    if user.group == 0:
        team = gamedata.deadally
    if user.group == 1:
        team = gamedata.deadenemy
    for i in team:
        if i.name == 'crow':
            team.remove(i)
    length = len(team)
    for i in team:
        name = i.name
        data = {'lv':0,'hp':0,'atk':0,'spd':0,'range':0,'tar':None,
  'effects':{}}
        data.update(characterdata[name])
        data['hp']=1
        order = user.order
        if user.group == 0:
            arrangeally(order)
        else:
            arrangeenemy(order)
        summon(name,order,0,data,user.group)
        
def hen0(user):#summon a chick
    data = characterdata['chicken']
    order = user.order
    if user.group == 0:
        arrangeally(order)
    else:
        arrangeenemy(order)
    summon('chicken',order,0,data,user.group)
    
def hen1(user):#summon a chick
    data = characterdata['chicken']
    order = user.order
    if user.group == 0:
        arrangeally(order)
    else:
        arrangeenemy(order)
    summon('chicken',order,0,data,user.group)
    summon('chicken',order,0,data,user.group)

def hen2(user):#summon a chick
    gamedata.add_hand.append('chicken')

def goat0(user):#give a random friends +2 atk
    friends = user.friends.sprites()
    if len(friends)>0:
        i = random.choice(friends)
        stats = [0,3,0,0]
        proj('candy_atk',user,i)
        i.gainstats(stats)
        proj('candy_atk',user,i)

def goat1(user):#give a random friends +2 atk
    friends = user.friends.sprites()
    if len(friends)>0:
        i = random.choice(friends)
        stats = [0,3,0,0]
        proj('candy_atk',user,i)
        i.gainstats(stats)
        friends.remove(i)
    if len(friends)>0:
        i = random.choice(friends)
        stats = [0,3,0,0]
        i.gainstats(stats)
        proj('candy_atk',user,i)

def goat2(user):#give a random friends +2 atk
    friends = user.friends.sprites()
    if len(friends)>0:
        i = random.choice(friends)
        stats = [0,user.atk,0,0]
        proj('candy_atk',user,i)
        i.gainstats(stats)
        proj('candy_ah',user,i)

def snake0(user):#deal 8 damage to a random foe
    foes = user.foe.sprites()
    if len(foes)>0:
        i = random.choice(foes)
        i.hurt(9)

def snake1(user):#deal 8 damage to a random foe
    foes = user.foe.sprites()
    if len(foes)>0:
        i = random.choice(foes)
        i.hurt(9)
    if len(foes)>0:
        i = random.choice(foes)
        i.hurt(9)
        
def snake2(user):#summon a snake
    data = characterdata['shadowsnake']
    order = user.order
    if user.group == 0:
        arrangeally(order)
    else:
        arrangeenemy(order)
    summon('shadowsnake',order,0,data,user.group)
    
def pig0(user):
    if user.group is 0:
        gamedata.extra_money +=1
        
def snail0(user):
    minrange = 99
    for i in user.friends:
        if i.range < minrange:
            minrange = i.display_range
            target = i
    if minrange < 99:
        effect = {'death':['snail0']}
        stats = [5,0,0,0]
        target.gainstats(stats)
        proj('candy_hp',user,target)
        target.addeffect(effect)
        
def snail1(user):
    minrange = 99
    for i in user.friends:
        if i.range < minrange:
            minrange = i.display_range
            target = i
    if minrange < 99:
        effect = {'death':['snail1']}
        stats = [10,0,0,0]
        target.gainstats(stats)
        proj('candy_hp',user,target)
        target.addeffect(effect)


def beaver0(user):
    data = characterdata['timber']
    order = user.order
    if user.group == 0:
        arrangeally(order)
    else:
        arrangeenemy(order)
    summon('timber',order,0,data,user.group)

def beaver1(user):
    data = characterdata['bigtimber']
    order = user.order
    if user.group == 0:
        arrangeally(order)
    else:
        arrangeenemy(order)
    summon('timber',order,0,data,user.group)

def beaver2(user):
    data = characterdata['timber']
    order = user.order
    if user.group == 0:
        arrangeally(order)
    else:
        arrangeenemy(order)
    summon('timber',order,0,data,user.group)
    summon('timber',order,0,data,user.group)
    summon('timber',order,0,data,user.group)

def bat0(user):
    for i in gamedata.characters:
        i.hurt(6)

def bat1(user):
    for i in gamedata.characters:
        i.hurt(12)

def bat2(user):
    damage = 4
    if user.group == 0:
        group = gamedata.deadally.sprites()
    else:
        group = gamedata.enemy.sprites()
    group.remove(user)
    damage += len(group)*2
    for i in gamedata.characters:
        i.hurt(damage)

def rhino2(user):
    user.mhp+=12
    for j in gamedata.characterstorage:#the prototype also gain stats
        if j[0]['id'] == user.id:
            j[1]['hp'] +=12

def summon_rat0(user):
    data = characterdata['rat']
    data['hp'] = 1
    order = user.order
    if user.group == 0:
        arrangeally(order)
    else:
        arrangeenemy(order)
    summon('rat',order,0,data,user.group)

def summon_rat1(user):
    data = characterdata['rat']
    data['hp'] = 1
    order = user.order
    if user.group == 0:
        arrangeally(order)
    else:
        arrangeenemy(order)
    for i in range(5):
        summon('rat',order,0,data,user.group)

def summon_rat2(user):
    data = {'lv':0,'hp':0,'atk':0,'spd':0,'range':0,'tar':None,
  'effects':{}}
    data.update(characterdata['rat'])
    data['effects'] = {'death':'rat2'}
    order = user.order
    if user.group == 0:
        arrangeally(order)
    else:
        arrangeenemy(order)
    summon('rat',order,0,data,user.group)

def rat0(user):
    effect = {'death':['summon_rat0']}
    for i in user.friends:
        if i.order == user.order+1:
            i.addeffect(effect)

def rat1(user):
    effect = {'death':['summon_rat1']}
    for i in user.friends:
        if i.order == user.order+1:
            i.addeffect(effect)

def rat2(user):
    effect = {'death':['summon_rat2']}
    for i in user.friends:
        if i.order == user.order+1:
            i.addeffect(effect)
            
def horse0(user):
    for i in user.friends:
        stats = [5,2,0,0]
        i.gainstats(stats)
        proj('candy_ah',user,i)

def horse1(user):
    for i in user.friends:
        stats = [10,4,0,0]
        i.gainstats(stats)
        proj('candy_ah',user,i)

def horse2(user):
    for i in user.friends:
        stats = [12,5,0,0]
        i.gainstats(stats)
        proj('candy_ah',user,i)
#selleffect:
def chicken1(user):
    friends = user.friends.sprites()
    for i in range(6):
        i = random.choice(friends)
        stats = [8,3,0,0]
        i.gainstats(stats)
        
def chicken2(user):
    #effect in store.py
    pass
        
def monkey0(user):
    for i in store:
        i.atk+=1
        
def monkey1(user):
    for i in store:
        i.atk+=1
        i.mhp+=5
        i.hp+=5
        
def monkey2(user):
    for i in store:
        i.atk+=1
    for i in hand:
        i.atk+=1
    for i in ally:
        stats = [0,1,0,0]
        i.gainstats(stats)
        
def pig2(user):
    gamedata.money +=6
    
def snail2(user):
    minrange = 99
    for i in user.friends:
        if i.range < minrange:
            minrange = i.display_range
            target = i
    if minrange < 99:
        effect = {'sell':['snail2']}
        stats = [7,0,0,0]
        target.gainstats(stats)
        proj('candy_hp',user,target)
        target.addeffect(effect)
    
#summoneffect:
def cow0(unit,user):
    stats = [3,0,0,0]
    unit.gainstats(stats)

def cow1(unit,user):
    stats = [6,0,0,0]
    unit.gainstats(stats)

def cow2(unit,user):
    friends = user.friends.sprites()
    i = random.choice(friends)
    stats = [3,0,0,0]
    i.gainstats(stats)

def giraffe0(unit,user):
    if unit.range > user.display_range:
        stats = [0,1,0,0]
        user.gainstats(stats)

def giraffe1(unit,user):
    if unit.range > user.display_range:
        stats = [0,2,0,0]
        user.gainstats(stats)

def giraffe2(unit,user):
    if unit.range < user.display_range:
        stats = [0,1,0,0]
        user.gainstats(stats)
    else:
        stats = [1,0,0,0]
        user.gainstats(stats)

def bear0(unit,user):
    if gamedata.window == 'battle':
        stats = [6,3,0,0]
        unit.gainstats(stats)

def bear1(unit,user):
    if gamedata.window == 'battle':
        stats = [12,6,0,0]
        unit.gainstats(stats)

def bear2(unit,user):
    if gamedata.window == 'battle':
        stats = [4,2,0,0]
        unit.gainstats(stats)
        data = [unit.lv,unit.hp,unit.atk,unit.spd,unit.range]
        order = unit.order
        if user.group == 0:
            arrangeally(order)
        else:
            arrangeenemy(order)
        summon(unit.name,order,0,data,user.group)
        
        
#frienddeatheffect:
def lion0(unit,user):
    stats = [0,3,0,0]
    for i in user.friends:
        i.gainstats(stats)
        proj('candy_atk',user,i)

def lion1(unit,user):
    stats = [0,6,0,0]
    for i in user.friends:
        i.gainstats(stats)
        proj('candy_atk',user,i)
        
def crocodile0(unit,user):
    stats = [3,2,0,0]
    user.gainstats(stats)
    
def crocodile1(unit,user):
    stats = [6,4,0,0]
    user.gainstats(stats)
    
def crocodile2(unit,user):
    stats = [3,1,0,0]
    user.gainstats(stats)
    for j in gamedata.characterstorage:#the prototype also gain stats
        if j[0]['id'] == user.id:
            j[1]['hp'] +=3
            j[1]['atk'] +=1

def hyena0(unit,user):
    user.hp+=10
    stats = [0,1,0,0]
    user.gain_speffect('cure')
    user.gainstats(stats)    
    user.hp=min(user.hp,user.mhp)

def hyena1(unit,user):
    user.hp+=20
    stats = [0,1,0,0]
    user.gain_speffect('cure')
    user.gainstats(stats)
    user.hp=min(user.hp,user.mhp)

def hyena2(unit,user):
    user.hp+=12
    if user.hp > user.mhp:
        user.gain_speffect('cure')
        amount = user.hp-user.mhp
        stats = [0,amount,0,0]
        user.gainstats(stats)
    user.hp=min(user.hp,user.mhp)

def vulture0(unit,user):
    if 'death' in unit.effects:
        effects = unit.effects['death']
        for j in effects:
            effect = {'death':[j]}
            user.addeffect(effect)
                
def vulture1(unit,user):
    if 'death' in unit.effects:
        effects = unit.effects['death']
        for j in effects:
            effect = {'death':[j]}
            user.addeffect(effect)
            effect = eval(j)
            effect(unit)

def vulture2(unit,user):
    if 'death' in unit.effects:
        effects = unit.effects['death']
        stats = [0,8,0,0]
        user.gain_speffect('cure')
        user.gainstats(stats)
        for j in effects:
            effect = {'death':[j]}
            user.addeffect(effect)
    
#gain stats effect
def elephant0(user,stats):
    for j in gamedata.characterstorage:#the prototype also gain stats
        if j[0]['id'] == user.id:
            j[1]['hp'] +=stats[0]
            j[1]['atk'] +=stats[1]
            j[1]['spd'] +=stats[2]
            j[1]['range'] +=stats[3]

def elephant1(user,stats):
    user.mhp+= int(stats[0]/2)
    user.hp+= int(stats[0]/2)
    user.atk+= int(stats[1]/2)
    user.spd+= int(stats[2]/2)
    user.range+= int(stats[3]/2)
    for j in gamedata.characterstorage:#the prototype also gain stats
        if j[0]['id'] == user.id:
            j[1]['hp'] +=stats[0] + int(stats[0]/2)
            j[1]['atk']+=stats[1] + int(stats[1]/2)
            j[1]['spd'] +=stats[2] + int(stats[2]/2)
            j[1]['range'] +=stats[3] + int(stats[3]/2)

def elephant2(user,effect):
    for j in gamedata.characterstorage:#the prototype also gain stats
        if j[0]['id'] == user.id:
            j[1]['effects']=user.effects

def camel0(user,stats):
    friends = user.friends.sprites()
    friends.remove(user)
    if len(friends)>0:
        i = random.choice(friends)
        i.mhp+=stats[0]
        i.hp+=stats[0]
        i.atk+=stats[1]
        i.spd+=stats[2]

def camel1(user,stats):
    friends = user.friends.sprites()
    friends.remove(user)
    if len(friends)>0:
        i = random.choice(friends)
        i.mhp+=stats[0]
        i.hp+=stats[0]
        i.atk+=stats[1]
        i.spd+=stats[2]
        friends.remove(i)
    if len(friends)>0:
        i = random.choice(friends)
        i.mhp+=stats[0]
        i.hp+=stats[0]
        i.atk+=stats[1]
        i.spd+=stats[2]
        
#global effect
def end_turn_effects(stage):
    #trigger end turn effects
    for i in ally:
        if 'end' in i.effects:
            ends = i.effects['end']
            for j in ends:
                effect = eval(j)
                effect(i)
                
def character_born(unit,group):                
    if group == 0:
        team  = ally
    else:
        team  = enemy
    for i in team:
        if 'friend_summon' in i.effects:
            effects = i.effects['friend_summon']
            for j in effects:
                effect = eval(j)
                effect(unit,i)
                    
def character_death(unit,group):
    if group == 0:
        team  = ally
    else:
        team  = enemy
    for i in team:
        if 'friend_death' in i.effects:
            effects = i.effects['friend_death']
            for j in effects:
                effect = eval(j)
                effect(unit,i)

def sell_effect(unit):
    if 'sell' in unit.effects:
        sells = unit.effects['sell']
        for i in sells:
            sellfunction = eval(i)
            sellfunction(unit)
    else:
        return

def test_triple(unit):#test if their is a triple
    same = 0
    if unit.star > 0:
        return False
    for i in gamedata.ally:
        if i.name == unit.name and i.star == unit.star and i.star == 0:
            same +=1
    for i in gamedata.hand:
        if i.name == unit.name and i.star == unit.star and i.star == 0:
            same +=1
            
    if same >= 3:
        same = 3
        extrastats = [0,0,0,0]
        for i in gamedata.ally:
            if same > 0 and i.name == unit.name and i.star == 0:
                i.buffs.clear()
                extrastats = comparestat(i,i.name,extrastats)#add extrastats
                gamedata.characters.remove(i)
                pygame.sprite.Sprite.kill(i)
                same -=1
        for i in gamedata.hand:
            if same > 0 and i.name == unit.name and i.star == 0:
                extrastats = comparestat(i,i.name,extrastats)#add extrastats
                pygame.sprite.Sprite.kill(i)
                for j in gamedata.hand:#other cards move 1 left
                    if j.order > i.order:
                        j.order -=1
                same -=1
                
        data = {'lv':unit.lv,'hp':unit.hp+extrastats[0],'atk':unit.atk+extrastats[1],
                'spd':unit.spd+extrastats[2],'range':unit.range+extrastats[3],'tar':unit.tar,
                'effects':unit.effects}
        pygame.sprite.Sprite.kill(unit)
        triple_character(unit.name,1,data)
        return True
    else:
        return False

def comparestat(unit,name,extrastats):
    data = character_data(name)
    if unit.hp > data['hp']:
       extrastats[0]+=unit.hp - data['hp']
    if unit.atk > data['atk']:
       extrastats[1]+=unit.atk - data['atk']
    if unit.spd > data['spd']:
       extrastats[2]+=unit.hp - data['spd']
    if unit.range > data['range']:
       extrastats[3]+=unit.range - data['range']
    return extrastats

            