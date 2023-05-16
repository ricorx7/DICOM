import numpy as np
import matplotlib.pyplot as plt
import os, glob
import pydicom
import pylab as pl
import sys
import matplotlib.path as mplPath
from matplotlib.animation import FuncAnimation

"""
Simple DICOM reader.  Read the DICOM file and display the data and images.
Display the slices as an animation.
"""
class DicomReader:

    def __init__(self, file_path) -> None:
        """
        If the file exists, read in the DICOM file.
        @param: File path to read the DICOM file
        """
        self.file_path = file_path

        self.fig, self.ax = plt.subplots(1,1)

        if os.path.exists(file_path):
            self.ds = pydicom.dcmread(file_path)
        else:
            print("File does not exist")

    def display_details(self) -> None:
        """
        Get all the details about the DICOM file.
        """
        # Normal mode:
        print()
        print(f"File path........: {self.file_path}")
        print(f"SOP Class........: {self.ds.SOPClassUID} ({self.ds.SOPClassUID.name})")
        print()

        pat_name = self.ds.PatientName
        print(f"Patient's Name...: {pat_name.family_comma_given()}")
        print(f"Patient ID.......: {self.ds.PatientID}")
        print(f"Modality.........: {self.ds.Modality}")
        print(f"Study Date.......: {self.ds.StudyDate}")
        print(f"Image size.......: {self.ds.Rows} x {self.ds.Columns}")
        print(f"Pixel Spacing....: {self.ds.PixelSpacing}")

        # use .get() if not sure the item exists, and want a default value if missing
        print(f"Slice location...: {self.ds.get('SliceLocation', '(missing)')}")

    def display_image(self, indice: int = -1) -> None:
        """
        Display an slice from the DICOM image.  If no indice is given,
        then the middle slice is chosen.
        @param indice: Which slice to display.
        """
        # Validate the indice
        # Select the middle indice if none is given or if bad
        if indice < 0 or indice > self.ds.pixel_array.shape[2]:
            indice = self.ds.pixel_array.shape[2] // 2

        pix = self.ds.pixel_array
        pix = pix*1+(-1024)
        self.ax.set_title(self.file_path)
        self.ax.set_ylabel('Slice Number: %s' % indice)
        plt.imshow(pix[:, :, indice])
        plt.show()

    def animate_slices(self) -> None:
        """
        Make an animation of all the slices.
        This will play through all the availables slices.
        """

        # Initialize the image
        img = self.ax.imshow(self.ds.pixel_array[:, :, 0])
        self.ax.set_title(self.file_path)
        self.ax.set_ylabel('Slice Number: %s' % 0)

        # Call the matplotlib animation fuction 
        # to call animate to display all the slices
        ani = FuncAnimation(self.fig, self.animate, frames=self.ds.pixel_array.shape[2], interval=100, repeat=False)

        # Display the animate plot
        plt.show()

    def animate(self, ind):
        """
        Call this function the image function to display
        the next indice in the slices of images.

        @param ind: Indice to display.
        """
        self.ax.imshow(self.ds.pixel_array[:, :, ind])
        self.ax.set_ylabel('Slice Number: %s' % ind)


if __name__ == "__main__":
    for f in glob.glob("stress-*.dcm"):
        filename = f.split("/")[-1]

        dicom_reader = DicomReader(filename)
        dicom_reader.display_details()
        #dicom_reader.display_image()
        dicom_reader.animate_slices()

