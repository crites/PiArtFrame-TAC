from decimal import Decimal, getcontext, localcontext
import random
from tqdm import tqdm

class Mandelbrot:
    def __init__(self, w = Decimal(4), h = Decimal(2), x = Decimal(-1), y = Decimal(0)):
        self.w = w
        self.h = h
        self.x = x
        self.y = y
        self.rendered = None
        self.rendered_res_x = 0
        self.rendered_res_y = 0

    def mandel_point(self, C_x, C_y, iter):
        # Standard Mandelbrot iteration: Z_0 = 0, Z_{n+1} = Z_n^2 + C
        Z_x = Decimal(0)
        Z_y = Decimal(0)
        for i in range(iter):
            Z_x_old = Z_x
            Z_x = Z_x * Z_x - Z_y * Z_y + C_x
            Z_y = Decimal(2) * Z_x_old * Z_y + C_y
            if (Z_x * Z_x + Z_y * Z_y) > Decimal(4):
                return 1
        return 0

    def render(self, res_x, res_y):
        # Approximation for number of iterations
        try:
            scale = -self.w.log10()
        except Exception:
            scale = Decimal(0)
        iter_count = int(50 + max(0, scale) * Decimal(100))

        # Use a local decimal context for precision during rendering
        desired_prec = int(max(0, scale) + 8)
        columns = []
        with localcontext() as ctx:
            ctx.prec = desired_prec
            for y_offset_i in tqdm(range(res_y, 0, -1)):
                row = []
                for x_offset_i in range(0, res_x):
                    p_x = self.x - self.w / Decimal(2) + Decimal(x_offset_i) / Decimal(res_x) * self.w
                    p_y = self.y - self.h / Decimal(2) + Decimal(y_offset_i) / Decimal(res_y) * self.h
                    row.append(self.mandel_point(p_x, p_y, iter_count))
                columns.append(row)

        self.rendered_res_x = res_x
        self.rendered_res_y = res_y
        self.rendered = columns

    def get_render(self):
        return self.rendered

    def is_area_uniform(self, x_offset, y_offset, w, h, w_div, h_div, w_start, h_start):
        first_point = self.rendered[int(y_offset) + int(h / h_div) * h_start][int(x_offset) + int(w / w_div) * w_start]
        for x in range(0, int(w / w_div)):
            for y in range(0, int(h / h_div)):
                if first_point != self.rendered[int(y_offset) + int(h / h_div) * h_start + y][
                    int(x_offset) + int(w / w_div) * w_start + x]:
                    return False
        return True

    def get_uniformness_of_area(self, w, h, x_offset, y_offset, w_div, h_div):
        uniformness = 0
        for w_start in range(w_div):
            for h_start in range(h_div):
                if self.is_area_uniform(x_offset, y_offset, w, h, w_div, h_div, w_start, h_start):
                    uniformness += 1
        return uniformness

    def zoom_on_interesting_area(self):
        choices = []
        # Upper left quadrant
        uniformness = self.get_uniformness_of_area(self.rendered_res_x / 2, self.rendered_res_y / 2, 0, 0, 2, 2)
        choices += [(self.x-self.w/4, self.y+self.h/4, uniformness)]
        # Upper right quadrant
        uniformness = self.get_uniformness_of_area(self.rendered_res_x / 2, self.rendered_res_y / 2, self.rendered_res_x / 2, 0, 2, 2)
        choices += [(self.x+self.w/4, self.y+self.h/4, uniformness)]
        # Lower left quadrant
        uniformness = self.get_uniformness_of_area(self.rendered_res_x / 2, self.rendered_res_y / 2, 0, self.rendered_res_y / 2, 2, 2)
        choices += [(self.x-self.w/4, self.y-self.h/4, uniformness)]
        # Lower right quadrant
        uniformness = self.get_uniformness_of_area(self.rendered_res_x / 2, self.rendered_res_y / 2, self.rendered_res_x / 2, self.rendered_res_y / 2, 2, 2)
        choices += [(self.x + self.w / 4, self.y - self.h / 4, uniformness)]

        self.w = self.w / 2
        self.h = self.h / 2

        # Filter out completely uniform squares
        choices = [x for x in choices if x[2]<4]
        # Filter out squares that have 2 or more uniform squares
        #  less_uniform_choices = [x for x in choices if x[2]<3]
        less_uniform_choices = choices
        if len(less_uniform_choices) != 0:
            self.x, self.y, u = random.choice(less_uniform_choices)
        else:
            self.x, self.y, u = random.choice(choices)
