lst = [1,2,3]
def realloc(tab, size):
    oldSize = len(tab)
    return [tab[i] if i < oldSize else None for i in range(size)]

lst1 = realloc(lst, 6)
print(lst1)