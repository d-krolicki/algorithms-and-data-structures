lst = [[1,2,3],[4,5,6],[7,8,9]]
conv = []
for it in lst:
    temp = [str(el) for el in it]
    conv.append(temp)
    temp = []
print(conv)