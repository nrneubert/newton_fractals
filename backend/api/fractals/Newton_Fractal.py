from typing import Optional, Tuple
from matplotlib.figure import Figure
from numpy.typing import NDArray

from colorsys import hls_to_rgb
from multiprocessing import Pool, cpu_count
from tqdm import tqdm
from numpy.polynomial import Polynomial

import numpy as np

class NewtonFractal : 

    def __init__(self, 
                 roots: Optional[NDArray[np.complexfloating]] = None, 
                 coeffs: Optional[NDArray[np.complexfloating]] = None,
                 max_iterations=1e9, tolerance=1e-3) :

        self.FIGURES_FOLDER = "./Figures/"

        self.max_iter = int(max_iterations)
        self.tolerance = float(tolerance)

        self.saturation = 0.75

        if(roots is None) == (coeffs is None) : 
            raise ValueError("Either 'roots' or 'coeffs' must be provided.")

        if(roots is not None) : self.poly = Polynomial.fromroots(roots)
        if(coeffs is not None) : self.poly = Polynomial(coeffs)
        self.roots = self.poly.roots()
        self.coeffs = self.poly.coef

        self.dpoly: Polynomial = self.poly.deriv()

    def hue(self, z: np.complexfloating) :
        return float(np.angle(z)) / (2 * np.pi)

    def lightness(self, iters: int) :
        return 0.5 / (1.0 + 0.18 * iters)

    def get_polynomial(self):
        res = ''
        for i, num in enumerate(self.coeffs):
            if i > 0:
                res += ' + ' if float(num) >= 0 else ' '
            res += f'{num:.1f}'
            if i != 0:
                res += f'z^{i}'
        return res
    
    def save_fig(self, fig: Figure, file_format: str = 'svg', dpi: int = 800) : 
        fig.savefig(f"{self.FIGURES_FOLDER}{self.get_polynomial()}.{file_format}", format=file_format, bbox_inches='tight', dpi=dpi)

    def perform_newton(self, x0) : 
        not_converged = True
        iters = 0
        curr_x = x0
        closest = None
        
        while not_converged and iters < self.max_iter : 
            new_x = curr_x - self.poly(curr_x)/self.dpoly(curr_x)
            
            curr_x = new_x
            iters += 1

            # Convergence test
            if np.isclose(new_x, self.roots, rtol=self.tolerance).any() : 
                root_proximity = np.abs(curr_x - self.roots)
                closest = np.argmin(root_proximity)
                not_converged = False
        
        if closest is None : 
            raise RuntimeError(f"Convergence not achieved after {iters} iterations for guess {x0}")
            
        return (self.roots[closest], iters)
    
    def compute_point(self, z: np.complexfloating) : 
        root_val, iters = self.perform_newton(z)
        return self.convert_to_rgb(root_val, iters)
    
    def convert_to_rgb(self, z: np.complexfloating, iterations: int) : 
        hls = self.hue(z), self.lightness(iterations), self.saturation
        return hls_to_rgb(*hls)

    def generate_fractal(self, real_lim: Tuple[float, float], imag_lim: Tuple[float, float], pixels: int, cores: int = 1) : 

        reals = np.linspace(*real_lim, pixels)
        imags = np.linspace(*imag_lim, pixels)

        X, Y = np.meshgrid(reals, imags)
        Z = X + 1j * Y
        Z_flat = Z.flatten()

        nprocs = min(cores, cpu_count())
        with Pool(processes=nprocs) as pool : 
            rgb_list = list(
                tqdm(pool.imap(self.compute_point, Z_flat),
                     total=Z_flat.size,
                     desc="Computing grid..."
                     )
            )

        rgb_array = np.array(rgb_list, dtype=float)
        rgb_array = rgb_array.reshape((pixels, pixels, 3))
        
        return rgb_array
    