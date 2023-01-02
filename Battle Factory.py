#----------PRESS PLAY AND ENJOY THE GAME----------

import random as rng
import numpy as np
import math
import character_Object as co
#--------------- FUNCTIONS --------------
class diff(): #FIXME: This isnt necessary at all
    def __init__(self):
        self.diffval = ''

def gamenotfinished():
    #This function would not know how to handle a move like self destruct defeating both pokemon and ending the game.
    'Returns a boolean value. Determines of either the player or the enemy is defeated. Updates the gameresult variable if the game ends. Requires zero parameters.'
    global gameresult
    plfnt = 0
    enfnt = 0
    for i in plteam:
        #print('pl',i,i[0])
        if i.real_HP <= 0:
            plfnt += 1
    for i in enteam:
        #print('en',i,i[0])
        if i.real_HP <= 0:
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
   
def damage_calc(attacker, defender='unknown', atkform='p', atktype=1, random=0):
    #This is where the damage calculation function will go. 
    if atkform == 'p':
        used_Attack = attacker.attack
    elif atkform == 's':
        used_Attack = attacker.sp_Attack
    if random == 0:
        crit_mult = 1
    if defender == 'unknown':
        used_Defense = 100
        return math.ceil(((((2*attacker.level / 5 + 2) * crit_mult * base_power * (used_Attack / used_Defense)) / 50) + 2))
    elif defender != 'unknown':
        #print(co.basestat(defender))
        if atkform == 'p':
            used_Defense = defender.defense
        elif atkform == 's':
            used_Defense = defender.sp_Defense
        if atktype == 1:
            return math.ceil(((((2*attacker.level / 5 + 2) * crit_mult * base_power * (used_Attack / used_Defense)) / 50) + 2)) * typechart[typedict[attacker.type]][typedict[defender.type]] * typechart[typedict[attacker.type]][typedict[defender.type_2]]
        if atktype == 2:
            return math.ceil(((((2*attacker.level / 5 + 2) * crit_mult * base_power * (used_Attack / used_Defense)) / 50) + 2)) * typechart[typedict[attacker.type_2]][typedict[defender.type]] * typechart[typedict[attacker.type_2]][typedict[defender.type_2]]
    #typechart[typedict[attacker.type]][typedict[defender.type]] * typechart[typedict[attacker.type]][typedict[defender.type_2]]
F_Count = 0
def attack(foe, atkform='p', atktype=1):
    'foe will either equal p or e. The input value will determine who is attacked. atkform is either p or s, and will determine if the attack uses attack/defense or special attack/defense stats. atktype determines the type that the pokemon will attack with.'
    global turnqueue #Accesses the turnqueue. This is necessary because if a pokemon faints, the turn queue is appended in order to allow another pokemon to be switched in.
    if foe == 'e':
        attacker = plteam[plcurr]
        defender = enteam[encurr]
    elif foe == 'p':
        attacker = enteam[encurr]
        defender = plteam[plcurr]
    if atkform == 'p':
        used_Attack = attacker.attack
        used_Defense = defender.defense
    elif atkform == 's':
        used_Attack = attacker.sp_Attack
        used_Defense = defender.sp_Defense
    print(f'\n{co.basestat(attacker)} attacks',end=' ')
    crit_mult = rng.randint(0,16)
    if crit_mult == 16:
        crit_mult = 1.5
    else:
        crit_mult = 1
    if atktype == 1:
        attacking_type = attacker.type
    elif atktype == 2:
        attacking_type = attacker.type_2
    print(f'using the {attacking_type} type!',end=' ')
    damage_Dealt = math.ceil(((((2*attacker.level / 5 + 2) * crit_mult * base_power * (used_Attack / used_Defense)) / 50) + 2) * typechart[typedict[attacking_type]][typedict[defender.type]] * typechart[typedict[attacking_type]][typedict[defender.type_2]])
    if foe == 'e':
        enteam[encurr].real_HP -= damage_Dealt
    elif foe == 'p':
        plteam[plcurr].real_HP -= damage_Dealt
        #plteam[plcurr].real_HP -= 0 #Hacks for playtesting
    if not(typechart[typedict[attacking_type]][typedict[defender.type]] * typechart[typedict[attacking_type]][typedict[defender.type_2]] == 0):    
        if foe == 'e':
            print(f'  (-{100 * damage_Dealt / defender.HP:.1f}%)')
        elif foe == 'p':
            print(f'  (\033[1;31m-{100 * damage_Dealt / defender.HP:.1f}%\033[1;37m)')
    if typechart[typedict[attacking_type]][typedict[defender.type]] *  typechart[typedict[attacking_type]][typedict[defender.type_2]] < 1 and not typechart[typedict[attacker.type]][typedict[defender.type]] *  typechart[typedict[attacker.type]][typedict[defender.type_2]] == 0:
        if foe == 'e':
            print('\033[1;31mIts not very effective...\033[1;37m',)
        if foe == 'p':
            print('\033[1;32mIts not very effective...\033[1;37m',)
    elif typechart[typedict[attacking_type]][typedict[defender.type]] * typechart[typedict[attacking_type]][typedict[defender.type_2]] > 1:
        if foe == 'e':
            print('\033[1;32mIts super effective!\033[1;37m')
        elif foe == 'p':
            print('\033[1;31mIts super effective!\033[1;37m')
    elif typechart[typedict[attacking_type]][typedict[defender.type]] * typechart[typedict[attacking_type]][typedict[defender.type_2]] == 0:
        print(f"\nIt doesn't effect the opposing {co.basestat(defender)}...")
    if crit_mult == 1.5 and typechart[typedict[attacking_type]][typedict[defender.type]] * typechart[typedict[attacking_type]][typedict[defender.type_2]] != 0:
        print('\n\033[1;33mCritical hit!\033[1;37m')
    if foe == 'e':
        if enteam[encurr].real_HP <= 0:
            enteam[encurr].real_HP = 0
            print(f'\n\033[1;32m{co.basestat(defender)} fainted!\033[1;37m')
            turnqueue[2].append(('efs'))
    elif foe == 'p':
        if plteam[plcurr].real_HP <= 0:
            plteam[plcurr].real_HP = 0
            print(f'\n\033[1;31m{co.basestat(defender)} fainted!\033[1;37m')
            global F_Count
            F_Count += 1
            turnqueue[2].append(('pfs'))

