import pygame
from pygame import Color
from pygame.locals import *
import pgzrun
import math
import random
import time
import sys
#gamefunctions
import gamedata
from gamedata import*
from gametext import*
from character import*
from store import*
from battlefunction import*
#initiate
pygame.init()

#initial vars:
mouse_type = 'info'
#time
t = pygame.time.get_ticks() #该时间指的从pygame初始化后开始计算，到调用该函数为止
clock = pygame.time.Clock()
#main fake_screen
screen = pygame.display.set_mode(screensize,HWSURFACE|DOUBLEBUF|RESIZABLE)
fake_screen = screen.copy()
fake_screen.fill(Color('white')) 
pygame.display.set_caption('ZooChess')
wallpaper = (255,255,255)
#game settings:
def game_setting():
    if setting:
        for i in buttons:
            if i.name == 'plus' or i.name == 'minus':
                buttons.remove(i)
    else:
        button('plus',pos)
        pos = (1/2*Width,Height*1/2)
        button('minus',pos)
        pos = (1/2*Width,Height*1/2)

def change_size(option):
    global sizerate
    if option == 1:
        sizerate +=0.05
    elif option == 0:
        sizerate -= 0.05
    sizerate = min(1,sizerate)
    sizerate = max(0.2,sizerate)
    print(sizerate)
    screen = pygame.display.set_mode((int(screensize[0]*sizerate),
                                                 int(screensize[1]*sizerate)),
                                                 HWSURFACE|DOUBLEBUF|RESIZABLE)
#update
def big_update():
    pass
    
def updategame():
    updatevar()
    updateimage()
    
def updatevar():
    if len(gamedata.add_hand) >0:#their are something add to hand
        for i in gamedata.add_hand:
            gamedata.add_hand.remove(i)
            new_item = storecharacter(i,0,0,0)
            new_item.price = basic_character_prize
            handitems = hand.sprites()
            new_item.order = len(handitems)+1
            new_item.pos = handposition(new_item.order)
            new_item.type = 'handitem'
            if test_triple(new_item) is False:
                hand.add(new_item)
                store.remove(new_item)
                new_item.refresh()

