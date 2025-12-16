import os
import sys

repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from tests import test_mandelbrot

failed = 0
for name in dir(test_mandelbrot):
    if name.startswith('test_'):
        func = getattr(test_mandelbrot, name)
        try:
            func()
            print(f"{name}: PASSED")
        except AssertionError as e:
            failed += 1
            print(f"{name}: FAILED - {e}")
        except Exception as e:
            failed += 1
            print(f"{name}: ERROR - {e}")

if failed:
    print(f"{failed} test(s) failed")
    sys.exit(1)
else:
    print("All tests passed")