def help_Menu():
    'Displays a help menu for the game.'
    global uinp
    uinp = ''
    while uinp != '1' and uinp != '2' and uinp != '3' and uinp != '4' and uinp != 'x':
        uinp = input('\nWhat would you like help with? (1: General Rules, 2: Pokemon, 3: In Battle, 4: Out of Battle, x: Exit): ')
        if uinp == '1':
            print('\n\033[1;33m----------GENERAL RULES----------\033[1;37m')
            print('In order to win the game, you will need to succeed in 16 rounds of Pokemon battling.\nYou will fight more difficult pokemon as you continue.\nYou will need to utilize prediction, planning, and various battle mechanics to win.\n')
            uinp = ''
        elif uinp == '2':
            print('\n\033[1;33m----------POKEMON----------\033[1;37m')
            print("\033[1;33mPokemon\033[1;37m are creatures that can fight in battle. Pokemon fight by using moves to inflict damage. As long as a Pokemon's \033[1;33mHP\033[1;37m is above 0, it can attack the opponent. When a Pokemon's HP reaches 0, it faints, and cannot continue battling.\n\nEach Pokemon posesses a different \033[1;33mtype\033[1;37m and stats. (You can view a Pokemon's typing, stats, and more in the summary menu.)\n\nA Pokemon's \033[1;33mtype\033[1;37m determines what kind of moves it can use to attack the opponent, as well as how much damage it will recieve from enemy attacks.\nFor example, a fire and fighting type Pokemon can only attack using the fire and fighting type, and would also recieve twice as much damage from an incoming water type move.\nA \033[1;33mmove\033[1;37m is an action that a Pokemon takes to deal damage. A move's damage is determined by the attacking Pokemon's offensive stats, the defending Pokemon's defensive stats, and the type and \033[1;33mform\033[1;37m of the move being used. A move's form can either be physical or special, and determines what offensive stat is drawn on for damage.\n\nAside from typing, Pokemon have six relevant stats used during battle:\n\n\033[1;33mHP\033[1;37m: Hit Points. The more HP a Pokemon has, the more damage it can recieve.\n\033[1;33mAttack\033[1;37m: The more attack a Pokemon has, the more damage it will do using physical moves.\n\033[1;33mDefense\033[1;37m: The more defense a Pokemon has, the more it will reduce incoming physical damage.\n\033[1;33mSp.Attack\033[1;37m: Special attack. The more special attack a Pokemon has, the more damage it will do using special moves.\n\033[1;33mSp.Defense\033[1;37m: Special defense. The more special defense a Pokemon has, the more it will reduce incoming special damage.\n\033[1;33mSpeed\033[1;37m: This stat determines what Pokemon moves first during a turn. The Pokemon with the higher speed stat will move first.\n\nPokemon have various other stats as well:\n\n\033[1;33mCP\033[1;37m: Combat Points. CP is an overall measure of a Pokemon's strength. Generally, Pokemon with a higher CP have better stats.\n\033[1;33mExp\033[1;37m: Experience points. Experience points are earned by pokemon that can evolve after winning a battle. Evolving is the process of turning into a more powerful Pokemon. Once a pokemon gains enough experience points, it will evolve on its own. You can check if a pokemon can evolve, as well as how much experience it has, in the summary screen.\n\033[1;33mNature\033[1;37m: A Pokemon's nature is random and can influence its stats. A nature will either raise one stat and lower another, or it will not do anything at all. You can see if a stat has been raised (+) or lowered (-) due to nature in the stat summary for a given Pokemon.\n\033[1;33mLevel\033[1;37m: Every pokemon is level 50 in this game, so level has no effect on gameplay. The higher the level, the stronger a pokemon gets.\n\n\033[1;33m(SCROLL UP ^)\033[1;37m")
            uinp = ''
        elif uinp == '3':
            print('\n\033[1;33m----------IN BATTLE----------\033[1;37m')
            print("There are three main actions that you as the player can take during a battle.\n\n\033[1;33mFight\033[1;37m: Your pokemon attacks the opponent. An attack's strength is determined by:\n1. The move's form.\n2. The attacking Pokemon's offensive stats.\n3. The defending Pokemon's defensive stats.\n4. The type matchup between the attacking and defending Pokemon.\nYou can read more about how damage works in the Pokemon section.\nWhen a Pokemon attacks, there is a 1 in 16 chance that the Pokemon will land a \033[1;33mcritical hit\033[1;37m. A critical hit increases the power of a move significantly.\nIf a Pokemon faints before using a move, it will not attack.\n\n\033[1;33mParty/Switch\033[1;37m: The party option is where you can view your Pokemon and their stats, as well as switch them into battle.\nyou can select a Pokemon by entering in the corresponding number next to its name.\nFrom there, you can use the summary command to view a Pokemon's stats (Stats are explained more thoroughly in the Pokemon section,) as well as the switch command to switch a Pokemon into battle.\n\n\033[1;33mSwitching\033[1;37m a Pokemon into battle counts as your action for a given turn, which means the Pokemon switching in \033[1;33mwill not be able to attack\033[1;37m as it switches in.\nA fainted Pokemon cannot switch into battle.\n\n\033[1;33mRun\033[1;37m: Run from the battle. The game ends with a loss.\n\n\033[1;33m(SCROLL UP ^)\033[1;37m")
            uinp = ''
            #\n - Pokemon can attack in two different ways: physically and specially. Physical Attacks involve physically attacking the opponent, while Special Attacks involve using energy, magic, or other non direct means of offense.
        elif uinp == '4':
            print('\n\033[1;33m----------OUT OF BATTLE----------\033[1;37m')
            print('At the beginning of the game, you will be given a selection of six Pokemon to choose from. You may take three of them to use in battle. Choose wisely!\n\nAfter you win a battle, your Pokemon will be healed and gain exp if they can evolve.\nPokemon are healed 75% after a regular battle, and are fully healed after a boss battle. If a Pokemon is already at max HP, they will not be healed.\nExp is discussed in the Pokemon section.\n\nAfter each battle, you will be given the opportunity to trade a Pokemon for one of the opponents Pokemon. The Pokemon you select for trade will leave your party, and a Pokemon selected from the opponents team will replace it. This Pokemon will be an identical copy from the opponents team.')
            uinp = ''
        if uinp == 'x':
            continue
    
    #Old help guide
    #print("\n-----GAME GUIDE-----\nThere are three main actions that you as the player can take.\n\nFight: Your pokemon attacks the opponent. An attack's strength is determined by:\n1. The move's form.\n - Pokemon can attack in two different ways: physically and specially. Physical attacks involve physically attacking the opponent, while special attacks involve using energy, magic, or other non direct means of offense.\n2. The attacking Pokemon's offensive stats.\n - Pokemon have two different offensive stats: attack and special attack. A higher offensive stat will increase the power of an attack of the corresponding form.\n3. The defending Pokmeon's defensive stats.\n - Pokemon also have Defense and Special Defense stats. The higher these stats are, the better a pokemon can take an attack of the respective form.\n4. The type matchup between the attacking and defending Pokemon.\n - Every pokemon has a type. When a pokemon attacks, it attacks with its type. Depending on the opponent's type, this may influence damage calculation. Some types are weak to others (A pokemon weak to an attack will take double damage,) some are resistant (A resistant Pokemon will take half damage,) some are neutral (no change,) and some are immune (No damage from an attack.) The game will notify the player when an attack is Super Effective, Not Very Effective, or Nullfied.\nHigher offensive stats, lower defensive stats, a super effective type matchup, and the correct move form will all increase the damage of an attack. A faster pokemon will attack before a slower pokemon. If a pokemons HP reaches 0, it faints, and cannot continue to battle. If a pokemon faints before using a move, it will not attack.\n")
    #print("Party: The party screen is where you can access a summary of each of your party pokemon's stats, and where you can switch out your pokemon. When you switch a pokemon, your pokemon is sent back to their pokeball, and another is sent out. The retreating pokemon retains damage that it already has. Switching a pokemon counts as an action for that turn, so the pokemon switching in will not be able to attack. If your pokemon faints on the field, you will be automatically prompted to send out another one, if you still have pokemon able to fight. Next, you can also use the switch menu to check the stats of your pokemon by selecting a pokemon and using the summary key. This screen will provide various stats about your Pokemon, including it's name, type, HP, offenses, defenses, speed, and more.\n")
    #print('Run: Run from the battle. The game ends with a loss.\n')
    #print('The game ends when either side defeats all of the other opposing pokemon. Your opponents pokemon are stronger than yours. In order to win, you will need to utilize effective type matchups to deal as much damage as possible. Experiment and learn what Pokemon need to be used when.')