def updateimage():
    #draw infos
    icons.empty()
    texts.clear()
    infotexts.clear()
    for i in backgrounds:
        fake_screen.blit(i.image, i.rect)
    if gamedata.window == 'store':#only draw storeitems in storeview
        for i in store:
            i.update()
            if i.touched:
                i.touch()
            fake_screen.blit(i.image, i.rect)
        for i in hand:
            i.update()
            if i.touched:
                i.touch()
                fake_screen.blit(i.image, i.rect)
        for i in gamedata.characters:
            if draged.has(i) is False:
                i.refresh()
            if i.touched:
                i.touch()
            fake_screen.blit(i.image, i.rect)
    if gamedata.window == 'battle':#draw battleitems
        if gamedata.battlestart is True:#if game started
            if gamedata.roundstart is False:#if round haven't start, initialize the round
                roundfunction(gamedata.round_number)
            elif gamedata.actionclock == 0 and gamedata.acting_character is not None and characters.has(gamedata.acting_character):
                #while action finished, refresh its place and refresh the acting character
                if gamedata.acting_character.motion == 'attack':
                    gamedata.acting_character.motion = None
                    gamedata.acting_character.refresh()
                    gamedata.target_character.hurt(gamedata.acting_character.display_atk)
                    #run the hurt function
                    gamedata.acting_character = gamedata.target_character
                    gamedata.actionclock = 1/2*gamedata.actiontime
                    #play the motion of attacked character
                else:
                    #attacked character finished motion, clear the acting_char for next acting character
                    gamedata.acting_character.refresh()
                    if gamedata.acting_character != gamedata.target_character and gamedata.target_character is not None:
                        #if their are new hurt target, change the acting character
                        gamedata.acting_character = gamedata.target_character
                        gamedata.actionclock = 1/2*gamedata.actiontime
                        gamedata.acting_character.refresh()
                    else:
                        gamedata.acting_character.motion = None
                        gamedata.acting_character = None
                        
                        
            elif gamedata.acting_character is not None and characters.has(gamedata.acting_character):#unfinished action, play the action motion
                if gamedata.acting_character.motion == 'attack':
                    gamedata.acting_character.attackmotion()
                elif gamedata.acting_character.motion == 'hurt':
                    gamedata.acting_character.hurtmotion()
                    
            else:#no acting character, generate a new one,and update the groups
                for i in characters:
                    if i.hp <= 0:
                        i.death()
                if acting_character is not None and characters.has(gamedata.acting_character):#the someeffect cause new action
                    take_action(gamedata.acting_character)#the function of a character's action
                    gamedata.actionclock = 1
                else:
                    gamedata.acting_character = next_character()#try to add fastest the unacted character
                    if gamedata.acting_character is not None and characters.has(gamedata.acting_character):
                        take_action(gamedata.acting_character)#the function of a character's action
                        gamedata.actionclock = 1
                    else:#all characters finished its round,then round is end
                        end_round()
        for i in characters:
            if draged.has(i) is False:
                i.refresh()
            if i.touched:
                i.touch()
            fake_screen.blit(i.image, i.rect)
            
    if gamedata.window == 'store' or gamedata.window == 'battle':
        updatemoney()
        for i in hand:
            i.update()
            fake_screen.blit(i.image, i.rect)
    for i in clicked_buttons:
        i.refresh()
    for i in buttons:
        fake_screen.blit(i.image, i.rect)
        if i.name == 'arrowup':
            if gamedata.storelv < gamedata.max_storelv:
                text = '$'
                text += str(gamedata.store_level_cost)
            else:
                text = 'max'
            price_text(text,i)
        if i.name == 'refresh':
            text = '$'
            text += str(gamedata.refresh_cost)
            price_text(text,i)
    for i in icons:
        fake_screen.blit(i.image, i.rect)
    for i in texts:
        fake_screen.blit(i.content, i.pos)
    for i in infotexts:
        #print all abilities of a character line by line
        line = 0
        for j in i.contents:
            pos = (i.x,i.y+50*line)
            fake_screen.blit(j, pos)
            line += 1
            
    for i in tip_images:
        i.refresh()
        fake_screen.blit(i.image, i.rect)    
    for i in tips:
        i.refresh()
        fake_screen.blit(i.content, i.Rect.center)
        
    if gamedata.has_choice is True:
        for i in choices:
            x = i.x
            y = i.y
            tip ('Choose a new ability for this unit',(1/2*Width -300,1/6*Height),180)
            pygame.draw.rect(fake_screen, (0,255,255), i.rect)
            pos = (x,y-90)
            fake_screen.blit(i.line1, pos)
            pos = (x,y-30)
            fake_screen.blit(i.line2, pos)
            pos = (x,y+30)
           #fake_screen.blit(self.line3, pos)
    
#buttonfunctions
def buttonfunction(i):
    i.flick()
    #setting
    if i.name is 'setting':
        game_setting()
    if i.name is 'plus':
        change_size(1);
    if i.name is 'minus':
        change_size(0);
        
    if i.name is 'buttonstart' or i.name is 'tostore':
        store_initialize()
        return
    if i.name is 'refresh':
        refreshstore(1)
        return
    if i.name is 'freeze':
        freeze_store()
        return
    if i.name is 'arrowup':
        store_levelup()
        return
    if i.name is 'tobattle':
        end_turn_effects(gamedata.stage)
        battle_initialize()
        return
    if i.name is 'battlestart':
        buttons.remove(i)
        battle_start_function()
        return
    if i.name is 'checkmark':#get the info of current team
        print_team_info()
        return
#initialize function:
def windowclear():#clear current gamedata.window
    buttons.empty()
    backgrounds.empty()
    icons.empty()
    draged.empty()
    texts.clear()
    tips.clear()
    
