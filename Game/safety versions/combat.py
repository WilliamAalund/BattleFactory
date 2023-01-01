# -*- coding: utf-8 -*-
# By submitting this assignment, I agree to the following:
#   "Aggies do not lie, cheat, or steal, or tolerate those who do."
#   "I have not given or received any unauthorized aid on this assignment."
#
# Name:         William Aalund, Josue Quintana, Hannia Balderas, Amanda Thomas
# Section:      528
# Assignment:   13.4
# Date:         18/11/2022

import random as rng
import numpy as np
import math
from Monster_Object import *
#TODO: 
        
moves = {'Tackle':40}
#Damage = ((((2*level / 5 + 2) * power * (A / D)) / 50) + 2) * targets * weather * critical * rng * stab * burn * other
#ideal = ['name', 'level', 'HP', 'HPMax', 'Atk', 'Def', 'SpAtk','SpDef', 'Speed', 'Type1']
#['Squirtle',6,1,13,'None']
plteam = [['Bulbasaur',20,54,54,30,30,37,37,29,'Grass'],['Squirtle',20,53,53,30,37,31,36,28,'Water'],['Charmander',20,51,51,32,28,35,31,37,'Fire'],['Pikachu',20,50,50,33,27,31,31,47,'Electric'],['Grimer',20,68,68,43,31,27,31,31,'Poison'],['Pidgeot',20,69,69,43,41,39,39,51,'Flying']]#FIXME
plcurr = 0
enteam = [['Scolipede',20,60,60,51,46,33,38,56,'Bug'],['Blastoise',20,67,67,44,51,45,53,42,'Water'],['Rhydon',20,78,78,63,59,29,29,27,'Rock'],['Surperior',20,66,66,41,49,41,49,56,'Grass']]
encurr = 0
turnqueue = [[],[],[]]
typedict = {'Normal':0,'Fire':1,'Water':2,'Grass':3,'Electric':4,'Ice':5,'Fighting':6,'Poison':7,'Ground':8,'Flying':9,'Psychic':10,'Bug':11,'Rock':12,'Ghost':13,'Dragon':14,'Dark':15,'Steel':16,'Fairy':17,'None':18}
#Dict points to index of a particular row or column on the type chart.
typechart = np.array([[1,1,1,1,1,1,1,1,1,1,1,1,.5,0,1,1,.5,1], #Normal
                      [1,.5,.5,2,1,2,1,1,1,1,1,2,.5,1,.5,1,2,1], #Fire
                      [1,2,.5,.5,1,1,1,1,2,1,1,1,2,1,.5,1,1,1], #Water
                      [1,.5,2,.5,1,1,1,.5,2,.5,1,.5,2,1,.5,1,.5,1], #Grass
                      [1,1,2,.5,.5,1,1,1,0,2,1,1,1,1,.5,1,1,1], #Electric
                      [1,.5,.5,2,1,.5,1,1,2,2,1,1,1,1,2,1,.5,1], #Ice
                      [2,1,1,1,1,2,1,.5,1,.5,.5,.5,2,0,1,2,2,.5], #Fighting
                      [1,1,1,2,1,1,1,.5,.5,1,1,1,.5,.5,1,1,0,2], #Poison
                      [1,2,1,.5,2,1,1,2,1,0,1,.5,2,1,1,1,2,1], #Ground
                      [1,1,1,2,.5,1,2,1,1,1,1,2,.5,1,1,1,.5,1], #Flying
                      [1,1,1,1,1,1,2,2,1,1,.5,1,1,1,1,0,.5,1,], #Psychic
                      [1,.5,1,2,1,1,.5,.5,1,.5,2,1,1,.5,1,2,.5,.5], #Bug
                      [1,2,1,1,1,2,.5,1,.5,2,1,2,1,1,1,1,.5,1], #Rock
                      [0,1,1,1,1,1,1,1,1,1,2,1,1,2,1,.5,1,1], #Ghost
                      [1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,1,.5,0], #Dragon
                      [1,1,1,1,1,1,.5,1,1,1,2,1,1,2,1,.5,1,.5], #Dark
                      [1,.5,.5,1,.5,2,1,1,1,1,1,1,2,1,1,1,.5,2], #Steel
                      [1,.5,1,1,1,1,2,.5,1,1,1,1,1,1,2,2,.5,1], #Fairy
                      [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]) #None
                      #N,Fi,W,G,E,I,Ft,Po,G,Fl,Ps,B,R,G,Dr,D,S,F
#Rows are attacking type, each column is the defending type
gameresult = 'U'

#--------------- FUNCTIONS --------------
class diff(): #FIXME
    def __init__(self):
        self.diffval = 0

def gamenotfinished():
    #This function would not know how to handle a move like self destruct defeating both pokemon and ending the game.
    'Returns a boolean value. Determines of either the player or the enemy is defeated. Updates the gameresult variable if the game ends. Requires zero parameters.'
    global gameresult
    plfnt = 0
    enfnt = 0
    for i in plteam:
        #print('pl',i,i[0])
q        if i[2] <= 0:
            plfnt += 1
    for i in enteam:
        #print('en',i,i[0])
  q      if i[2] <= 0:
            enfnt += 1
    #print(len(enteam),enfnt,len(plteam),plfnt)
    if enfnt == len(enteam) or plfnt == len(plteam):
        if enfnt == len(enteam):
            gameresult = 'W'
        elif plfnt == len(plteam):
            gameresult = 'L'
        return False
    else:
        return True
       
def attack(foe, atkform='p'):
    'foe will either equal p or e. The input value will determine who is attacked. atkform is either p or s, and will determine if the attack uses attack/defense or special attack/defense stats.'
    try: #In case there is an issue with the pokemon list or other problems, this will rase an error message.
        global turnqueue #Accesses the turnqueue. This is necessary because if a pokemon faints, the turn queue is appended in order to allow another pokemon to be switched in.
        if foe == 'e':
            attacker = plteam[plcurr]
            defender = enteam[encurr]
        elif foe == 'p':
            attacker = enteam[encurr]
            defender = plteam[plcurr]
        if atkform == 'p':
            pspindicator = 4
        elif atkform == 's':
            pspindicator = 6
        print(f'\n{attacker[0]} attacks!',end=' ')
        crit_mult = rng.randint(0,16)
        if crit_mult == 16:
            crit_mult = 1.5
        else:
            crit_mult = 1
        if foe == 'e':
            #Damage = ((((2*attacker[1] / 5 + 2) * 60 * (attacker[4] / defender[5])) / 50) + 2)
q            enteam[encurr][2] -= math.ceil(((((2*attacker[1] / 5 + 2) * crit_mult * difficulty.diffval * (attacker[pspindicator] / defender[pspindicator + 1])) / 50) + 2) * typechart[typedict[attacker[9]]][typedict[defender[9]]]) #FIXME
            #print(math.ceil(((((2*attacker[1] / 5 + 2) * 60 * (attacker[pspindicator] / defender[pspindicator + 1])) / 50) + 2) * typechart[typedict[attacker[9]]][typedict[defender[9]]]))
        elif foe == 'p':
q            plteam[plcurr][2] -= math.ceil(((((2*attacker[1] / 5 + 2) * crit_mult * difficulty.diffval * (attacker[pspindicator] / defender[pspindicator + 1])) / 50) + 2) * typechart[typedict[attacker[9]]][typedict[defender[9]]]) #FIXME
q        print(f'-{math.ceil(((((2*attacker[1] / 5 + 2) * crit_mult * difficulty.diffval * (attacker[pspindicator] / defender[pspindicator + 1])) / 50) + 2) * typechart[typedict[attacker[9]]][typedict[defender[9]]])}',end='') #FIXME
        if typechart[typedict[attacker[9]]][typedict[defender[9]]] < 1 and not typechart[typedict[attacker[9]]][typedict[defender[9]]] == 0:
            print('\nIts not very effective...')
q        elif typechart[typedict[attacker[9]]][typedict[defender[9]]] > 1:
            print('\nIts super effective!')
q        elif typechart[typedict[attacker[9]]][typedict[defender[9]]] == 0:
            print(f"\nIt doesn't effect the opposing {defender[0]}...")
q        if crit_mult == 1.5 and typechart[typedict[attacker[9]]][typedict[defender[9]]] != 0:
            print('\nCritical hit!')
q        if foe == 'e':
            if enteam[encurr][2] <= 0:
                enteam[encurr][2] = 0
                print(f'\n{defender[0]} fainted!')
                turnqueue[2].append(('efs'))
        elif foe == 'p':
q            if plteam[plcurr][2] <= 0:
q                plteam[plcurr][2] = 0
                print(f'\n{defender[0]} fainted!')
                turnqueue[2].append(('pfs'))
                #print(turnqueue)
    #List with lists inside of the list
    #For every element in turn queue
    #If the element[1] == 1:
        #Throw it into the first list
    #Else
    #Throw
    #sortedtq = [[],[],[]]
    except:
        print('Error calculating damage.')

def runturn(): 
    'Performs a turn between the enemy and the player.'
    #enemies should switch to the next pokemon based off of a decision making process.
    #Turn commands should become standardized.
    #Speed ties need to be programmed.
    #There needs to be multiple sorting algorithms for different queues.
    global turnqueue #Enables the broader turn queue to be referenced, the player action is stored there
    global plcurr #global variable for the players party pokemon
    global encurr #global variable for the enemy's party pokemon
    turnqueue[1].append(('em',0,enteam[encurr],0)) #Adds enemy attack to the turn queue. The enemy will only attack
    for priority in turnqueue: #Priority = each list. Higher priorities (greater numbers) are handled first.
        priority.sort(key= lambda command: command[3], reverse=False)
        if turnqueue.index(priority) == 1: #If the attack portion of queue

            priority.sort(key= lambda command: command[2][8], reverse=True) #Sort attacks based on speed
    for priority in turnqueue:
        for command in priority:
            if command[0] == 'pm':
q                if not plteam[plcurr][2] <= 0:
                    attack('e')
            elif command[0] == 'pmp':
q                if not plteam[plcurr][2] <= 0:
                    attack('e', atkform='p')
            elif command[0] == 'pms':
q                if not plteam[plcurr][2] <= 0:
                    attack('e', atkform='s')
            elif command[0] == 'em':
q                if not enteam[encurr][2] <= 0:
                    attack('p')
            if command[0] == 'ps':
q                print(f'\nCome back {plteam[plcurr][0]}!')
                plcurr = command[3]
q                print(f'\n{plteam[plcurr][0]} was sent out!')
            if command == 'pfs':
                if gamenotfinished():
                    printparty(plteam)
                    plcurr = party_select()
q                    print(f'\n{plteam[plcurr][0]} was sent out!')
            if command == 'efs': #Command that signals the enemy needs to switch their pokemon into the match
                if gamenotfinished():
                    #While the current pokemon enteam[encurr][2] <= 0:
                    #encurr = rng.randint(0,len(enteam))
q                    while enteam[encurr][2] <= 0:
                        encurr = rng.randint(0,len(enteam) - 1)
                    #Add 1 to the encurr
                    #encurr += 1
q                    print(f'\nThe enemy sends out {enteam[encurr][0]}!')
    turnqueue = [[],[],[]]

def party_select(backout=False):
    'Function that returns a number that corresponds to a party pokemon. If backout is true, than the menu can be exited.'
    uinp = ''
    if backout == True:
        exittext = ' (enter x to exit the menu)'
    else:
        exittext = ''
    while not uinp.isdigit():
        uinp = input(f'Enter a number from 0-{len(plteam) - 1} that corresponds to the desired Pokemon{exittext}: ')
        if uinp == 'x' and backout == True:
            return 'Exit'
        if uinp == 'x' and backout == False:
            print('You must select a Pokemon.')
        if uinp.isdigit():
            if not (int(uinp) > -1 and int(uinp) <= len(plteam) - 1):
                print('Enter a valid value.')
                uinp = ''  
            if plteam[int(uinp)][2] <= 0:
q                print(f'{plteam[int(uinp)][0]} has no energy left to fight!')
                uinp = ''
            elif plcurr == int(uinp):
q                print(f'{plteam[plcurr][0]} is already on the field.')
                uinp = ''
    return int(uinp)

def printparty(team):
    'Takes as an argument a list of pokemon objects. All objects in the list must be pokemon.'
    print('\n')
    i = 0
    for poke in team:
q        print(f'{i}. {poke[0]} HP: {poke[2]} / {poke[3]}   {poke[9]}')
        i += 1

#--------------- GAME LOOP ---------------

#try:
#    print('Welcome to pokemon')

difficulty = diff() 
difficulty.diffval = input('Welcome to Pokemon! Enter an integer to set the difficulty.\n(0 is easy, 40 is normal, 60 is hard, and 100+ is expert): ') #FIXME
#difficulty = input('Welcome to Pokemon! Enter an integer to set the difficulty.\n(0 is easy, 40 is normal, 60 is hard, and 100+ is expert): ')
while not difficulty.diffval.isdigit(): #FIXME
    difficulty.diffval = input('Welcome to Pokemon! Enter an integer to set the difficulty.\n(0 is easy, 40 is normal, 60 is hard, and 100+ is expert): ') #FIXME
difficulty.diffval = int(difficulty.diffval) #FIXME

while gamenotfinished(): #Core gameloop
q    uinp = input(f'\n{plteam[plcurr][0]} (You): {plteam[plcurr][2]} / {plteam[plcurr][3]} | {enteam[encurr][0]}: {100 * enteam[encurr][2]/enteam[encurr][3]:.1f}% \nWhat will you do? (z fight, s switch, r run, h help): ')
    
    if uinp == 'z':
        while uinp != 'm' and uinp != 'p' and uinp != 'x':
            uinp = input('Select an attack (p physical, m special, x cancel): ')
        if uinp == 'p':
            turnqueue[1].append(('pmp',0,plteam[plcurr],0))
        elif uinp == 'm':
            turnqueue[1].append(('pms',0,plteam[plcurr],0))
        elif uinp == 'x':
            continue
        runturn()
    if uinp == 's':
        printparty(plteam)
        uinp = party_select(backout = True)
        if uinp == 'Exit':
            continue
        else:
            turnqueue[0].append(('ps',10,plteam[plcurr],uinp))
            runturn()
    if uinp == 'r': #Run away
        print('You ran away!')
        break
    if uinp == 'h': #Help menu
        print("\n-----GAME GUIDE-----\nThere are three main actions that you as the player can take.\n\nFight: Your pokemon attacks the opponent. An attack's strength is determined by:\n1. The move's form.\n - Pokemon can attack in two different ways: physically and specially. Physical attacks involve physically attacking the opponent, while special attacks involve using energy, magic, or other non direct means of offense.\n2. The attacking Pokemon's offensive stats.\n - Pokemon have two different offensive stats: attack and special attack. A higher offensive stat will increase the power of an attack of the corresponding form.\n3. The defending Pokmeon's defensive stats.\n - Pokemon also have Defense and Special Defense stats. The higher these stats are, the better a pokemon can take an attack of the respective form.\n4. The type matchup between the attacking and defending Pokemon.\n - Every pokemon has a type. When a pokemon attacks, it attacks with its type. Depending on the opponent's type, this may influence damage calculation. Some types are weak to others (A pokemon weak to an attack will take double damage,) some are resistant (A resistant Pokemon will take half damage,) some are neutral (no change,) and some are immune (No damage from an attack.) The game will notify the player when an attack is Super Effective, Not Very Effective, or Nullfied.\nHigher offensive stats, lower defensive stats, a super effective type matchup, and the correct move form will all increase the damage of an attack. A faster pokemon will attack before a slower pokemon. If a pokemons HP reaches 0, it faints, and cannot continue to battle. If a pokemon faints before using a move, it will not attack.\n")
        print('Switch: Your pokemon is sent back to their pokeball, and another is sent out. The retreating pokemon retains damage that it already has. Switching a pokemon counts as an action for that turn, so the pokemon switching in will not be able to attack. If your pokemon faints on the field, you will be automatically prompted to send out another one, if you still have pokemon able to fight.\n')
        print('Run: Run from the battle. The game ends with a loss.\n')
        print('The game ends when either side defeats all of the other opposing pokemon. Your opponents pokemon are stronger than yours. In order to win, you will need to utilize effective type matchups to deal as much damage as possible. Experiment and learn what Pokemon need to be used when.')

#Prints out the final result of the program.
if gameresult == 'W':
    print('\nThe enemy was defeated!')
    plfnt = 0
    for i in plteam:
        #print('pl',i,i[0])
        if i[2] <= 0:
            plfnt += 1
    print(f'You won with {len(plteam) - plfnt} out of {len(plteam)} Pokemon remaining! (Difficulty: {difficulty.diffval})') #FIXME
elif gameresult == 'L':
    print('\nYou were defeated! You blacked out...')
