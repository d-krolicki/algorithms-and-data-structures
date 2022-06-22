class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None


class Tree:
    def __init__(self):
        self.root = None
    
    def make_root(self, node):
        if type(node) == Node:
            self.root = node
        else:
            raise TypeError('Inappropiate argument passed to make_root() function.')
    
    
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


def insert(root, key, value):
    if key == root.key:
        root.value = value
    
    if key < root.key:
        if root.left:
            return insert(root.left, key, value)
        else:
            root.left = Node(key, value)
            return root

    if root.right:
        return insert(root.right, key, value)
    else:
        root.right = Node(key, value)
        return root


def search(root, key):
    try:
        if key == root.key:
            return root.value
        elif key < root.key:
            return search(root.left, key)
        elif key > root.key:
            return search(root.right, key)
    except:
        return None


def find_min_key(root):
    if root.left:
        return find_min_key(root.left)
    return root.key


def find_max_key(root):
    if root.right:
        return find_max_key(root.right)
    return root.key


def find_min_node(root):
    if root.left:
        return find_min_node(root.left)
    return root


def inorder_successor(root, key):
    if root.right is not None:
        return find_min_node(root)
    while root:
        if root.key < key:
            root = root.right
        elif root.key > key:
            successor = root
            root = root.left
        else:
            break
    return successor

def delete(root, key):
    

def test():
    tree = Tree()
    keys = [50,15,62,5,20,58,91,3,8,37,60,24]
    values = "ABCDEFGHIJKL"
    root = Node(keys[0], values[0])
    tree.make_root(root)
    for i in range(1,len(keys)):
        root = insert(root, keys[i], values[i])
    tree.print_tree()
test()