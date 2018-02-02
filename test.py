test=[(1,2),(3,4),(5,6),(7,8)]
i=0
while i < len(test):
    print(i)
    if test[i][0]> 3:
        del test[i]
        i=i-1
    i +=1
print(test)