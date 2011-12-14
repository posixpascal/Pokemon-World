#!/usr/bin/env python

print "Generate Button Table.. ",

Buttons = [
    1,2,3,4,5,6,7,8,9
]


#region: tab_1
Buttons += xrange(10, 43)
Buttons += xrange(60, 87)
Buttons.pop(30)
print "[DONE]"


f = open("created_function.txt", "w")
str = ""#empty.str
print "Create Functions.. ",
for button in Buttons:
    str += "self.connect(self.pushButton__%s, QtCore.SIGNAL('clicked()'), lambda w=%s: self.pushButton_click(w))" % (button, button)
    str += "\n"

str += "\n\n"    
for label in xrange(1, 401):
    str += "self.connect(self.label_%s, QtCore.SIGNAL('clicked()'), lambda w=%s: self.label_click(w))" % (label, label)
    str += "\n"
    
print "[DONE]"
print "Write Changes to File..",    
f.write(str)
print "[DONE]"

print "Clean up Script..",
f.close()
del str
del Buttons
print "[DONE]"

# I know that Cleaning is unneccassarry but well. you' comment to.
