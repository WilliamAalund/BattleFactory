import numpy as np
import csv
import random as rng
#Credit to amgilles: https://gist.github.com/armgilles/194bcff35001e7eb53a2a8b441e8b2c6#file-pokemon-csv
#Credit to simsketch: https://gist.github.com/simsketch/1a029a8d7fca1e4c142cbfd043a68f19
#Credit to tenlaven: 
naturedict = {'Hardy': ('attack','attack'),'Lonely': ('attack','defense'),'Adamant': ('attack','sp_Attack'),'Naughty': ('attack','sp_Defense'),'Brave': ('attack','speed'),
              'Bold': ('defense','attack'),'Docile': ('defense','defense'),'Impish': ('defense','sp_Attack'),'Lax': ('attack','sp_Defense'),'Relaxed': ('defense','speed'),
              'Modest': ('sp_Attack','attack'),'Mild': ('sp_Attack','defense'),'Bashful': ('sp_Attack','sp_Attack'),'Rash': ('sp_Attack','sp_Defense'),'Quiet': ('sp_Attack','speed'),
              'Calm':('sp_Defense','attack'),'Gentle':('sp_Defense','defense'),'Careful':('sp_Defense','sp_Attack'),'Quirky':('sp_Defense','sp_Defense'),'Sassy':('sp_Defense','speed'),
              'Timid':('speed','attack'),'Hasty':('speed','defense'),'Jolly':('speed','sp_Attack'),'Naive':('speed','sp_Defense'),'Serious':('speed','speed')}
    
def basestat(uinp, stat='species'):
    'Returns a given base stat for a pokemon. uinp is a pokemon object.'
    with open('pokemon.csv') as statsheet:
        poke_reader = csv.reader(statsheet,delimiter=',')
        pokemon_stats = list(poke_reader) #Index of pokemon stats starts at 1. Example: pokemon_stats[1] = Bulbasaur stats
        #print(pokemon_stats[uinp.species][3])
        if stat == 'species':
            return pokemon_stats[uinp.species_ID][3]
        elif stat == 'HP':
            return int(pokemon_stats[uinp.species_ID][15])
        elif stat == 'attack':
            return int(pokemon_stats[uinp.species_ID][16])
        elif stat == 'defense':
            return int(pokemon_stats[uinp.species_ID][17])
        elif stat == 'sp_Attack':
            return int(pokemon_stats[uinp.species_ID][18])
        elif stat == 'sp_Defense':
            return int(pokemon_stats[uinp.species_ID][19])
        elif stat == 'speed':
            return int(pokemon_stats[uinp.species_ID][20])
        elif stat == 'type':
            return pokemon_stats[uinp.species_ID][4]
        elif stat == 'type_2':
            #print(pokemon_stats[uinp][5])
            return pokemon_stats[uinp.species_ID][5]
        elif stat == 'evolution':
            return pokemon_stats[uinp.species_ID][22]

def nature_Multiplier(nature, stat, return_Type = 'number'):
    'Returns the correct stat multiplier for a corresponding nature and stat. Both parameters are strings return_Type will determine if the function outputs either a number usable for calculation, or a symbol that can be displayed in text, and represents a stat buff.'
    if return_Type == 'number':
        if naturedict[nature][0] == stat and naturedict[nature][1] == stat:
            return 1
        elif naturedict[nature][0] == stat:
            return 1.1
        elif naturedict[nature][1] == stat:
            return 0.9
        else:
            return 1 
    elif return_Type == 'text':
        if naturedict[nature][0] == stat and naturedict[nature][1] == stat:
            return ''
        elif naturedict[nature][0] == stat:
            return '+'
        elif naturedict[nature][1] == stat:
            return '-'
        else:
            return ''

def random_Nature():
    'Returns a random nature value from the possible natures that a pokemon can have. All possible natures are located in the naturedict dictionaries, and the value that is returned is a string.'
    naturelist = []
    for nature in naturedict:
        naturelist.append(nature)
    return naturelist[rng.randint(0,len(naturelist) - 1)]

def random_From_Roster(BST_Floor=0, BST_Limit=None, color_Limit=None):
    roster_List = []
    with open('pokemon.csv') as statsheet:
        poke_reader = csv.reader(statsheet,delimiter=',')
        pokemon_stats = list(poke_reader) #Index of pokemon stats starts at 1. Example: pokemon_stats[1] = Bulbasaur stats
        if BST_Limit != None:
            for poke in pokemon_stats:
                if poke[21].isdigit() and int(poke[21]) <= BST_Limit and int(poke[21]) >= BST_Floor:
                    roster_List.append(pokemon_stats.index(poke))
            return roster_List[rng.randint(0,len(roster_List) - 1)]
                    

