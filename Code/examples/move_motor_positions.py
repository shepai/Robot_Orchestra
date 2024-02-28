import time
from droid_class import Droid

d=Droid()
array=[150,150,100,110,50,40,100,180,180,40,180,40,50,100]
d.set_specific(1,100)
d.setMotors(array)
time.sleep(1)
d.setMotors([180 for i in range(len(array))])
time.sleep(1)
mov=[180 for i in range(len(array))]
mov[7]=50
d.setMotors(mov)