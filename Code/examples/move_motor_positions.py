import time
from droid_class import Droid

d=Droid()
array=[150,150,100,110,50,40,100,180,180,40,180,40,50,100] #set arms by side
d.setMotors(array)
time.sleep(1)
mov=[180 for i in range(len(array))]
d.setMotors(mov) #set them all to highest positions
time.sleep(1)
mov[7]=50 #change just one of them
d.setMotors(mov)