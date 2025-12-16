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


def test_mandel_point_initialization_matches_manual():
    """Verify implementation uses Z_0 = 0 by comparing to a manual implementation."""
    from mandelbrot import Mandelbrot

    def manual_mandel_point(C_x, C_y, iterations):
        Z_x = Decimal(0)
        Z_y = Decimal(0)
        for i in range(iterations):
            Z_x_old = Z_x
            Z_x = Z_x * Z_x - Z_y * Z_y + C_x
            Z_y = Decimal(2) * Z_x_old * Z_y + C_y
            if (Z_x * Z_x + Z_y * Z_y) > Decimal(4):
                return 1
        return 0

    m = Mandelbrot()
    test_points = [
        (Decimal('0'), Decimal('0')),
        (Decimal('-0.75'), Decimal('0.1')),
        (Decimal('0.3'), Decimal('0.5')),
    ]
    for Cx, Cy in test_points:
        assert m.mandel_point(Cx, Cy, 50) == manual_mandel_point(Cx, Cy, 50)


def test_render_returns_matrix_and_values():
    """Small render should return a 2D matrix of 0/1 values."""
    # avoid tqdm output during test
    try:
        import tqdm
        orig_tqdm = getattr(tqdm, 'tqdm', None)
        tqdm.tqdm = lambda x, *args, **kwargs: x
    except Exception:
        orig_tqdm = None

    from mandelbrot import Mandelbrot
    m = Mandelbrot()
    m.render(10, 8)
    arr = m.get_render()
    assert len(arr) == 8
    assert all(len(row) == 10 for row in arr)
    flat = [v for row in arr for v in row]
    assert all(v in (0, 1) for v in flat)

    if orig_tqdm is not None:
        import tqdm as _tq
        _tq.tqdm = orig_tqdm
