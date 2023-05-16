import pydicom as dicom
import matplotlib.pylab as plt
import cv2

# specify your image path
image_path = 'stress-sax-gated.dcm'
ds = dicom.dcmread(image_path)

pixel_array_numpy = ds.pixel_array

#plt.imshow(ds.pixel_array)

image_format = '.jpg' # or '.png'
image_path = image_path.replace('.dcm', image_format)

cv2.imwrite(image_path, pixel_array_numpy)