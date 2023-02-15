import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import threading
import pydicom
import numpy as np
import os
from skimage import feature
import pyvista as pv
import time
import scipy

def checkIfDcmFileIsCT(pathToDCMFile):
    if(pathToDCMFile):
        if(pathToDCMFile.endswith(".dcm")):
            slice = [pydicom.dcmread(pathToDCMFile)]
            if(str(slice[0]['SOPClassUID']).endswith("CT Image Storage")):
                return True
    return False

def getPathsToAllFilesWithExtension(folderName = "", extension = ".dcm"):
    listOfFiles = []

    for root, dirs, files in os.walk(folderName):
        for file in files:
            if(file.endswith(extension)):
                currentFile = os.path.join(root,file)
                listOfFiles.append(currentFile)
    return listOfFiles




def checkIfFolderContainsCTScans(folderName)->bool:
    for root, dirs, files in os.walk(folderName):
        for file in files:
            if(file.endswith(".dcm")):
                currentFile = os.path.join(root,file)
                currentFileIsACTScan:bool = checkIfDcmFileIsCT(currentFile)
                #print(f"{currentFile} is {currentFileIsACTScan}")
                if(not currentFileIsACTScan):
                    return False
    return True


def open_CT(file_path):
    slices = [pydicom.dcmread(file_path + '/' + s) for s in os.listdir(file_path)]

    slices.sort(key = lambda sl: int(sl.InstanceNumber))
    locations = np.stack([sl.SliceLocation for sl in slices])
    images = np.stack([sl.pixel_array for sl in slices])
    slope = slices[0].RescaleSlope
    intercept = slices[0].RescaleIntercept
    images = slope * images.astype(np.float64)
    images += intercept

    slice_thickness = slices[0].SliceThickness
    spacing_bw_rows = float(slices[0].PixelSpacing[0])
    spacing_bw_cols = float(slices[0].PixelSpacing[1])

    return images, slice_thickness, spacing_bw_rows, spacing_bw_cols, locations

def thresh_edge_CT(images,threshold):
    num_slices= images.shape[0]
    edges = images
    for i in range(num_slices):
        edges[i] = feature.canny(images[i]>threshold)
    return edges

def extract_PT_Cloud(edges,sl_thickness,row_spacing,col_spacing,locations):
    dimensions = edges.shape
    count =1
    for sl_num in range(dimensions[0]):
        for rows in range(dimensions[1]):
            for cols in range(dimensions[2]):
                if edges[sl_num][rows][cols] == 1:
                    if count==1:
                        point_cloud = np.array([float((float(cols) * col_spacing) - (col_spacing/2)), float((float(rows) * row_spacing) - (row_spacing/2)), float(locations[sl_num])])
                    else:
                        holder = np.array([float((float(cols) * col_spacing) - (col_spacing/2)), float((float(rows) * row_spacing)- (row_spacing/2)), float(locations[sl_num])])
                        point_cloud = np.vstack((point_cloud,holder))
                    count += 1
    return point_cloud


def create_mesh(point_cloud):
	tree= scipy.spatial.KDTree(point_cloud)
	dist, ind= tree.query(point_cloud,100)
	dist_new= dist[:,1:]
	averages= np.zeros((dist.shape[0],1))
	for i in range(dist.shape[0]):
		averages[i] = np.mean(dist[i])
	alph= np.mean(averages)
	pcd= pv.PolyData(point_cloud)
	print("poly data created")
	mesh= pcd.delaunay_3d(alpha=alph)
	print("delaunay created")
	return mesh,alph

def viewMesh(mesh):
	mesh.plot(show_edges=True)
	return

def save_mesh_stl(mesh,name):
	surf=mesh.extract_surface().clean()
	surf.save(name)
	return


def generateSTLFromFolderOfCTDicoms(fileDirectory = "", nameForSTLFileThisFunctionIsCreating:str = ""):
    if(not nameForSTLFileThisFunctionIsCreating):
        print("ERROR FUNCTION CALL NEEDS FILE NAME")
        exit()

    print(f"running elyse rier method for {nameForSTLFileThisFunctionIsCreating}")
    image_stack, sl_thickness, row_spacing, col_spacing , sl_locations = open_CT(fileDirectory)

    edge_image = thresh_edge_CT(image_stack,600)

    surface_points = extract_PT_Cloud(edge_image,sl_thickness,row_spacing,col_spacing,sl_locations )

    #plot_PT_Cloud(surface_points)

    mesh,alpha = create_mesh(surface_points)

    #viewMesh(mesh)

    save_mesh_stl(mesh, nameForSTLFileThisFunctionIsCreating)


    return

def main():
    fileDirectory = "data"

    listOfDirsThatContainCTScans = []

    os.makedirs("Results", exist_ok = True)

    for root, dirs, files in os.walk(fileDirectory):
        for dir in dirs:
            currentDir = os.path.join(root,dir)
            dirContainsCTScans:bool = checkIfFolderContainsCTScans(currentDir)
            if(dirContainsCTScans):
                listOfDirsThatContainCTScans.append(currentDir)

    print(listOfDirsThatContainCTScans)




    x:int = 0
    for folderThatContainsCTScans in listOfDirsThatContainCTScans:
        nameForSTLFile:str = f"Results/new_mesh_{x}.stl"
        try:
            generateSTLFromFolderOfCTDicoms(folderThatContainsCTScans,nameForSTLFile)
        except Exception as ex:
            print(ex)

        x+=1






    return



if __name__ == "__main__":
    main()
