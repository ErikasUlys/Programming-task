import laspy
import numpy as np
import pptk
import os
from Octree import Octree

#Reads the .las file
def read_las(file_path):
    las = laspy.read(file_path)
    return las

#Extracts point coordinates from the data mass
def extract_points(las_data):
    return np.vstack((las_data.x, las_data.y, las_data.z)).transpose()

def main():
    absolute_path = os.path.dirname(__file__)
    relative_path = "..\Data\dataset.las"
    full_path = os.path.join(absolute_path, relative_path)
    
    CENTER = (2743500, 1234500, 2150)
    STARTING_SIZE = 1000
    DEPTH = 2

    point_cloud = read_las(full_path)
    points = extract_points(point_cloud)
    tree = Octree(STARTING_SIZE, CENTER, DEPTH)
    
    #Saves all the point to octree
    for point in points:
        tree.insertNode(point, point)

    #Collects all the points in octree to display them    
    newPoints = []
    for node in tree.iterateDepthFirst():
        for point in node.point:
            newPoints.append(point)
    v = pptk.viewer(newPoints)

    #Creates 5 points around the center of the graphical representation
    #so that the camera would circle aroud
    poses = []
    for i in range(0, 5):
        poses.append([CENTER[0], CENTER[1], CENTER[2], i * np.pi/2, np.pi/4, 2000])
    v.play(poses, 4 * np.arange(5), repeat=True, interp='linear')

    input("Press Enter to continue...")

main()