def game_initialize():#the mian game initialize function
    initialize_startwindow()
    initialize_data()

def initialize_data():
    for i in gamedata.characterdata:
        data = gamedata.characterdata[i]
        level = data['lv']
        if level == 1:
            gamedata.lv1.append(i)
        if level == 2:
            gamedata.lv2.append(i)
        if level == 3:
            gamedata.lv3.append(i)
        if level == 4:
            gamedata.lv4.append(i)
        if level == 5:
            gamedata.lv5.append(i)
    
def initialize_startwindow():#start gamedata.window you enter
    global Height,Width
    pos = (1/2*Width,3/4*Height)
    button('buttonstart',pos)
    
def store_initialize():#initialize the store 
    global Height,Width
    gamedata.window = 'store'
    #update vars
    gamedata.store_level_cost -=1
    gamedata.store_level_cost = max(gamedata.store_level_cost,0)
    gamedata.stage +=1
    gamedata.MAX_money +=1
    gamedata.MAX_money = min(gamedata.MAX_money,MAX_MAX_money)
    #clear stuffs
    windowclear()
    for i in gamedata.characters:
        pygame.sprite.Sprite.kill(i)
    gamedata.characters.empty()
    gamedata.deadally.clear()
    gamedata.deadenemy.clear()
    gamedata.money =gamedata.MAX_money
    gamedata.money += gamedata.extra_money
    gamedata.extra_money = 0
    gamedata.allyfront = 1/2*Width
    gamedata.allyheight = 1/2*Height + 50
    for i in gamedata.characterstorage:#remember the characters
        data1 = i[0]
        data2= i[1]
        name = data1['name']
        order = data1['order']
        star = data1['star']
        summon(name,order,star,data2,0)
        
    for i in hand:#test triples
        test_triple(i)
    #draw buttons
    pos = (13/16*Width,Height*1/12)
    button('refresh',pos)
    pos = (14/16*Width,Height*1/12)
    button('freeze',pos)
    pos = (7/8*Width,Height-150)
    button('pouch',pos)
    pos = (1/8*Width,Height*3/4)
    button('tobattle',pos)
    pos = (1/8*Width,Height*1/4)
    button('checkmark',pos)
    pos = (1/16*Width,Height*1/12)
    button('arrowup',pos)
    pos = (15/16*Width,Height*1/12)
    button('setting',pos)
    #draw backgrounds
    size = (Width,int(Height/5))
    pos = (1/2*Width,150)
    background('store_area',size,pos)
    pos = (1/2*Width,1/2*Height+50)
    background('team_area',size,pos)
    pos = (1/2*Width,Height-150)
    background('hand_area',size,pos)
    refreshstore(0)
    
def battle_initialize():#initialize battlefield
    global battlestart
    gamedata.window = 'battle'
    windowclear()
    gamedata.battlestart = False
    #clear groups
    gamedata.sequence.clear()
    gamedata.characterstorage.clear()
    #variables
    gamedata.actiontime = -1
    gamedata.round = 0
    gamedata.allyfront = 1/2*Width
    gamedata.allyheight = 1/2*Height + 50
    initialize_battlefield(gamedata.stage)
    #draw buttons
    pos = (7/8*Width,Height-150)
    button('pouch',pos)
    pos = (1/2*Width,Height*1/4)
    button('battlestart',pos)
    #draw backgrounds
    size = (Width,300)
    pos = (1/2*Width,1/2*Height+50)
    background('team_area',size,pos)
    roundfunction(0)
    
