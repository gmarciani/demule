from statistics.chisquare import chisquare_univariate
from libs.des.rvms import idfChisquare
from rnd.tests.error import error_two_tails
from plots.chisquare import scatter


SAMSIZE = 7200      # SAMSIZE >= 10*BINS
BINS = 720          # BINS = T!
T = 6               # T> 3
CONFIDENCE = 0.95   # CONFIDENCE >= 0.95


def statistics(generator, streams, samsize=SAMSIZE, bins=BINS, t=T):
    data = []
    for stream in range(streams):
        generator.stream(stream)
        observed = observations(generator.rnd, samsize, bins, t)
        chi = chisquare(observed, samsize)
        result = (stream, chi)
        data.append(result)
    return data


def observations(uniform, samsize, bins, t):
    observed = [0] * bins
    for i in range(samsize):
        U = [uniform() for _ in range(t)]
        r = t - 1
        b = 0
        while r > 0:
            mx = 0
            for j in range(1,r + 1):
                if U[j] > U[mx]:
                    mx = j
            b = (r + 1) * b + mx
            U[mx], U[r] = U[r], U[mx]
            r -= 1
        observed[b] += 1
    return observed


def chisquare(observed, samsize):
    bins = len(observed)
    expected = lambda x: samsize / bins
    value = chisquare_univariate(observed, expected)
    return value


def critical_min(bins, confidence=CONFIDENCE):
    return idfChisquare(bins - 1, (1 - confidence) / 2)


def critical_max(bins, confidence=CONFIDENCE):
    return idfChisquare(bins - 1, 1 - (1 - confidence) / 2)


def error(data, mn, mx, confidence=CONFIDENCE):
    return error_two_tails(data, mn, mx, confidence)


def plot(data, mn, mx, title=None, filename=None):
    scatter(data, mn, mx, title, filename)