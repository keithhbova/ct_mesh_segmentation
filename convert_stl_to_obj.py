import meshio
import os

def getListOfAllStlFilesFromDirectory(folderName:str = ""):
    listOfFiles = []

    for root, dirs, files in os.walk(folderName):
        for file in files:
            if(file.endswith(".stl")):
                currentFile = os.path.join(root,file)
                listOfFiles.append(currentFile)
    return listOfFiles


def main()->None:

    listOfStlFiles = getListOfAllStlFilesFromDirectory("Results")
    x:int = 0
    os.makedirs("ResultsObj", exist_ok = True)

    for stlFile in listOfStlFiles:
        mesh = meshio.read(stlFile)
        meshio.write(f'ResultsObj/new_mesh_{x}.obj', mesh, file_format='obj')
        x+=1

    return




if __name__ == '__main__':
    main()
