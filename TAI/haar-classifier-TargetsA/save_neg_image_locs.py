##################################################################
## MODULES
##################################################################
import os
import cv2
import numpy as np
import urllib.request

from PIL import Image

## useful resources:
## https://pythonprogramming.net/haar-cascade-object-detection-python-opencv-tutorial/

##################################################################
## PREPARE TERMINAL/CODE
##################################################################
os.system('clear') # clear terminal window

##################################################################
## FUNCTIONS
##################################################################
def createFilePath(names):
    ''' creatFilePath
    PURPOSE / OUTPUT:
        Turn an ordered list of names and concatinate them into a filepath.
    '''
    return ('/'.join([x for x in names if x != ''])).replace('//', '/')

##################################################################
## CREATING SET OF DISTORTED IMAGES
##################################################################
## home directory of data
base_filepath = os.path.dirname(os.path.realpath(__file__))
## list of subfolders where each simulation's data is stored
folder_name = 'negative-images'

## filepath to the current target images
tmp_filepath_name = createFilePath([base_filepath, folder_name]).replace('//', '/')
## list of sub-directories
sub_folder_names = [ f.path for f in os.scandir(tmp_filepath_name) if f.is_dir() ]
## number of negative images
num_images = sum([ len(files) for r, d, files in os.walk(tmp_filepath_name) ])
## print information to the console
print('In directory: \n\t' + tmp_filepath_name)
print('There are a total of ' + str(len(sub_folder_names)) + ' image folders.')
print('There are a total of ' + str(num_images) + ' images.')
# print('\n'.join(sub_folder_names))

## save filepath to negative images to file
num_images_used = 0
for sub_folder in sub_folder_names:
    for image_name in os.listdir(sub_folder):
        tmp_image = Image.open(sub_folder + '/' + image_name)
        width, height = tmp_image.size
        if ((width > 100) and (height > 100)):
            num_images_used += 1
            line = sub_folder + '/' + image_name + '\n'
            with open('bg.txt', 'a') as f:
                f.write(line)

print('A total of ' + str(num_images_used) + ' images were saved to bg.txt')
