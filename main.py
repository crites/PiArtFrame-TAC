# comment added 01/28
import sys

import numpy as np
from PIL import Image as im

from mandelbrot import Mandelbrot

# Set to the name of your e-ink device
# See: https://github.com/robweber/omni-epd#displays-implemented
DISPLAY_TYPE = "waveshare_epd.epd7in5_V2"

# VS Code is cool!!
# Git is pretty cool!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# new comment 12/15/2025
# Comment change
# Disable when running the waveshare panel
# False display Mandelbrot image on e-Paper display
# True display Mandelbrot image on computer monitor / Raspberry Pi monitor
DEBUG = True
# DEBUG = False  01/26 test change 938
#
#
if not DEBUG:
    from omni_epd import EPDNotFoundError, displayfactory

if __name__ == "__main__":
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

    while True:  # Start of infinite loop
        # Print that a render is starting
        print("Starting render...")
        mandelbrot.render(WIDTH, HEIGHT)  # Generate an image of the Mandelbrot set
        # Report the current X coordinate after rendering
        print("Done!", mandelbrot.x)  # signals the completion of the rendering process.
        # Get the rendered array and convert to 8-bit image data
        arr = mandelbrot.get_render()
        arr = (np.asarray(arr) * 255).astype(np.uint8)
        image = im.fromarray(arr)  # creates an image from the NumPy array
        # Save the image as BMP
        # Convert to 1-bit pixels for e-paper displays
        image = image.convert("1")

        if DEBUG:
            image.show()  # If so, the image is displayed directly (probably on a standard computer screen).
        else:
            epd.prepare()
            epd.clear()
            epd.display(image)
            epd.sleep()

        mandelbrot.zoom_on_interesting_area()  # object that modifies its state to zoom into a specific area of the Mandelbrot set, possibly to display more
        # interesting or detailed fractal patterns in subsequent renders.

        # When debugging, run just once
        if DEBUG:
            break
