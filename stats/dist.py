import math
import random

def normal_pdf(x, mu=0.0, sigma=1.0):
    return math.exp(-((x - mu) ** 2) / (2 * sigma * sigma)) / (sigma * math.sqrt(2 * math.pi))

def normal_cdf(x, mu=0.0, sigma=1.0):
    return 0.5 * (1 + math.erf((x - mu) / (sigma * math.sqrt(2))))

def normal_sample(mu=0.0, sigma=1.0):
    return random.gauss(mu, sigma)

def binomial_pmf(k, n, p):
    if k < 0 or k > n:
        return 0.0
    return math.comb(n, k) * (p ** k) * ((1 - p) ** (n - k))

def poisson_pmf(k, lam):
    return math.exp(-lam) * (lam ** k) / math.factorial(k)