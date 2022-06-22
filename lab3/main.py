from copy import *

def realloc(tab, size):
    oldSize = len(tab)
    return [tab[i] if i < oldSize else None for i in range(size)]

class Queue:
    def __init__(self):
        self.size = 5
        self.tab = [None for i in range(self.size)]
        self.write_index = 0
        self.read_index = 0
    
    # def __str__(self):
    #     return str([el for el in self.tab])   #

    def is_empty(self):
        if self.write_index == self.read_index and self.tab[self.read_index] is None:
            return True
        return False

    def peek(self):
        if self.is_empty():
            return None
        return self.tab[self.read_index]

    def dequeue(self):
        if self.is_empty():
            return None
        temp = deepcopy(self.tab[self.read_index])
        self.tab[self.read_index] = None
        self.read_index += 1
        if self.read_index > self.size - 1:
            self.read_index = 0
        return temp
    
    def enqueue(self, arg):
        self.tab[self.write_index] = arg

        if self.write_index == self.size - 1:
            self.write_index = 0
        else:
            self.write_index += 1

        if self.write_index == self.read_index:
            newSize = 2*self.size
            self.tab = realloc(self.tab, newSize)
            for i in range(self.size - self.read_index):
                self.tab[newSize - i - 1] = self.tab[self.size - i - 1]
                self.tab[self.read_index + i] = None
            self.read_index += self.size + 2
            self.size = len(self.tab)

    def get_queue(self):
        temp = []
        for el in self.tab[self.read_index:]:
            if el is not None:
                temp.append(el)
            else:
                continue
        for el in self.tab[:self.read_index]:
            if el is not None:
                temp.append(el)
            else:
                continue
        # print(temp)
        return temp
Q = Queue()

Q.enqueue(1)
Q.enqueue(2)
Q.enqueue(3)
Q.enqueue(4)

print("Usunięta wartość: ",Q.dequeue())

print("Peek:", Q.peek())

print("Kolejka: ", Q.get_queue())

Q.enqueue(5)
Q.enqueue(6)
Q.enqueue(7)
Q.enqueue(8)

print("Tablica: ", Q.tab)
while(Q.get_queue()):
    print("Usunięto: ",Q.dequeue())

print("Kolejka: ", Q.get_queue())

