import pygame
from pygame.locals import *
import math
import random
import os

#from. import upgradetype
#from upgradetype import *
#from. import characterintro
from characterintro import *
#basicvars
pygame.init()
endgame = False
Width = 1920
Height = 1050
pi = math.pi
fps = 30
screensize = (Width, Height)
sizerate = 1.0
max_shooter = 6
timer = 0
windowlist = ['start','update','store','battle']
window = 'start'
#store
max_refresh_basic = 10
max_refresh = 10
refresh_time = 0
max_storelv = 5
storelv = 1
store_level_cost = 6
refresh_cost = 1
MAX_MAX_money = 10
MAX_money = 2#the money you can have at most
extra_money = 0#extra_money get for somereason
money = 3
price = 3
storelen = 3
characterlen = 5
handlen = 8
basic_character_prize = 1
has_choice = False#whether their is a triple and need to choose
#battle
max_stage = 14#if you are alive after turn 12, you win.
life = 200#if your life is below 0, you lose.
battlestart = False#whether battle is started
turnstart = False#judge whether turn is started
roundstart = False
actionlist = pygame.sprite.Group()#the character in action, character will wait other character until it take action
animationlist = pygame.sprite.Group()
round_number = 0#restore the turn
stage = 0 # each encounter is a stage
max_round = 20 # max battle turn for each battle
max_spd = 20 #max data for characters
sequence = []#action sequence
add_hand = []#things need to add to hand
attacksequence = [0,10,20,24,27,29,30,30,30,30,30,30,30,30,30,30,28,23,17,9,0]
attack_time = len(attacksequence)
hurtsequence = [350,350,350,350,350,340,320,290,250,200,140]
hurt_time = len(hurtsequence)
projectile_time = 15
#groups
buttons = pygame.sprite.Group()
clicked_buttons = pygame.sprite.Group()
#character
summon_trigger = False #whether to test summon function
draged = pygame.sprite.Group()
icons = pygame.sprite.Group()
digits = pygame.sprite.Group()
speffects = pygame.sprite.Group() 
projs = pygame.sprite.Group()
characters = pygame.sprite.Group()
characterstorage = []#store the characters
frozestore = pygame.sprite.Group()#store the characters
ally = pygame.sprite.Group()
enemy = pygame.sprite.Group()
store = pygame.sprite.Group()
hand = pygame.sprite.Group()
backgrounds = pygame.sprite.Group()
foregrounds = pygame.sprite.Group()
hurtenemy = pygame.sprite.Group()
deadally = []
deadenemy = []
pygame.font.init()
fontpath = 'C:\\Users\\tonyb\\Desktop\\codes\\py_files\\games\\beeware-tutorial\\cubeanimals\\src\\cubeanimals\\tahoma.ttf'
#fontpath = 'tahoma.ttf'
f = pygame.font.Font(fontpath,32)
f2 = pygame.font.Font(fontpath,40)
f3 = pygame.font.Font(fontpath,48)
f4 = pygame.font.Font(fontpath,60)#
f5 = pygame.font.Font(fontpath,150)#money

'''
charactername = ['hen','rat','dog','goat','frog','sloth','monkey','rabbit',
                 'crocodile','cow','duck','buffalo','pig','snake','owl','zebra',
                 'gorilla','parrot','penguin','horse',
                 'rat',
                 ]
'''

lv1 = []
lv2 = []
lv3 = []
lv4 = []
lv5 = []

win_sound= pygame.mixer.Sound("C:\\Users\\tonyb\\Desktop\\codes\\py_files\\games\\beeware-tutorial\\cubeanimals\\src\\cubeanimals\\sounds\effect\_win.wav")
lose_sound = pygame.mixer.Sound("C:\\Users\\tonyb\\Desktop\\codes\\py_files\\games\\beeware-tutorial\\cubeanimals\\src\\cubeanimals\\sounds\effect\_lose.wav")
hit_sound = pygame.mixer.Sound("C:\\Users\\tonyb\\Desktop\\codes\\py_files\\games\\beeware-tutorial\\cubeanimals\\src\\cubeanimals\\sounds\effect\_hit.wav")
button_sound = pygame.mixer.Sound("C:\\Users\\tonyb\\Desktop\\codes\\py_files\\games\\beeware-tutorial\\cubeanimals\\src\\cubeanimals\\sounds\effect\_button.wav")
gainstats_sound = pygame.mixer.Sound("C:\\Users\\tonyb\\Desktop\\codes\\py_files\\games\\beeware-tutorial\\cubeanimals\\src\\cubeanimals\\sounds\effect\_gainstats.wav")
refresh_sound = pygame.mixer.Sound("C:\\Users\\tonyb\\Desktop\\codes\\py_files\\games\\beeware-tutorial\\cubeanimals\\src\\cubeanimals\\sounds\effect\_refresh.ogg")

