import numpy as np
from scipy.interpolate import InterpolatedUnivariateSpline
from scipy.stats import chisquare
from scipy.optimize import curve_fit
from matplotlib import pyplot as plt
import time

# Cleaned version of the pdf.py in computing_methods/project2 folder

class ProbabilityDensityFunction(InterpolatedUnivariateSpline):
	"""Class describing a probability density function.
	"""

	def __init__(self, x, y, k=3):
		"""Constructor.
		"""
		InterpolatedUnivariateSpline.__init__(self, x, y, k=k)

		# for every value in x evaluate the integral from x[0] to x, and
		# fill a new array with those values
		ycdf = np.array([self.integral(x[0], xcdf) for xcdf in x])
		self.cdf = InterpolatedUnivariateSpline(x, ycdf)

		# better way to do that
		_x, _i = np.unique(ycdf, return_index=True)
		_y = x[_i]
		self.ppf = InterpolatedUnivariateSpline(_x, _y)

	def prob(self, x1, x2):
		"""Return the probability for the random variable to be included
		between x1 and x2.
		"""
		return self.cdf(x2) - self.cdf(x1)

	def rnd(self, size=1000):
		"""Return an array of random values from the pdf.
       		"""
		return self.ppf(np.random.uniform(size=size))


