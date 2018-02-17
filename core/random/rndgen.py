"""
Implementation of a multi-stream Lehmer pseudo-random generator.

Keep in mind the following table:

╔════════════╦════════════════════════════════════════════════╗
║            ║                      BITS                      ║
║            ╠═════╦═══════╦════════════╦═════════════════════╣
║            ║ 8   ║ 16    ║ 32         ║ 64                  ║
╠════════════╬═════╬═══════╬════════════╬═════════════════════╣
║ MODULUS    ║ 127 ║ 32479 ║ 2147483647 ║ 9223372036854775783 ║
╠════════════╬═════╬═══════╬════════════╬═════════════════════╣
║ MULTIPLIER ║ 14  ║ 16374 ║ 48271      ║                     ║
╠════════════╬═════╬═══════╬════════════╬═════════════════════╣
║ STREAMS    ║ 64  ║ 128   ║ 256        ║ 512                 ║
╠════════════╬═════╬═══════╬════════════╬═════════════════════╣
║ JUMPER     ║ 14  ║ 32748 ║ 22925      ║                     ║
╠════════════╬═════╬═══════╬════════════╬═════════════════════╣
║ CHECKV     ║     ║       ║ 399268537  ║                     ║
╠════════════╬═════╬═══════╬════════════╬═════════════════════╣
║ CHECKI     ║     ║       ║ 10000      ║                     ║
╚════════════╩═════╩═══════╩════════════╩═════════════════════╝
"""

DEFAULT_MODULUS = 2147483647
DEFAULT_MULTIPLIER = 48271
DEFAULT_STREAMS = 256
DEFAULT_JUMPER = 22925
DEFAULT_ISEED = 123456789


class MarcianiMultiStream(object):
    """
    Implementation of a multi-stream Lehmer pseudo-random number generator.
    """

    def __init__(self, iseed=DEFAULT_ISEED,
                 modulus=DEFAULT_MODULUS,
                 multiplier=DEFAULT_MULTIPLIER,
                 streams=DEFAULT_STREAMS,
                 jumper=DEFAULT_JUMPER):
        """
        Creates a new random number generator.
        :param iseed: (int) the initial seed; must be positive.
        Default is 123456789.
        :param modulus: (int) the modulus; must be positive and prime.
        Default is 2147483647.
        :param multiplier: (int) the multiplier; must be a FP/MC multiplier of
        *modulus*.
        Default is 48271.
        :param streams: (int) the number of disjoint streams; must be positive.
        Default is 256.
        :param jumper: (int) the jumper for the given streams; must be a
        suitable jumper for the given number of *streams*.
        Default is 22925.
        """
        self._iseed = self._seed = iseed
        self._stream = 0
        self._modulus = modulus
        self._multiplier = multiplier
        self._streams = streams
        self._jumper = jumper

        self._init = False

        self._seeds = [int(self._iseed)] * self._streams
        self.plant_seeds(self._iseed)

    def plant_seeds(self, x):
        """
        Initializes all the streams of the generator.
        :param x: (int) the initial seed.
        """
        Q = int(self._modulus / self._jumper)
        R = int(self._modulus % self._jumper)

        self._init = True
        s = self._stream
        self.stream(0)
        self.put_seed(x)
        self._stream = s
        for j in range(1, self._streams):
            x = int(self._jumper * (self._seeds[j - 1] % Q) - R * int((self._seeds[j - 1] / Q)))
            if x > 0:
                self._seeds[j] = x
            else:
                self._seeds[j] = x + self._modulus

    def get_initial_seed(self):
        """
        Retrieves the initial seed for the 1st stream.
        :return: (int) the initial seed of 1st stream.
        """
        return self._iseed

    def get_seed(self):
        """
        Retrieves the seed of the current stream.
        :return: (int) the seed of the current stream.
        """
        return self._seeds[self._stream]

    def put_seed(self, x):
        """
        Initializes the current stream with the specified seed.
        :param x: (int) the seed.
        """
        if x > 0:
            x %= self._modulus
        else:
            raise ValueError(
                "x must be a positive number in (0, modulus). Found {}".format(
                    x))
        self._seeds[self._stream] = int(x)

    def stream(self, stream_id):
        """
        Selects the current stream.
        :param stream_id: stream index in [0,STREAMS-1]
        """
        self._stream = stream_id % self._streams
        if self._init is False and self._stream != 0:
            self.plant_seeds(self._iseed)

    def get_streams_number(self):
        """
        Retrieves the total number of streams.
        :return: (int) the number of streams.
        """
        return self._streams

    def rnd(self):
        """
        Generates a pseudo-random number from uniform distribution in [0,1)
        :return: a uniform pseudo-random float in [0,1)
        """
        Q = int(self._modulus / self._multiplier)
        R = int(self._modulus % self._multiplier)

        t = int(self._multiplier * (self._seeds[self._stream] % Q) -
                R * int(self._seeds[self._stream] / Q))
        if t > 0:
            self._seeds[self._stream] = int(t)
        else:
            self._seeds[self._stream] = int(t + self._modulus)

        return float(self._seeds[self._stream] / self._modulus)
    

class MarcianiSingleStream:
    """
    Implementation of a single-stream Lehmer pseudo-random number generator.
    """

    def __init__(self, iseed=DEFAULT_ISEED,
                 modulus=DEFAULT_MODULUS,
                 multiplier=DEFAULT_MULTIPLIER):
        """
        Creates a new random number generator.
        :param iseed: (int) the initial seed; must be positive.
        Default is 123456789.
        :param modulus: (int) the modulus; must be positive and prime.
        Default is 2147483647.
        :param multiplier: (int) the multiplier; must be a FP/MC multiplier of
        *modulus*.
        Default is 48271.
        """
        self._iseed = iseed
        self._seed = iseed
        self._modulus = modulus
        self._multiplier = multiplier
        
    def get_initial_seed(self):
        """
        Retrieves the initial seed for the 1st stream.
        :return: (int) the initial seed of 1st stream.
        """
        return self._iseed
    
    def get_seed(self):
        """
        Retrieves the seed..
        :return: (int) the seed.
        """
        return self._seed
    
    def put_seed(self, x):
        """
        Initializes the generator with the specified seed.
        :param x: (int) the seed.
        """
        if x > 0:
            x %= self._modulus
        else:
            raise ValueError("x must be a positive number in (0, modulus). Found {}".format(x))
        
    def rnd(self):
        """
        Generates a pseudo-random number from uniform distribution in [0,1)
        :return: a uniform pseudo-random float in [0,1)
        """
        Q = int(self._modulus / self._multiplier)
        R = int(self._modulus % self._multiplier)
    
        t = int(self._multiplier * (self._seed % Q) - R * int(self._seed / Q))
        
        if t > 0:
            self._seed = int(t)
        else:
            self._seed = int(t + self._modulus)
    
        return float(self._seed / self._modulus)


if __name__ == "__main__":
    CHECK = 399268537
    MODULUS = 2147483647
    MULTIPLIER = 48271
    DEFAULT = 123456789
    seed = int(DEFAULT)

    generator = MarcianiSingleStream(iseed=1)
    for _ in range(0, 10000):
        generator.rnd()
    if generator.get_seed() != CHECK:
        raise RuntimeError("{} is not correct!".format(generator.__class__.__name__))

    generator = MarcianiMultiStream(iseed=1)
    for _ in range(0, 10000):
        generator.rnd()
    if generator.get_seed() != CHECK:
        raise RuntimeError("{} is not correct!".format(generator.__class__.__name__))

