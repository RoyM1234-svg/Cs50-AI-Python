import random
poss = ['random', 'best']
res = random.choices(poss,weights=[1,0],k=1)
print (res)
if res == ['random']:
    print("yes")