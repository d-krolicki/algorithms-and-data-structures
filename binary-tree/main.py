class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None

    def insert(self, key, value):
        if self.key == key:
            self.value = value
            return

        if key < self.key:
            if self.left:
                self.left.insert(key, value)
                return
            self.left = Node(key, value)
            return
        
        if self.right:
            self.right.insert(key,value)
            return
        self.right = Node(key,value)

    def find_min_node(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    def delete(self, key):

        if self is None:
            return self

        elif key < self.key:
            if self.left:
                self.left = self.left.delete(key)
            return self

        elif key > self.key:
            if self.right:
                self.right = self.right.delete(key)
            return self

        elif self.right is None:
            return self.left

        elif self.left is None:
            return self.right

        successor = self.right

        while successor.left:
            successor = successor.left
        self.key = successor.key
        self.right = self.right.delete(successor.key)
        return self

    def find_min_key(self):
        current = self
        while current.left is not None:
            current = current.left
        return current.key

    def find_max_key(self):
        current = self
        while current.right is not None:
            current = current.right
        return current.key

    def search(self, key):
        try:
            if key == self.key:
                return self.value
            if key < self.key:
                return self.left.search(key)
            return self.right.search(key)
        except:
            return None
    
    def height(self, root):
        if root is None:
            return 0
        left_height = self.height(root.left)
        right_height = self.height(root.right)
        return max(left_height, right_height) + 1



class Tree:
    def __init__(self):
        self.root = None
    
    def make_root(self, node):
        if type(node) == Node:
            self.root = node
        else:
            raise TypeError("Inappropiate argument type passed to make_root() function.")

    def print_tree(self):
        print("==============")
        self._print_tree(self.root, 0)
        print("==============")

    def _print_tree(self, node, lvl):
        if node!=None:
            self._print_tree(node.right, lvl+5)

            print()
            print(lvl*" ", node.key, node.value)
     
            self._print_tree(node.left, lvl+5)
    

def inorder_traversal(root, path):
    if root:
        inorder_traversal(root.left, path)
        path.append((root.key, root.value))
        # print("{0} : {1}".format(root.key, root.value))
        inorder_traversal(root.right, path)
    return path

def test():
    tree = Tree()
    keys = [50,15,62,5,20,58,91,3,8,37,60,24]
    values = "ABCDEFGHIJKL"
    root = Node(keys[0], values[0])
    tree.make_root(root)
    for i in range(1,len(keys)):
        tree.root.insert(keys[i], values[i])
    
    tree.print_tree()
    print(inorder_traversal(root, []))
    print(root.search(24))
    root.insert(20, "AA")
    root.insert(6, "M")
    root.delete(62)
    root.insert(59, "N")
    root.insert(100, "P")
    root.delete(8)
    root.delete(15)
    root.insert(55, "R")
    root.delete(50)
    root.delete(5)
    root.delete(24)
    print(root.height(root))
    print(inorder_traversal(root, []))
    tree.print_tree()
test()