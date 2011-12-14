#!/usr/bin/env python

import os
import sys
import time
import math
import urllib
import urllib2
import random

from pokemon.constants import *
from pokemon.attacks import *
from pokemon.types import *
from pokemon.pokemon import *
from pokemon.sprites import *
from pokemon.tunnels import PokefansTunnel
from pokemon.party import Party



def gp(x):
    x = int(x) / 8
    print Pokemon[x]

def typ2hex(typ):
    for t in Types:
        if Types[t] == typ: return t



class Pokemon_Class:
    def __init__(self):
        self.id = 0x0
        self.level = 0x0#0
        self.trainer_id = 0x0
        self.nickname = 0x0
        self.type_1 = 0xf#nulltype
        self.type_2 = 0xf#nulltype
        self.base_hp = 0x0
        self.base_atk = 0x0
        self.base_def = 0x0
        self.base_satk = 0x0
        self.base_sdef = 0x0
        self.base_spez = 0x0
        self.base_init = 0x0
        self.base_exp = 0x0
        self.died = 0x0
        
        self.EV = {
            'hp': 0,
            'atk': 0,
            'def': 0,
            'spez': 0,
            'spd': 0 }
        self.IV = {
            'hp': random.randint(0, 15),
            'atk': random.randint(0, 15),
            'def': random.randint(0, 15),
            'spez': random.randint(0, 15),
            'spd': random.randint(0, 15) }
        
        #battle_vars
        self.current_hp = 0x0#self._hp - self.current_hp - ifnull: die
        self.boosts = [0x0,0x0,0x0,0x0,0x0,0x0]
        #              atk,def,spd,spe,acc,eva
        self.status = 0x0#for: every status
        self.sub_status = 0x0#for: confuse/lovely(gsk)
        self.delegator = 0x0#has delegator?
        self.delegator_hp = 0x0#how much hp got the delegator
        self.exp_type = EXPBase[0xf]
        self.angriffe = {
            0: {'id':0x0, 'used_ap':0x0, 'is_blocked': 0x0},
            1: {'id':0x0, 'used_ap':0x0, 'is_blocked': 0x0},
            2: {'id':0x0, 'used_ap':0x0, 'is_blocked': 0x0},
            3: {'id':0x0, 'used_ap':0x0, 'is_blocked': 0x0},
        }
        self.catch_rate = 0x0
        self.catch_able = 0x0
        
    
    def get(self, stat):
        # FORMULA FOR HP:
        
        # ((IV + BASEHP + (math.sqrt(EVS)/8) + 50) * LEVEL / 50) + 10
        if stat == "hp": return int(round((self.IV["hp"] + self.base_hp + (math.sqrt(self.EV["hp"])/8)+50) * self.level / 50) + 10)
        else: return int(round((self.IV[stat] + int(getattr(self, "base_%s" % (stat))) + (math.sqrt(self.EV[stat])/8)) * self.level / 50) + 5)

    def dealDamage(self, pokemon_id, attack_id):
        # detect whether use specdef or def.
        if Attacks[pokemon_id.angriffe[attack_id]['id']]['typ'] in SpecialTypes:
            type = 0
        else: type = 1
        
        base_dmg = Attacks[pokemon_id.angriffe[attack_id]['id']]['atk']
        if type == 0:
            base_def = self.get('spez')
            atk = pokemon_id.get('spez')
        else:
            base_def = self.get('def')
            atk = pokemon_id.get('atk')
            
 
        if isStab(Attacks[pokemon_id.angriffe[attack_id]['id']]['typ'], pokemon_id): STAB = 1.5
        else: STAB = 1.0
        
        Type = 1#calculate type here
        Critical = 1
        other = 1
        rax = random.uniform(0.85,1.00)
       
        # ( (2*self.level+10)/250) * (atk/base_def) * base_dmg + 2)
        d = ( (2.0*float(pokemon_id.level) + 10.0)/250.0 * (float(atk)/float(base_def)) \
              * float(base_dmg) + float(2))
        min = round((STAB * Type * Critical * other) * 0.85, 3)
        max = round((STAB * Type * Critical * other) * 1.00, 3)
        range = random.uniform(min,max)
        print round(d*range) # round up (not pokemon:valid)
        
    def fill_stats(self):
        self.base_hp = Pokemon[self.id]["base_kp"]
        self.base_atk = Pokemon[self.id]["base_atk"]
        self.base_def = Pokemon[self.id]["base_def"]
        self.base_satk = Pokemon[self.id]["base_satk"]
        self.base_sdef = Pokemon[self.id]["base_sdef"]
        self.base_spd = Pokemon[self.id]["base_spd"]
        self.base_spez = Pokemon[self.id]["base_satk"]
        # add type of pokemon
        if len(Pokemon[self.id]["types"]) == 2:
            self.type_1 = Pokemon[self.id]['types'][0]
            self.type_2 = Pokemon[self.id]['types'][1]
        else: self.type_1 = Pokemon[self.id]['types'][0]
    def add_atk(self, idx):#please rewrite
        for atk in self.angriffe:
            if self.angriffe[atk]["id"] == idx: return False# attacke nicht 2mal lernbar.
            if self.angriffe[atk]["id"] == 0x0:
                self.angriffe[atk]["id"] = idx
                return True
        # pkm kann bereits 4 attacken => alte verlernen.
        d = ''
        while d == "":
            d = raw_input("Welche Attacke soll vergessen werden?: ")
            if d.isdigit() == True:
                if d >= 1 and d <= 4:
                    self.angriffe[d-1]["id"] = idx
                    break
                    
        
        return False#atk nicht lernbar

        
    def learn_attack(self, name):
        if Pokemon[self.id]["attacks"].has_key(name):
            for atk in Attacks:
                if Attacks[atk]["name"] == name:
                    self.add_atk(atk)
                    return True
        else: return False
        
    def auto_guess(self, id):
        return Pokemon[id]["name"]
    
    def details_array(self):
        return {
            "name": self.name,
            "id": self.id,
            "angriffe": self.angriffe,
        }
    
    def __str__(self):
        return "self.name"
    def __unicode__(self):
        return "self."    
        
    def details(self):#add webinterface in 0.4
        pass
        
    def id_by_name(self, n):
        for pokemon in Pokemon:
            if Pokemon[pokemon]["name"] == n: return pokemon
                
    
    
if __name__ == "__main__":
    Bisasam = Pokemon_Class()
    Bisasam.id = Bisasam.id_by_name("Karpador")
    Bisasam.fill_stats()
    Bisasam.name = Bisasam.auto_guess(Bisasam.id)
    Bisasam.learn_attack("Egelsamen")
    Bisasam.learn_attack("Solarstrahl")
    Bisasam.level = 100

    # deal damage to Bisasam
    Bisasam.current_hp = 5
    Garados = Pokemon_Class()
    Garados.id = Garados.id_by_name("Garados")
    Garados.fill_stats()
    Garados.name = Garados.auto_guess(Garados.id)
    Garados.learn_attack("Hyperstrahl")#without level up
    Garados.learn_attack("Hydropumpe")
    Garados.level = 100
    

    Bisasam.dealDamage(Garados, 1)
