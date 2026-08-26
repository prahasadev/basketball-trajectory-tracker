
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

G = 9.81
RIM_HEIGHT = 3.05
def parabola(x, a, b, c):
  return a * x**2 + b * x + c
