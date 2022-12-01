'''
try:
    import pygame_sdl2
    pygame_sdl2.import_as_pygame()
except ImportError:
    pass
'''
import os
import math
import random
import time
import sys
#window pos
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,35)
import pygame
import pgzrun
from pygame import Color
from pygame.locals import *
#gamefunctions
#initialize pygame
pygame.init()
import gamedata
from gamedata import*
from gametext import*
from character import*
from store import*
from battlefunction import*
#initiate
setting = False
tobattle = False
quitgame = False
#initial vars:
mouse_type = 'info'
#time
t = pygame.time.get_ticks() 
clock = pygame.time.Clock()
#main fake_screen
screen = pygame.display.set_mode(screensize, HWSURFACE|DOUBLEBUF|RESIZABLE
                                 )
fake_screen = screen.copy()
fake_screen.fill(Color('white')) 
pygame.display.set_caption('Cube Animals')
wallpaper = (255,255,255)
#game settings:
def game_setting():
    global setting
    if setting:
        for i in buttons:
            if i.name == 'scrup' or i.name == 'scrdown' or i.name == 'volup' or i.name == 'voldown':
                buttons.remove(i)
        for i in backgrounds:
            if i.name == 'setting_back':
                backgrounds.remove(i)
                foregrounds.remove(i)
        setting = False
    else:
        setting = True
        
        pos = (0.52*Width,Height*0.46)
        button('voldown',pos)
        pos = (0.59*Width,Height*0.46)
        button('volup',pos)
        
        pos = (0.52*Width,Height*0.645)
        button('scrdown',pos)
        pos = (0.59*Width,Height*0.645)
        button('scrup',pos)
        size = (565,719)
        pos = (0.5*Width,Height*0.5)
        foreground('setting_back',size,pos)
        

def change_size(option):
    global sizerate
    if option == 1:
        sizerate +=0.05
    elif option == 0:
        sizerate -= 0.05
    sizerate = min(1,sizerate)
    sizerate = max(0.2,sizerate)
    screen = pygame.display.set_mode((int(screensize[0]*sizerate),
                                    int(screensize[1]*sizerate)),
                                    HWSURFACE|DOUBLEBUF|RESIZABLE
                                     )

