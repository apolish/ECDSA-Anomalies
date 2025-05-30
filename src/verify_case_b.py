from sympy import mod_inverse, sqrt_mod

def recover_private_key_case_b(s, s_zr, z, r, a, n):
    # Step 1: compute discriminant
    D = (s * s - 4 * a * ((s_zr + s) % n)) % n

    # Step 2: solve for m1 using modular square root
    roots = sqrt_mod(D, n, all_roots=True)
    if not roots:
        return {"error": "No modular sqrt exists for discriminant D."}

    results = []
    for root in roots:
        numerator = (s + root) % n
        denominator = (2 * a) % n
        try:
            denom_inv = mod_inverse(denominator, n)
        except:
            continue  # skip if denominator not invertible
        m1 = (numerator * denom_inv) % n

        s_zk = (a * m1) % n
        z_inv = mod_inverse(z, n)
        k = (s_zk * z_inv) % n
        rk = (r * k) % n
        rk_inv = mod_inverse(rk, n)
        s_rxk = (s - s_zk) % n
        x = (s_rxk * rk_inv) % n

        results.append({
            "s_zk": s_zk,
            "s_rxk": s_rxk,
            "z-1": z_inv,
            "k": k,
            "rk": rk,
            "(rk)-1": rk_inv,
            "x": x,
            "m1": m1,
        })

    return results

# Example usage: Tx #6 (Case B) from paper
example = {
    "s": 4559,
    "s_zr": 5917,
    "z": 142,
    "r": 533,
    "a": 485,
    "n": 9967 # const!
}

results = recover_private_key_case_b(**example)
print("Recovered values:")
for res in results:
    for key, val in res.items():
        print(f"{key} = {val}")
    print("-" * 40)
