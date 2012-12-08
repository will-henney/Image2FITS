"""
image2fits.py - Convert an RGB image to 3 FITS channels

Author: William Henney 
Version 0.1 - 07 Apr 2011
"""

import numpy
import pyfits
from PIL import Image
import argparse

parser = argparse.ArgumentParser(description="Convert an RGB or Grayscale image to FITS format")
parser.add_argument("file", type=open,  help='Image file to convert')
args = parser.parse_args()

im = Image.open(args.file)           # read the image
assert im.mode in ["RGB", "L" ], \
    "File %s is of type '%s', which is not supported" % (args.file, im.mode)
a = numpy.array(im)                  # convert to array
filestem = args.file.name.split('.')[0] 

def add_comments(hdu):
    hdu.header.add_comment("Written by image2fits.py, Will Henney 2011,2012")
    hdu.header.add_comment("Converted from  %s" % (args.file.name))
    

if im.mode == "RGB":
    # split out the channels, flipping the y-axis
    r, g, b = [a[::-1,:,i] for i in 0, 1, 2]   
    # Write each channel to a FITS file: XXX-red.fits, XXX-green.fits, XXX-blue.fits
    for chan, color in zip([r, g, b], ["red", "green", "blue"]):
        hdu =  pyfits.PrimaryHDU(chan)
        # Use the OBJECT keyword to describe this channel
        hdu.header.update('OBJECT', "%s channel" % (color))
        add_comments(hdu)
        hdu.writeto("%s-%s.fits" % (filestem, color), clobber=True)
else:
    hdu =  pyfits.PrimaryHDU(a[::-1,:])
    add_comments(hdu)
    hdu.writeto("%s.fits" % (filestem), clobber=True)



