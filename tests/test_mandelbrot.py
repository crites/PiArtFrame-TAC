from decimal import Decimal
import os
import sys
import types


def test_mandel_point_examples():
    """Verify mandel_point returns expected values for basic cases."""
    # Ensure repository root is on the Python path
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    if repo_root not in sys.path:
        sys.path.insert(0, repo_root)
    try:
        from mandelbrot import Mandelbrot
    except ModuleNotFoundError as exc:
        if exc.name == 'tqdm':
            tqdm_stub = types.ModuleType("tqdm")
            def dummy_tqdm(iterable, *args, **kwargs):
                return iterable
            tqdm_stub.tqdm = dummy_tqdm
            sys.modules['tqdm'] = tqdm_stub
            from mandelbrot import Mandelbrot
        else:
            raise

    m = Mandelbrot()
    assert m.mandel_point(Decimal('0'), Decimal('0'), 10) == 0
    assert m.mandel_point(Decimal('2'), Decimal('2'), 10) == 1
