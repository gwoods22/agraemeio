import random
heads=[]
tails=[]
loop = 0
while loop < 100:
    flip = random.randint(0,1)
    if flip == 1:
        heads.append('yay')
    else:
        tails.append('yay')
    loop+=1
print('There was {} heads and {} tails.'.format(len(heads),len(tails)))