def runturn():
    'Performs a turn between the enemy and the player.'
    #enemies should switch to the next pokemon based off of a decision making process.
    #Turn commands should become standardized.
    #Speed ties need to be programmed.
    #There needs to be multiple sorting algorithms for different queues.
    global turnqueue #Enables the broader turn queue to be referenced, the player action is stored there
    global plcurr #global variable for the player's party pokemon
    global encurr #global variable for the enemy's party pokemon
    if enteam[encurr].type_2 == 'None': #One type AI
        if damage_calc(enteam[encurr], defender=plteam[plcurr], atkform='p') >= damage_calc(enteam[encurr], defender=plteam[plcurr], atkform='s'):
            turnqueue[1].append(('emp',0,enteam[encurr],0))
        elif damage_calc(enteam[encurr], defender=plteam[plcurr], atkform='p') < damage_calc(enteam[encurr], defender=plteam[plcurr], atkform='s'):   
            turnqueue[1].append(('ems',0,enteam[encurr],0))
    elif enteam[encurr].type_2 != 'None':
        move1 = damage_calc(enteam[encurr], defender=plteam[plcurr], atkform='p')
        move2 = damage_calc(enteam[encurr], defender=plteam[plcurr], atkform='p', atktype=2)
        move3 = damage_calc(enteam[encurr], defender=plteam[plcurr], atkform='s', atktype=1)
        move4 = damage_calc(enteam[encurr], defender=plteam[plcurr], atkform='s', atktype=2)
        movelist = [move1,move2,move3,move4]
        movelist.sort(reverse=True)
        if move1 == movelist[0]:   
            turnqueue[1].append(('emp',0,enteam[encurr],0)) #Adds enemy attack to the turn queue. The enemy will only attack
        elif move2 == movelist[0]:
            turnqueue[1].append(('emp2',0,enteam[encurr],0))
        elif move3 == movelist[0]:
            turnqueue[1].append(('ems',0,enteam[encurr],0))
        elif move4 == movelist[0]:
            turnqueue[1].append(('ems2',0,enteam[encurr],0))
        else:
            turnqueue[1].append(('emp',0,enteam[encurr],0))
    for priority in turnqueue: #Priority = each list. Higher priorities (greater numbers) are handled first.
        priority.sort(key= lambda command: command[3], reverse=False)
        if turnqueue.index(priority) == 1: #If the attack portion of queue

            priority.sort(key= lambda command: command[2].speed, reverse=True) #Sort attacks based on speed
    for priority in turnqueue:
        for command in priority:
            if command[0] == 'pm': #Archaic command
                if not plteam[plcurr].real_HP <= 0:
                    attack('e')
            elif command[0] == 'pmp': #Player move physical
                if not plteam[plcurr].real_HP <= 0:
                    attack('e', atkform='p')
            elif command[0] == 'pmp2': #Player move physical using second type
                if not plteam[plcurr].real_HP <= 0:
                    attack('e', atkform='p',atktype=2)
            elif command[0] == 'pms': #Player move special
                if not plteam[plcurr].real_HP <= 0:
                    attack('e', atkform='s')
            elif command[0] == 'pms2': #Player move special using second type
                if not plteam[plcurr].real_HP <= 0:
                    attack('e', atkform='s',atktype=2)
            elif command[0] == 'em': #Enemy move
                if not enteam[encurr].real_HP <= 0:
                    attack('p')
            elif command[0] == 'emp': #Enemy physical move
                if not enteam[encurr].real_HP <= 0:
                    attack('p',atkform='p')
            elif command[0] == 'emp2': #Enemy physical move using second type
                if not enteam[encurr].real_HP <= 0:
                    attack('p',atkform='p',atktype=2)
            elif command[0] == 'ems': #Enemy special move
                if not enteam[encurr].real_HP <= 0:
                    attack('p',atkform='s')
            elif command[0] == 'ems2': #Enemy special move using second type
                if not enteam[encurr].real_HP <= 0:
                    attack('p',atkform='s',atktype=2)
            if command[0] == 'ps': #Player switch
                print(f'\nCome back {co.basestat(plteam[plcurr])}!')
                plcurr = command[3]
                print(f'\n{co.basestat(plteam[plcurr])} was sent out!')
            if command == 'pfs': #Player faint switch
                if gamenotfinished():
                    plcurr = party_select(plteam)
                    print(f'\n{co.basestat(plteam[plcurr])} was sent out!')
            if command == 'efs': #Command that signals the enemy needs to switch their pokemon into the match
                if gamenotfinished():
                    #While the current pokemon enteam[encurr][2] <= 0:
                    #encurr = rng.randint(0,len(enteam))
                    while enteam[encurr].real_HP <= 0:
                        encurr = rng.randint(0,len(enteam) - 1)
                    #Add 1 to the encurr
                    #encurr += 1
                    print(f'\nThe enemy sends out {co.basestat(enteam[encurr])}!')
                    append_encounter_list(enteam[encurr], element='pokemon')
    turnqueue = [[],[],[]]

