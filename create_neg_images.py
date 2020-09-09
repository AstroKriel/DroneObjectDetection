##################################################################
## MODULES
##################################################################
import os
import cv2
import numpy as np
import urllib.request

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

def store_raw_images():
    neg_images_link = '/image-net.org/api/text/imagenet.synset.geturls?wnid=n00523513'   
    neg_image_urls = urllib.request.urlopen(neg_images_link).read().decode()
    pic_num = 1
    if not os.path.exists('neg'):
        os.makedirs('neg')
    for i in neg_image_urls.split('\n'):
        try:
            print(i)
            urllib.request.urlretrieve(i, "neg/"+str(pic_num)+".jpg")
            img = cv2.imread("neg/"+str(pic_num)+".jpg", cv2.IMREAD_GRAYSCALE)
            # should be larger than samples / pos pic (so we can place our image on it)
            resized_image = cv2.resize(img, (100, 100))
            cv2.imwrite("neg/"+str(pic_num)+".jpg",resized_image)
            pic_num += 1
            
        except Exception as e:
            print(str(e))  

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
    print('\t Total of ' + str(len(list_image_names)) + ' target images...')
    print('\t Creating ' + str(N) + ' distorted images...')
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
