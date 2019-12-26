from klefki.crypto.ssss import SSSS
from klefki.types.algebra.groups import EllipticCurveGroup
from klefki.types.algebra.fields import FiniteField
from klefki.types.algebra.utils import randfield
from functools import reduce
from operator import mul


class VSS(SSSS):
    def __init__(self, F: FiniteField, G: EllipticCurveGroup):
        self.G = G
        super().__init__(F)


    def setup(self, secret, k, n, poly_params = []):
        if not poly_params:
            poly_params = [randfield(self.F) for _ in range(k - 1)]

        self.poly_proofs = [self.G**p for p in [secret] + poly_params]

        return super().setup(secret, k, n, poly_params)


    def verify(self, x, y):
        return self.verify_proofs(x, y, self.poly_proofs, self.G, self.k)


    @staticmethod
    def verify_proofs(x, y, proofs, G, k):
        return G ** y == reduce(mul, [proofs[i] ** (x ** i) for i in range(k)])
