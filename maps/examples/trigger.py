# This Trigger is just a basic example of WHAT a Trigger is used for
# The normal driven trigger is usable like this:
# <trigger.name> <posx>.<posy> <trigger.params>
# Well, there are some triggers which handle things diffrent.
# There is one trigger which is executed on die (just as an example)
# Its build like this:
# Character.Loose Map_Move 'latest'
# The "latest" Parameter on MAP_MOVE is the last POK_CENTER.
# Well.. you can not reborn in an unknown city ;) for example.
# ------
# You can even combine triggers like:
# Character.Loose Map_Move 'latest'
# Character.Loose StealMoney 10p
# Character.Loose HealPkm ALL FULL
# Character.Loose ReadLine loose_msg.txt RANDOM
# This is the FULL Character-Loose Trigger Example
# -----
# But how can I build my own triggers?
# Its simple
# First create a new File at ./triggers/mytriggername.py
# Fill the file with the following content:


class MyAwesomeTrigger():
  requires = ['PARTY','ITEMS']
  adapt = 'Character.Loose'
  times = 1#just once (or always)
  def on_execute(self, param):
    return 'HealPkm ALL 10p'
    
# This Plugin would HEAL your Pokemon (each) with 10% before dieing