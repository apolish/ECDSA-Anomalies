from sympy import mod_inverse

def recover_private_key_case_a(s, z, r, n, a, m):
    # k = szk * z⁻¹ mod n
    z_inv = mod_inverse(z, n)
    s_zk = a * m
    k = (s_zk * z_inv) % n

    # srxk = s - szk mod n
    s_rxk = (s - s_zk) % n

    # x = srxk * (r * k)⁻¹ mod n
    rk = (r * k) % n
    rk_inv = mod_inverse(rk, n)
    x = (s_rxk * rk_inv) % n

    return {
        "z-1": z_inv,
        "s_zk": s_zk,
        "s_rxk": s_rxk,
        "rk": rk,
        "(rk)-1": rk_inv,
        "k": k,
        "x": x
    }

# Example usage: Tx #1 from the paper (Vulnerability A, m1 = 1)
example = {
    "s": 7584,
    "z": 9572,
    "r": 4141,
    "n": 9967, # const!
    "a": 1204,
    "m": 1     # const!
}

result = recover_private_key_case_a(**example)
print("Recovered values:")
for key, val in result.items():
    print(f"{key} = {val}")
