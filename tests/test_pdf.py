import unittest
import sys 
sys.path.append('/home/michele/Documenti/CM2/splrand2')

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
if sys.flags.interactive:
	plt.ion()
# try running with -i flag to see the consequences

from splrand2.pdf import ProbabilityDensityFunction

class testPdf(unittest.TestCase):

	def test_triangular(self):
		"""test triangular distribution"""
		x = np.linspace(0., 1., 100)
		y = 2. * x

		pdf = ProbabilityDensityFunction(x, y)

		plt.figure('pdf triangular')
		plt.plot(x, pdf(x))
		plt.xlabel('x')
		plt.ylabel('pdf(x)')

		plt.figure('cdf triangular')
		plt.plot(x, pdf.cdf(x))
		plt.xlabel('x')
		plt.ylabel('cdf(x)')

		plt.figure('ppf triangular')
		# make sure that the domain of the ppf is the interval [0,1]
		# (we can't just simply take the x array cause it exceed in the
		# most general case)
		q = np.linspace(0., 1., 250)
		plt.plot(q, pdf.ppf(q))
		plt.xlabel('q')
		plt.ylabel('ppf(q)')

		plt.figure('Sampling triangular')
		rnd = pdf.rnd(1000000)
		plt.hist(rnd, bins=200)

		# pdf inherits the __call__ method from the spline class. From the
		# scipy manuals: "evaluate spline at position x"
		a = np.array([0.2, 0.6])
		print(pdf(a))

	def test_gauss(self, mu=0., sigma=1., support=10., num_points=500,
				   rnd_sample = 100000):
		"""Unit test with a gaussian distribution"""
		from scipy.stats import norm
		x = np.linspace(-support * sigma + mu, support * sigma + mu, num_points)
		y = norm.pdf(x, mu, sigma)
		pdf = ProbabilityDensityFunction(x,y)

		plt.figure('pdf gaussian')
		plt.plot(x, pdf(x))
		plt.xlabel('x')
		plt.ylabel('pdf(x)')

		plt.figure('cdf gaussian')
		plt.plot(x, pdf.cdf(x))
		plt.xlabel('x')
		plt.ylabel('cdf(x)')

		plt.figure('ppf gaussian')
		# make sure that the domain of the ppf is the interval [0,1]
		# (we can't just simply take the x array cause it exceed in the
		# most general case)
		q = np.linspace(0., 1., 250)
		plt.plot(q, pdf.ppf(q))
		plt.xlabel('q')
		plt.ylabel('ppf(q)')

		plt.figure('Sampling gaussian')
		# Here's what rnd function does: it generates some random values
		# in the [0,1] interval. For every point, the ppf is evaluated.
		# What we get is a set of point whose histogram should be similar
		# to the pdf function (with some constant missing).
		rnd = pdf.rnd(rnd_sample)
		ydata, edges, _ = plt.hist(rnd, bins=200) # ignore the last elem.
		xdata = 0.5 * (edges[1:] + edges[:-1])

		def f(x, C, mu, sigma):
			'''
			Given x array, evaluate the y value according to the gaussian
			function with parameters mu and sigma. The histogram we get is
			not normalized, so we add a constant on the left.
			'''
			return C * norm.pdf(x, mu, sigma)

		popt, pcov = curve_fit(f, xdata, ydata)
		print(popt[0]) # C, mu, sigma
		print(rnd_sample * (edges[1] - edges[0])) # whyyyyyy
		print(np.sqrt(pcov.diagonal())) # covariance matrix
		_x = np.linspace(-10, 10, 500)
		# *popt: pass every argument in the popt list
		_y = f(_x, *popt)

		plt.plot(_x, _y)

		mask = ydata > 0
		chi2 = sum(((ydata[mask] - f(xdata[mask], *popt)) / np.sqrt(ydata[mask])) ** 2.)
		nu = mask.sum() - 3
		sigma = np.sqrt(2 * nu)
		print(chi2, nu, sigma)
		# multinomial distribution

if __name__ == '__main__':
	unittest.main(exit=not sys.flags.interactive)
