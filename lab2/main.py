#zadanie nie ukonczone

import copy

class BoundListElement:
    def __init__(self, data=None, next=None):
        self.data = data
        self.next = next

class BoundList:
    def __init__(self):
        self.head = None
        self.actual = self.head

    # def __str__(self):
    def destroy(self):
        self.head = None
    
    def add(self, arg):
        new_el = BoundListElement(arg)
        new_el.next = self.head #2 wskazuje na 3
        self.head = new_el

    def append(self, arg):
        new_el = BoundListElement(arg)
        if(self.head):
            actual = self.head
            while(actual.next):
                actual = actual.next
            actual.next = new_el
        else:
            self.head = new_el

    def remove(self):
        self.actual = self.head.next
        self.head = self.actual
        self.actual = self.head

    def pop_back(self):
        prev = self.head
        while prev.next.next:
            prev = prev.next
        prev.next = None
        
        
    def is_empty(self):
        if self.head:
            return False
        return True

    def length(self):
        ct = 1  #zaczynamy od 1 aby pozbyć się indeksowania od 0
        actual = self.head
        while(actual.next):
            ct += 1
            actual = actual.next
        return ct

    def get(self):
        return self.head.data

    def printlist(self):
        actual = self.head
        while(actual):
            print(actual.data)
            actual = actual.next



lst = BoundList()
lst.append(3)
lst.append(4)
# # lst.printlist()
# print('\n\n')
lst.add(2)
# lst.printlist()
# print('\n\n\n')
# lst.add(5)
lst.printlist()
print('----------------------------')
lst.pop_back()
lst.printlist()
# lst.remove()
# lst.printlist()
# lst.add(5)
# lst.append('abc')
# lst.printlist()
# lst.printlist()
# lst.remove()
# lst.printlist()
# print(lst.get())