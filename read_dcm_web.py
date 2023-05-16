import pydicom
from matplotlib import pyplot as plt
from io import BytesIO
from PIL import Image
import threading
from flask import Flask, Response, render_template
import numpy as np
import os

app = Flask(__name__)


def dicom_to_web_image(file_path):
    if os.path.exists(file_path):
    
        # Load the DICOM file
        dicom_file = pydicom.dcmread(file_path)


        # Get the raw pixel data from the DICOM file
        # Set to float to prevent under or overflow losses if an Integer
        pixels = dicom_file.pixel_array.astype(float)

        # Scale the image with values between 0 and 255
        scaled_image = (np.maximum(pixels, 0) / pixels.max()) * 255.0

        scaled_image = np.uint8(scaled_image)
        final_image = Image.fromarray(scaled_image, 'RGB')

        final_image.save(os.path.join("static", file_path + ".png"))
        

    else:
        print(file_path + " does not exist")

    # Create a Matplotlib figure with the image
    #fig = plt.figure(frameon=False)
    #plt.imshow(pixels, cmap='gray')
    #plt.axis('off')
    #plt.show()

    # Save the Matplotlib figure to a bytes buffer
    #buf = BytesIO()
    #fig.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
    #buf.seek(0)

    # Open the bytes buffer as a PIL Image object
    #img = Image.open(buf)

    #print(file_path)
    #img.save(file_path + ".png")

    # Return the raw PNG image data as a byte string
    #return img.tobytes()



@app.route('/')
def display_dicom():
    #file_path = 'stress-raw-static.dcm'
    file_path = 'stress-sax-gated.dcm'
    dicom_to_web_image(file_path)
    return render_template("index.html", dicom_image = file_path + ".png")

if __name__ == '__main__':
    app.run(debug=True)