def hidestore(button):
    for i in backgrounds:
        if i.name == 'store_area':
            pass
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
    global tobattle
    #draw infos
    texts.clear()
    infotexts.clear()
    check_max_refresh()
    icons.empty()
    #display images
    for i in backgrounds:
        fake_screen.blit(i.image, i.rect)
    if gamedata.window == 'store':#only draw storeitems in storeview
        icons.empty()
        for i in store:
            if i.placing is True:
                icon('place',i)
            if draged.has(i) is False:
                i.refresh()
            if i.touched:
                i.touch()
            fake_screen.blit(i.image, i.rect)
        for i in hand:
            if i.placing is True:
                icon('place',i)
            if draged.has(i) is False:
                i.refresh()
            if i.touched:
                i.touch()
                fake_screen.blit(i.image, i.rect)
        for i in gamedata.characters:
            if i.placing is True:
                icon('place',i)
            if draged.has(i) is False:
                i.refresh()
            if i.touched:
                i.touch()
            animations = gamedata.animationlist.sprites()
            if len(animations)>0:#action finished, show the effect animation
                for i in animations:
                    i.sp_animation()
            fake_screen.blit(i.image, i.rect)
    if gamedata.window == 'battle':#draw battleitems
        if gamedata.battlestart is True:#if battle started
            animations = gamedata.animationlist.sprites()
            if len(animations)>0:#action finished, show the effect animation
                for i in animations:
                    if characters.has(i):
                        i.sp_animation()
                    
            if gamedata.roundstart is False:#if round haven't start, initialize the round
                roundfunction(gamedata.round_number)
            elif len(gamedata.actionlist.sprites())>0:
                #animation continue
                for i in gamedata.actionlist:
                    if characters.has(i):
                        i.actionmotion()
                        
            elif len(gamedata.projs.sprites())>0:#no projectile animation
                for i in projs:
                    i.update()
                    fake_screen.blit(i.image, i.rect)
                   
            elif len(animations)==0:#no acting character or animation, generate a new action,and update the groups
                for i in characters:
                    i.refreshbuffs()
                    if i.hp <= 0:
                    #update dead characters
                        i.death()                        
                acting_character = next_character()#try to add fastest the unacted character
                if acting_character is not None:
                    take_action(acting_character)#the function of a character's action
                else:#all characters finished its round,then round is end
                     end_round()
            

        for i in characters:
            if i.placing is True:
                icon('place',i)
            if draged.has(i) is False:
                i.refresh()
            if i.touched:
                i.touch()
            fake_screen.blit(i.image, i.rect)
        
            
    if gamedata.window == 'store' or gamedata.window == 'battle':
        updatemoney()
        for i in hand:
            if draged.has(i) is False:
                i.refresh()
            fake_screen.blit(i.image, i.rect)
        
    for i in foregrounds:
        fake_screen.blit(i.image, i.rect)
        
    for i in clicked_buttons:
        i.refresh()
        
    for i in buttons:
        fake_screen.blit(i.image, i.rect)
        if i.name == 'upgrade':
            if gamedata.storelv < gamedata.max_storelv:
                text = '$'
                text += str(gamedata.store_level_cost)
                generate_digit_text(text,i,'w')
            else:
                text = ''
            
        if i.name == 'refresh':
            text = ''
            text += str(gamedata.refresh_time)
            text += '!'
            text += str(gamedata.max_refresh)
            
            generate_digit_text(text,i,'w')
            
        if i.name == 'life':
            text = ''
            text += str(gamedata.life)
            generate_digit_text(text,i,'m')
            
    for i in icons:
        fake_screen.blit(i.image, i.rect)
        
    #for i in digits:
        #fake_screen.blit(i.image, i.rect)
        
    for i in texts:
        fake_screen.blit(i.content, i.pos)
        
    for i in tip_images:
        i.refresh()
        fake_screen.blit(i.image, i.rect)
    for i in infotexts:
        #print all abilities of a character line by line
        line = 0
        for j in i.contents:
            pos = (i.x,i.y+50*line)
            fake_screen.blit(j, pos)
            line += 1   
    for i in tips:
        i.refresh()
        fake_screen.blit(i.content, i.Rect.center)
        
    if gamedata.has_choice is True:
        have_back = False#the background of choices
        for i in backgrounds:
            if i.name == 'triple_back':
                have_back = True
        if have_back is False:
            size = (1557,804)
            pos = (0.5*Width,Height*0.5)
            foreground('triple_back',size,pos)
        for i in choices:
            fake_screen.blit(i.image, i.rect)
            fake_screen.blit(i.unitimage,(0.45*Width,Height*0.4))
            x = i.x
            y = i.y
            #print discription text
            for text in i.new_properties:
               line = f3.render(text,False,(0,0,0))#new ability
               rect = line.get_rect()
               fake_screen.blit(line, (x-215,y+50))
               y+=75
            #print stats text
            line = f3.render("+"+str(i.stats[0]),False,(0,0,0))#new ability
            rect = line.get_rect()
            fake_screen.blit(line, (x-135,i.y-210))
            
            line = f3.render("+"+str(i.stats[1]),False,(0,0,0))#new ability
            rect = line.get_rect()
            fake_screen.blit(line, (x+40,i.y-210))
            
            line = f3.render("+"+str(i.stats[2]),False,(0,0,0))#new ability
            rect = line.get_rect()
            fake_screen.blit(line, (i.x+194,i.y-210))
    else:
        for i in backgrounds:
            if i.name == 'triple_back':
                backgrounds.remove(i)
                foregrounds.remove(i)
           #fake_screen.blit(self.line3, pos)
    #whether to battle or not
    animations = gamedata.animationlist.sprites()
    if tobattle == True:
        if len(gamedata.projs.sprites())>0:#store proj
            for i in projs:
                i.update()
                fake_screen.blit(i.image, i.rect)
        elif len(animations) > 0:
             pass
        else:
            tobattle = False
            battle_initialize()
    
#buttonfunctions
def buttonfunction(i):
    global tobattle
    i.click()
    #setting
    if i.name is 'setting':
        game_setting()
        pygame.mixer.Sound.play(button_sound)
    if i.name is 'scrup':
        change_size(1)
    if i.name is 'scrdown':
        change_size(0)
    if i.name is 'hide_store':
        hidestore(i)  
    if i.name is 'game_start' or i.name is 'tostore':
        store_initialize()
        return
    if i.name is 'refresh':
        refreshstore(1)
        return
    if i.name is 'freeze':
        freeze_store()
        return
    if i.name is 'upgrade':
        store_levelup()
        pygame.mixer.Sound.play(button_sound)
        return
    if i.name is 'end_turn':
        pygame.mixer.Sound.play(button_sound)
        end_turn_effects(gamedata.stage)
        #print_team_info()
        tobattle = True
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
    tip_images.clear()
    
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
    button('game_start',pos)
    
