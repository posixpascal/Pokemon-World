#!/usr/bin/env python

import pygame
import os
import sys
import time
import math

from pygame.locals import *
from pokemon.sprites import Sprites
from Battle_Test import BattleWindow

if not pygame.font: print "ERROR: No suitable Font-Driver installed!"
if not pygame.mixer: print "ERROR: No suitable Sound-Driver installed!"

def load_image(name, colorkey=None):
    fullname = os.path.join(name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error, message:
        print 'Cannot load image:', name
        raise SystemExit, message
    if image.get_alpha() == None:
        image = image.convert()
    else: image = image.convert_alpha()
    
    image.set_colorkey([0,255,0], RLEACCEL)
    return image, image.get_rect()
    

def load_sound(name):
    class NoneSound:
        def play(self): pass
    if not pygame.mixer:
        return NoneSound()
    fullname = os.path.join('data', name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error, message:
        print 'Cannot load sound:', wav
        raise SystemExit, message
    return sound
    

class MapSprite(pygame.sprite.Sprite):
    image = None
  
    def __init__(self, arg, location):
        pygame.sprite.Sprite.__init__(self)
        try: i = load_image(os.path.join("sprites","map",Sprites[arg]["sprite"] + ".jpg"))
        except: i = load_image(os.path.join("sprites","map", arg["sprite"] + ".jpg"))
        MapSprite.image = i[0]
        self.image = MapSprite.image
        self.rect = i[1]
        self.rect.topleft = location
    
    
class Character(pygame.sprite.Sprite):
    image = None
  
    def __init__(self, location, pobj):
        self.pobj = pobj
        self.mc = pobj.MapContent
        self.has_passed_mob_fields = 0
        pygame.sprite.Sprite.__init__(self)
        i = load_image("g.jpg", [0x00,0xFF,0x0])
        Character.image = i[0]
        self.old = (0,0,0,0)
        self.image = Character.image
        self.rect = i[1]
        self.start_pos = [7, 5]
        self.rect.topleft = location 
        self.screen = pygame.display.get_surface().get_rect()
        self.view = 0x1#front

    def update(self, amount):
        # Make a copy of the current rectangle for use in erasing
        self.old = self.rect
        #print self.MapContent[self.old[1]/16][self.old[0]/16]
        #print self.MapContent[y][x]
        # Move the rectangle by the specified amount
        self.new_rect = self.rect.move(amount)
        i = 1
        level = 0
        try: level = self.mc[self.new_rect.y / 16][self.new_rect.x / 16]["level"]
        except:
            i = 0
            if self.new_rect.y / 16 == -1:
                # map_change to next route.
                mp_n = self.pobj.MapTrigger["MapCh"][self.new_rect.x/16][self.new_rect.y/16].replace("\n","")
                self.pobj.RenderMap(mp_n)
        if i == 0: pass
        else:
            if level == 0x2:
                pass#
            elif level == 0x4:
                Sign(self.new_rect.x/16, self.new_rect.y/16, self.screen)
      
            else:
                self.rect = self.new_rect
        if level == 0x3:
            self.pobj.battle()
            self.has_passed_mob_fields += 1
        elif level == 0x6:
            x,y = int(self.rect.x/16),int(self.rect.y/16)
            try:
                curmap = self.pobj.MapTrigger["door"][x][y]
                self.pobj.RenderMap(curmap)
            except: print "No Door set on: x%s, y%s" % (x,y)
        # Check to see if we are off the screen
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.x > (self.screen.width - self.rect.width):
            self.rect.x = self.screen.width - self.rect.width
        if self.rect.y < 0:
            self.rect.y = 0
        elif self.rect.y > (self.screen.height - self.rect.height):
            self.rect.y = self.screen.height - self.rect.height    

      
  
def Sign(x,y, screen): 
    return 1
    mapn = "alabastia"
    f = open("maps/%s/triggers.pcf" % (mapn), "r")
    for trigger in f.readlines():
        if trigger.split(" ")[0] == "sign":
            if int(trigger.split(" ")[1].split(".")[0]) == x and int(trigger.split(" ")[1].split(".")[1]) == y:
                f = open(os.path.join("maps",mapn, trigger.split(" ")[2]), "r")
                for line in f.readlines():
                    # wait for user_press_x
                    pygame.event.post(pygame.event.Event(0x28, {'text': line}))#fire event:sign
           
class Pokemon_Game:
    def __init__(self):
        pygame.init()
        self.stop_update = 0
        self.movable = 1#allows character to move
        self.sign = 0#sign_reader
        self.isDialog = 0
        self.mob_rate = 0
        self.DialogEventsHold = 0
        self.screen = pygame.display.set_mode((20*16, 20*16))#pygame.FULLSCREEN (for start sequence) #d
        pygame.mouse.set_visible(1)
        pygame.key.set_repeat(1, 300)
        self.Position = {"player":{"x":0x0,"y":0x0}, "c":{}}
        self.RenderMap("test")
        #pygame.display.update()
        
        self.clock = pygame.time.Clock()
        running = True
        loops = 0
        while running:
            self.clock.tick(30)#30.fps limitation here.
            for event in pygame.event.get():
        
                if event.type == QUIT:
                    running = 0
                elif event.type == 40:
                    # incoming: text_arg
                    txt = event.text
                    Dialog(txt)
                if self.movable == 1:
                    if event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                            pygame.event.post(pygame.event.Event("QUIT"))
                        elif event.key == K_LEFT:
                            self.Player.view = 0x3
                            self.Player.update([-16,0])
                        elif event.key == K_UP:#up
                            #self.Player.cimage("h.jpg")
                            self.Player.view = 0x2
                            self.Player.update([0,-16])
                        elif event.key == K_DOWN:
                            self.Player.view = 0x1
                            self.Player.update([0, 16])
                        elif event.key == K_RIGHT:
                            self.Player.view = 0x0
                            self.Player.update([16,0])
                if self.isDialog:
                    if self.DialogEventsHold <= 1:
                        self.readmap(self.map_name)
                        self.isDialog = 0
                        if not self.stop_update: pygame.display.update()
                    else:
                        self.DialogEventsHold -= 1
                x = MapSprite(self.MapContent[self.Player.old[1]/16][self.Player.old[0]/16],[self.Player.old[0],self.Player.old[1]])
                self.screen.blit(x.image, x.rect)
                self.screen.blit(self.Player.image, self.Player.rect)
                if not self.stop_update: pygame.display.update([self.Player.old, self.Player.rect])
    def battle(self):
        print "Start Battling"
        BattleWindow().draw_interface(130)
        self.battle_clock = pygame.time.Clock()
        i = 0
        while True:
            print i
            self.battle_clock.tick(20)
            i += 1
            if i == 100: break
        self.render_map_full(self.map_name)
    
    def render_map_full(self, x): pass
    def movePlayer(self, posxy):
        x, y = posxy[0],posxy[1]
        self.readmap(self.map_name)
        
        self.Player = Character([x*16,y*16], self)
        self.screen.blit(self.Player.image, self.Player.rect)
        if not self.stop_update: pygame.display.update()
        
    def RenderMap(self, mn):
        self.map_name = mn
        
        pygame.display.set_caption("Pokemon - {Current Map: %s}" % (mn))
        self.screen.fill(( 0xFF, 0xFF, 0xFF ))
        self.MapSettings = self.getMapSettings(mn)
        

        self.readmap(mn)
        
        self.Player = Character([self.Position["player"]["x"]*16,self.Position["player"]["y"]*16], self)
        #self.Dialog("    %s" % (self.map_name.title()))
        self.screen.blit(self.Player.image, self.Player.rect)
        
        pygame.display.update()    
    
    def fadeBlack(self):
        self.screen.fill(( 0x0, 0x0, 0x0 ))# black transition for battles
        pygame.display.update()
        
    def getMapSettings(self, mn):
        self.MapTrigger = {
        "door": {},
        "sign": {},
        "MapCh":{}
    }
        f = open(os.path.join("maps",mn, "settings.pcf"), "r")
        for line in f.readlines():
            line = line.split("\n")[0]
            if line.split(" ")[0] == "wild_pkm_rate":
                wpr = int(line.split(" ")[1])
            elif line.split(" ")[0] == "wild_pkm":
                wp = "".join(line.split(" ")[1:]).split(",")
            elif line.split(" ")[0] == "start_pos":
                d = line.split(" ")[1].split(".")
                x,y = int(d[0]),int(d[1])
                self.Position["player"]["x"] = x
                self.Position["player"]["y"] = y
    # get triggers here
        u = open(os.path.join("maps", mn, "triggers.pcf"))
        for line in u.readlines():
            line.split("\n")[0]
            if line.split(" ")[0] == "map_ch":
                f = line.split(" ")[1].split(".")
                x,y = int(f[0]),int(f[1])
                self.MapTrigger["MapCh"][x] = {y: line.split(" ")[2]}
            elif line.split(" ")[0] == "door":
                xy = line.split(" ")[1].split(".")
                x, y = xy[0], xy[1]
                mapname = line.split(" ")[2]
                self.MapTrigger["door"][int(x)] = {int(y):mapname}
                #self.Position["player"]["x"] = int(line.split(" ")[3].split(".")[0])
                #self.Position["player"]["y"] = int(line.split(" ")[3].split(".")[1])
        return {'wpr':wpr,'wp':wp}
  
    def Dialog(self, text):
        font = pygame.font.Font(None, 16)
        surf = pygame.display.get_surface()
        color = (255,255,255)
        rect = pygame.Rect(0, 0, 20*16, 30)
        width = 0
        pygame.draw.rect(surf, color, rect, width)
        t = font.render(text, True, (0x0,0x0,0x0))
        textRect1 = t.get_rect()
        textRect1.x = 10
        textRect1.y = 10
        self.isDialog = 1
        self.DialogEventsHold = 5*30
        self.screen.blit(t, textRect1)
        pygame.display.update()

    def readmap(self, mn):
        f = open(os.path.join("maps",mn,"world.pcf"),"r")
        i = 0
        u = 0
        self.MapContent = {}
        for row in f.readlines():
            self.MapContent[i] = {}
            for obj in row.split(","):
                obj = int(obj, 16)
                x = MapSprite(obj, [u*16,i*16])
                self.screen.blit(x.image, x.rect)
                self.MapContent[i][u] = Sprites[obj]
                u += 1
            u = 0
            i += 1
    
    
    
if __name__ == "__main__": Pokemon_Game()