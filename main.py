from mandelbrot import Mandelbrot
from PIL import Image as im
import numpy as np
import sys

# Set to the name of your e-ink device (https://github.com/robweber/omni-epd#displays-implemented)
DISPLAY_TYPE = "waveshare_epd.epd7in5_V2"

# Disable when running the waveshare panel
# False display Mandelbrot image on e-Paper display
# True display Mandelbrot image on computer monitor / Raspberry Pi monitor
DEBUG = True
# DEBUG = False  01/26 test change 938

if not DEBUG:
    from omni_epd import displayfactory, EPDNotFoundError

mandelbrot = Mandelbrot()

# default height and width - need to hardcode for debug mode
WIDTH = 800
HEIGHT = 480
if not DEBUG:
    try:
        epd = displayfactory.load_display_driver(DISPLAY_TYPE)
    except EPDNotFoundError:
        print(f"Couldn't find {DISPLAY_TYPE}")
        sys.exit()

    WIDTH = epd.width
    HEIGHT = epd.height

    epd.prepare()
    epd.clear()
    epd.sleep()

while True:                                         # Start of infinite loop
    print("Starting render...")                     #  prints a message indicating the start of the rendering process.
    mandelbrot.render(WIDTH,HEIGHT)                 # Generate an image of the Mandelbrot set
    print("Done!")                                  # signals the completion of the rendering process.
    arr = mandelbrot.get_render()                   #  retrieves the rendered data from the mandelbrot object.
    arr = (np.asarray(arr)*255).astype(np.uint8)    # converts the rendered data to a NumPy array, scales the values (possibly for contrast adjustment), 
                                                    # and casts them to 8-bit unsigned integers, a common format for image data
    image = im.fromarray(arr)                       # creates an image from the NumPy array
    # Save the image as BMP
    image = image.convert("1")                      # converts the image to a 1-bit pixel format, suitable for black-and-white displays, like e-paper.

    if DEBUG:
        image.show()                                # If so, the image is displayed directly (probably on a standard computer screen).
    else:                       
        epd.prepare()
        epd.clear()
        epd.display(image)
        epd.sleep()

    mandelbrot.zoom_on_interesting_area()     #object that modifies its state to zoom into a specific area of the Mandelbrot set, possibly to display more 
                                              # interesting or detailed fractal patterns in subsequent renders.
