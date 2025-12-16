"""PiArtFrame -- render Mandelbrot frames for e-ink displays.

This module supports a development mode (local preview) and a
hardware mode that uses the ``omni_epd`` display drivers.

Run with ``--debug`` to show a single preview locally. Use
``--runs N`` to render a fixed number of frames in non-debug mode.
"""

from typing import Optional
import argparse
import logging
import sys

import numpy as np
from PIL import Image as im

from mandelbrot import Mandelbrot

# Set to the name of your e-ink device. See project README for options.
DISPLAY_TYPE = "waveshare_epd.epd7in5_V2"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Show a single preview locally and exit",
    )
    parser.add_argument(
        "--runs",
        type=int,
        default=0,
        help=("Number of frames to render in non-debug mode. " "0 means run forever"),
    )
    parser.add_argument(
        "--display",
        default=DISPLAY_TYPE,
        help="E-paper display identifier to load (omni_epd)",
    )
    return parser.parse_args()


def try_load_display(display_name: str):
    """Try to import and load the e-paper display driver.

    Returns the driver instance or raises ImportError if the
    driver package is not available.
    """
    try:
        from omni_epd import EPDNotFoundError, displayfactory  # type: ignore

        epd = displayfactory.load_display_driver(display_name)
    except Exception as exc:  # pylint: disable=broad-except
        raise ImportError("Display driver not available") from exc
    return epd


def main(argv: Optional[list] = None) -> int:
    args = parse_args() if argv is None else parse_args()

    debug = bool(args.debug)
    runs = int(args.runs)

    logging.basicConfig(level=logging.DEBUG if debug else logging.INFO)
    log = logging.getLogger("piartframe")

    mandelbrot = Mandelbrot()

    # default values for debug mode
    width = 800
    height = 480
    epd = None

    if not debug:
        try:
            epd = try_load_display(args.display)
        except ImportError:
            log.exception("Couldn't load display driver %s", args.display)
            return 1
        width = epd.width
        height = epd.height
        epd.prepare()
        epd.clear()
        epd.sleep()

    iteration = 0
    while True:
        log.info("Starting render (%d)", iteration)

        mandelbrot.render(width, height)
        log.info("Done (x=%s)", mandelbrot.x)

        # Convert boolean render (0/1) to 8-bit and create PIL image
        arr = mandelbrot.get_render()
        arr = (np.asarray(arr) * 255).astype(np.uint8)
        image = im.fromarray(arr).convert("1")

        if debug:
            image.show()
            break
        # Hardware path
        epd.prepare()
        epd.clear()
        epd.display(image)
        epd.sleep()

        # Zoom in for more detail in the next frame
        mandelbrot.zoom_on_interesting_area()

        iteration += 1
        if runs and iteration >= runs:
            break

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
