casinos = int(input("How many casino's did you go to? "))

cash = 0
while casinos > 0:
    casinos-=1
    cash+=1
    cash = cash*2
    cash+=1

print(cash)
