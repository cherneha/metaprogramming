class Node:
    def __init__(self, data):
        self.left = None
        self.right = None
        self.data = data


class Tree:

    a = 8
    b = 10

    def __init__(self):
        self.root = None

    def insert(self, root, data):

        if self.root == None:
            self.root = Node(data)

        elif root == None:
            root = Node(data)

        else:
            if data <= root.data:
                root.left = self.insert(root.left, data)

            elif data > root.data:
                root.right = self.insert(root.right, data)

        return root

    def inorder(self, root):
        if root == None:
            return
        self.inorder(root.left)
        print (root.data)
        self.inorder(root.right)


