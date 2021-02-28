class OpBinary:
    """docstring for ClassName"""
    def __init__(self,type,left,right,operator):
        self.type="opbin"
        self.left=left
        self.right=right
        self.operator=operator

class Tree:
    def __init__(self,type,children=None,leaf = None,count = 0):
        self.type = type
        self.children=children
        self.leaf = leaf
        self.count = count

    def __str__(self):
        if self.children is not None:
            for x in  self.children:
                print(x)
            print(self.leaf)                                        
        return self.type


            
            