def party_select(team, backout=False, in_battle=True):
    'Function that returns a number that corresponds to a party pokemon. If backout is true, than the menu can be exited. If in_battle is False, then the game will not check plcurr when selecting a pokemon.'
    uinp = ''
    if backout == True: #If you are allowed to exit the menu
        exittext = ' (h: help, x: exit)'
    else:
        exittext = ' (h: help)'
    while not uinp.isdigit(): #While the user value isnt even a number
        printparty(team)
        uinp = input(f'\033[1;37mEnter a number from 0-{len(team) - 1} that corresponds to the desired Pokemon{exittext}: ')
        if uinp == 'h':
            help_Menu()
        if uinp == 'x' and backout == True: #FIXME: Does this 'Exit' thing really need to be here?
            return 'Exit'
        if uinp == 'x' and backout == False:
            print('You must select a Pokemon.')
        if uinp.isdigit():
            if not (int(uinp) > -1 and int(uinp) <= len(team) - 1):
                print('\033[1;31mEnter a valid value.')
                uinp = ''  
            elif team[int(uinp)].real_HP <= 0:
                print(f'\033[1;31m{co.basestat(team[int(uinp)])} has no energy left to fight!')
                uinp = ''
            else:
                print(f'\n{co.basestat(team[int(uinp)])} is selected. ',end='')
                temp = ''
                while temp != 'z':
                    if in_battle == True:
                        temp = input('(z: switch, s: summary, x: previous): ')
                    if in_battle == False:
                        temp = input('(z: select, s: summary, x: previous): ')
                    if temp == 'z':
                        if plcurr == int(uinp) and in_battle:
                            print(f'\033[1;31m{co.basestat(team[int(uinp)])} is already on the field.')
                            uinp = ''
                        else:
                            break
                    if temp == 's':
                        team[int(uinp)].print_Stat()
                    if temp == 'x':
                        uinp = ''
                        break
    return int(uinp)