characterdata = {
    #special
    'chameleon':  {'lv':0,'hp':9,'atk':1,'spd':6,'range':6,'tar':'rand','effects':{'start':['chameleon0']}},
    #summonings
    'chicken':  {'lv':0,'hp':3,'atk':3,'spd':6,'range':6,'tar':'rand','effects':{}},
    'duckling':  {'lv':0,'hp':5,'atk':4,'spd':6,'range':1,'tar':'rand','effects':{}},
    'shadowsnake':  {'lv':0,'hp':9,'atk':9,'spd':8,'range':3,'tar':'rand','effects':{}},
    'bigmouse':{'lv':0,'hp':6,'atk':6,'spd':6,'range':4,'tar':'rand','effects':{}},
    'timber':{'lv':0,'hp':20,'atk':0,'spd':1,'range':1,'tar':'rand','effects':{}},
    'bigtimber':{'lv':0,'hp':40,'atk':0,'spd':1,'range':1,'tar':'rand','effects':{}},
    
    #lv1(9)
    'hen':    {'lv':1,'hp':6,'atk':3,'spd':4,'range':3,'tar':'rand','effects':{'death':['hen0']},},
    'dog':    {'lv':1,'hp':9,'atk':2,'spd':7,'range':4,'tar':'rand','effects':{'passive':['dog0']}},
    'goat':   {'lv':1,'hp':12,'atk':2,'spd':8,'range':1,'tar':'rand','effects':{'death':['goat0']}},
    'frog':   {'lv':1,'hp':6,'atk':3,'spd':7,'range':7,'tar':'rand','effects':{'start':['frog0']}},
    'rabbit': {'lv':1,'hp':8,'atk':3,'spd':10,'range':6,'tar':'rand','effects':{'attack':['rabbit0']}},
    'sloth':  {'lv':1,'hp':15,'atk':1,'spd':1,'range':2,'tar':'rand','effects':{'hurt':['sloth0']}},
    'monkey':  {'lv':1,'hp':7,'atk':3,'spd':6,'range':6,'tar':'rand','effects':{'sell':['monkey0']}},
    'bee':  {'lv':1,'hp':8,'atk':3,'spd':7,'range':4,'tar':'rand','effects':{'end':['bee0']}},
    'marmot': {'lv':1,'hp':12,'atk':1,'spd':5,'range':3,'tar':'rand','effects':{'start':['marmot0']}},
    
    #lv2(12)
    'snake':  {'lv':2,'hp':9,'atk':4,'spd':8,'range':8,'tar':'rand','effects':{'death':['snake0']}},
    'cow':    {'lv':2,'hp':13,'atk':3,'spd':3,'range':2,'tar':'rand','effects':{'friend_summon':['cow0']}},
    'buffalo':{'lv':2,'hp':17,'atk':2,'spd':6,'range':1,'tar':'rand','effects':{'hurt':['buffalo0']}},
    'zebra':  {'lv':2,'hp':15,'atk':5,'spd':7,'range':3,'tar':'rand','effects':{'attack':['zebra0']}},
    'pig':    {'lv':2,'hp':16,'atk':3,'spd':3,'range':2,'tar':'rand','effects':{'death':['pig0']}},
    'owl':    {'lv':2,'hp':9,'atk':5,'spd':6,'range':9,'tar':'far','effects':{'special':['owl0']}},
    'snail':{'lv':2,'hp':12,'atk':3,'spd':1,'range':2,'tar':'rand','effects':{'death':['snail0']}},
    'eagle':  {'lv':2,'hp':11,'atk':4,'spd':8,'range':7,'tar':'rand','effects':{'passive':['eagle0']}},
    'koala':  {'lv':2,'hp':9,'atk':5,'spd':2,'range':3,'tar':'rand','effects':{'hurt':['koala0']}},
    'ostrich': {'lv':2,'hp':10,'atk':2,'spd':8,'range':5,'tar':'rand','effects':{'attack':['ostrich0']}},
    'sparrow': {'lv':2,'hp':10,'atk':1,'spd':6,'range':6,'tar':'rand','effects':{'end':['sparrow0']}},
    'mole': {'lv':2,'hp':8,'atk':4,'spd':3,'range':4,'tar':'rand','effects':{'death':['mole0']}},
    'walrus':{'lv':2,'hp':15,'atk':3,'spd':2,'range':4,'tar':'rand','effects':{'end':['walrus0']}},
    
    #lv3(14)
    'duck':   {'lv':3,'hp':15,'atk':4,'spd':5,'range':1,'tar':'rand','effects':{'attack':['duck0']}},
    'bat':{'lv':3,'hp':13,'atk':6,'spd':7,'range':4,'tar':'rand','effects':{'death':['bat0']}},
    'penguin':{'lv':3,'hp':13,'atk':5,'spd':4,'range':8,'tar':'rand','effects':{'attack':['penguin0']}},
    'rhino':  {'lv':3,'hp':20,'atk':6,'spd':5,'range':1,'tar':'rand','effects':{'hurt':['rhino0']}},
    'gorilla':{'lv':3,'hp':16,'atk':3,'spd':6,'range':2,'tar':'rand','effects':{'special':['gorilla0']}},
    'parrot': {'lv':3,'hp':14,'atk':4,'spd':8,'range':7,'tar':'rand','effects':{'attack':['parrot0']}},
    'crocodile':{'lv':3,'hp':15,'atk':4,'spd':4,'range':5,'tar':'rand','effects':{'friend_death':['crocodile0']}},
    'fox':  {'lv':3,'hp':15,'atk':5,'spd':7,'range':4,'tar':'rand','effects':{'end':['fox0']}},
    'beaver':  {'lv':3,'hp':20,'atk':5,'spd':3,'range':2,'tar':'rand','effects':{'death':['beaver0']}},
    'narwhal':   {'lv':3,'hp':16,'atk':3,'spd':4,'range':3,'tar':'rand','effects':{'start':['narwhal0']}},
    'giraffe':{'lv':3,'hp':18,'atk':2,'spd':6,'range':5,'tar':'rand','effects':{'friend_summon':['giraffe0']}},
    'leopard':{'lv':3,'hp':14,'atk':3,'spd':10,'range':6,'tar':'rand','effects':{'attack':['leopard0']}},
    'firefly':{'lv':3,'hp':16,'atk':2,'spd':2,'range':9,'tar':'rand','effects':{'attack':['firefly0']}},
    'alpaca':{'lv':3,'hp':21,'atk':4,'spd':4,'range':4,'tar':'rand','effects':{'hurt':['alpaca0']}},
    
    #lv4(14)
    'rat':   {'lv':4,'hp':14,'atk':5,'spd':7,'range':4,'tar':'rand','effects':{'death':['rat0']}},
    'panda':   {'lv':4,'hp':12,'atk':3,'spd':4,'range':7,'tar':'rand','effects':{'end':['panda0']}},
    'horse':  {'lv':4,'hp':16,'atk':6,'spd':9,'range':4,'tar':'rand','effects':{'death':['horse0']}},
    'shark':  {'lv':4,'hp':29,'atk':6,'spd':5,'range':1,'tar':'rand','effects':{'end':['shark0']}},
    'hyena':  {'lv':4,'hp':25,'atk':7,'spd':6,'range':4,'tar':'rand','effects':{'friend_death':['hyena0']}},
    'vulture':  {'lv':4,'hp':18,'atk':6,'spd':6,'range':8,'tar':'rand','effects':{'friend_death':['vulture0']}},
    'crow':   {'lv':4,'hp':17,'atk':6,'spd':7,'range':4,'tar':'rand','effects':{'death':['crow0']}},
    'beetle':  {'lv':4,'hp':20,'atk':6,'spd':4,'range':3,'tar':'rand','effects':{'special':['beetle0']}},
    'soldiercrab':{'lv':4,'hp':1,'atk':8,'spd':2,'range':3,'tar':'rand','effects':{'start':['soldiercrab0']}},
    'scorpion':{'lv':4,'hp':13,'atk':1,'spd':3,'range':4,'tar':'rand','effects':{'start':['scorpion0']}},
    'elephant': {'lv':4,'hp':30,'atk':3,'spd':3,'range':5,'tar':'rand','effects':{'gain_stats':['elephant0']}},
    'turtle': {'lv':4,'hp':14,'atk':4,'spd':1,'range':1,'tar':'rand','effects':{'hurt':['turtle0']}},
    'badger': {'lv':4,'hp':24,'atk':4,'spd':6,'range':4,'tar':'rand','effects':{'hurt':['badger0']}},
    'bear':{'lv':4,'hp':20,'atk':6,'spd':4,'range':5,'tar':'rand','effects':{'friend_summon':['bear0']}},
    
    #lv5(11)
    'moose':{'lv':5,'hp':28,'atk':6,'spd':6,'range':3,'tar':'rand','effects':{'attack':['moose0']}},
    'tiger':{'lv':5,'hp':22,'atk':5,'spd':8,'range':2,'tar':'rand','effects':{'attack':['tiger0']}},
    'lion':{'lv':5,'hp':25,'atk':5,'spd':6,'range':6,'tar':'rand','effects':{'friend_death':['lion0']}},
    'orca':{'lv':5,'hp':32,'atk':5,'spd':4,'range':2,'tar':'rand','effects':{'end':['orca0']}},
    'anglerfish':{'lv':5,'hp':20,'atk':7,'spd':4,'range':8,'tar':'rand','effects':{'end':['anglerfish0']}},
    #'octopus':{'lv':5,'hp':32,'atk':8,'spd':8,'range':8,'tar':'rand','effects':{'hurt':['octopus0']}},
    'spider':{'lv':5,'hp':20,'atk':4,'spd':4,'range':8,'tar':'rand','effects':{'hurt':['spider0']}},
    'camel':{'lv':5,'hp':34,'atk':6,'spd':4,'range':5,'tar':'rand','effects':{'gain_stats':['camel0']}},
    'fly':{'lv':5,'hp':12,'atk':4,'spd':6,'range':4,'tar':'rand','effects':{'death':['fly0']}},
    'pheonix':{'lv':5,'hp':36,'atk':9,'spd':7,'range':7,'tar':'rand','effects':{'attack':['pheonix0']}},
    'hippo':{'lv':5,'hp':32,'atk':4,'spd':2,'range':4,'tar':'rand','effects':{'hurt':['hippo0']}},
    }

