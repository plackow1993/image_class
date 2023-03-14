#making python file to extract pixel data and recreate image using said data.

from PIL import Image
import numpy as np
image = Image.open("letter.jpg")

box = (150, 40, 290, 220)
region = image.crop(box)

print(region)
#region.show()

#way to create an array to use in image processing model
a = np.asarray(image)

print(a.shape)
count = 0
counter = 0

for m in a:
    for n in m:
        a[count,counter,:]=np.subtract([255, 255, 255],n)
        counter += 1
    count += 1
    counter = 0
    
print(a)
#way to create image from an array
new_image = Image.fromarray(a)
new_image.show()

print(region.size)

#trying to manually invert an image
