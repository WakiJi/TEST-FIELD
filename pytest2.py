from Crypto.Util.number import inverse, long_to_bytes
from math import isqrt  # 使用 math.isqrt 代替 sympy.isqrt

def add_THcurve(P, Q, a, p):
    if P == (0, 0):
        return Q
    if Q == (0, 0):
        return P
    x1, y1 = P
    x2, y2 = Q
    inv = inverse(a * x1 * y1 * x2 ** 2 - y2, p)
    x3 = (x1 - y1 ** 2 * x2 * y2) * inv % p
    y3 = (y1 * y2 ** 2 - a * x1 ** 2 * x2) * inv % p
    return x3, y3

def mul_THcurve(n, P, a, p):
    R = (0, 0)
    while n > 0:
        if n % 2 == 1:
            R = add_THcurve(R, P, a, p)
        P = add_THcurve(P, P, a, p)
        n //= 2
    return R

def baby_step_giant_step(Q, G, p, a):
    m = isqrt(p) + 1
    baby_steps = {}
    current = (0, 0)
    for j in range(m):
        baby_steps[current] = j
        current = add_THcurve(current, G, a, p)
    
    inv = inverse(mul_THcurve(m, G, a, p), p)
    giant_step = Q
    for i in range(m):
        if giant_step in baby_steps:
            return i * m + baby_steps[giant_step]
        giant_step = add_THcurve(giant_step, inv, a, p)
    
    return None

# Example values
p = 10297529403524403127640670200603184608844065065952536889
a = 2
G = (8879931045098533901543131944615620692971716807984752065, 4106024239449946134453673742202491320614591684229547464)
Q = (6784278627340957151283066249316785477882888190582875173, 6078603759966354224428976716568980670702790051879661797)

m = baby_step_giant_step(Q, G, p, a)
if m is not None:
    FLAG = long_to_bytes(m)
    print(f"FLAG: DASCTF{{{FLAG.decode()}}}")
else:
    print("Unable to find FLAG")
