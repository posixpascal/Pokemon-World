# This File is used for dyncore settings.
# You can modify this file as you wish but be careful to not overwrite
# setdr.py in ./pokemon/setdr.py

try:
  from graphic_engine import Character
except: pass

def start_pos(posxy):
  x = int(posxy.split(".")[0])*16
  y = int(posxy.split(".")[1])*16
  Character.move(x,y)
  Character.sprites.update()
  

  