def printparty(team):
    'Takes as an argument a list of pokemon objects. All objects in the list must be pokemon.'
    print('')
    i = 0
    for poke in team:
        if poke.real_HP / poke.HP < 0.25:    
            print(f'\033[1;37m{i}. {co.basestat(poke)} HP:\033[1;31m {poke.real_HP} / {poke.HP} \033[1;37m  {co.basestat(poke,stat="type")}', end = '')
        elif poke.real_HP / poke.HP < 0.5:
            print(f'\033[1;37m{i}. {co.basestat(poke)} HP:\033[1;33m {poke.real_HP} / {poke.HP} \033[1;37m  {co.basestat(poke,stat="type")}', end = '')
        else:
            print(f'\033[1;37m{i}. {co.basestat(poke)} HP: {poke.real_HP} / {poke.HP}  {co.basestat(poke,stat="type")}',end = '')
        if '' != co.basestat(poke,stat="type_2"):
            print(f' {co.basestat(poke,stat="type_2")}')
        else:
            print()
        i += 1
        
def game_loop(team):
    while gamenotfinished(): #Core gameloop
        print('\033[1;30m----------------------------------------------\033[1;37m',end='')
        if plteam[plcurr].real_HP / plteam[plcurr].HP < 0.25:
            uinp = input(f'\n{co.basestat(plteam[plcurr])} (You) HP:\033[1;31m {plteam[plcurr].real_HP} / {plteam[plcurr].HP} ({100 * plteam[plcurr].real_HP / plteam[plcurr].HP:.1f}%)\033[1;37m | {co.basestat(enteam[encurr])} HP: {100 * enteam[encurr].real_HP/enteam[encurr].HP:.1f}% \nWhat will you do? (z: fight, s: party, r: run, h: help): ')
        elif plteam[plcurr].real_HP / plteam[plcurr].HP < 0.5:
            uinp = input(f'\n{co.basestat(plteam[plcurr])} (You) HP:\033[1;33m {plteam[plcurr].real_HP} / {plteam[plcurr].HP} ({100 * plteam[plcurr].real_HP / plteam[plcurr].HP:.1f}%)\033[1;37m | {co.basestat(enteam[encurr])} HP: {100 * enteam[encurr].real_HP/enteam[encurr].HP:.1f}% \nWhat will you do? (z: fight, s: party, r: run, h: help): ')
        else:
            uinp = input(f'\n{co.basestat(plteam[plcurr])} (You) HP: {plteam[plcurr].real_HP} / {plteam[plcurr].HP} ({100 * plteam[plcurr].real_HP / plteam[plcurr].HP:.1f}%) | {co.basestat(enteam[encurr])} HP: {100 * enteam[encurr].real_HP/enteam[encurr].HP:.1f}% \nWhat will you do? (z: fight, s: party, r: run, h: help): ')
        
        if uinp == 'z': #Attack
            if plteam[plcurr].type_2 == 'None': #One type menu
                while uinp != 'm' and uinp != 'p' and uinp != 'x':
                    uinp = input('Select an attack (p: physical, m: special, x: cancel): ')
                    if uinp == 'p':
                        turnqueue[1].append(('pmp',0,plteam[plcurr],0))
                        runturn()
                    elif uinp == 'm':
                        turnqueue[1].append(('pms',0,plteam[plcurr],0))
                        runturn()
                    elif uinp == 'x':
                        break
            elif plteam[plcurr].type_2 != 'None': #Two type menu
                while uinp != 'm1' and uinp != 'm2' and uinp != 'p1' and uinp != 'p2':
                    uinp = input(f'Select an attack: (p1: {plteam[plcurr].type} physical, m1: {plteam[plcurr].type} special, p2: {plteam[plcurr].type_2} physical, m2: {plteam[plcurr].type_2} special, x: cancel): ')
                    if uinp == 'p1':
                        turnqueue[1].append(('pmp',0,plteam[plcurr],0))
                        runturn()
                    elif uinp == 'p2':
                        turnqueue[1].append(('pmp2',0,plteam[plcurr],0)) 
                        runturn()
                    elif uinp == 'm1':
                        turnqueue[1].append(('pms',0,plteam[plcurr],0))
                        runturn()
                    elif uinp == 'm2':
                        turnqueue[1].append(('pms2',0,plteam[plcurr],0))
                        runturn()
                    elif uinp == 'x':
                        break
        if uinp == 's':
            #printparty(plteam)
            uinp = party_select(plteam, backout = True)
            if uinp == 'Exit':
                continue
            else:
                turnqueue[0].append(('ps',10,plteam[plcurr],uinp))
                runturn()
        if uinp == 'r': #Run away
            print('\nYou ran away!')
            global gameresult
            gameresult = 'RL'
            break
        if uinp == 'h': #Help menu
            help_Menu()

