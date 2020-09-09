#!/usr/bin/env python3

##################################################################
## MODULES
##################################################################
import os
import cv2
import numpy as np

from imgaug import augmenters as iaa

## useful resources:
## https://github.com/aleju/imgaug

##################################################################
## PREPARE TERMINAL/CODE
##################################################################
os.system('clear') # clear terminal window

##################################################################
## FUNCTIONS
##################################################################
def meetCondition(element):
    if element.endswith('.jpg') and not(element.__contains__('aug')):
            return True
    return False

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
sub_folder_names = ['training-images/TargetA1', 'training-images/TargetA2']
## number of copies of image to make with augemntations
N = 5
## should previous agumented images be deleted?
bool_aug_delete = 1

## define distortions to apply
seq = iaa.Sequential([
    iaa.MotionBlur(k=[3, 10], angle=[-45, 45]), # apply motion blur
    iaa.Affine(rotate=(-45, 45)),               # rotate the image
    iaa.AdditiveGaussianNoise(scale=(5, 10))    # introduce gaussian noise
], random_order=True)                           # apply distortions in a random order

## for each target folder
for i in range(len(sub_folder_names)):
    print('Looking at folder: ' + sub_folder_names[i])
    ## filepath to the current target images
    tmp_filepath_name = createFilePath([base_filepath, sub_folder_names[i]]).replace('//', '/')
    ## delete previously made augmented images
    if bool_aug_delete:
        print('\t Removing old augmented images...')
        [os.remove(createFilePath([tmp_filepath_name, tmp_file])) for tmp_file in os.listdir(tmp_filepath_name) if tmp_file.__contains__('aug')]
        print(' ')
    ## list of target images to apply augmentations to
    list_image_names = list(filter(meetCondition, sorted(os.listdir(tmp_filepath_name))))
    ## for each target image
    for j in range(len(list_image_names)):
        print('\t Applying distortions to: ' + list_image_names[j])
        for k in range(N):
            ## load image
            image_orig = cv2.imread(createFilePath([tmp_filepath_name, list_image_names[j]]))
            ## apply distortion to image
            image_aug = seq(image=image_orig)
            ## save image
            tmp_name = list_image_names[j].split('.jpg')[0] + '_aug_' + str(k) + '.jpg'
            tmp_file_name = createFilePath([base_filepath, sub_folder_names[i], tmp_name])
            cv2.imwrite(tmp_file_name, image_aug)
    ## look at the next folder
    print(' ')