def store_initialize():#initialize the store 
    global Height,Width
    gamedata.summon_trigger = False
    gamedata.window = 'store'
    #update vars
    gamedata.refresh_time = 0
    gamedata.store_level_cost -=1
    gamedata.store_level_cost = max(gamedata.store_level_cost,0)
    gamedata.stage +=1
    gamedata.MAX_money +=1
    gamedata.MAX_money = min(gamedata.MAX_money,MAX_MAX_money)
    #clear stuffs
    windowclear()
    pygame.mixer.music.stop()
    pygame.mixer.music.load('sounds\store.mp3')
    pygame.mixer.music.play(loops=0,start=0)
    for i in gamedata.characters:
        pygame.sprite.Sprite.kill(i)
    gamedata.characters.empty()
    gamedata.actionlist.empty()
    gamedata.animationlist.empty()
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
    gamedata.ally.sprites().sort(key=takeorder)
    arrangeally(-1)
    for i in hand:#test triples
        test_triple(i)
    gamedata.summon_trigger = True
    #draw buttons
    pos = (13/16*Width,Height*1/12)
    button('refresh',pos)
    pos = (14/16*Width,Height*1/12)
    button('freeze',pos)
    pos = (0.87*Width,Height*0.23)
    button('end_turn',pos)
    pos = (1/16*Width,Height*1/12)
    button('upgrade',pos)
    pos = (15/16*Width,Height*1/12)
    button('setting',pos)
    pos = (0.82*Width,Height*0.8)
    button('pouch',pos)
    #draw backgrounds
    size = (Width,Height)
    pos = (1/2*Width,0.5*Height)
    background('main_back',size,pos)
    pos = (1/2*Width,0.84*Height)
    size = (Width,Width*178/1200)
    background('hand_area',size,pos)
    size = (Width,int(Height*0.3))
    pos = (1/2*Width,Height*0.15)
    background('store_area',size,pos)
    pos = (0.065*Width,0.68*Height)
    button('life',pos)
    refreshstore(0)
    
def battle_initialize():#initialize battlefield
    global battlestart
    gamedata.window = 'battle'
    windowclear()
    gamedata.battlestart = False
    #clear groups
    gamedata.sequence.clear()
    gamedata.characterstorage.clear()
    gamedata.actionlist.empty()
    gamedata.animationlist.empty()
    #remember froze store
    gamedata.frozestore.empty()
    pygame.mixer.music.stop()
    pygame.mixer.music.load('sounds/battle.mp3')
    pygame.mixer.music.play(loops=0,start=0)
    for i in gamedata.store:
        if i.froze is True:
            gamedata.frozestore.add(i)
    #variables
    gamedata.actiontime = -1
    gamedata.round = 0
    gamedata.allyfront = 1/2*Width
    gamedata.allyheight = 1/2*Height + 50
    initialize_battlefield(gamedata.stage)
    #draw buttons
    pos = (0.5*Width,Height*0.35)
    button('battlestart',pos)
    #pos = (0.475*Width,Height*0.07)
    #button('hide_store',pos)
    #draw backgrounds
    size = (Width,Height)
    pos = (1/2*Width,int(0.5* Height))
    background('battle_back',size,pos)
    size = (Width,int(Height*0.7))
    pos = (1/2*Width,0.84*Height)
    size = (Width,Width*317/2200)
    background('hand_area_battle',size,pos)
    #size = (Width,int(Height*0.3))
    #pos = (1/2*Width,Height*0.15)
    #background('store_area',size,pos)
    pos = (0.065*Width,0.68*Height)
    button('life',pos)

    
#motions function
def mouse_down(pos):
    global draged,store,hand
    if gamedata.endgame:
        pygame.quit()
        sys.exit()
    for i in buttons:
        if i.rect.collidepoint(pos):
            buttonfunction(i)
    if gamedata.has_choice is True:#if clicked a choice, choose it
        for i in choices:
            if i.rect.collidepoint(pos):
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
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == VIDEORESIZE:
                screen = pygame.display.set_mode((int(screensize[0]*sizerate),
                                                 int(screensize[1]*sizerate)),
                                                 HWSURFACE|DOUBLEBUF|RESIZABLE
                                                 )
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
            
    fake_screen.fill(wallpaper)
    updategame()
    screen.blit(pygame.transform.scale(fake_screen,
                                       screen.get_rect().size),
                                       (0, 0))   
    pygame.display.update()

mainloop()