def print_Final_Stat():
    print(f'\n---FINAL STATS---\nBattles won: {W_Count}\nOwn Pokemon fainted: {F_Count}\n\n---STARRING---')
    for poke in encountered_list:
        print(co.basestat(poke))
        
def append_encounter_list(item, element='team'):
    'Adds pokemon to a master list of all pokemon encountered in the run. team is the list that the function pulls Pokemon from.'
    if element == 'team':
        for poke in item:
            encountered_list.append(poke)
    elif element == 'pokemon':
        encountered_list.append(item)
#--------------- INITIALIZED VARIABLES -------------
print('\033[1;37mWelcome to the Battle Factory!\nLoading. Please wait.',end='')
W_Count = 0
difficulty = diff() 
difficulty.diffval = 0
#difficulty = input('Welcome to Pokemon! Enter an integer to set the difficulty.\n(0 is easy, 40 is normal, 60 is hard, and 100+ is expert): ')
#This game is too difficult for a dedicated difficulty setting. I don't want to make players feel like they have to go higher.
'''while not difficulty.diffval.isdigit(): #FIXME
    difficulty.diffval = input('\033[1;37mWelcome to the Battle Factory! Enter an integer between 0 and 50 to set the difficulty. (0 is standard gameplay, integers above 0 are harder.): ') #FIXME
    if difficulty.diffval.isdigit():
        if int(difficulty.diffval) > 50 or int(difficulty.diffval) < 0:
            print('\n\033[1;31mPlease enter a number from 0-50.\n')
            difficulty.diffval = '' '''
