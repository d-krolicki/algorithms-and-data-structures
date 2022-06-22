# Python3 implementation of
# the above approach
 
''' A binary tree node has data, pointer
to left child and a pointer
to right child '''
class Node:
   
    def __init__(self, data):
       
        self.data = data
        self.left = None
        self.right = None
 
# Recursive function to find the
# parent of the given node
def findParent(node : Node,
               val : int,
               parent : int) -> None:
    if (node is None):
        return
 
    # If current node is
    # the required node
    if (node.data == val):
       
        # Print its parent
        print(parent)
    else:
       
        # Recursive calls
        # for the children
        # of the current node
        # Current node is now
        # the new parent
        findParent(node.left,
                   val, node.data)
        findParent(node.right,
                   val, node.data)
 
# Driver code
if __name__ == "__main__":
 
    root = Node(1)
    root.left = Node(2)
    root.right = Node(3)
    root.left.left = Node(4)
    root.left.right = Node(5)
    node = 3
    findParent(root, node, -1)