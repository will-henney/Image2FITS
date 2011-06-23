"""
image2fits.py - Convert an RGB image to 3 FITS channels

Author: William Henney 
Version 0.1 - 07 Apr 2011
"""

import numpy
import pyfits
from PIL import Image
import argparse

parser = argparse.ArgumentParser(description="Convert an RGB image to 3 FITS channels")
parser.add_argument("file", type=open,  help='RGB image file to convert')
args = parser.parse_args()

rgbim = Image.open(args.file)           # read the image
assert rgbim.mode == 'RGB', "File %s is not an RGB image" % (args.file)
a = numpy.array(rgbim)                  # convert to array
r, g, b = [a[::-1,:,i] for i in 0, 1, 2]   # split out the channels, flipping the y-axis

filestem = args.file.name.split('.')[0] 

# Write each channel to a FITS file: XXX-red.fits, XXX-green.fits, XXX-blue.fits
for chan, id in zip([r, g, b], ["red", "green", "blue"]):
    hdu =  pyfits.PrimaryHDU(chan)
    # Use the OBJECT keyword to describe this channel
    hdu.header.update('OBJECT', "%s channel of %s" % (id, args.file.name))
    hdu.header.add_comment("Written by image2fits.py, Will Henney 2011")
    # 
    hdu.writeto("%s-%s.fits" % (filestem, id), clobber=True)



