##################################################################
## MODULES
##################################################################
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

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

def createFolder(folder_name):
    ''' createFolder
    PURPOSE:
        Create the folder passed as a filepath to inside the folder.
    OUTPUT:
        Commandline output of the success/failure status of creating the folder.
    '''
    if not(os.path.exists(folder_name)):
        os.makedirs(folder_name)
        print('SUCCESS: Folder created. \n\t' + folder_name)
        print(' ')
    else:
        print('WARNING: Folder already exists (folder not created). \n\t' + folder_name)
        print(' ')

def meetCondition(element):
    global target_name
    if element.__contains__(target_name) and element.endswith('.jpg'):
        return True
    return False

##################################################################
## CLASSIFY PRACTICE IMAGES
##################################################################
global target_name
## home directory of data
base_filepath = os.path.dirname(os.path.realpath(__file__))
## list of subfolders where each simulation's data is stored
target_name = 'TargetA1'
target_folder_names = 'target-images'
filepath_target_folder = createFilePath([base_filepath, target_folder_names, target_name]).replace('//', '/')
## list of target images to classify
list_image_names = list(filter(meetCondition, sorted(os.listdir(filepath_target_folder))))
print('Classifting images in the directory: \n\t' + filepath_target_folder)
print('\t Total of ' + str(len(list_image_names)) + ' target images...')
print(' ')
## create directory where classified images will be saved
filepath_save_folder = createFilePath([base_filepath, 'classified-images', target_name]).replace('//', '/')
createFolder(filepath_save_folder)
## delete all previously classified images
[os.remove(createFilePath([filepath_save_folder, tmp_file])) for tmp_file in os.listdir(filepath_save_folder)]

## load cascade classifiers
target_cascade = cv2.CascadeClassifier('cascade_A1.xml')

## test the classifier on every image
print('Starting the classifier...')
for tmp_image in list_image_names:
    ## load image
    img_orig = cv2.imread(createFilePath([filepath_target_folder, tmp_image]))
    ## convert image to gray-scale
    gray = cv2.cvtColor(img_orig, cv2.COLOR_BGR2GRAY)
    ## search the image for targets
    targets = target_cascade.detectMultiScale(gray, 3, 3)
    ## indicate where a target has been found
    for (x, y, w, h) in targets:
        cv2.rectangle(img_orig, (x, y), (x+w, y+h), (255, 0, 0), 2)
    ## save image
    tmp_name = 'classified_' + tmp_image
    tmp_file_name = createFilePath([filepath_save_folder, tmp_name])
    cv2.imwrite(tmp_file_name, img_orig)