#motions function
def mouse_down(pos):
    global draged,store,hand   
    for i in buttons:
        if i.rect.collidepoint(pos):
            buttonfunction(i)
    if gamedata.has_choice is True:#if clicked a choice, choose it
        for i in choices:
            if i.Rect.collidepoint(pos):
                i.choose()
                item = i.target
                x = item.x
                order = order_interval(x)
                data = {'lv':item.lv,'hp':item.hp,'atk':item.atk,'spd':item.spd,'range':item.range,'tar':item.tar,
                'effects':item.effects}
                summon(item.name,order,item.star,data,0)
                pygame.sprite.Sprite.kill(item)
                arrangeally(-1)
        return
    if gamedata.window == 'store' or gamedata.battlestart is False:
        #check drag, only in store view
        isdrag = False
        dragedsprites = draged.sprites()
        if len(dragedsprites) >0:
            isdrag = True
        if isdrag is False:
            #if mouse collide a dragable item,drag it
            for i in store:
                if i.rect.collidepoint(pos):
                    draged.add(i)
                    isdrag = True
                    break
            for i in hand:
                if i.rect.collidepoint(pos):
                    draged.add(i)
                    isdrag = True
                    break
            #when drag a character, it leave its place
            for i in ally:
                if i.rect.collidepoint(pos):
                    arrangeally(i.order)
                    draged.add(i)
                    i.drag(pos)
                    isdrag = True
                    arrangeally(-1)
                    break
                
            for i in ally:
                if i.rect.collidepoint(pos):
                    arrangeally(i.order)
                    draged.add(i)
                    i.drag(pos)
                    isdrag = True
                    arrangeally(-1)
                    break
                
def mouse_up(pos):
    global draged
    #released draged item
    if gamedata.window == 'store'or battlestart == False:
        dragedsprites = draged.sprites()
        if len(dragedsprites) > 0:
            for i in draged:
                release(i)
    draged.empty()
    arrangeally(-1)

def mouse_motion(pos):
    global draged
    #check if item are touched,refreshing the placing condition
    for i in store:
        i.placing = False
        if checktouch(i,pos):
            break
    for i in hand:
        i.placing = False
        if checktouch(i,pos):
            break
    for i in characters:
        i.placing = False
        if checktouch(i,pos):
            break       
    for i in characters:
        i.placing = False
        if checktouch(i,pos):
            break
    if gamedata.window == 'store' or battlestart == False:
        #if draged, update position and show place icon if in the ally area
        for i in draged:
            i.drag(pos)
            show_place(i)
            break
            
    pygame.display.update()
    
    
def key_motion(key): #get key input
    pass

def key_up():#functions when key up
    pass

#game functions
game_initialize()
while True:
    global sizerate
    clock.tick(fps)#fps = 60
    # 循环获取事件，监听事件
    for event in pygame.event.get():
        # 判断用户是否点了关闭按钮
        if event.type == pygame.QUIT:
            # 当用户关闭游戏窗口时执行以下操作
            # 这里必须调用quit()方法，退出游戏
            pygame.quit()
            #终止系统
            sys.exit()
        elif event.type == VIDEORESIZE:
                screen = pygame.display.set_mode((int(screensize[0]*sizerate),
                                                 int(screensize[1]*sizerate)),
                                                 HWSURFACE|DOUBLEBUF|RESIZABLE)
        #motions
        #when choosing, can not do other things
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = (int(event.pos[0]/sizerate),int(event.pos[1]/sizerate))
            mouse_down(pos)
        if gamedata.has_choice is False: 
            if event.type == pygame.MOUSEBUTTONUP:
                pos = (int(event.pos[0]/sizerate),int(event.pos[1]/sizerate))
                mouse_up(pos)
            if event.type == pygame.MOUSEMOTION:
                pos = (int(event.pos[0]/sizerate),int(event.pos[1]/sizerate))
                mouse_motion(pos)
            if event.type == pygame.KEYDOWN:
                key_motion(event.key)
            if event.type == pygame.KEYUP:
                key_up()
            
    #更新并绘制屏幕内容
    fake_screen.fill(wallpaper)
    updategame()
    screen.blit(pygame.transform.scale(fake_screen, screen.get_rect().size), (0, 0))   
    pygame.display.update()

mainloop()