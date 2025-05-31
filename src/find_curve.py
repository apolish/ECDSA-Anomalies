import sympy


def is_on_curve(point, p, a, b):
    if point is None:
        return True
    x, y = point
    return (y**2 - x**3 - a * x - b) % p == 0


def inverse_mod(k, p):
    return pow(k, -1, p)


def point_add(P, Q, p, a):
    if P is None:
        return Q
    if Q is None:
        return P
    x1, y1 = P
    x2, y2 = Q
    if x1 == x2 and (y1 + y2) % p == 0:
        return None
    if x1 == x2:
        m = (3 * x1**2 + a) * inverse_mod(2 * y1, p) % p
    else:
        m = (y2 - y1) * inverse_mod(x2 - x1, p) % p
    x3 = (m * m - x1 - x2) % p
    y3 = (m * (x1 - x3) - y1) % p
    return (x3, y3)


def scalar_multiply(k, P, p, a):
    Q = None
    while k:
        if k & 1:
            Q = point_add(Q, P, p, a)
        P = point_add(P, P, p, a)
        k >>= 1
    return Q


def find_point_on_curve(p, a, b):
    for x in range(2, p):  # x > 1
        rhs = (x**3 + a * x + b) % p
        roots = sympy.sqrt_mod(rhs, p, all_roots=True)
        if roots:
            for y in roots:
                if y > 1:
                    return (x, y)
    return None


def compute_curve_order(p, a, b):
    count = 1  # includes a point at infinity
    for x in range(p):
        rhs = (x**3 + a * x + b) % p
        roots = sympy.sqrt_mod(rhs, p, all_roots=True)
        if roots:
            count += len(roots)
    return count


def find_curve_with_generator(p, n, max_a=50, max_b=50, max_results=10, g_x_more=1, g_y_more=1):
    print(f"Searching for up to {max_results} working curves with p = {p}, n = {n} ...")
    found = 0
    for a in range(max_a):
        for b in range(1, max_b):
            order = compute_curve_order(p, a, b)
            if order % n != 0:
                continue
            P = find_point_on_curve(p, a, b)
            if P is None or not is_on_curve(P, p, a, b):
                continue
            G = scalar_multiply(1, P, p, a)
            if not is_on_curve(G, p, a, b):
                continue
            test = scalar_multiply(n, G, p, a)
            if test is None:
                Gx, Gy = G
                if Gx > g_x_more and Gy > g_y_more:
                    print(f"Found working curve #{found + 1}:")
                    print(f"p = {p}")
                    print(f"a = {a}")
                    print(f"b = {b}")
                    print(f"G = {G}")
                    print(f"n = {n}")
                    found += 1
                    if found >= max_results:
                        return
    if found == 0:
        print("No valid curves found.")


# === MAIN ENTRY POINT ===
if __name__ == "__main__":
    p = 10007
    n = 9967
    find_curve_with_generator(p, n, max_a=50, max_b=50, max_results=10, g_x_more=1, g_y_more=1)
