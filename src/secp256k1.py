import collections
import hashlib
import time
import random
from fractions import Fraction
from datetime import datetime

class Secp256k1:
    """Mathematical implementation of secp256k1"""

    def __init__(self):
        """Initialization of secp256k1 curve parameters for specific range"""
        EllipticCurve = collections.namedtuple("EllipticCurve", "name mode p a b g n")
        # Ranges of elliptic curve parameters (from 1T to 2^256):
        """
        # test
        p = 10007
        a = 48,
        b = 22,
        g = (4, 1668)
        n = 9967

        # legacy
        p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
        a = 0
        b = 7
        g = (
            0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
            0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
        )
        n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
        """
        self.__curve = EllipticCurve(
            "secp256k1",
            "test",
            # Field characteristic:
            p = 10007,
            # Curve coefficients:
            a = 48,
            b = 22,
            # Base point:
            g = (
                4, # x - coordinate
                1668  # y - coordinate
            ),
            # Subgroup order:
            n = 9967
        )
        self.__k_inv = 0
    
    def get_elliptic_curve(self):
        return self.__curve

    def get_k_inversed(self):
        return self.__k_inv

    def inverse_mod(self, k, p):
        """Computing the inverse of k mod p (extended Euclidean algorithm)"""
        if k == 0:
            raise ZeroDivisionError("division by zero")
        return pow(k, -1, p)  # Using a built-in Python 3 method
    
    def is_on_curve(self, point):
        """Checking if a point belongs to a curve"""
        if point is None:
            return True
        x, y = point
        return (y**2 - x**3 - self.__curve.a * x - self.__curve.b) % self.__curve.p == 0

    def point_add(self, P, Q):
        """Adding two points P + Q on a curve"""
        if P is None:
            return Q
        if Q is None:
            return P
        x1, y1 = P
        x2, y2 = Q

        if x1 == x2 and y1 != y2:
            # point1 + (-point1) = 0
            return None

        if x1 == x2:
            # Handling the case of doubling a point (P == Q)
            m = (3 * x1**2 + self.__curve.a) * self.inverse_mod(2 * y1, self.__curve.p) % self.__curve.p
            x3 = (m**2 - 2 * x1) % self.__curve.p
        else:
            m = (y2 - y1) * self.inverse_mod(x2 - x1, self.__curve.p) % self.__curve.p
            x3 = (m**2 - x1 - x2) % self.__curve.p

        y3 = (m * (x1 - x3) - y1) % self.__curve.p

        return (x3, y3)

    def scalar_multiply(self, k, P):
        """Multiplying a point P by a scalar k"""
        if k % self.__curve.n == 0 or P is None:
            return None

        Q = None
        while k: # bitwise decomposition of k (private key)
            if k & 1:
                # Add
                Q = self.point_add(Q, P) # for bits with a bit size of '1'
            # Double
            P = self.point_add(P, P) # for each bit including '0' and '1'
            k >>= 1 # shift one digit to the right
        
        if isinstance(Q, tuple) and len(Q) == 2:
            return Q
        else:
            return (0, 0)

    def generate_keypair(self, private_key=None):
        """Generates random private and public keys"""
        if private_key is None:
            private_key = random.randrange(1, self.__curve.n - 1)
        public_key = self.scalar_multiply(private_key, self.__curve.g)
        return private_key, public_key

    def hash_message(self, message):
        """Calculates SHA-256 hash of the message"""
        if self.__curve.mode == "test":
            return random.randrange(1, self.__curve.n - 1)
        elif self.__curve.mode == "legacy":
            return int.from_bytes(hashlib.sha256(message).digest(), "big") % self.__curve.n
        

    def sign_message(self, private_key, message, z=None):
        """Signs the message"""
        z = self.hash_message(message)
        while True:
            k = random.randrange(1, self.__curve.n - 1)
            x, _ = self.scalar_multiply(k, self.__curve.g)
            r = x % self.__curve.n
            if r == 0:
                continue
            k_inv = self.inverse_mod(k, self.__curve.n)
            s = ((z + r * private_key) * k_inv) % self.__curve.n
            if s != 0:
                self.__k_inv = k_inv
                return (k_inv, z, r, s)
    
    def verify_signature(self, public_key, signature):
        """Verifies the signature"""
        _, z, r, s = signature
        if not (1 <= r < self.__curve.n and 1 <= s < self.__curve.n):
            return False

        w = self.inverse_mod(s, self.__curve.n)
        u1 = (z * w) % self.__curve.n
        u2 = (r * w) % self.__curve.n
        P1 = self.scalar_multiply(u1, self.__curve.g)
        P2 = self.scalar_multiply(u2, public_key)
        
        if P1 is None or P2 is None:
            return False

        X, _ = self.point_add(P1, P2)
        if X is None:
            return False
        
        return (X % self.__curve.n) == r
    
    def generate_unique_keys(self, count, range_start, range_end):
        if self.__curve.mode == "test":
            return random.sample(range(range_start, range_end), count)
        elif self.__curve.mode == "legacy":
            seen = set()
            while len(seen) < count:
                candidate = random.randrange(range_start, range_end)
                if candidate not in seen:
                    seen.add(candidate)
            return list(seen)

