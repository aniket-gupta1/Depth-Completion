# CVPR Project Fall 2021


## Contents
1. [Introduction]
2. [Dependencies]
3. [Inference]


## Introduction
This project contains the code for the CVPR Fall 2021 project of Aniket Gupta (NUID: 002190453)

## Dependencies
1. Python 3.7
2. Pytorch 1.7.0+
3. KITTI depth completion dataset
4. KITTI stereo dataset

## Inference
Some data has been provided in the 'kitty_data_tiny' folder which contains raw RGB images as well as the Lidar depth maps

To test the model,

'''
chmod +x run_model.sh
./run_model.sh
'''

The output of the depth maps will be stored in the 'output_with_stereo_disparities' folder.
The data in the 'output_with_RGB' folder shows the output depth maps produced by the baseline network.


## Contact
gupta.anik@northeastern.edu