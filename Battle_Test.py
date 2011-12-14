#!/usr/bin/env python
# -*- coding: utf-8 -*-


import pygame
import os
import sys
import time
import math

from pygame.locals import *
from pokemon.sprites import Sprites
from pokemon.pokemon import Pokemon
from libpokemon import Pokemon_Class

if not pygame.font: print "ERROR: No suitable Font-Driver installed!"
if not pygame.mixer: print "ERROR: No suitable Sound-Driver installed!"

class BattleWindow:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((250, 240))
        self.screen.fill((0xFF,0xFF,0xFF))
        
    
    def draw_interface(self, enemy_pokemon, user_pokemon):
        # enemy.background
        pygame.draw.line(self.screen, (0x0,0x0,0x0), (10,35), (10, 50), 2)
        pygame.draw.line(self.screen, (0x0,0x0,0x0), (11,50), (150, 50), 2)
        pygame.draw.line(self.screen, (0x0,0x0,0x0), (140,46), (150, 50), 2)
        pygame.draw.line(self.screen, (0x0,0x0,0x0), (140,48), (150, 50), 2)
        #enemy.position
        enemy = pygame.image.load("sprites/pokemon/%s_wild.png" % (enemy_pokemon.id + 1))
        self.screen.blit(enemy, (170, 0))
        #enemy.name
        bold_font = pygame.font.SysFont("Verdana", 10, True)
        
        try:
            font = pygame.font.SysFont("Arial", 13)
        except:
            font = pygame.font.Font(None, 19)
        s = font.render(Pokemon[int(enemy_pokemon.id)]["name"], False, (0x0,0x0,0x0))
        self.screen.blit(s, (8,6))
        #enemy.level
        del s
        s = bold_font.render(":L"+str(enemy_pokemon.level), True, (0x0,0x0,0x0))
        self.screen.blit(s, (30, 20))
        
        
        #enemy.hp_bar
        self.draw_hp_bar(enemy_pokemon, (30, 35))
        
        
        #user.background
        pygame.draw.line(self.screen, (0x0,0x0,0x0), (230,130), (230, 150), 2)
        pygame.draw.line(self.screen, (0x0,0x0,0x0), (91,150), (230, 150), 2)
        pygame.draw.line(self.screen, (0x0,0x0,0x0), (90,150), (229, 150), 2)
        pygame.draw.line(self.screen, (0x0,0x0,0x0), (90,150), (100, 146), 2)
        pygame.draw.line(self.screen, (0x0,0x0,0x0), (100,148), (90, 150), 2)
        
        #user.position
        user = pygame.image.load("sprites/pokemon/%s_back.png" % (user_pokemon.id + 1))
        self.screen.blit(user, (15, 90))
        
        #user.name
        s2 = font.render(Pokemon[int(user_pokemon.id)]["name"], False, (0x0,0x0,0x0))
        self.screen.blit(s2, (150, 95))
        
        #user.level
        del s2
        s2 = bold_font.render(":L " + str(user_pokemon.level), False, (0x0,0x0,0x0))
        self.screen.blit(s2, (145, 108))
        
        #user.hpbar
        self.draw_hp_bar(user_pokemon, (115,128))
        
        #user.currenthp
        # user.get('hp') - user.current_hp
        s2 = bold_font.render("HP: %s/%s" % (user_pokemon.get('hp')-user_pokemon.current_hp, user_pokemon.get('hp')), False, (0x0,0x0,0x0))
        self.screen.blit(s2, (165, 136))
        
        
        
        
        self.di2()
        pygame.display.update()
      
    def di2(self):
        pass
        
        
    def draw_hp_bar(self, user_pokemon, posxy):
        #clear hpbar (for update reasons)
        HPCOLOR = (99,171,92)
        aHP = ((user_pokemon.get('hp') - user_pokemon.current_hp)*100)/user_pokemon.get('hp')
        if aHP >= 75: HPCOLOR = (99,171,92)
        elif aHP >= 25: HPCOLOR = (242,239,65)
        else: HPCOLOR = (171,92,92)
        
        #draw black border
        xsurface = pygame.Surface((102, 7))
        xsurface.fill((0x0,0x0,0x0))
        self.screen.blit(xsurface,(posxy[0],posxy[1]))
        if user_pokemon.get('hp') - user_pokemon.current_hp < 0:
            print "Pokemon died"
        else:  
            # draw full white screen
            hpsurface = pygame.Surface((100, 5))
     
            hpsurface.fill((0xFF,0xFF,0xFF))
            self.screen.blit(hpsurface, (posxy[0]+1,posxy[1]+1))#green overlay
            
            #calculate current hp
       
            xh = int(round(user_pokemon.get('hp')))
            h = int((xh - user_pokemon.current_hp) * 100 / xh)

            print user_pokemon.current_hp
            try: hpsurface = pygame.Surface((h, 5))
            except: print user_pokemon + " has died during an attack"
            hpsurface.fill(HPCOLOR)
            self.screen.blit(hpsurface, (posxy[0]+1,posxy[1]+1))#green overlay
        
        
    
    def keep_alive(self):
        self.battle_clock = pygame.time.Clock()
        i = 1
        while True:
            self.battle_clock.tick(20)
            i += 1
            if i == 30: break
            
if __name__ == "__main__":
    # debugging purposes
    Bisasam = Pokemon_Class()
    Bisasam.id = Bisasam.id_by_name("Bisasam")
    Bisasam.fill_stats()
    Bisasam.name = Bisasam.auto_guess(Bisasam.id)
    Bisasam.learn_attack("Egelsamen")
    Bisasam.learn_attack("Giftpuder")
    Bisasam.level = 14

    # deal damage to Bisasam
    Bisasam.current_hp = 5
    Garados = Pokemon_Class()
    Garados.id = Garados.id_by_name("Garados")
    Garados.fill_stats()
    Garados.name = Garados.auto_guess(Garados.id)
    Garados.learn_attack("Hyperstrahl")
    Garados.learn_attack("Donnerblitz")
    Garados.learn_attack("Surfer")
    Garados.learn_attack("Erdbeben")
    Garados.level = 81
    d = BattleWindow()
    d.draw_interface(Garados,Bisasam)
    d.keep_alive()