class Pokemon:
    def __init__(self):
        self.species_ID = 1 #Pokedex number
        self.level = 100 #Level ranging from 1 - 100 is legal
        self.exp = 0
        self.max_Exp = 0
        self.CP = 0
        self.real_HP = 0 #The number that determines if a pokemon is fainted or not
        self.HP = 0
        self.attack = 0
        self.defense = 0
        self.sp_Attack = 0
        self.sp_Defense = 0
        self.speed = 0
        self.IV_HP = 0
        self.IV_Attack = 0
        self.IV_Defense = 0 
        self.IV_Sp_Attack = 0
        self.IV_Sp_Defense = 0
        self.IV_Speed = 0
        self.EV_HP = 0
        self.EV_Attack = 0
        self.EV_Defense = 0 
        self.EV_Sp_Attack = 0
        self.EV_Sp_Defense = 0
        self.EV_Speed = 0
        self.EV_Total = self.EV_HP + self.EV_Attack + self.EV_Defense + self.EV_Sp_Attack + self.EV_Sp_Defense + self.EV_Speed
        self.nature = 'Adamant'
        self.item = '-'
        self.type = 'None' #FIXME: Type system needs to become more robust, and shouldnt have to be stored in the pokemon object.
        self.type_2 = 'None'

        
    def calc_Stat(self):
        'Calculates the real stats of a pokemon object using given parameters.'
        self.type = basestat(self, stat='type')
        if basestat(self, stat='type_2') == '':
            self.type_2 = 'None'
        else:
            self.type_2 = basestat(self, stat='type_2')
        if basestat(self) == 'Shedinja':
            self.HP = 1
        else:
            self.HP = int((((2 * basestat(self, stat = 'HP') + self.IV_HP + (self.EV_HP / 4)) * self.level) / 100) + self.level + 10)
        self.attack = int(((((2 * basestat(self, stat = 'attack') + self.IV_Attack + (self.EV_Attack / 4)) * self.level) / 100) + 5) * nature_Multiplier(self.nature, 'attack'))
        self.defense = int(((((2 * basestat(self, stat = 'defense') + self.IV_Defense + (self.EV_Defense / 4)) * self.level) / 100) + 5) * nature_Multiplier(self.nature, 'defense'))
        self.sp_Attack = int(((((2 * basestat(self, stat = 'sp_Attack') + self.IV_Sp_Attack + (self.EV_Sp_Attack / 4)) * self.level) / 100) + 5) * nature_Multiplier(self.nature, 'sp_Attack'))
        self.sp_Defense = int(((((2 * basestat(self, stat = 'sp_Defense') + self.IV_Sp_Defense + (self.EV_Sp_Defense / 4)) * self.level) / 100) + 5) * nature_Multiplier(self.nature, 'sp_Defense'))
        self.speed = int(((((2 * basestat(self, stat = 'speed') + self.IV_Speed + (self.EV_Speed / 4)) * self.level) / 100) + 5) * nature_Multiplier(self.nature, 'speed'))
        self.EV_Total = self.EV_HP + self.EV_Attack + self.EV_Defense + self.EV_Sp_Attack + self.EV_Sp_Defense + self.EV_Speed
        self.CP = int((self.HP + self.attack + self.defense + self.sp_Attack + self.sp_Defense + self.speed) * 6 * self.level / 100 + ((self.EV_Total * 2.0511811024) * self.level / 100)) #10000 CP = 600 BST pokemon with max IV and fully invested EV
        #int((((2 * basestat(self, stat = 'HP') + self.IV_HP + (self.EV_HP / 4)) * self.level) / 100) + self.level + 10)
        #int(((((2 * basestat(self, stat = 'attack') + self.IV_attack + (self.EV_attack / 4)) * self.level) / 100) + 5) * nature_Multiplier(self.nature, 'attack'))
        #int(((((2 * basestat(self, stat = 'defense') + self.IV_Defense + (self.EV_Defense / 4)) * self.level) / 100) + 5) * nature_Multiplier(self.nature, 'defense'))
        if self.real_HP > self.HP:
            self.real_HP = self.HP
        if self.CP > 10000:
            self.CP = 10000
        if self.CP < 10:
            self.CP = 10
            
    def roll_Attributes(self, floor=31,ceiling=31):
        'Will provide random values for the IV and nature stats. Used to generate new wild pokemon. floor is used to determine the minimum IV value that can be rolled, and cieling determines the maximum value that can be rolled.'
        self.IV_HP = rng.randint(floor,ceiling)
        self.IV_Attack = rng.randint(floor,ceiling)
        self.IV_Defense = rng.randint(floor,ceiling)
        self.IV_Sp_Attack = rng.randint(floor,ceiling)
        self.IV_Sp_Defense = rng.randint(floor,ceiling)
        self.IV_Speed = rng.randint(floor,ceiling)
        self.nature = random_Nature()
        self.calc_Stat()
    
    def heal(self):
        while self.real_HP < self.HP:
            self.real_HP += 1
    
    def exp_Gain(self,exp_Val):
          self.exp += exp_Val
          if self.exp >= 3:
              tempname = basestat(self)
              HP_Ratio = self.real_HP / self.HP
              if basestat(self, stat='evolution') == 'n':
                  self.species_ID += 1
              elif basestat(self, stat='evolution').isdigit():
                  
                  
                  '''with open('pokemon.csv') as statsheet:
                      poke_reader = csv.reader(statsheet,delimiter=',')
                      pokemon_stats = list(poke_reader) #Index of pokemon stats starts at 1. Example: pokemon_stats[1] = Bulbasaur stats
                      new_Evolution_ID = 0
                      for poke in pokemon_stats:
                          if poke[2] == basestat(self, stat='evolution'):
                              break
                          else:
                              new_Evolution_ID += 1'''
                  self.species_ID = int(basestat(self, stat='evolution'))
                  #print('species ID',self.species_ID)
              self.calc_Stat()
              print(f'\033[1;35m* {tempname} evolved into {basestat(self)}!\033[1;37m')
              self.real_HP = int(self.HP * HP_Ratio)
              self.exp = 0
    
    
    def print_Stat(self,det=1):
        'Displays the stats of a specific pokemon object. det determines the amount of detail displayed. 1 = Level + Stats.' #FIXME: Add more precision
        if basestat(self, stat='evolution') == 'n' or basestat(self, stat='evolution') != '' and basestat(self, stat='evolution') != 'm':
            can_Evolve = 'Can evolve'
        else:
            can_Evolve = "Cannot evolve"
        if det >= 1:
            print(f'\n{basestat(self)} |',basestat(self, stat='type'),basestat(self, stat='type_2'),'\nCP:',self.CP,'\nLevel:',self.level,'\nExp:',self.exp,'/ 3',f'{can_Evolve}','\nHP:',self.real_HP,'/',self.HP,'\nAttack:',self.attack,nature_Multiplier(self.nature, 'attack', return_Type = 'text'),'\nDefense:',self.defense,nature_Multiplier(self.nature, 'defense', return_Type = 'text'),'\nSp.Attack:',self.sp_Attack,nature_Multiplier(self.nature, 'sp_Attack', return_Type = 'text'),'\nSp.Defense:',self.sp_Defense,nature_Multiplier(self.nature, 'sp_Defense', return_Type = 'text'),'\nSpeed:',self.speed,nature_Multiplier(self.nature, 'speed', return_Type = 'text'),'\nNature:',self.nature,'\n')
        if det >= 2:   
            print('IV Values: HP',self.IV_HP,'Attack',self.IV_Attack,'Defense',self.IV_Defense,'sp_Attack',self.IV_Sp_Attack,'sp_Defense',self.IV_Sp_Defense,'speed',self.IV_Speed)
        if det >= 3:
            print(basestat(self, stat = 'sp_Attack'))

def new_Pokemon(species_ID,level=5,cheat=0):
    'Returns a new pokemon object using a species input'
    new_Poke = Pokemon()
    new_Poke.species_ID = species_ID
    new_Poke.level = level
    new_Poke.roll_Attributes()
    new_Poke.real_HP = new_Poke.HP
    
    return new_Poke

#random_From_Roster(BST_Limit=450)
#poke1 = new_Pokemon(109, level = 50)
#poke1.print_Stat(det=1)
#print(basestat(poke1, stat='evolution')) #This is a string
#poke1.exp_Gain(3)
#print('\033[1;35mExample text')


        