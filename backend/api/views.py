from django.shortcuts import render
from django.http import JsonResponse
from .fractals.Newton_Fractal import NewtonFractal
import numpy as np

# Create your views here.
def newton_fractal(request) : 
    real_lim = (-2., 2.)
    imag_lim = (-2., 2.)
    pixels = 200
    cores = 16

    amps = np.zeros(shape=9, dtype=complex)
    amps[0] = -16.0
    amps[5] = +15.0
    amps[-1] = 1.0
    nf = NewtonFractal(coeffs=amps)

    rgb_array = nf.generate_fractal(real_lim, imag_lim, pixels, cores)
    rgb_list = (rgb_array * 255).tolist()

    return JsonResponse({'rgb': rgb_list})

