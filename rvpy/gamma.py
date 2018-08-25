import numpy as np
from scipy.stats import gamma
from . import distribution

class Gamma(distribution.Distribution):
    def __init__(self, alpha, beta):
        assert alpha > 0 and beta > 0, "alpha and beta must be positive"

        self.alpha = alpha
        self.beta = beta

        # Scipy backend
        self.sp = gamma(a=alpha, scale=beta)

        # Initialize super - does nothing yet.
        super().__init__()

    def __repr__(self):
        return f"Gamma(alpha={self.alpha}, beta={self.beta})"

    def __add__(self, other):
        if isinstance(other, Gamma):
            return Gamma(self.alpha + other.alpha, self.beta)
        else:
            raise TypeError("Only addition of scalars supported")

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        return self.__add__(-other)

    def __rsub__(self, other):
        return (-self).__add__(other)

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return Gamma(self.alpha, other*self.beta)
        else:
            raise TypeError("Only multiplication by scalar supported")

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        if isinstance(other, (int, float)) and other != 0:
            return self.__mul__(1 / other)
        else:
            raise ZeroDivisionError("Cannot divide by zero!")

    def mgf(self, t):
        return np.where(t < 1/self.beta,
                   (1 - self.beta * t) ** (-self.alpha),
                   np.nan
               )

    def to_exponential(self):
        assert self.alpha == 1, "Alpha must be 1 to downcast"
        return Exponential(self.beta)

class Exponential(Gamma):
    def __init__(self, rate):
        # Get Gamma distribution initialization
        super().__init__(1, 1/rate)

        # Parameters
        self.rate = rate
        self.scale = 1 / rate

    def __repr__(self):
        return f"Exponential(rate={self.rate})"

    def to_gamma(self):
        return Gamma(alpha=1, beta=self.scale)

class ChiSq(Gamma):
    def __init__(self, df):
        # Get Gamma distribution initialization
        super().__init__(alpha=2*df, beta=2)

        # Parameters
        self.df = df

    def __repr__(self):
        return f"ChiSq(df={self.df})"

    def to_gamma(self):
        return Gamma(alpha=2*df, beta=2)
