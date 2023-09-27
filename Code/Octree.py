import numpy as np
from OctNode import OctNode

class Octree(object):
    #Initializes starting octree cube
    def __init__(self, squareSize, origin, max_value=10):
        self.root = OctNode(origin, squareSize, 0, [])
        self.squareSize = squareSize
        self.limit = max_value

    #Creates new cube
    @staticmethod
    def CreateNode(position, size, objects):
        return OctNode(position, size, objects)

    #Inserts given point into the octree
    def insertNode(self, position, point=None):
        if np.any(position < self.root.bottomFrontLeft):
            return None
        if np.any(position > self.root.topBackRight):
            return None
        
        if point is None:
            point = position

        return self.__insertNode(self.root, self.root.size, self.root, position, point)

    #Private method to insert point into correct node
    def __insertNode(self, root, size, parent, position, point):
        if root is None:
            pos = parent.position

            offset = size / 2

            branch = self.__findBranch(parent, position)

            newCenter = (0, 0, 0)

            if branch == 0:
                newCenter = (pos[0] - offset, pos[1] - offset, pos[2] - offset )
            elif branch == 1:
                newCenter = (pos[0] - offset, pos[1] - offset, pos[2] + offset )
            elif branch == 2:
                newCenter = (pos[0] - offset, pos[1] + offset, pos[2] - offset )
            elif branch == 3:
                newCenter = (pos[0] - offset, pos[1] + offset, pos[2] + offset )
            elif branch == 4:
                newCenter = (pos[0] + offset, pos[1] - offset, pos[2] - offset )
            elif branch == 5:
                newCenter = (pos[0] + offset, pos[1] - offset, pos[2] + offset )
            elif branch == 6:
                newCenter = (pos[0] + offset, pos[1] + offset, pos[2] - offset )
            elif branch == 7:
                newCenter = (pos[0] + offset, pos[1] + offset, pos[2] + offset )

            if (self.__isInSphere(newCenter, point, offset)):
                return OctNode(newCenter, size, parent.depth + 1, [point])
        elif ( not root.isLeafNode and (np.any(root.position != position) or (root.position != position))):
            branch = self.__findBranch(root, position)
            offset = root.size / 2
            root.branches[branch] = self.__insertNode(root.branches[branch], offset, root, position, point)
        elif root.isLeafNode:
            if root.depth >= self.limit:
                if self.__isInSphere(root.position, point, size/2):
                    root.point.append(point)
            else:
                root.point.append(point)
                objList = root.point
                root.point = None
                root.isLeafNode = False
                
                newSize = root.size / 2
                
                for obj in objList:
                    if hasattr(obj, "position"):
                        pos = obj.position
                    else:
                        pos = obj
                    branch = self.__findBranch(root, pos)
                    root.branches[branch] = self.__insertNode(root.branches[branch], newSize, root, pos, obj)
        return root

    #Private method to find the branch in which the given position is/should be
    #branch index corresponds to number 0-7 depending on signs of the coordinates
    #     0 1 2 3 4 5 6 7
    #  x| - - - - + + + +
    #  y| - - + + - - + +
    #  z| - + - + - + - +
    @staticmethod
    def __findBranch(root, position):
        index = 0
        if (position[0] >= root.position[0]):
            index |= 4
        if (position[1] >= root.position[1]):
            index |= 2
        if (position[2] >= root.position[2]):
            index |= 1
        return index

    #Iterates through all the nodes
    def iterateDepthFirst(self):
        gen = self.__iterateDepthFirst(self.root)
        for n in gen:
            yield n

    #Private method to iterate octree nodes
    @staticmethod
    def __iterateDepthFirst(root):
        for branch in root.branches:
            if branch is None:
                continue
            for n in Octree.__iterateDepthFirst(branch):
                yield n
            if branch.isLeafNode:
                yield branch
    
    #Checks if the point is in the sphere
    @staticmethod
    def __isInSphere(point1, point2, radius): 
        dist = np.linalg.norm(point1 - point2)
        return radius >= dist
