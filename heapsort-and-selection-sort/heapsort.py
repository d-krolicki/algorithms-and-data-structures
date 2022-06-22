# zadanie ukończone

import copy
import random
import time
class pQueueNode:


    def __init__(self, priority, data):
        self.priority = priority
        self.data = data


    def __str__(self):
        return "{}:{}".format(self.priority, self.data)
    

    def __lt__(self, other):
        if self.priority < other.priority:
            return True
        return False
    

    def __gt__(self, other):
        if self.priority > other.priority:
            return True
        return False



class pQueue:


    def __init__(self, maxsize=1, u_data=None):
        self.max_size = maxsize
        self.current_size = 0
        self.tab = [None for _ in range(self.max_size)]
        self.u_data = u_data
        if self.u_data:
            self.h_size = len(self.u_data)
    

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
        if new_index > self.h_size-1:
            # print("left() returned None.")
            return None
        return new_index


    def right(self, index):
        new_index = 2*index + 2
        if new_index > self.h_size-1:
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

    def h_swap(self, first, last):
        self.u_data[first], self.u_data[last] = self.u_data[last], self.u_data[first]
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
        for i in range(self.h_size-1):
            print(self.u_data[i], end = ', ')
        if self.u_data[self.h_size-1]: 
            print(self.u_data[self.h_size-1] , end = ' ')
        print( '}')


    def print_tree(self, idx, lvl):
        if idx<self.h_size:        
            try:   
                self.print_tree(self.right(idx), lvl+1)
            except:
                pass
            print(2*lvl*'  ', self.u_data[idx] if self.u_data[idx] else None)
            try:           
                self.print_tree(self.left(idx), lvl+1)
            except:
                pass

    def heapify(self, n, i):
        """
        Heapify an array.\n
        i - index of the root
        """
        root = i    # index of the root
        left = 2 * i + 1    # left child
        right = 2 * i + 2   # right child

        if left < n and self.u_data[left].priority > self.u_data[root].priority:
            root = left
        if right < n and self.u_data[right].priority > self.u_data[root].priority:
            root = right
        if root != i:
            self.h_swap(i, root)
            self.heapify(n, root)
        return self
    
    def build_heap(self):
        n = len(self.u_data)
        for i in range(n//2-1, -1, -1):
            self.heapify(n, i)
        return self
        
    def heap_sort(self):
        n = len(self.u_data)

        for i in range(n-1, -1, -1):
            self.h_swap(0, i)
            self.heapify(i, 0)
        return self

    def selection_sort_swap(self):
        for i in range(self.h_size-1):
            minValIndex = i
            for j in range(i+1, self.h_size):
                if self.u_data[j].priority < self.u_data[minValIndex].priority:
                    minValIndex = j
            if minValIndex != i:
                self.h_swap(i, minValIndex)
        return self
        
    def selection_sort_shift(self):
        for i in range(self.h_size-1):
            minValIndex = i
            for j in range(i+1, self.h_size):
                if self.u_data[j].priority < self.u_data[minValIndex].priority:
                    minValIndex = j
            if minValIndex != i:
                # self.h_swap(i, minValIndex)
                self.u_data.insert(i, self.u_data.pop(minValIndex))
        return self

lst = [random.randint(0,99) for _ in range(10000)]
lst2 = [random.randint(0,1000   ) for _ in range(10000)]

def test():
    lstt = [5,5,7,2,5,1,7,5,1,2]
    keys = "ABCDEFGHIJ"
    lst_v = [pQueueNode(lstt[i], keys[i]) for i in range(len(lst))]
    pQ = pQueue(u_data=lst_v)
    pQ.build_heap()
    pQ.print_tab()
    pQ.print_tree(0,0)
    pQ.heap_sort()
    pQ.print_tab()
    """
    Sortowanie nie jest stabilne, kolejność elementów zmienia się.
    """

def test2():
    # lst = [random.randint(0,99) for _ in range(10000)]
    keys = "A"*10000
    lst_v = [pQueueNode(lst[i], keys[i]) for i in range(len(lst))]
    pQ = pQueue(u_data=lst_v)
    t_start = time.perf_counter()
    pQ.build_heap()
    pQ.heap_sort()
    t_stop = time.perf_counter()
    print(f"Czas obliczeń dla metody heap sort: {t_stop-t_start:.7f}")
    return t_stop-t_start

def test3():
    lstt = [5,5,7,2,5,1,7,5,1,2]
    keys = "ABCDEFGHIJ"
    lst_v = [pQueueNode(lstt[i], keys[i]) for i in range(len(lst))]
    pQ = pQueue(u_data=lst_v)
    pQ.selection_sort_shift()
    pQ.print_tab()

def test4():
    # lst = [random.randint(0,99, seed=42) for _ in range(10000)]
    keys = "A"*10000
    lst_v = [pQueueNode(lst2[i], keys[i]) for i in range(len(lst))]
    pQ = pQueue(u_data=lst_v)
    t_start = time.perf_counter()
    pQ.selection_sort_swap()
    t_stop = time.perf_counter()
    print(f"Czas obliczeń dla metody selection sort - swap: {t_stop-t_start:.7f}")
    return t_stop-t_start

def test5():
    # lst = [random.randint(0,99]) for _ in range(10000)]
    keys = "A"*10000
    lst_v = [pQueueNode(lst2[i], keys[i]) for i in range(len(lst))]
    pQ = pQueue(u_data=lst_v)
    t_start = time.perf_counter()
    pQ.selection_sort_shift()
    t_stop = time.perf_counter()
    print(f"Czas obliczeń dla metody selection sort - shift: {t_stop-t_start:.7f}")
    return t_stop-t_start

def test6():
    # lst = [random.randint(0,99) for _ in range(10000)]
    keys = "A"*10000
    lst_v = [pQueueNode(lst2[i], keys[i]) for i in range(len(lst))]
    pQ = pQueue(u_data=lst_v)
    t_start = time.perf_counter()
    pQ.build_heap()
    pQ.heap_sort()
    t_stop = time.perf_counter()
    print(f"Czas obliczeń dla metody heap sort: {t_stop-t_start:.7f}")
    return t_stop-t_start

# test()
heap_time_0_99 = test2() #heapsort 0-99
# test3()
swap_time = test4() #swap
shift_time = test5() #shift
heap_time_0_1000 = test6()  #heapsort 0-1000

print(f"Metoda heapsort posortowała listę {int(swap_time/heap_time_0_1000)} razy szybciej niż selection sort - swap.")
print(f"Metoda heapsort posortowała listę {int(shift_time/heap_time_0_1000)} razy szybciej niż selection sort - shift.")