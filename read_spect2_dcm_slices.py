import numpy as np
import matplotlib.pyplot as plt
import os, glob
import pydicom
import pylab as pl
import sys
import matplotlib.path as mplPath

class IndexTracker(object):
    def __init__(self, ax, X):
        self.ax = ax
        ax.set_title('Scroll to Navigate through the DICOM Image Slices')

        self.X = X
        rows, cols, self.slices = X.shape
        self.ind = self.slices//2

        self.im = ax.imshow(self.X[:, :, self.ind])
        self.update()

    def onscroll(self, event):
        print("%s %s" % (event.button, event.step))
        if event.button == 'up':
            self.ind = (self.ind + 1) % self.slices
        else:
            self.ind = (self.ind - 1) % self.slices
        self.update()

    def update(self):
        self.im.set_data(self.X[:, :, self.ind])
        ax.set_ylabel('Slice Number: %s' % self.ind)
        self.im.axes.figure.canvas.draw()

fig, ax = plt.subplots(1,1)

#os.system("tree C:/Users/Dicom_ROI")

plots = []

for f in glob.glob("stress-sax*.dcm"):
    pass
    filename = f.split("/")[-1]
    ds = pydicom.dcmread(filename)
    pix = ds.pixel_array
    pix = pix*1+(-1024)
    plots.append(pix)

y = np.dstack(plots)

tracker = IndexTracker(ax, y)

fig.canvas.mpl_connect('scroll_event', tracker.onscroll)
plt.show()