effectdata = {
    'strengthen':16,
    'weaken':23,
    'cure':18,
    'block':18,
    'damage':17,
    'death':28,
    }


def generate_lv_item(lv):
    box = 'lv'
    box += str(lv)
    box = eval(box)
    name = random.choice(box)
    return name

def generate_store_item(lv):#chose from database until find a unit with acceptable lv 
    i = random.randint(1,lv)
    box = 'lv'
    box += str(i)
    box = eval(box)
    name = random.choice(box)
    return name

def get_intro(effect):#get the introductions of effects
    texts = ''
    if effect[0] is 'passive':
        texts += 'passive:'
    elif effect[0] is 'start':
        texts += 'battlestart:'
    elif effect[0] is 'attack':
        texts += 'act:'
    elif effect[0] is 'hurt':
        texts += 'hurt:'
    elif effect[0] is 'death':
        texts += 'death:'
    elif effect[0] is 'end':
        texts += 'end of turn:'
    elif effect[0] is 'sell':
        texts += 'when sold:'
    elif effect[0] is 'friend_summon':
        texts += 'friend summon:'
    elif effect[0] is 'friend_death':
        texts += 'friend death:'
    #other effect do not have introduction
    for i in effect[1]:
        texts += ' '
        texts += intro[i]
    return texts

