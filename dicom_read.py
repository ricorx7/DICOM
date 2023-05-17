import numpy as np
import matplotlib.pyplot as plt
import os, glob
import pydicom
import pylab as pl
import sys
import matplotlib.path as mplPath
from matplotlib.animation import FuncAnimation, FFMpegWriter

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

        self.fig = None
        self.ax = None

        if os.path.exists(file_path):
            self.ds = pydicom.dcmread(file_path)
        else:
            print("File does not exist")

    def init_figure(self) -> None:
        """
        Initialize the figure and axis.
        Check if it has already been initialized.
        """
        if self.fig is None or self.ax is None:
            self.fig, self.ax = plt.subplots(1,1)

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
        # Init figure
        self.init_figure()

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

    def animate_slices(self, save_to_mp4: bool = False, save_to_html5: bool = False) -> None:
        """
        Make an animation of all the slices.
        This will play through all the availables slices.

        @param: save_to_mp4: Save the video to MP4 video format if True.
        @param: save_to_html5: Save the video to HTML5 video format if True.
        """

        # Init figure
        self.init_figure()

        # Initialize the image
        img = self.ax.imshow(self.ds.pixel_array[:, :, 0])
        self.ax.set_title(self.file_path)
        self.ax.set_ylabel('Slice Number: %s' % 0)

        # Call the matplotlib animation fuction 
        # to call animate to display all the slices
        anim = FuncAnimation(self.fig, self.animate, frames=self.ds.pixel_array.shape[2], interval=100, repeat=False)

        if save_to_mp4:
            # saving to m4 using ffmpeg writer
            writervideo = FFMpegWriter(fps=6)
            anim.save(self.file_path + '.mp4', writer=writervideo)
            plt.close()

        if save_to_html5:
            # converting to an html5 video
            video = anim.to_html5_video()
            print(video)
            plt.close()

        if not save_to_mp4 and not save_to_html5:
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
        #dicom_reader.animate_slices(save_to_mp3=True)
        dicom_reader.animate_slices(save_to_html5=True)

