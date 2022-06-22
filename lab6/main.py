#zadanie ukończone po terminie

import copy


class pQueueNode:


    def __init__(self, priority, data):
        self.priority = priority
        self.data = data


    def __str__(self):
        return f"{self.priority}:{self.data}"
    

    def __lt__(self, other):
        if self.priority < other.priority:
            return True
        return False
    

    def __gt__(self, other):
        if self.priority > other.priority:
            return True
        return False



class pQueue:


    def __init__(self, maxsize=1):
        self.max_size = maxsize
        self.current_size = 0
        self.tab = [None for _ in range(self.max_size)]
    

    def is_empty(self):
        if self.tab[0] is None:
            return True
        return False


    def check_size(self):
        if self.current_size >= self.max_size:
            self.tab = self.tab + [None for _ in range(len(self.tab))]
            self.max_size = self.max_size * 2
        elif self.current_size < self.max_size/2:
            self.tab = self.tab[:self.current_size+1]
            self.max_size = self.max_size/2
        return self

    
    def left(self, index):
        new_index = 2*index + 1
        if new_index > self.max_size-1:
            # print("left() returned None.")
            return None
        return new_index


    def right(self, index):
        new_index = 2*index + 2
        if new_index > self.max_size-1:
            # print("right() returned None.")
            return None
        return new_index


    def parent(self,index):
        if index % 2 == 1:  #indeksy nieparzyste
            new_index = index//2
            if new_index <= 0:
                return 0
            return new_index
        else:   #indeksy parzyste
            new_index = index//2 - 1
            if new_index <= 0:
                return 0
            return new_index

    
    def swap(self, first, last):
        self.tab[first], self.tab[last] = self.tab[last], self.tab[first]
        return self


    def peek(self):
        return copy.deepcopy(self.tab[0].data)


    def enqueue(self, node):
        if type(node) != pQueueNode:
            raise ValueError("Only pQueueNode object can be inserted into pQueue object.")

        self.tab[self.current_size] = node

        temp = self.current_size 
        par = self.parent(temp)
        
        while True:
            if self.tab[temp] > self.tab[par]:
                self.swap(temp, par)
            else:
                break
            temp = par
            par = self.parent(temp)

        self.current_size += 1
        self.check_size()
        return self


    def dequeue(self):
        if self.is_empty():
            return None
        temp = copy.deepcopy(self.tab[0])
        self.tab = self.tab[1:]
        self.tab.append(None)
        self.current_size -= 1
        self.check_size()
        return temp.data


    def print_tab(self):
        print ('{', end=' ')
        for i in range(self.current_size-1):
            print(self.tab[i], end = ', ')
        if self.tab[self.current_size-1]: 
            print(self.tab[self.current_size-1] , end = ' ')
        print( '}')


    def print_tree(self, idx, lvl):
        if idx<self.current_size:        
            try:   
                self.print_tree(self.right(idx), lvl+1)
            except:
                pass
            print(2*lvl*'  ', self.tab[idx] if self.tab[idx] else None)
            try:           
                self.print_tree(self.left(idx), lvl+1)
            except:
                pass


def test1():
    pQ = pQueue()
    prios = [4, 7, 6, 7, 5, 2, 2, 1]
    datas = "ALGORYTM"
    for i in range(len(prios)):
        # print(f"Inserting: Node({prios[i]},{datas[i]})")
        pQ.enqueue(pQueueNode(prios[i], datas[i]))
    # print(pQ.tab)
    pQ.print_tree(0,0)
    pQ.print_tab()
    print(pQ.dequeue())
    print(pQ.peek())
    pQ.print_tab()
    while not pQ.is_empty():
        print(pQ.dequeue())
    pQ.print_tab()
test1()