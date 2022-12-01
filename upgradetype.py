import math
import random
import gamedata
import characterintro
from gamedata import*
from characterintro import*

teams = ['plain','mountain','forest','water']

charactername = ['chicken','cow','bear','dog','goat','frog','cow', 'crocodile','duck','buffalo','pig',
              'gorilla','parrot','bear','penguin','snake','rabbit','sloth','monkey','giraffe','horse']

triple_upgrades = {
    #lv 0
    'chicken': [{'stats':[3,3,0,0],'sell':['chicken1']},
                {'stats':[3,3,0,0],'sell':['chicken2']}],
    #lv 1
    'hen': [{'stats':[6,3,0,0],'death':['hen1']},
                {'stats':[6,3,0,0],'death':['hen2']}],
    'dog':[{'stats':[7,2,0,1],'passive':['dog1']},
                {'stats':[12,2,0,0],'remove':'passive','hurt':['dog2']}],
    'frog': [{'stats':[4,2,0,0],'start':['frog1']},
                {'stats':[3,4,0,0],'start':['frog2']}],
    'goat': [{'stats':[16,3,0,0],'death':['goat1']},
                {'stats':[4,3,0,0],'death':['goat2']}],
    'sloth': [{'stats':[14,0,0,0],'hurt':['sloth1']},
                {'stats':[6,0,0,3],'remove':'hurt','attack':['sloth2']}],
    'rabbit': [{'stats':[7,3,4,0],'attack':['rabbit1']},
                {'stats':[5,3,0,0],'remove':'attack','end':['rabbit2']}],
    'bee': [{'stats':[7,3,0,0],'end':['bee1']},
                {'stats':[8,3,0,2],'end':['bee2']}],
    'monkey': [{'stats':[6,3,0,0],'sell':['monkey1']},
               {'stats':[6,3,0,0],'sell':['monkey2']}],
    'marmot': [{'stats':[10,3,0,0],'start':['marmot1']},
               {'stats':[5,2,0,2],'start':['marmot2']}],
    #lv 2
    'snake': [{'stats':[8,4,0,0],'death':['snake1']},
               {'stats':[4,4,0,0],'death':['snake2']}],
    'cow': [{'stats':[12,3,0,0],'friend_summon':['cow1']},
               {'stats':[3,3,0,0],'friend_summon':['cow2']}],
    'buffalo': [{'stats':[14,2,0,0],'hurt':['buffalo1']},
                {'stats':[14,2,0,1],'hurt':['buffalo2']}],
    'pig': [{'stats':[16,2,0,0],'remove':'death','attack':['pig1']},
               {'stats':[16,3,0,0],'remove':'death','sell':['pig2']}],
    'owl': [{'stats':[9,4,0,0]},
            {'stats':[0,5,4,0]}],
    'zebra': [{'stats':[8,4,0,2]},
              {'stats':[14,2,0,0],'attack':['zebra1']}],
    'eagle': [{'stats':[9,3,0,0],'passive':['eagle1']},
              {'stats':[9,3,0,0],'passive':['eagle2']}],
    'koala': [{'stats':[5,4,0,0],'hurt':['koala1']},
              {'stats':[8,4,0,1],'hurt':['koala2']}],
    'ostrich':[{'stats':[8,2,0,0],'attack':['ostrich1']},
              {'stats':[21,2,0,0],'attack':['ostrich2']}],
    'snail':[{'stats':[8,3,0,0],'death':['snail1']},
              {'stats':[8,3,0,0],'sell':['snail2']}],
    'sparrow':[{'stats':[7,1,0,0],'end':['sparrow1']},
              {'stats':[10,2,0,0],'end':['sparrow2']}],
    'mole':[{'stats':[7,3,0,0],'death':['mole1']},
              {'stats':[7,3,0,0],'death':['mole2']}],
    'walrus': [{'stats':[12,3,0,0],'end':['walrus1']},
              {'stats':[6,1,0,0],'end':['walrus2']}],
    #lv 3
    'duck': [{'stats':[25,2,0,0],'remove':'attack','hurt':['duck0']},
               {'stats':[5,4,0,2]}],
    'bat': [{'stats':[12,5,0,0],'death':['bat1']},
              {'stats':[6,3,0,0],'death':['bat2']}],
    'penguin': [{'stats':[12,4,4,0],'attack':['penguin1']},
              {'stats':[8,5,0,0],'remove':'attack','start':['penguin2']}],
    'rhino': [{'stats':[18,4,0,0],'hurt':['rhino1']},
              {'stats':[18,4,0,0],'remove':'hurt','death':['rhino2']}],
    'gorilla': [{'stats':[12,2,0,1],'special':['gorilla0'],'attack':['gorilla1']},
              {'stats':[12,0,0,0],'special':['gorilla2']}],
    'crocodile': [{'stats':[14,4,0,0],'friend_death':['crocodile1']},
               {'stats':[10,4,0,0],'friend_death':['crocodile2']}],
    'beaver': [{'stats':[15,3,0,0],'death':['beaver1']},
              {'stats':[5,2,0,3],'remove':'death','friend_death':['beaver2']}],
    'fox': [{'stats':[12,4,0,0],'end':['fox1']},
              {'stats':[16,4,0,1],'end':['fox2']}],
    'parrot': [{'stats':[12,3,0,0],'attack':['parrot1']},
              {'stats':[12,3,0,0],'attack':['parrot2']}],
    'narwhal': [{'stats':[12,2,0,0],'start':['narwhal1']},
              {'stats':[12,2,0,3],'remove':'start','attack':['narwhal2']}],
    'leopard': [{'stats':[13,3,0,0],'attack':['leopard1']},
              {'stats':[13,3,0,0],'attack':['leopard2']}],
    'giraffe': [{'stats':[14,2,0,0],'friend_summon':['giraffe1']},
              {'stats':[8,4,0,0],'friend_summon':['giraffe2']}],
    'alpaca': [{'stats':[18,2,0,0],'hurt':['alpaca1']},
               {'stats':[14,2,0,0],'hurt':['alpaca2']},],   
    'firefly': [{'stats':[15,2,0,0],'attack':['firefly1']},
              {'stats':[10,2,0,0],'attack':['firefly2']}],
    #lv4
    'rat': [{'stats':[12,4,0,0],'death':['rat1']},
            {'stats':[14,4,0,0],'death':['rat2']}],
    'panda': [{'stats':[12,0,0,0],'end':['panda1']},
            {'stats':[0,0,0,0],'end':['panda2']}],
    'horse': [{'stats':[4,5,0,0],'death':['horse1']},
            {'stats':[10,1,0,0],'death':['horse2']}],
    'shark': [{'stats':[24,6,0,0],'end':['shark1']},
            {'stats':[18,5,0,0],'end':['shark2']}],
    'bear': [{'stats':[18,6,0,0],'friend_summon':['bear1']},
              {'stats':[12,4,0,0],'friend_summon':['bear2']}],
    'soldiercrab': [{'stats':[0,6,0,0],'start':['soldiercrab1']},
              {'stats':[15,0,0,0],'start':['soldiercrab2']}],
    'hyena': [{'stats':[20,5,0,0],'friend_death':['hyena1']},
              {'stats':[20,2,0,0],'friend_death':['hyena2']}],
    'vulture': [{'stats':[12,3,0,0],'friend_death':['vulture1']},
              {'stats':[24,3,0,0],'friend_death':['vulture2']}],
    'crow': [{'stats':[15,5,0,0],'death':['crow1']},
              {'stats':[15,5,0,0],'death':['crow2']}],
    'scorpion': [{'stats':[10,3,0,0],'start':['scorpion1']},
              {'stats':[10,3,0,0],'start':['scorpion2']}],
    'turtle': [{'stats':[9,2,0,0],'hurt':['turtle1']},
              {'stats':[4,2,0,0],'hurt':['turtle2']}],
    'beetle': [{'stats':[20,6,0,0],'special':['beetle1']},
              {'stats':[12,3,0,0],'special':['beetle2']}],
    'elephant': [{'stats':[20,2,0,0],'gain_stats':['elephant1']},
              {'stats':[15,2,0,0],'gain_stats':['elephant2']}],
    'badger': [{'stats':[20,4,0,0],'hurt':['badger1']},
              {'stats':[20,0,0,0],'hurt':['badger2']}],
    #lv5
    'moose': [{'stats':[20,6,0,0],'attack':['moose1']},
              {'stats':[25,6,0,3],'attack':['moose0']}],
    'tiger': [{'stats':[20,0,0,0],'attack':['tiger1']},
              {'stats':[26,6,0,0],'attack':['tiger2']}],
    'lion': [{'stats':[20,0,0,0],'friend_death':['lion1']},
              {'stats':[16,4,0,0],'remove':'friend_death','start':['lion2']}],
    'orca': [{'stats':[18,3,0,0],'end':['orca1']},
              {'stats':[0,3,0,0],'end':['orca2']}],
    'anglerfish': [{'stats':[9,3,0,0],'end':['anglerfish1']},
              {'stats':[18,6,0,0],'end':['anglerfish2']}],
    'octopus': [{'stats':[24,8,0,0],'hurt':['octopus1']},
              {'stats':[24,0,0,0],'remove':'hurt','attack':['octopus1']}],
    'spider': [{'stats':[10,2,0,0],'hurt':['spider1']},
              {'stats':[20,4,0,0],'hurt':['spider2']}],
    'fly': [{'stats':[0,0,0,0],'death':['fly1']},
        {'stats':[18,4,0,0],'remove':'death','hurt':['fly2']}],
    'hippo': [{'stats':[32,4,0,0],'attack':['hippo1']},
              {'stats':[36,2,0,0],'attack':['hippo2']}],
    'camel': [{'stats':[10,7,0,1],'gain_stats':['camel1']},
              {'stats':[30,1,0,0],'gain_stats':['camel1']}],
    'pheonix': [{'stats':[36,9,0,0],'attack':['pheonix1']},
              {'stats':[36,3,0,0],'attack':['pheonix2']}],
    }