if __name__ == "__main__":
    secp256k1 = Secp256k1()
    curve = secp256k1.get_elliptic_curve()

    # Key generation
    time_start = time.time()
    private_key, public_key = secp256k1.generate_keypair()
    print("Private key:")
    print(f"  d: {private_key}, ({str(bin(private_key))[2:]})")
    print("Public key:")
    print(f"  x: {public_key[0]}")
    print(f"  y: {public_key[1]}")
    time_spent = time.time() - time_start
    print(f"Spent time: {time_spent:.3f} sec.")
    print("")

    # Checking if a point belongs to a curve
    time_start = time.time()
    is_on_curve = secp256k1.is_on_curve(public_key)
    print(f"Is the point on curve?: {is_on_curve}")
    time_spent = time.time() - time_start
    print(f"Spent time: {time_spent:.3f} sec.")
    print("")

    # Signing the message
    time_start = time.time()
    message = b"Hello, secp256k1!"
    signature = secp256k1.sign_message(private_key, message)
    print("Signature parameters:")
    print(f"  c: {str(hex(signature[0]))[2:]}")
    print(f"  z: {str(hex(signature[1]))[2:]}")
    print(f"  r: {str(hex(signature[2]))[2:]}")
    print(f"  s: {str(hex(signature[3]))[2:]}")
    time_spent = time.time() - time_start
    print(f"Spent time: {time_spent:.3f} sec.")
    print("")

    # Signature verification
    time_start = time.time()
    is_valid = secp256k1.verify_signature(public_key, signature)
    print(f"Signature validation: {is_valid}")
    time_spent = time.time() - time_start
    print(f"Spent time: {time_spent:.3f} sec.")
    print("")
    
    # Output of private key structure results
    time_start = time.time()
    column_widths = [6, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 20, 20]
    line_length = 166
    if curve.mode == "test":
        column_widths = [6, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 20, 20]
        line_length = 166
    elif curve.mode == "legacy":
        column_widths = [6, 80, 80, 80, 80, 80, 80, 80, 80, 80, 80, 160, 160]
        line_length = 1126
    header_title = ["case", "s", "s_zk", "s_rxk", "s_zr", "z", "r", "x", "k", "q", "a", "m1", "m2"]
    header_line = '-' * line_length

    ecdsa_data = []
    range_start = 1 #0XDD15FE86AFFAD91249EF0EB713F39EBEAA987B6E6FD2A0000000000000000000
    range_end = curve.n - 1  # (n - 1) is the maximum private key value!
    total_key_count = 9965

    unique_numbers = secp256k1.generate_unique_keys(total_key_count, range_start, range_end)
    progress_indicator = max(1, total_key_count // 10)

    case_A_count = 0
    case_B_count = 0

    i = 0
    transaction_limit_per_key = 10036
    for private_key in unique_numbers:
        i += 1
        _, public_key = secp256k1.generate_keypair(private_key)
        if secp256k1.is_on_curve(public_key):
            transaction_count_limit_per_key = 0
            while transaction_count_limit_per_key <= transaction_limit_per_key: # transaction count limit for each private key
                transaction_count_limit_per_key += 1
                signature = secp256k1.sign_message(private_key, b"".join([str(random.randrange(1, curve.n - 1)).encode()]))
                #if curve.verify_signature(public_key, signature): # It's recommended to avoid losing in the performance!
                k = signature[0]
                z = signature[1]
                r = signature[2]
                s = signature[3]
                x = private_key
                s_zk = (z * k) % curve.n
                s_rxk = (r * x * k) % curve.n
                if s_zk > 0 and s_rxk > 0:
                    if (s_zk + s_rxk) == s:
                        s_zr = (z * r) % curve.n
                        if s_zr > s:
                            q = s_zr - s
                            a = s % q
                            if a > 1 and a != s and a == (s_zr % q):
                                m1 = Fraction(s_zk, a)
                                m2 = Fraction(s + s_zr, s_rxk)
                                if m1.denominator == 1:
                                    if m1 != m2 and m1 == 1: # Remove 'and m1 == 1' condition when you need to get all m1 values, not only filtered by m1 = 1
                                        case_A_count += 1
                                        ecdsa_data.append(['A', s, s_zk, s_rxk, s_zr, z, r, x, k, q, a, m1, m2])
                                    elif m1 == m2 and m1 > 1:
                                        case_B_count += 1
                                        ecdsa_data.append(['B', s, s_zk, s_rxk, s_zr, z, r, x, k, q, a, m1, m2])
        if i % progress_indicator == 0:
            print(f"{i} keys ({i * transaction_limit_per_key} transactions) generated...")

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    file_name = f"transaction_list_{timestamp}.txt"
    output_lines = []
    with open(file_name, "w") as file:
        file.write("Elliptic curve parameters:\n")
        file.write(f"name = {curve.name}\n")
        file.write(f"mode = {curve.mode}\n")
        file.write(f"p = {curve.p}\n")
        file.write(f"a = {curve.a}\n")
        file.write(f"b = {curve.b}\n")
        file.write(f"g = {curve.g}\n")
        file.write(f"n = {curve.n}\n")
        file.write("\n")
        if len(ecdsa_data) > 0:
            file.write(f"{header_line}\n")
            file.write("".join(f"{header:<{width}}" for header, width in zip(header_title, column_widths)) + "\n")
            file.write(f"{header_line}\n")
            for row in ecdsa_data:
                formatted_row = []
                for value, width in zip(row, column_widths):
                    formatted_value = f"{str(value):<{width}}" if isinstance(value, Fraction) else f"{value:<{width}}"
                    formatted_row.append(formatted_value)
                file.write("".join(formatted_row) + "\n")
            file.write(f"{header_line}\n")
            file.write("".join(f"{header:<{width}}" for header, width in zip(header_title, column_widths)) + "\n")
            file.write(f"{header_line}\n")

        file.write("\n")
        file.write("Statistics:\n")
        file.write("\n")
        file.write(f"Total private key count:   {total_key_count}\n")
        file.write(f"Transaction limit per key: {transaction_limit_per_key}\n")
        file.write(f"Total transaction count:   {total_key_count * transaction_limit_per_key}\n")
        file.write(f"Case A transaction count:  {case_A_count}\n")
        file.write(f"Case B transaction count:  {case_B_count}\n")
        time_spent = time.time() - time_start
        file.write(f"Spent time: {time_spent:.3f} sec.\n")
