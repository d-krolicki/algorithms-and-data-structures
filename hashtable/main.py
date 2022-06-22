class Element:
    def __init__(self, value, key):
        self.value = value
        self.key = key

class hashTable:
    def __init__(self, size, c1:int=1, c2:int=0):
        self.size = size
        self.tab = [None for i in range(size)]
        if type(c1) != int or type(c2) != int:
            raise TypeError("c1 and c2 must be integers.")
        self.c1 = c1
        self.c2 = c2
    
    def __str__(self):
        temp = "{"
        for i in range(self.size):
            if self.tab[i]:
                temp += str(i) + " : " + str(self.tab[i].value) + " "
            else:
                temp += str(i) + " : " + str(self.tab[i]) + " "
        temp = temp.rstrip()
        temp += "}"
        return temp

    def hash(self, key):
        index = 0
        if type(key) == int:
            index = key % self.size
            return index
        elif type(key) == str:
            temp = 0
            for el in key:
                temp += ord(el)
            index = temp % self.size
            return index
        else:
            raise TypeError("In class hashTable, wrong data was passed to the hash() function - check for type concurrency.")
    

    def insert(self, arg:Element):
        index = self.hash(arg.key)
        if not self.tab[index]: #a.k.a. if self.tab[index] is None:
            self.tab[index] = arg
        else:
            if self.tab[index].key == arg.key:
                self.tab[index] = arg
            else:
                self.handle_collision(arg, index)
                # raise NotImplementedError("Solve the problem using open addressing method.")

    def handle_collision(self, arg:Element, index:int):
        i = 0
        while True:
            if index + i*self.c1 + (i**2)*self.c2 > self.size:
                # print(self)
                raise IndexError("Brak miejsca.")
                # print("IndexError: Brak miejsca.")
                # break
            if not self.tab[self.hash(index + i*self.c1 + (i**2)*self.c2)]:   #a.k.a. if self.tab[h(x) + c1*i + c2*i^2] is None:
                self.tab[self.hash(index + i*self.c1 + (i**2)*self.c2)] = arg
                break
            else:
                i += 1
    
    def remove(self, arg):
        index = hash(arg)
        try:
            if self.tab[index]:
                self.tab[index] = None
                print(self.tab[index])
            else:
                # print("ValueError: Brak danej.")
                raise ValueError("Brak danej.")
        except:
            raise ValueError("Wystąpił inny błąd - możliwe, że zakres tablicy został przekroczony.")
            # print("Brak danej lub wystąpił inny błąd.")

    def search(self, key):
        index = self.keychecker(self.hash(key), key)
        try:
            return self.tab[index].value
        except:
            return None

    def keychecker(self, key, index):
        keys_matched = False
        start = index
        checked_indices = set()
        try:
            for i in range(self.size):
                if self.tab[index] and self.tab[index].key == key:
                    keys_matched = True
                    break
                index = (start + self.c1 * i + self.c2 * i**2) % self.size
                if index in checked_indices:
                    return None, keys_matched
                checked_indices.add(index)
            return index
        except:
            # print("Wystąpił błąd przy sprawdzaniu klucza - możliwe, że nastąpiło wyjście poza zakres.")
            return None

def test_function_1(c1=1,c2=0):
    table = hashTable(13,c1,c2)
    keys = [1,2,3,4,5,18,31,6,7,8,9,10,11,12,13]
    values = "ABCDEFGHIJKLMNO"
    for i in range(len(keys)):
        table.insert(Element(values[i], keys[i]))
    
    print()
    print(table.search(5), '\n')
    print(table.search(14), '\n')

    table.insert(Element("Z", 5))
    print(table, '\n')

    table.remove(5)
    print(table, '\n')

    table.remove(table.hash("test"))    #aby wstawić element do pełnej tablicy, klucze muszą być zgodne albo trzeba zwolnić miejsce, albo powiększyć tablicę
    table.insert(Element("W", "test"))
    print(table)


def test_function_2(c1=1,c2=0):
    values = "ABCDEFGHIJKLMNO"
    keys = [13 * i for i in range(1, len(values)+1)]
    table = hashTable(13,c1,c2)
    for i in range(len(values)):
        table.insert(Element(values[i], keys[i]))
    print(table)

# test_function_1()

# test_function_2()

# test_function_1(0,1)

# test_function_2(0,1)