def get_upgrades(name):
    return triple_upgrades[name]

def upgrade_change(upgrade):
    stats = upgrade['stats']
    line1 = ''#stat
    line2 = ''#changed ability
    line3 = ''#removed ability
    new_ability = None
    remove = None
    #changed ability
    if 'special' in upgrade:
        line2 += ''
        for i in upgrade['special']:
            line2 += intro[i]
            new_ability = ('special',upgrade['special'])
    if 'gain_stats' in upgrade:
        line2 += ''
        for i in upgrade['gain_stats']:
            line2 += intro[i]
            new_ability = ('gain_stats',upgrade['gain_stats'])
    if 'friend_summon' in upgrade:
        line2 += 'friend summon:'
        for i in upgrade['friend_summon']:
            line2 += intro[i]
            new_ability = ('friend_summon',upgrade['friend_summon'])
    if 'friend_death' in upgrade:
        line2 += 'friend death:'
        for i in upgrade['friend_death']:
            line2 += intro[i]
            new_ability = ('friend_death',upgrade['friend_death'])
    if 'sell' in upgrade:
        line2 += 'when sold:'
        for i in upgrade['sell']:
            line2 += intro[i]
            new_ability = ('sell',upgrade['sell'])
    if 'passive' in upgrade:
        line2 += 'passive:'
        for i in upgrade['passive']:
            line2 += intro[i]
            new_ability = ('passive',upgrade['passive'])
    if 'start' in upgrade:
        line2 += 'battlestart:'
        for i in upgrade['start']:
            line2 += intro[i]
            new_ability = ('start',upgrade['start'])
    if 'attack' in upgrade:
        line2 += 'act:'
        for i in upgrade['attack']:
            line2 += intro[i]
            new_ability = ('attack',upgrade['attack'])
    if 'hurt' in upgrade:
        line2 += 'hurt:'
        for i in upgrade['hurt']:
            line2 += intro[i]
            new_ability = ('hurt',upgrade['hurt'])
    if 'death' in upgrade:
        line2 += 'death:'
        for i in upgrade['death']:
            line2 += intro[i]
            new_ability = ('death',upgrade['death'])
    if 'end' in upgrade:
        line2 += 'end of turn:'
        for i in upgrade['end']:
            line2 += intro[i]
            new_ability = ('end',upgrade['end'])

    if 'remove' in upgrade:
        line3 = 'remove ability: '
        removed_ability = upgrade['remove']
        if removed_ability is 'attack':
            line3 += 'act'
        else:
            line3 += removed_ability
        remove = upgrade['remove']
    
    change = (stats,new_ability,remove)
    return (stats,line2,line3,change)