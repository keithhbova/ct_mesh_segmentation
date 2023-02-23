# OBJ Dataset Generator:

The purpose of this code is to provide a tool for segmenting .obj files generated from medical data. 

<img src="/assets/image_of_mesh_segmentation.png" alt="Alt text" title="Optional title">

The code in this repository is designed for use with:

### MedMeshCNN

https://github.com/LSnyd/MedMeshCNN

### And the blender part segmentation toolbox:

https://github.com/LSnyd/PartSegmentationToolbox

## Background

recursive_ct_converter.py iterates through the data folder and generates a folder of .stl files.

convert_stl_to_obj.py iterates through the results of recursive_ct_converter, and generates .obj files.

## Usage:

clone this repository. Create a "data" folder:

```bash
mkdir data
```

Place all dicom files in this folder.

NOTE: all dicom files for a patient should be placed in their own individual folder. 

<img src="/assets/image_of_input.png" alt="Alt text" title="Optional title">

Run the converter on the data:

```bash
python recursive_ct_converter.py
```

This will take some time. 

After it is complete, run the obj converter:

```bash
python convert_stl_to_obj.py
```

The results will save to a "ResultsObj" folder:

<img src="/assets/image_of_results.png" alt="Alt text" title="Optional title">

## Part Segmentation:

After the .obj files have been generated, they can be used for training a meshCNN model. 

Follow the instructions in this repository to label your own dataset:

https://github.com/LSnyd/PartSegmentationToolbox

...and the instructions in this repository to train an instance of meshCNN:

https://github.com/LSnyd/MedMeshCNN


## References:

The recursive_ct_converter uses a method outlined in Elyse Rier's master thesis: 

"3D MODELS OF BONE FROM CT IMAGES BASED ON 3D POINT CLOUDS"

The thesis can be found in the references folder.

All dicom files were provided by:

https://www.cancerimagingarchive.net/



