import pygame
from pygame.locals import *
import math
import random
global enemyteam
from enemylist import*
from gamedata import*
from gametext import*
from character import*
from store import*
#the copy of characters in battle
def takeorder(unit):
    return unit.order

def initialize_battlefield(stage):#initialize the characters before the battle
    gamedata.summon_trigger = False
    gamedata.deadally.clear
    gamedata.deadenemy.clear
    gamedata.round_number = 0
    gamedata.ally.sprites().sort(key=takeorder)
    for item in ally:
        item.buffs.clear()
        effects = {}
        ieffects = item.effects
        for i in ieffects:
            effects[i] = []
            for j in ieffects[i]:
                effects[i] .append(j)
        data1 =  {'name':item.name,'star':item.star,'order':item.order,'id':item.id}
        data2 =  {'lv':item.lv,'hp':item.hp,'atk':item.atk,'spd':item.spd,'range':item.range,'tar':item.tar,
                'effects':effects}
        data = [data1,data2]
        gamedata.characterstorage.append(data)
        
    initialize_enemy(stage)
    gamedata.enemy.sprites().sort(key=takeorder)
    arrangeally(-1)
    arrangeenemy(-1)
    random.shuffle(gamedata.characters.sprites())
    gamedata.summon_trigger = True

    
def initialize_enemy(gstage):#summon enemy belongs to the data
    enemy.empty()
    enemy_team = [-1,'h']
    enemystage = enemy_team[0]
    while enemystage is not gstage:
        enemy_team = random.choice(random_enemy_team)
        enemystage = enemy_team[0]
    
    enemyamount = len(enemy_team)
    for i in range(enemyamount-1) :
        enemydata = enemy_team[i+1]
        data1 = enemydata[0]
        data2 = enemydata[1]
        name = data1['name']
        order = data1['order']
        star = data1['star']
        summon(name,order,star,data2,1)
    arrangeenemy(-1)

def battle_start_function():#functions at battlestart
    gamedata.battlestart = True
    for i in characters:
        if 'start' in i.effects:#if a character has gamestart effect, cast it
            for j in i.effects['start']:
                function = eval(j)
                function(i)
        if 'special' in i.effects:#some special are triggered when summon
            specials = i.effects['special']
            for special in specials:
                if special == 'gorilla0':
                    i.max_action = 2
                if special == 'gorilla2':
                    i.max_action = 3
    for i in characters:
        i.refresh()

def end_round():#function before a round's ending
    gamedata.round_number += 1
    gamedata.roundstart = False
    for i in characters:
        i.refresh()
    arrangeally(-1)
    arrangeenemy(-1)

def roundfunction(round_number):#runs when a new_round is started, called by main
    global sequence
    end = judge_end(round_number)
    if end is not 'continue':
        pygame.mixer.music.stop()
        gamedata.battlestart = False
        if end is 'fail':
            enemies = gamedata.enemy.sprites()
            gamedata.life -= len(enemies)+gamedata.storelv
            gamedata.life = max(gamedata.life,0)
            #life_tip(len(enemies),gamedata.life)

        if gamedata.life <= 0:
            tip_image('end_lose',(0.5*Width,0.5*Height),120)
            gamedata.endgame = True
            
        elif gamedata.stage >= gamedata.max_stage:
            tip_image('end_win',(0.5*Width,0.5*Height),120)
            gamedata.endgame = True
        else:
            end_buttons(end)
        
        return end
    #rearrange the characters
    arrangeally(-1)
    arrangeenemy(-1)
    update_stats()
    gamedata.roundstart = True
    
def judge_end(round_number):#judge if and how the game is end
    allys = ally.sprites()
    allynum = len(allys)
    allenemy = enemy.sprites()
    enenum = len(allenemy)
    if allynum <= 0 and enenum <= 0:
        return 'draw'
    elif allynum <= 0:
        pygame.mixer.Sound.play(lose_sound)
        return 'fail'       
    elif enenum <= 0:
        pygame.mixer.Sound.play(win_sound)
        return 'win'       
    elif round_number > max_round:
        return 'draw'
    else:
        return 'continue'

def end_buttons(end):
    pos = (1/2*Width,1/4*Height)
    if end == 'win' and gamedata.endgame == False:
        tip_image('end_v',(0.5*Width,0.34*Height),90)
    elif end == 'fail' and gamedata.endgame == False:
        tip_image('end_d',(0.5*Width,0.34*Height),90)
    pos = (0.5*Width,Height*0.35)
    button('tostore',pos)

def update_stats():
    for i in characters:
        i.remained_action = i.max_action#refresh_actions
                
def next_character():#only return survived characters
    for j in range(max_spd+1):
        for i in characters:
            if i.remained_action > 0 and i.spd > max_spd-j:
                i.remained_action -=1
                i.tempstat = [0,0,0,0]
                return i
    return None#if all characters used its action or dead
                
                
def take_action(unit):
    unit.round_action()
        
    
    