difficulty.diffval = int(difficulty.diffval) #FIXME
len_roster = 1078 #This value should equal the length of the csv file for the pokemon
starter_Max_BST = 335 #Maximum BST that starters can have
base_enemy_BST = 350 #Base value for enemy base stat total
BST_Enemy_Increment = 22
enemy_Random_BST_Limit = base_enemy_BST + W_Count * BST_Enemy_Increment
base_power = 80
encountered_list = []
#Damage = ((((2*level / 5 + 2) * power * (A / D)) / 50) + 2) * targets * weather * critical * rng * stab * burn * other
#ideal = ['name', 'level', 'HP', 'HPMax', 'Atk', 'Def', 'SpAtk','SpDef', 'Speed', 'Type1']
plteam = []
plcurr = 0
encurr = 0
enteam = [co.new_Pokemon(co.random_From_Roster(BST_Limit=300),level=50 + difficulty.diffval),]
bossteam1 = [co.new_Pokemon(116,level=50 + difficulty.diffval),co.new_Pokemon(235,level=50 + difficulty.diffval),co.new_Pokemon(200,level=50 + difficulty.diffval)] #Grimer, Yanma, Crocanaw
b1name = 'Dylan'
bossteam2 = [co.new_Pokemon(27,level=50 + difficulty.diffval),co.new_Pokemon(551,level=50 + difficulty.diffval),co.new_Pokemon(741,level=50 + difficulty.diffval)] #Mandibuzz, Raticate, Magnezone
b2name = 'June'
bossteam3 = [co.new_Pokemon(290,level=50 + difficulty.diffval),co.new_Pokemon(291,level=50 + difficulty.diffval),co.new_Pokemon(292,level=50 + difficulty.diffval)] #Entei, Suicune, Raikou
b3name = 'Nemona'
bossteam4 = [co.new_Pokemon(1065,level=50 + difficulty.diffval),co.new_Pokemon(1077,level=50 + difficulty.diffval),co.new_Pokemon(1072,level=50 + difficulty.diffval)] #Hisuian Samurott, Hisuian Braviary, Origin Dialga
b4name = 'Grug'
print('.',end='')
turnqueue = [[],[],[]]
typedict = {'Normal':0,'Fire':1,'Water':2,'Grass':3,'Electric':4,'Ice':5,'Fighting':6,'Poison':7,'Ground':8,'Flying':9,'Psychic':10,'Bug':11,'Rock':12,'Ghost':13,'Dragon':14,'Dark':15,'Steel':16,'Fairy':17,'None':18}
#Dict points to index of a particular row or column on the type chart.
typechart = np.array([[1,1,1,1,1,1,1,1,1,1,1,1,.5,0,1,1,.5,1,1], #Normal
                      [1,.5,.5,2,1,2,1,1,1,1,1,2,.5,1,.5,1,2,1,1], #Fire
                      [1,2,.5,.5,1,1,1,1,2,1,1,1,2,1,.5,1,1,1,1], #Water
                      [1,.5,2,.5,1,1,1,.5,2,.5,1,.5,2,1,.5,1,.5,1,1], #Grass
                      [1,1,2,.5,.5,1,1,1,0,2,1,1,1,1,.5,1,1,1,1], #Electric
                      [1,.5,.5,2,1,.5,1,1,2,2,1,1,1,1,2,1,.5,1,1], #Ice
                      [2,1,1,1,1,2,1,.5,1,.5,.5,.5,2,0,1,2,2,.5,1], #Fighting
                      [1,1,1,2,1,1,1,.5,.5,1,1,1,.5,.5,1,1,0,2,1], #Poison
                      [1,2,1,.5,2,1,1,2,1,0,1,.5,2,1,1,1,2,1,1], #Ground
                      [1,1,1,2,.5,1,2,1,1,1,1,2,.5,1,1,1,.5,1,1], #Flying
                      [1,1,1,1,1,1,2,2,1,1,.5,1,1,1,1,0,.5,1,1], #Psychic
                      [1,.5,1,2,1,1,.5,.5,1,.5,2,1,1,.5,1,2,.5,.5,1], #Bug
                      [1,2,1,1,1,2,.5,1,.5,2,1,2,1,1,1,1,.5,1,1], #Rock
                      [0,1,1,1,1,1,1,1,1,1,2,1,1,2,1,.5,1,1,1], #Ghost
                      [1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,1,.5,0,1], #Dragon
                      [1,1,1,1,1,1,.5,1,1,1,2,1,1,2,1,.5,1,.5,1], #Dark
                      [1,.5,.5,1,.5,2,1,1,1,1,1,1,2,1,1,1,.5,2,1], #Steel
                      [1,.5,1,1,1,1,2,.5,1,1,1,1,1,1,2,2,.5,1,1], #Fairy
                      [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]) #None
                      #N,Fi,W,G,E,I,Ft,Po,G,Fl,Ps,B,R,G,Dr,D,S,F,None
#Rows are attacking type, each column is the defending type
gameresult = 'U'
W_Thresh = 15 #For testing purposes
#--------------- GAME LOOP ---------------
rentteam = [co.new_Pokemon(co.random_From_Roster(BST_Floor=300,BST_Limit= starter_Max_BST),level=50),co.new_Pokemon(co.random_From_Roster(BST_Floor=300,BST_Limit= starter_Max_BST),level=50),co.new_Pokemon(co.random_From_Roster(BST_Floor=300,BST_Limit= starter_Max_BST),level=50),co.new_Pokemon(co.random_From_Roster(BST_Floor=300,BST_Limit= starter_Max_BST),level=50),co.new_Pokemon(co.random_From_Roster(BST_Floor=300,BST_Limit= starter_Max_BST),level=50),co.new_Pokemon(co.random_From_Roster(BST_Floor=300,BST_Limit=starter_Max_BST),level=50),]
print('. done')
#pokeselect = party_select(rentteam, backout=True, in_battle=False)
#print(pokeselect)
print('\nBefore you can battle, you will need to select three Pokemon to take with you. Choose three pokemon from this list, and then continue.')
while len(plteam) < 3:
    pokeselect = party_select(rentteam, in_battle=False)
    plteam.append(rentteam[pokeselect])
    rentteam.pop(pokeselect)
    if not(3-len(plteam) == 0):
        print(f'Select {3-len(plteam)} more Pokemon.')
append_encounter_list(plteam)
append_encounter_list(enteam)
#append_encounter_list(enteam[encurr])

#Player must win 10 games to escape the loop
while W_Count <= W_Thresh:
    if gameresult == 'U':
        print(f'\n\033[1;33mBattle No. {W_Count + 1} out of 16\033[1;37m')
        game_loop(enteam)
    #Prints out the final result of the program.
    if gameresult == 'W':
        print('\033[1;33m\nThe enemy was defeated!\033[1;37m\n')
        W_Count += 1
        if W_Count <= W_Thresh:
            for poke in plteam:
                if co.basestat(poke, stat='evolution') == 'n' or co.basestat(poke, stat='evolution').isdigit():
                    print(f'\033[1;34m^ {co.basestat(poke)} gained 1 exp point.\033[1;37m')
                    poke.exp_Gain(1)
                if W_Count == 4 or W_Count == 8 or W_Count == 12 or W_Count == 16 and poke.real_HP != poke.HP: #W Count = boss battle
                    poke.real_HP += int(poke.HP)
                    print(f'\033[1;32m+ {co.basestat(poke)} fully healed.\033[1;37m')
                elif poke.real_HP != poke.HP:
                    poke.real_HP += int(poke.HP * (3 / 4))
                    print(f'\033[1;32m+ {co.basestat(poke)} healed for 75% of max HP.\033[1;37m')
                if poke.real_HP > poke.HP:
                    poke.real_HP = poke.HP
            for poke in enteam:
                poke.real_HP = poke.HP
            print("You can choose to trade one of your Pokemon for one of your opponent's. If you select to trade one of your own Pokemon, you must exchange it. If you do not want to exchange Pokemon, input x.")
            pokeselect = party_select(plteam, backout=True, in_battle=False)
            if not pokeselect == 'Exit':
                print('Choose a new Pokemon to trade and take with you.')
                for poke in enteam:
                    poke.level = 50
                    poke.calc_Stat()
                partyselect = party_select(enteam, in_battle=False)
                plteam[pokeselect] = enteam.pop(partyselect)
            if W_Count == 3: #W Count = round before boss battle
                enteam = bossteam1
                print(f'\n\033[1;31mBoss 1 incoming!\n\nBoss trainer {b1name} challenges you to a battle!\033[1;31m')
            elif W_Count == 7:
                enteam = bossteam2
                print(f'\n\033[1;31mBoss 2 incoming!\n\nBoss trainer {b2name} challenges you to a battle!\033[1;31m')
            elif W_Count == 11:
                enteam = bossteam3
                print(f'\n\033[1;31mBoss 3 incoming!\n\nBoss trainer {b3name} challenges you to a battle!\033[1;31m')
            elif W_Count == 15:
                enteam = bossteam4
                print(f'\n\033[1;31mFinal Boss incoming!\n\nWeilder {b4name} dares your approach!\033[1;31m')
            else:
                enemy_Random_BST_Limit = base_enemy_BST + W_Count * BST_Enemy_Increment
                enemy_Random_BST_Floor = 170 + W_Count * BST_Enemy_Increment
                enteam = [co.new_Pokemon(co.random_From_Roster(BST_Floor= enemy_Random_BST_Floor, BST_Limit= enemy_Random_BST_Limit),level=50 + difficulty.diffval),co.new_Pokemon(co.random_From_Roster(BST_Floor= enemy_Random_BST_Floor, BST_Limit= enemy_Random_BST_Limit),level=50 + difficulty.diffval),co.new_Pokemon(co.random_From_Roster(BST_Floor= enemy_Random_BST_Floor, BST_Limit= enemy_Random_BST_Limit),level=50 + difficulty.diffval),]
            gameresult = 'U'
            plcurr = 0
            encurr = 0
            append_encounter_list(enteam[encurr], element='pokemon')
        elif W_Count > W_Thresh:
            print('---YOU ARE A POKEMON MASTER---')
            print_Final_Stat()
            print('\nThanks to amgilles and simsketch on Github for the pokemon .csv file\n\nTHANKS FOR PLAYING')
    elif gameresult == 'L':
        print('\n\n\033[1;31mYou were defeated! You blacked out...\033[1;37m')
        print_Final_Stat()
        break
    elif gameresult == 'RL':
        print_Final_Stat()
        break
    gameresult = 'U'