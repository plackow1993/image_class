#making python file to extract pixel data and recreate image using said data.

from PIL import Image
import numpy as np
from datetime import datetime
import sys
import math
import os, glob


for filename in glob.glob('*.txt'):
    
    with open(filename) as f:
        lines = f.readlines()
    lines = lines[0][:]

    if 'n' in lines:
        lines = lines.replace('n', 'A')
    
    if 'n' in lines:
        print('failed')
    file_num = filename[0:2]

    ####### Loading in reference sequence
    #National Center for Biotechnology Information
    #National Library of Medicine
    #info@ncbi.nlm.nih.gov

    # with open('covid_ref.txt') as f:
    #     lines = f.readlines()
    # lines = lines[0][:-4]

    ##### Creation of sequence map ####
    #use a matrix of 230x(4*130) for the samples (cut off 3 repeated As at the end of ref_seq)

    #mapping letters to on/off switch A=0, T=1, C=2, G=3
    def mapping(A):
        input = ['A', 'T', 'C', 'G']
        y = input.index(A)
        return y
    
    act_seq = np.ndarray(shape = (230,130), dtype = int)
    
    counter = 0
    for n in range(0, act_seq.shape[0]):
        for m in range(0, act_seq.shape[1]):
            act_seq[n,m] = mapping(lines[counter])
            counter += 1



    if 4 in act_seq:
        print(file_num, np.count_nonzero(act_seq==4))
    
    ########################################


    #shade is a value that will remain intensity value. Shade = 255 is all white.
    shade = 255

    #way to create an array to use in image processing model
    a = np.random.randint(low=0,high=1, size = (230,520,3))
    #print(a)
    #need to come up with a way to selectively change intensity (black to white) for instances of 4 (ATCG) but keep things mostly the same. So randomize for sections of images.
    #maybe 255*1 for 100% certainty of ATCG and randomize intensities under 200.
    count = 0
    counter = 0

    ##original version to create random image
    #for m in a:
    #    for n in m:
    #        #on off switch for creation of an image
    #        if counter % 4 == 0:
    #            switch = rng.integers(low=0, high=4, size = 1)
    #        if counter % 4 == switch:
    #            a[count,counter,:]=np.add([shade, shade, shade],n)
    #        counter += 1
    #    count += 1
    #    counter = 0
        
        
        
    #new version to create pseudoimage. Create a nxm/4 matrix of sequences, where A=0, T=1, C=2, G=3.
    for m in a:
        for n in m:
            #on off switch for creation of an image
            counter2 = counter % 4
            switch = act_seq[count, math.floor(counter/4)]
            if counter2 == switch:
                a[count,counter,:]=np.add([shade, shade, shade],n)
            counter += 1
        count += 1
        counter = 0


    #need to make an artificial image coordinate map into a convertible unit8 format
    a=a.astype(np.uint8)

    #way to create image from an array
    new_image = Image.fromarray(a)
    #new_image.show()

    new_image.save("actual{}_heatmap.png".format(file_num))