def character_data(name):
    data = characterdata[name]
    return data

#get position:
def storeposition(order):
    x=190*order+310
    y=200
    pos =(x,y)
    return pos

def handposition(order):
    x= 185*order -5
    y= Height - 130
    pos =(x,y)
    return pos

def allyposition(order):
    x= Width/2-180*order-150
    y= Height/2+160
    pos =(x,y)
    return pos

def enemyposition(order):
    x= Width/2+180*order+150
    y= Height/2+160
    pos =(x,y)
    return pos

def order_interval(x):
    global characterlen
    for i in range(characterlen):
        place =  allyposition(i)
        nextplace =  allyposition(i+1)
        if place[0]-x  < x-nextplace[0] or i == characterlen-1:
            return i
    return characterlen-1
        
class background(pygame.sprite.Sprite):
    def __init__(self,name,size,pos):
        pygame.sprite.Sprite.__init__(self)
        self.name =name
        self.pos =pos
        self.imagename = "images/bkg/"+self.name+".png"
        self.image = pygame.image.load(self.imagename).convert_alpha()
        self.image = pygame.transform.scale(self.image,size)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        backgrounds.add(self)

class foreground(background):#background but in higher layer
    def __init__(self,name,size,pos):
        background.__init__(self,name,size,pos)
        foregrounds.add(self)

class button(pygame.sprite.Sprite):
    def __init__(self,name,pos):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.pos = pos
        self.imagename = "images/button/"+self.name+".png"
        self.image = pygame.image.load(self.imagename).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.clock = 0
        buttons.add(self)
        
    def click(self):
        self.imagename = "images/whitebutton/"+self.name+".png"
        self.image = pygame.image.load(self.imagename).convert_alpha()
        self.clock = 4
        clicked_buttons.add(self)
        
    def refresh(self):
        self.clock -=1
        if self.clock <=0:
            self.imagename = "images/button/"+self.name+".png"
            self.image = pygame.image.load(self.imagename).convert_alpha()
            clicked_buttons.remove(self)
            
    def remove(self):
        pass